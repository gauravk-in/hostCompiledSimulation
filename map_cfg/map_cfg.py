#-----------------------------------------------------------------
# map_cfg.py: Map Control Flow Graphs from Binary and ISC
#-----------------------------------------------------------------

from optparse import OptionParser
from subprocess import call
import logging
import re

from cfg_binary import parse_binary, print_debug_binary
from cfg_isc import parse_isc, print_debug_isc


from collections import deque

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
    
def mapping(cfgISC, blockIndISC, cfgObj, blockIndObj, mergedLevelsISC):
#     a = input("Press Enter to continue...")
    mappingStackISC.append(blockIndISC)
    mappingStackObj.append(blockIndObj)
    blockISC = cfgISC.listBlocks[blockIndISC]
    blockObj = cfgObj.listBlocks[blockIndObj]
    print "\tMapping blocks ISC:%s and OBJ:%d" % (blockISC.name, blockIndObj)
    print "\tmergedLevelsISC = %d" % (mergedLevelsISC)
    
    if (blockISC.isReturning == 1 and
        blockObj.isReturning == 1):
        print "\t\tBoth Blocks return!!!"
        blockISC.mapsTo.append(blockIndObj)
        blockObj.mapsTo.append(blockIndISC)
        mappingStackISC.pop()
        mappingStackObj.pop()
        return 0 
    
    if (blockISC.flow != blockObj.flow or 
        (blockISC.nestingLevel - mergedLevelsISC) != blockObj.nestingLevel or
        blockISC.isReturning != blockObj.isReturning):
        print "\t\tFlow, or nesting level did not match or only one of them returns!"
        mappingStackISC.pop()
        mappingStackObj.pop()
        return -1
     
#     if (blockIndISC, blockIndObj) in mappingDict:
#         return mappingDict[(blockIndISC, blockIndObj)]
     
    mincost = -1
    listSuccISC = cfgISC.successorBlocks(blockIndISC)
    listSuccObj = cfgObj.successorBlocks(blockIndObj)
    listSuccWOBackEdgeISC = cfgISC.successorBlocksWOBackEdges(blockIndISC)
    listSuccWOBackEdgeObj = cfgObj.successorBlocksWOBackEdges(blockIndObj)

    if(len(listSuccWOBackEdgeISC) != len(listSuccWOBackEdgeObj)):
        if(blockObj.hasConditionalExec == 1 and 
           len(listSuccWOBackEdgeObj) == len(listSuccWOBackEdgeISC) - 1):
            print "\t\t Conditional Execution Found!"
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
                            print "\t\t case 1"
                            mappingStackISC.append(succ1BlockISC)
                            mappingStackObj.pop() # popping blockIndObj, because mapping it again
                            if mapping(cfgISC, succ2BlockISC, cfgObj, blockIndObj, mergedLevelsISC + 1) == 0:
                                cfgISC.listBlocks[blockIndISC].mapsTo.append(blockIndObj)
                                cfgISC.listBlocks[succ1BlockISC].mapsTo.append(blockIndObj)
                                cfgISC.listBlocks[succ2BlockISC].mapsTo.append(blockIndObj)
                                cfgObj.listBlocks[blockIndObj].mapsTo.append(succ2BlockISC)
                                mappingStackISC.pop()
                                mappingStackISC.pop()
                                return 0
                            else:
                                mappingStackISC.pop()
                                mappingStackObj.append(blockIndObj)
                                
                            
#                     if succSucc1BlockISC in (set(listSuccISC) - {succ1BlockISC}):
#                         # case 1
#                         print "\t\tcase 1"
#                         for succSuccSucc1BlockISC in cfgISC.successorBlocks(succSucc1BlockISC):
#                             if succSuccSucc1BlockISC in mappingStackISC:
#                                 continue
#                             for succBlockObj in listSuccObj:
#                                 if succBlockObj in mappingStackObj:
#                                     continue
#                                 mappingStackISC.append(succ1BlockISC)
#                                 mappingStackISC.append(succSucc1BlockISC)
#                                 if mapping(cfgISC, succSuccSucc1BlockISC, cfgObj, succBlockObj, mergedLevelsISC+1) == 0: 
#                                     cfgISC.listBlocks[blockIndISC].mapsTo.append(blockIndObj)
#                                     cfgISC.listBlocks[succ1BlockISC].mapsTo.append(blockIndObj)
#                                     cfgISC.listBlocks[succSucc1BlockISC].mapsTo.append(blockIndObj)
#                                     cfgObj.listBlocks[blockIndObj].mapsTo.append(succSucc1BlockISC)
#                                     mappingStackISC.pop()
#                                     mappingStackISC.pop()
#                                     mappingStackISC.pop()
#                                     mappingStackObj.pop()
#                                     return 0
#                                 else:
#                                     mappingStackISC.pop()
#                                     mappingStackISC.pop()
                                    
                    for succ2BlockISC in list(set(listSuccISC) - {succ1BlockISC}):
                        if succ2BlockISC in mappingStackISC:
                            continue
                        for succSucc2BlockISC in cfgISC.successorBlocks(succ2BlockISC):
                            if succSucc2BlockISC in mappingStackISC:
                                continue
                            if succSucc1BlockISC == succSucc2BlockISC:
                                # case 2
                                print "\t\t case 2"
                                mappingStackISC.append(succ1BlockISC)
                                mappingStackISC.append(succ2BlockISC)
                                mappingStackObj.pop() # popping blockIndObj, because mapping it again
                                if mapping(cfgISC, succSucc1BlockISC, cfgObj, blockIndObj, mergedLevelsISC+2) == 0:
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
                                    mappingStackISC.pop()
                                    mappingStackISC.pop()
                                    mappingStackObj.append(blockIndObj)
                                    
#                                 for succSuccSucc1BlockISC in cfgISC.successorBlocks(succSucc1BlockISC):
#                                     if succSuccSucc1BlockISC in mappingStackISC:
#                                         continue
#                                     for succBlockObj in listSuccObj:
#                                         if succBlockObj in mappingStackObj:
#                                             continue
#                                         mappingStackISC.append(succ1BlockISC)
#                                         mappingStackISC.append(succ2BlockISC)
#                                         mappingStackISC.append(succSucc1BlockISC)
#                                         if mapping(cfgISC, succSuccSucc1BlockISC, cfgObj, succBlockObj, mergedLevelsISC+2) == 0: 
#                                             cfgISC.listBlocks[blockIndISC].mapsTo.append(blockIndObj)
#                                             cfgISC.listBlocks[succ1BlockISC].mapsTo.append(blockIndObj)
#                                             cfgISC.listBlocks[succ2BlockISC].mapsTo.append(blockIndObj)
#                                             cfgISC.listBlocks[succSucc1BlockISC].mapsTo.append(blockIndObj)
#                                             cfgObj.listBlocks[blockIndObj].mapsTo.append(succSucc1BlockISC)
#                                             mappingStackISC.pop()
#                                             mappingStackISC.pop()
#                                             mappingStackISC.pop()
#                                             mappingStackISC.pop()
#                                             mappingStackObj.pop()
#                                             return 0
#                                         else:
#                                             mappingStackISC.pop()
#                                             mappingStackISC.pop()
#                                             mappingStackISC.pop()
        else:
            print "no. of successors not same, and difference more than one."
            print "ISC Block %d; Obj Block %d" % (blockIndISC, blockIndObj)
            exit(1)

    print "Successors of ISC:%d" % (blockIndISC),
    print cfgISC.successorBlocks(blockIndISC)                
    for succBlockISC in cfgISC.successorBlocks(blockIndISC):
        if succBlockISC in mappingStackISC:
            continue
        for succBlockObj in listSuccObj:
            if succBlockObj in mappingStackObj:
                continue
            print "recursing on mapping"
            if mapping(cfgISC, succBlockISC, cfgObj, succBlockObj, mergedLevelsISC) == 0:
                blockISC.mapsTo.append(blockIndObj)
                blockObj.mapsTo.append(blockIndISC)
            else:
                continue
    
    mappingStackISC.pop()
    mappingStackObj.pop()                                    
    print "Here"    
    return 0

def map_cfg(listISCFileNames, listObjdumpFileNames, listBinaryFileNames):
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

    print_debug_isc (listISCFunctions)
    print_debug_binary (listObjdumpFunctions, gdbMapping)

    mappingStackISC = []  
    mappingStackObj = []      
    for fnISC in listISCFunctions:
        cfgISC = fnISC.cfg
        fnObj = find(lambda fn: fn.functionName == fnISC.functionName, listObjdumpFunctions)
        cfgObj = fnObj.cfg
        
        print "Mapping Function %s" % (fnISC.functionName)
        if mapping(cfgISC, 0, cfgObj, 0, 0) == 0:
            print "Mapping Found!!!!"
        else:
            print "Fuck my life!!!"
            
    printDebugMapCFG(listISCFunctions, listObjdumpFunctions, gdbMapping)


if __name__ == "__main__":
#     listISCFileNames = []
#     listObjdumpFileNames = []
    logging.basicConfig(level=logging.WARNING)
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
    