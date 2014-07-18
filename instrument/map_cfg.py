#-----------------------------------------------------------------
# map_cfg.py: Map Control Flow Graphs from Binary and ISC
#-----------------------------------------------------------------

from optparse import OptionParser
from subprocess import call
import logging
import re
from collections import deque
import sys
from PyQt4 import QtGui, QtCore

from cfg_binary import parse_binary, print_debug_binary
from cfg_isc import parse_isc, print_debug_isc
from display_cfg import display_cfgs



######################################################
## Global Variables
######################################################

COND_EXEC_BLOCKLEN_THRESH = 4

app = None

listISCFileNames = []
listObjdumpFileNames = []
listBinaryFileNames = []

class GDBMapTarget:
    def __init__(self, fileName, lineNum):
        self.fileName = fileName
        self.lineNum = lineNum

def printDebugMapCFG(listISCFunctions, listObjdumpFunctions, gdbMapping):
    for func in listObjdumpFunctions:
        print("\nFileName : %s" % (func.fileName))
        print("Function : %s" % (func.functionName))
        ISCFuncCfg = find(lambda fn: fn.functionName == func.functionName, listISCFunctions).cfg
        i = 0
        for block in func.cfg.listBlocks:
            print("\t Block %d: line %d - %d, flow = %f, nestingLevel = %d" % 
                  (i, block.startLine, block.endLine, 
                   block.flow, block.nestingLevel))
            print "\t Maps to ",
            block.mapsTo = list(set(block.mapsTo))
            for blockIndISC in block.mapsTo:
                print ISCFuncCfg.listBlocks[blockIndISC].name+", ",
            print ""
            for funcCall in block.listFunctionCalls:
                print("\t\t calls %s()" % (funcCall))
            if block.hasConditionalExec == 1:
                print("\t\t Conditional Execution Instruction!")
            if block.isReturning == 1:
                print("\t\t returns")
            for edge in func.cfg.listEdges:
                if edge.fromBlockIndex == i:
                    print("\t\t Edge to block %d" % (edge.toBlockIndex))
            for lineNum in range(block.startLine, block.endLine):
                if lineNum in gdbMapping:
                    ISCFileName = gdbMapping[lineNum].fileName
                    ISCLineNum = gdbMapping[lineNum].lineNum
                    ISCBlock = ISCFuncCfg.find(lineNum = ISCLineNum)
                    if ISCBlock is not None:
                        ISCBlockName = ISCFuncCfg.find(lineNum = ISCLineNum).name
                    else:
                        ISCBlockName = "%d" % (ISCLineNum)
                    print("\t\t Line %d from %s:%s" % (lineNum,
                                                       gdbMapping[lineNum].fileName,
                                                       ISCBlockName))
            i = i + 1
            
    for func in listISCFunctions:
        print("\nFileName : %s" % (func.fileName))
        print("Function : %s" % (func.functionName))
        ObjFuncCfg = find(lambda fn: fn.functionName == func.functionName, listObjdumpFunctions).cfg
        i = 0
        for block in func.cfg.listBlocks:
            print("\t Block %s: line %d - %d, flow = %f, nestingLevel = %d" % 
                  (func.cfg.listBlocks[i].name, block.startLine, block.endLine, 
                   block.flow, block.nestingLevel))
            print "\t Maps to ",
            print list(set(block.mapsTo))
            for funcCall in block.listFunctionCalls:
                print("\t\t calls %s()" % (funcCall))
            if block.hasConditionalExec == 1:
                print("\t\t Conditional Execution Instruction!")
            if block.isReturning == 1:
                print("\t\t returns")
            for edge in func.cfg.listEdges:
                if edge.fromBlockIndex == i:
                    print("\t\t Edge to block %s" % (func.cfg.listBlocks[edge.toBlockIndex].name))
            i = i + 1

def gdbMappingDebug(gdbMapping):
    for lineNum in gdbMapping:
        print ("line %d maps to %s:%d" % (lineNum, gdbMapping[lineNum].fileName, gdbMapping[lineNum].lineNum))

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item

def getGDBMapping(binFileName, objdumpLineNumForAddress):
    gdbMapping = {}
    
    re_gdbInfoLineOutput = re.compile('Line (\d*) of "(.*)" starts at address 0x([0-9a-f]*).*')
    
    # File Name for GDB Command file
    gdbXFileName = binFileName+".gdbx"
    gdbXFile = open(gdbXFileName, 'w')
    
    for address in objdumpLineNumForAddress:
        line = "info line *0x%x\n" % (int(address, 16))
        gdbXFile.write(line)
    
    gdbXFile.write("quit\n")
    gdbXFile.close()
    
    gdbOutputFileName = binFileName+".gdbo"
    gdbOutputFile = open(gdbOutputFileName, 'w')
    call(args=["gdb", "--quiet", "--command="+gdbXFileName, binFileName], 
         stdout=gdbOutputFile)
    gdbOutputFile.close()
    
    gdbOutputFile = open(gdbOutputFileName, 'r')
    for line in gdbOutputFile:
        m = re_gdbInfoLineOutput.match(line)
        if m is not None:
            targetLineNum =  int(m.group(1), 10)
            targetFileName = m.group(2)
            objdumpAddress = m.group(3)
            objdumpLineNum = objdumpLineNumForAddress[objdumpAddress]
            gdbMapping[objdumpLineNum] = GDBMapTarget(targetFileName, targetLineNum)
    gdbOutputFile.close()
    
#     gdbMappingDebug(gdbMapping)
    
    return gdbMapping
    
mappingStackISC = []  
mappingStackObj = []    
    
def mapping(cfgISC, blockIndISC, cfgObj, blockIndObj, mergedLevelsISC, gdbMapping):
#     raw_input("Press any key to continue ...")
    '''
    Recursinve Function to trace the Control Flow Graphs in Depth First Fashion
    in order to match the corresponding blocks
    
    Algorithm:
    1. The recursive function is first called for the root block of ISC and 
        Objdump. The current node index is stored in blockIndISC and blockIndObj. 
    2. mappingStackISC and mappingStackObj are stacks to maintain the control
        flow for each branch in ISC and Objdump. The current node index is added
        to the stack.
    3. Here after each situation is carefully handled. 
        a. Both blocks return.
            1. If both blocks are returning, we assume the blocks match as there
                should be only one returning block in each.
            2. We add the index of ISC block to mapsTo array in the Objdump
                block, and vice-a-versa.
            3. We pop one entry from the mappingStackISC and mappingStackObjdump
                for the matched node.
        b. Check if flow, nesting level and isReturning are not same.
            1. Either of these being not same means, the blocks don't match.
        c. listSuccObj is list of successors of blockIndObj, and similarly
            listSuccISC is list of successors of blockIndISC.
        d. if length of list of successors without back edges for both
            blocks is not same and current obj block has conditional 
            execution (predication).
            1. Calculate the length of the shortest block in the list of
                successors. This length should be smaller than the
                threshold, for it to be optimal for conditional execution.
                If true:
                a. case 1: The current ISC block has 2 branches, and one of 
                    the branch merges with the other.
                    In this case, the the Obj block is matched to the common
                    child, and all three ISC blocks are matched to the
                    current Obj block.
                b. case 2: the current ISC block has 2 branches, and both 
                    merge with a fourth node.
                    In this case, the the Obj block is matched to the fourth
                    node, and all four ISC blocks are matched to the current
                    Obj block.
                -> In each of the case, we call mapping function recursively
                    on the current obj block and the common child in the 
                    conditional execution construct. The mapping function
                    checks if corresponding decision is supported by
                    following nodes in ISC and Objdump CFGs, and returns 0,
                    only when mapping function returns 0, saying this is
                    the best match.
                -> If neither matches, it means it is either not Conditional
                    Execution, or it is a corner case.
                If false:
                a. Issue warning, for corner case that may occur for last
                    ISC node in the conditional execution construct. In this
                    case we will proceed to check for the method to match.
        e. Coming here means, conditional execution was not found. If length of 
            list of successors is same, run mapping function for match of the 
            successor blocks. If mapping succeeds, pop one entry from each stack
            for blockIndISC and blockIndObj and return 0.
        f. Coming here means no conditional execution, and length of successors
            lists is not equal. Refer the the GDB Mapping to match the blocks 
            now, since nothing else works!
    
    '''
    
#     a = input("Press Enter to continue...")
    mappingStackISC.append(blockIndISC)
    mappingStackObj.append(blockIndObj)
    blockISC = cfgISC.listBlocks[blockIndISC]
    blockObj = cfgObj.listBlocks[blockIndObj]
    logging.debug("\tMapping blocks ISC:%s and OBJ:%d" % (blockISC.name, blockIndObj))
    logging.debug( "\tmergedLevelsISC = %d" % (mergedLevelsISC))
    
    if (blockISC.isReturning == 1 and
        blockObj.isReturning == 1):
        logging.debug( "\t\tBoth Blocks return!!!")
        blockISC.mapsTo.append(blockIndObj)
        blockObj.mapsTo.append(blockIndISC)
        mappingStackISC.pop()
        mappingStackObj.pop()
        return 0 
    
    listSuccISC = cfgISC.successorBlocks(blockIndISC)
    listSuccObj = cfgObj.successorBlocks(blockIndObj)
    listSuccWOBackEdgeISC = cfgISC.successorBlocksWOBackEdges(blockIndISC)
    listSuccWOBackEdgeObj = cfgObj.successorBlocksWOBackEdges(blockIndObj)

    if (blockISC.isReturning == 1 and 
        len(listSuccObj) == 1 and 
        cfgObj.listBlocks[listSuccObj[0]].isReturning == 1):
        print "Here"
        blockISC.mapsTo.append(blockIndObj)
        blockObj.mapsTo.append(blockIndISC)
        cfgObj.listBlocks[listSuccObj[0]].mapsTo.append(blockIndISC)
        mappingStackISC.pop()
        mappingStackObj.pop()
        return 0

    if (blockISC.flow != blockObj.flow or 
#         (blockISC.nestingLevel - mergedLevelsISC) != blockObj.nestingLevel or
        blockISC.isReturning != blockObj.isReturning):
        logging.debug( "\t\tFlow did not match or only one of them returns!")
        logging.debug( "")
#         logging.debug( "\t\tblockISC.nestingLevel - mergedLevelsISC = %d; blockObj.nestingLevel = %d" % ((blockISC.nestingLevel-mergedLevelsISC), blockObj.nestingLevel))
        mappingStackISC.pop()
        mappingStackObj.pop()
        return -1
     
#     if (blockIndISC, blockIndObj) in mappingDict:
#         return mappingDict[(blockIndISC, blockIndObj)]
     
    mincost = -1
    
    logging.debug("\t Checking for Conditional Execution")
    if(len(listSuccWOBackEdgeISC) != len(listSuccWOBackEdgeObj)) and blockObj.hasConditionalExec == 1:
        minSuccBlockLength = -1
        for succBlockISC in listSuccISC:
            blockLength = cfgISC.listBlocks[succBlockISC].endLine - cfgISC.listBlocks[succBlockISC].startLine
            if blockLength < minSuccBlockLength:
                minSuccBlockLength = blockLength
                
        if minSuccBlockLength < COND_EXEC_BLOCKLEN_THRESH:
            logging.debug( "\t\t Conditional Execution Found!")
            # Conditional Execution!
            for succ1BlockISC in listSuccISC:
                if succ1BlockISC in mappingStackISC:
                    continue
                for succSucc1BlockISC in cfgISC.successorBlocks(succ1BlockISC):
                    if succSucc1BlockISC in mappingStackISC:
                        continue
                    for succ2BlockISC in list(set(listSuccISC) - {succ1BlockISC}):
                        if succ2BlockISC in mappingStackISC:
                            continue
                        if succSucc1BlockISC == succ2BlockISC:
                            # case 1
                            logging.debug( "\t\t case 1")
                            mappingStackISC.append(succ1BlockISC)
                            mappingStackObj.pop() # popping blockIndObj, because mapping it again
                            if mapping(cfgISC, succ2BlockISC, cfgObj, blockIndObj, mergedLevelsISC + 1, gdbMapping) == 0:
                                cfgISC.listBlocks[blockIndISC].mapsTo.append(blockIndObj)
                                cfgISC.listBlocks[succ1BlockISC].mapsTo.append(blockIndObj)
                                cfgISC.listBlocks[succ2BlockISC].mapsTo.append(blockIndObj)
                                cfgObj.listBlocks[blockIndObj].mapsTo.append(succ2BlockISC)
                                mappingStackISC.pop()
                                mappingStackISC.pop()
                                return 0
                            else:
                                print "HERE!!"
                                mappingStackObj.append(blockIndObj) # Adding what was removed above
                                # mappingStackISC.append(succ2BlockISC) # was already done above, no need to do again
                                mappingStackISC.append(succ2BlockISC)
                                listSuccSucc2BlockISC = cfgISC.successorBlocks(succ2BlockISC)
                                for succSucc2BlockISC in listSuccSucc2BlockISC:
                                    if succSucc2BlockISC in mappingStackISC:
                                        continue;
                                    for succBlockObj in listSuccObj:
                                        if succBlockObj in mappingStackISC:
                                            continue;
                                        if mapping(cfgISC, succSucc2BlockISC, cfgObj, succBlockObj, mergedLevelsISC+2, gdbMapping) == 0:
                                            cfgISC.listBlocks[blockIndISC].mapsTo.append(blockIndObj)
                                            cfgISC.listBlocks[succ1BlockISC].mapsTo.append(blockIndObj)
                                            cfgISC.listBlocks[succ2BlockISC].mapsTo.append(blockIndObj)
                                            cfgObj.listBlocks[blockIndObj].mapsTo.append(succ2BlockISC)
                                            mappingStackISC.pop() # succ1BlockISC
                                            mappingStackISC.pop() # succ2BlockISC
                                            mappingStackISC.pop() # blockIndISC
                                            mappingStackObj.pop() # blockIndObj
                                            return 0
                                            
                                # Coming here means case 1 could not be successfully mapped            
                                mappingStackISC.pop() # succ1BlockISC
                                mappingStackISC.pop() # succ2BlockISC
                                                                  
                    for succ2BlockISC in list(set(listSuccISC) - {succ1BlockISC}):
                        if succ2BlockISC in mappingStackISC:
                            continue
                        for succSucc2BlockISC in cfgISC.successorBlocks(succ2BlockISC):
                            if succSucc2BlockISC in mappingStackISC:
                                continue
                            if succSucc1BlockISC == succSucc2BlockISC:
                                # case 2
                                logging.debug( "\t\t case 2")
                                mappingStackISC.append(succ1BlockISC)
                                mappingStackISC.append(succ2BlockISC)
                                mappingStackObj.pop() # popping blockIndObj, because mapping it again
                                if mapping(cfgISC, succSucc1BlockISC, cfgObj, blockIndObj, mergedLevelsISC+2, gdbMapping) == 0:
                                    cfgISC.listBlocks[blockIndISC].mapsTo.append(blockIndObj)
                                    cfgISC.listBlocks[succ1BlockISC].mapsTo.append(blockIndObj)
                                    cfgISC.listBlocks[succ2BlockISC].mapsTo.append(blockIndObj)
                                    cfgISC.listBlocks[succSucc1BlockISC].mapsTo.append(blockIndObj)
                                    cfgObj.listBlocks[blockIndObj].mapsTo.append(succSucc1BlockISC)
                                    mappingStackISC.pop()
                                    mappingStackISC.pop()
                                    mappingStackISC.pop()
                                    return 0
                                else:
                                    # mappingStackISC.append(succ1BlockISC) # Was already done above, no need twice
                                    # mappingStackISC.append(succ2BlockISC) # Was already done above, no need twice
                                    mappingStackISC.append(succSucc1BlockISC)
                                    mappingStackObj.append(blockIndObj) # was popped above, restoring it
                                    listSuccSuccSucc1BlockISC = cfgISC.successorBlocks(succSucc1BlockISC)
                                    for succSuccSucc1BlockISC in listSuccSuccSucc1BlockISC:
                                        if succSuccSucc1BlockISC in mappingStackISC:
                                            continue
                                        for succBlockObj in listSuccObj:
                                            if succBlockObj in mappingStackISC:
                                                continue;
                                            if mapping(cfgISC, succSuccSucc1BlockISC,
                                                       cfgOBJ, succBlockObj,
                                                       mergedLevelsISC+3, gdbMapping) == 0:
                                                mappingStackISC.pop() # succ1BlockISC
                                                mappingStackISC.pop() # succ2BlockISC
                                                mappingStackISC.pop() # succSucc1BlockISC
                                                mappingStackISC.pop() # blockIndISC
                                                mappingStackObj.pop() # blockIndObj
                                                return 0
                                    
                                    # Coming here means case 2 could not be successfully mapped
                                    mappingStackISC.pop() # succ1BlockISC
                                    mappingStackISC.pop() # succ1BlockISC
                                    mappingStackISC.pop() # succSucc1BlockISC
                                    
            # Should not come here!
            logging.warning ("Expected Conditional Execution, but not of the matches were valid!")
            #TODO: Add more information about warning
        else:
            logging.warning("Conditional Execution found, but suspecting it to be last node, since length of successor block is more than threshold")
            #TODO: Add more information about warning

    logging.debug("\t Checking if length of successors is same!")
    logging.debug("\t len(listSuccISC) = %d; len(listSuccObj) = %d" % (len(listSuccISC), len(listSuccObj)))
    if len(listSuccISC) == len(listSuccObj):
        logging.debug ("\t\t length of successors lists is same!")                                        
        for succBlockISC in listSuccISC:
            if succBlockISC in mappingStackISC:
                logging.debug("%d in mappingStackISC" % succBlockISC)
                continue
            for succBlockObj in listSuccObj:
                if succBlockObj in mappingStackObj:
                    logging.debug("%d in mappingStackISC" % succBlockObj)
                    continue
                if mapping(cfgISC, succBlockISC, cfgObj, succBlockObj, mergedLevelsISC, gdbMapping) == 0:
                    blockISC.mapsTo.append(blockIndObj)
                    blockObj.mapsTo.append(blockIndISC)
                    mappingStackISC.pop()
                    mappingStackObj.pop() 
                    return 0
                else:
                    continue

    deepestISCBlock = -1
    deepestISCBlockNestingLevel = -1
    logging.debug ("GDBMAPPING:  using gdbMapping to map blockObj %d:%d-%d" % (blockIndObj, blockObj.startLine, blockObj.endLine))
    blockObj.mapsTo = []
    for lineNum in range(blockObj.startLine, blockObj.endLine):
        if lineNum in gdbMapping:
            ISCFileName = gdbMapping[lineNum].fileName
            ISCLineNum = gdbMapping[lineNum].lineNum
#             logging.debug("GDBMAPPING:  objline %d maps to %s:%d" % (lineNum, ISCFileName, ISClineNum))
            for i in range(len(cfgISC.listBlocks)):
                if (cfgISC.listBlocks[i].startLine <= ISCLineNum and
                    cfgISC.listBlocks[i].endLine >= ISCLineNum):
                    if i not in blockObj.mapsTo:
                        blockObj.mapsTo.append(i)
                    if deepestISCBlockNestingLevel < cfgISC.listBlocks[i].nestingLevel and i != blockIndISC:
                        # The deepest ISC Block is not inserted in mappingStackISC
                        #    because mapping will be called on this block, and
                        #    it will be inserted by the next iteration of the
                        #    mapping function. Insert the block in stack, which
                        #    was previously thought of being deepest.
                        logging.debug ("GDBMAPPING:  deepestISCBlock = %s" % cfgISC.listBlocks[i].name)
                        if deepestISCBlock != -1:
                            mappingStackISC.append(deepestISCBlock)
                        deepestISCBlock = i
                        deepestISCBlockNestingLevel < cfgISC.listBlocks[i].nestingLevel
                        break
                    else:
                        mappingStackISC.append(i)
                        continue
    
    if deepestISCBlock != -1:
        mappingStackObj.pop() # popping blockIndObj from stack, as mapping is called on it again.
        mergedLevelsISC = mergedLevelsISC + cfgISC.listBlocks[deepestISCBlock].nestingLevel - blockISC.nestingLevel
        if mapping(cfgISC, deepestISCBlock, cfgObj, blockIndObj, mergedLevelsISC, gdbMapping) == 0:
            for i in range(len(blockObj.mapsTo)-1):
                # pop each entry from ISC to which the blockIndObj maps to
                mappingStackISC.pop()
            return 0 # successful mapping

    logging.error("No mapping algorithm has worked!")
    #TODO : Add more information about error
    exit(1)

def map_cfg(listISCFileNames, listObjdumpFileNames, listBinaryFileNames):
    global mappingStackISC
    global mappingStackObj
    listISCFunctions = []
    listFunctionNames = []
    listObjdumpFunctions = []
    gdbMapping = []
    
    # Parse the ISC files
    for ISCFileName in listISCFileNames:
        listISCFunctions = listISCFunctions + parse_isc(ISCFileName)
        for function in listISCFunctions:
            listFunctionNames.append(function.functionName)
            logging.debug("parsed "+ISCFileName) 
    
    # Parse the objdump files
    for ObjdumpFileName in listObjdumpFileNames:
        (tempListObjdumpFunctions, objdumpLineNumForAddress) = parse_binary(ObjdumpFileName, 
                                                                   listFunctionNames)
        listObjdumpFunctions = listObjdumpFunctions +  tempListObjdumpFunctions
        
   
    # Check that we found all functions in ISC in Objdump
    if len(listISCFunctions) != len(listObjdumpFunctions):
        raise ParseError("all functions in ISC file not found in Objdump file!")
    
    for function in listISCFunctions:
        logging.debug("Computing flow for function %s from file %s" % (function.functionName, function.fileName))
        function.cfg.computeFlow()
        
    for function in listObjdumpFunctions:
        logging.debug("Computing flow for function %s from file %s" % (function.functionName, function.fileName))
        function.cfg.computeFlow()

    for binaryFileName in listBinaryFileNames:
        gdbMapping = getGDBMapping(binaryFileName, objdumpLineNumForAddress)


#     print_debug_isc (listISCFunctions)
#     print_debug_binary (listObjdumpFunctions, gdbMapping)
    printDebugMapCFG(listISCFunctions, listObjdumpFunctions, gdbMapping)
     
#     display_cfgs(app, listISCFunctions[0].cfg, listObjdumpFunctions[0].cfg, "%s" % listISCFunctions[0].functionName)
    
    for fnISC in listISCFunctions:
        mappingStackISC = []  
        mappingStackObj = []  
        cfgISC = fnISC.cfg
        fnObj = find(lambda fn: fn.functionName == fnISC.functionName, listObjdumpFunctions)
        cfgObj = fnObj.cfg
        
        logging.debug( "Mapping Function %s" % (fnISC.functionName))
        if mapping(cfgISC=cfgISC, blockIndISC=0, cfgObj=cfgObj, blockIndObj=0, mergedLevelsISC=0, gdbMapping=gdbMapping) == 0:
            logging.debug( "Mapping Found!!!!")
            print mappingStackISC
            print mappingStackObj
        else:
            logging.debug( "Fuck my life!!!")
            
#     print_debug_isc (listISCFunctions)
#     print_debug_binary (listObjdumpFunctions, gdbMapping)
            
    printDebugMapCFG(listISCFunctions, listObjdumpFunctions, gdbMapping)
    
    for funcISC in listISCFunctions:
        funcObj = find(lambda fn: fn.functionName == funcISC.functionName, listObjdumpFunctions)
        display_cfgs(app, funcISC.cfg, funcObj.cfg, "%s" % fnISC.functionName)
        
    return listISCFunctions, listObjdumpFunctions


if __name__ == "__main__":
#     listISCFileNames = []
#     listObjdumpFileNames = []
    app = QtGui.QApplication(sys.argv)

    logging.basicConfig(level=logging.DEBUG)
    optparser = OptionParser()
    optparser.add_option("-i", "--isc", action="append", dest="listISCFileNames",
                         type="string", help="ISC Filename. For multiple files, use -i <filename> multiple times.",
                         metavar="FILE")
    optparser.add_option("-o", "--objdump", action="append",
                         type="string", dest="listObjdumpFileNames", 
                         help="Objdump Filename. For multiple files, use -o <filename> multiple times.",
                         metavar="FILE")
    optparser.add_option("-b", "--binary", action="append",
                         type="string", dest="listBinaryFileNames", 
                         help="Binary Filename. For multiple files, use -b <filename> multiple times.",
                         metavar="FILE")
    
    (options, args) = optparser.parse_args()
    
    if (len(args) > 0):
        print "Addtional arguments are being ignored"
    
    listISCFileNames =  options.listISCFileNames
    listObjdumpFileNames = options.listObjdumpFileNames
    listBinaryFileNames = options.listBinaryFileNames
    
    map_cfg(listISCFileNames, listObjdumpFileNames, listBinaryFileNames)
    