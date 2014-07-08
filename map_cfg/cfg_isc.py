#-----------------------------------------------------------------
# cfg_isc.py: Construct Control Flow Graph for Intermediate Source Code
#-----------------------------------------------------------------

import sys
import re
from cfg import *

# RE for function definition
#   group(1) is function Name
#   if group(2) == "){", single line definition
#   elif group(2) == $, multi line definition
re_funcDef = re.compile('(?:\w*\s+)*\**(\w+)\s*\([,\s\w&\[\]\*]*($|\)\s*\{)')
re_funcDefArgLine = re.compile('[,\s\w&\[\]\*]*($|\)\s*\{)')
re_basicBlockLabel = re.compile('\s*(\w*bb_[0-9]*):')
re_basicBlockStart = re.compile('\s*//\s*#\s*PRED:./*')
re_basicBlockEnd = re.compile('\s*//\s*#\s*SUCC:./*')
re_gotoLine = re.compile('\s*goto\s*(\w*bb_[0-9]*);')
re_funcCallLine = re.compile('\s*(\w*)\s*\([,\s\w&\[\]\*]*\);')
re_returnLine = re.compile('\s*return\s*.*;')
re_funcDefEnd = re.compile('\s*\}')

class BasicBlockTargets:
    def __init__(self, name, listTargets = None):
        self.name = name
        if listTargets == None:
            self.listTargets = []
        else:
            self.listTargets = listTargets

def parse_isc(fileName):
    listFunctions = []
    
    # State Management
    inFunctionBody = 0      # is 1, when inside Function Body
    inFuncDefArgMultiLine = 0       # is 1, when inside multiline argument list for func Def.
    currFuncName = ""
    currFuncStartLine = 0
    currFuncEndLine = 0
    listCurrFuncBasicBlocks = []
    listCurrFuncBasicBlockTargets = []
    listCurrFuncBBEdges = []
    
    inBasicBlock = 0
    currBasicBlockName = ""
    currBasicBlockStartLine = 0
    currBasicBlockEndLine = 0
    isCurrBasicBlockReturning = 0
    listCurrBlockFuncCalls = []
    listCurrBasicBlockTargets = []
    
    lineNum = 0
    file = open(fileName, 'r')
    for line in file:
        lineNum = lineNum + 1
        '''
        Loop to parse each line in the code.
        Algorithm:
        1. We only care about the code inside functions. Look for function
           definitions. 
            a. Single Line Definition
            b. Multiple Line Parameters
        2. Inside the function body, we want to look for basic block labels,
           function calls, goto instructions and return instructions.
            a. Labels:
                1. Record the name of the basic block.
                2. Basic Block starts at next line with "// # PRED..."
                3. Basic Block ends at line with "// # SUCC..."
            b. Goto:
                1. Keep list of targets of current basic block.
                2. Keep a list of all basic blocks with list of their targets.
            c. Function Calls:
                1. Keep list of functions called by current block.
            d. Return Instructions
                1. Keep note if current Basic Block Returns.
                
        '''
        # 1. Look for function definition
        m = re_funcDef.match(line)
        if m is not None:
            if m.group(2) == "":
                # 1.b. Multi Line Function Arguments
                inFuncDefArgMultiLine = 1
                currFuncName = m.group(1)
                continue
            else:
                # 1.a. Single Line Definition
                inFunctionBody = 1
                currFuncName = m.group(1)
                currFuncStartLine = lineNum + 1
                continue
                
        if inFuncDefArgMultiLine == 1:
            # 1.b. Multi Line Function Arguments
            m = re_funcDefArgLine.match(line)
            if m is not None:
                if m.group(1) == "":
                    # Next line is still argument list
                    continue
                else:
                    # End of Argument List. Start of function body in next line.
                    inFuncDefArgMultiLine = 0
                    inFunctionBody = 1
                    currFuncStartLine = lineNum + 1
                    continue
            else:
                raise ParseError("Not found the expected Multi Line Argument List at %s:%d." & (fileName, lineNum))
                exit(1)
                
        # 2. Inside Function Body    
        if inFunctionBody == 1:
            # 2.a Look for labels
            m = re_basicBlockLabel.match(line)
            if m is not None:
                # 2.a.1 Record name of Basic Block
                currBasicBlockName = m.group(1)
                continue
            
            # 2.a.2. Look for start of Basic Block
            m = re_basicBlockStart.match(line)
            if m is not None:
                inBasicBlock = 1
                currBasicBlockStartLine = lineNum + 1
                continue;
            
            if inBasicBlock == 1:
                # 2.a.3. Look for end of basic block
                m = re_basicBlockEnd.match(line)
                if m is not None:
                    inBasicBlock = 0
                    currBasicBlockEndLine = lineNum - 1
                    listCurrFuncBasicBlocks.append(BasicBlock(currBasicBlockStartLine,
                                                              currBasicBlockEndLine,
                                                              isCurrBasicBlockReturning,
                                                              listCurrBlockFuncCalls,
                                                              currBasicBlockName))
                    # 2.b.2. List of Basic Blocks with list of their targets
                    listCurrFuncBasicBlockTargets.append(BasicBlockTargets(currBasicBlockName,
                                                                           listCurrBasicBlockTargets))
                    # Resetting state variabless
                    currBasicBlockName = ""
                    currBasicBlockStartLine = 0
                    currBasicBlockEndLine = 0
                    isCurrBasicBlockReturning = 0
                    listCurrBlockFuncCalls = []               
                    listCurrBasicBlockTargets = [] 
                    continue;
                
                # 2.b. look for goto instructions
                m = re_gotoLine.match(line)
                if m is not None:
                    # 2.b.1. List of targets of current basic block
                    targetBlock = m.group(1)
                    listCurrBasicBlockTargets.append(targetBlock)
                    continue
                
                # 2.c. look for function calls
                m = re_funcCallLine.match(line)
                if m is not None:
                    # 2.c.1. List of functions called by current block
                    funcCallName = m.group(1)
                    listCurrBlockFuncCalls.append(funcCallName)
                    continue
            
                # 2.d. look for return instructions
                m = re_returnLine.match(line)
                if m is not None:
                    # Flag to say current basic block returns
                    isCurrBasicBlockReturning = 1
                    continue
            
            # look for end of function definition
            m = re_funcDefEnd.match(line)
            if m is not None:
                currFuncEndLine = lineNum - 1
                for blockTarget in listCurrFuncBasicBlockTargets:
                    startBlockIndex = -1
                    index = 0
                    for block in listCurrFuncBasicBlocks:
                        if block.name == blockTarget.name:
                            startBlockIndex = index
                            break
                        index = index + 1
                        
                    if startBlockIndex == -1:
                        raise ParseError("Block %s with entry in listCurrFuncBasicBlockTargets not found in listCurrFuncBasicBlocks" % (blockTarget.name))
                        exit(1)
                        
                    for target in blockTarget.listTargets:
                        endBlockIndex = -1
                        index = 0
                        for block in listCurrFuncBasicBlocks:
                            if block.name == target:
                                endBlockIndex = index
                                break
                            index = index + 1
                        if endBlockIndex == -1:
                            raise ParseError("Block %s, a target of block %s with entry in listCurrFuncBasicBlockTargets not found in listCurrFuncBasicBlocks" % (target, blockTarget.name))
                            exit(1)
                        listCurrFuncBBEdges.append(BBEdge(startBlockIndex,
                                                          endBlockIndex))
                    
                    if not blockTarget.listTargets and listCurrFuncBasicBlocks[startBlockIndex].isReturning == 0:
                        # if current block had no targets, edge to next block
                        listCurrFuncBBEdges.append(BBEdge(startBlockIndex,
                                                          startBlockIndex + 1))
                
                listFunctions.append(FunctionDesc(currFuncName,
                                                  fileName,
                                                  currFuncStartLine,
                                                  currFuncEndLine,
                                                  ControlFlowGraph(listCurrFuncBasicBlocks,
                                                                   listCurrFuncBBEdges)))                        
                
                # Resetting State Variables
                inFunctionBody = 0
                inFuncDefArgMultiLine = 0
                currFuncName = ""
                currFuncStartLine = 0
                currFuncEndLine = 0
                listCurrFuncBasicBlocks = []
                listCurrFuncBasicBlockTargets = []
                listCurrFuncBBEdges = []
                continue

    file.close()
    return listFunctions

def print_debug_isc(listFunctions):
    for func in listFunctions:
        print("\nFileName : %s" % (func.fileName))
        print("Function : %s" % (func.functionName))
        i = 0
        for block in func.cfg.listBlocks:
            print("\t Block %s: line %d - %d, flow = %f" % (block.name, block.startLine, block.endLine, block.flow))
            for funcCall in block.listFunctionCalls:
                print("\t\t calls %s()" % (funcCall))
            if block.isReturning == 1:
                print("\t\t returns")
            for edge in func.cfg.listEdges:
                if edge.fromBlockIndex == i:
                    print("\t\t Edge to block %s" % (func.cfg.listBlocks[edge.toBlockIndex].name))
            i = i + 1
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        listFileNames = sys.argv[1:]
    else:
        print_usage()
        exit(1)
    
    listFunctions = []
    
    for fileName in listFileNames:
        listFunctions = listFunctions + parse_isc(fileName)
    
    print_debug_isc(listFunctions)