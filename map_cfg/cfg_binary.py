#-----------------------------------------------------------------
# cfg_binary.py: Construct Control Flow Graph for Binary
#-----------------------------------------------------------------

import sys
import re
from cfg import *

re_sectionStart = re.compile('Disassembly of section .(.*):')
re_funcDef = re.compile('\s*([0-9a-f]*)\s*<(.*)>:')
re_instruction = re.compile('\s*([0-9a-f]*):\s*[0-9a-f]*\s*(.*)')
re_branchInst = re.compile('\s*(b(?:l|x|lx|xj)?(?:eq|ne|mi|pl|hi|ls|ge|lt|gt|le)?)\s*([0-9a-f]*)\s*<(.*)>')
re_unconditionalBranchInst = re.compile('\s*(b(?:l|x|lx|xj)?)\s*([0-9a-f]*)\s*<(.*)>')
re_conditionalBranchInst = re.compile('\s*(b(?:l|x|lx|xj)?(?:eq|ne|mi|pl|hi|ls|ge|lt|gt|le))\s*([0-9a-f]*)\s*<(.*)>')
re_returnInst = re.compile('\s*(bx)\s*(lr)')

listFunctionsIgnore = ['__cs3_interrupt_vector',
                        '__cs3_reset',
                        '__cs3_start_asm_sim',
                        '__cs3_heap_start_ptr',
                        '__cs3_start_c',
                        '__do_global_dtors_aux',
                        'frame_dummy',
                        'atexit',
                        'exit',
                        '__register_exitproc',
                        '__call_exitprocs',
                        'register_fini',
                        '__libc_fini_array',
                        '__cs3_premain',
                        '_exit',
                        '__cs3_isr_interrupt',
                        '__libc_init_array']
            

def print_usage():
    print("Usage:")
    print("\t %s <objdump_fileName>\n" % (sys.argv[0]))

    
def parse_binary(fileName, listFunctionNames = []):
    '''
    Returns a list of all the functions defined in the objdump, along with the
    control flow graph of each of the function.
    '''
    
    # State Management Variables
    inTextSection = 0   # is 1, when inside Text Section
    inFuncBody = 0      # is 1, when inside Function Body
    currFuncName = ""
    currFuncFileName = ""
    currFuncStartLine = 0
    listCurrFuncBlockStartLineNum = []
    listCurrFuncBlockEndLineNum = []
    listCurrFuncBlockStartAddress = []
    listCurrFuncBlockEndAddress = []
    lineNumForAddress = {}
    branchInstAtLine = {}
    returnInstAtLine = {}
    functionCallAtLine = {}
    
    # list of functions that will be returned
    listFunctions = []
    
    file = open(fileName, 'r')
    lineNum = 0
    for line in file:
        '''
        Main loop that parses the objdump file line by line.
        Algorithm:
        1. We only care for the .text section. Ignore lines in other sections.
        2. Inside text section, look for start of function definition.
        3. Inside Function, look for branch instruction. At each branch inst.
            a. End of block at branch instruction.
            b. Start of block at target of branch instruction.
            c. End of block at inst. before target of branch inst.
            d. Start of block at inst. after branch inst.
        4. Inside Function, also look for return instruction.
            a. End of block at return instruction.
        ''' 
        lineNum = lineNum + 1;
        # 1. Ignore sections other than .text sections
        m = re_sectionStart.match(line);
        if m == None and inTextSection == 0:
            continue
        elif (m != None and m.group(1) != "text"):
            if(inTextSection == 1):
                # was in text section, and text section ended
                break
        elif (m != None and m.group(1) == "text"):
            inTextSection = 1
            continue
        elif m == None and inTextSection == 1:
            # inside text section
            # 2. Look for start of function definition.
            m = re_funcDef.match(line)
            # if listFunctionNames provided, check if function name is in list
            # if not, check that function name is not in listFunctionsIgnore
            if m is not None and ((len(listFunctionNames) > 0 and 
                                   m.group(2) in listFunctionNames) or 
                                  (len(listFunctionNames) == 0 and 
                                   m.group(2) not in listFunctionsIgnore)):
                inFuncBody = 1
                currFuncName = m.group(2)
                currFuncFileName = fileName
                currFuncStartLine = lineNum + 1
                listCurrFuncBlockStartLineNum.append(currFuncStartLine)
                continue
            
            if(inFuncBody == 1):
                m = re_instruction.match(line)
                if m is not None:
                    address = m.group(1)
                    lineNumForAddress[address] = lineNum;
                    inst = m.group(2)
                    
                    m = re_branchInst.match(inst)
                    if m is not None and m.group(3).startswith(currFuncName):
                        # Branch Instruction
                        branchInstAtLine[lineNum] = inst
                        # 3.a End Block at Branch Inst.
                        listCurrFuncBlockEndAddress.append(address)
                        # 3.b Start Block at Target Address
                        targetAdd = m.group(2);
                        listCurrFuncBlockStartAddress.append(targetAdd)
                        # 3.c End Block before Target Address
                        listCurrFuncBlockEndAddress.append("%x" % (int(targetAdd, 16) - 4))
                        # 3.d Start Block after Branch Inst.
                        listCurrFuncBlockStartAddress.append("%x" % (int(address, 16) + 4))
                        continue
                    elif m is not None and not m.group(3).startswith(currFuncName):
                        # Function call
                        functionCallAtLine[lineNum] = inst
                        continue
                    
                    m = re_returnInst.match(inst)
                    if m is not None:
                        # Return Instruction
                        returnInstAtLine[lineNum] = inst
                        listCurrFuncBlockEndAddress.append(address)
                        continue
                    
                    continue
                else:
                    # inside Function, instruction did not match i.e. end of
                    #    function body.
                    # TODO: Explicitly check for a blank line
                    inFuncBody = 0
                    currFuncEndLine = lineNum - 1
                    # Construct the CFG here.
                    
                    # Create list of line numbers
                    for add in listCurrFuncBlockStartAddress:
                        listCurrFuncBlockStartLineNum.append(lineNumForAddress[add])
                    for add in listCurrFuncBlockEndAddress:
                        listCurrFuncBlockEndLineNum.append(lineNumForAddress[add])
                    
                    # Remove duplicates from the lists
                    listCurrFuncBlockStartLineNum = list(set(listCurrFuncBlockStartLineNum))
                    listCurrFuncBlockEndLineNum = list(set(listCurrFuncBlockEndLineNum))
                    # Sort the lists
                    listCurrFuncBlockStartLineNum.sort()
                    listCurrFuncBlockEndLineNum.sort()
                    
                    # Ensure length of lists is equal
                    if len(listCurrFuncBlockStartLineNum) != len(listCurrFuncBlockEndLineNum):
                        raise ParseError("Length of lists of block start and end line numbers do not match for function %s" % (currFuncName))
                    
                    # Create List of Blocks
                    listBlocks = []
                    for i in range(len(listCurrFuncBlockStartLineNum)):
                        listBlocks.append(BasicBlock(listCurrFuncBlockStartLineNum[i],
                                                     listCurrFuncBlockEndLineNum[i]))
                    
                    
                    
                    # Create list of Edges
                    listEdges = []
                    for lNum in branchInstAtLine:
                        edgeStartBlockIndex = -1;
                        edgeEndBlockIndex = -1;
                        
                        for i in range(len(listBlocks)):
                            if listBlocks[i].endLine == lNum:
                                edgeStartBlockIndex = i;
                        inst = branchInstAtLine[lNum]
                        m = re_branchInst.match(inst)
                        targetAdd = m.group(2)
                        targetLine = lineNumForAddress[targetAdd]
                        for i in range(len(listBlocks)):
                            if listBlocks[i].startLine == targetLine:
                                edgeEndBlockIndex = i;
                        
                        if (edgeStartBlockIndex == -1 or edgeEndBlockIndex == -1):
                            raise ParseError("Matching edge for branch inst. could not be created in function %s" % (currFuncName))
                        
                        listEdges.append(BBEdge(edgeStartBlockIndex, 
                                                edgeEndBlockIndex))
                        
                        # For Conditional Branches, add an edge to next block
                        m = re_conditionalBranchInst.match(inst)
                        if m is not None:
                            listEdges.append(BBEdge(edgeStartBlockIndex,
                                                    edgeStartBlockIndex + 1))
                            
                    # For Block End Line, which are not branch instructions,
                    #    add edge to next block
                    for i in range(len(listBlocks)):
                        blockEndLine = listBlocks[i].endLine;
                        if blockEndLine not in branchInstAtLine and blockEndLine not in returnInstAtLine:
                            listEdges.append(BBEdge(i, i + 1))
                            
                    # Mark the returning blocks
                    for lNum in returnInstAtLine:
                        for block in listBlocks:
                            if block.endLine == lNum:
                                block.isReturning = 1
                                
                    # Add list of functions called in each block
                    for lNum in functionCallAtLine:
                        inst = functionCallAtLine[lNum]
                        m = re_branchInst.match(inst)
                        calledFuncName = m.group(3)
                        for block in listBlocks:
                            if block.startLine <= lNum and block.endLine >= lNum:
                                block.listFunctionCalls.append(calledFuncName)
                        
                    # Add the current function and the CFG to the list of functions
                    listFunctions.append(FunctionDesc(currFuncName,
                                                      currFuncFileName,
                                                      currFuncStartLine,
                                                      currFuncEndLine,
                                                      ControlFlowGraph(listBlocks,
                                                                       listEdges)))
                    
                    # reset the state management variables
                    currFuncName = ""
                    currFuncFileName = ""
                    currFuncStartLine = 0
                    currFuncEndLine = 0
                    listCurrFuncBlockStartLineNum = []
                    listCurrFuncBlockEndLineNum = []
                    listCurrFuncBlockStartAddress = []
                    listCurrFuncBlockEndAddress = []
                    lineNumForAddress = {}
                    branchInstAtLine = {}
                    returnInstAtLine = {}
                    functionCallAtLine = {}
    
    return listFunctions
                    
                    
def print_debug_binary(listFunctions):
    for func in listFunctions:
        print("\nlFileName : %s" % (func.fileName))
        print("Function : %s" % (func.functionName))
        i = 0
        for block in func.cfg.listBlocks:
            print("\t Block %d: line %d - %d, flow = %f" % (i, block.startLine, block.endLine, block.flow))
            for funcCall in block.listFunctionCalls:
                print("\t\t calls %s()" % (funcCall))
            if block.isReturning == 1:
                print("\t\t returns")
            for edge in func.cfg.listEdges:
                if edge.fromBlockIndex == i:
                    print("\t\t Edge to block %d" % (edge.toBlockIndex))
            i = i + 1
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        print_usage()
        exit(1)
        
    listFunctions = parse_binary(fileName)
    
    print_debug_binary(listFunctions)