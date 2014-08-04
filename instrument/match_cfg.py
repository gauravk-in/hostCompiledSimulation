from optparse import OptionParser
from subprocess import call
import logging
import re
from collections import deque
import sys
from PyQt4 import QtGui, QtCore

from cfg_binary import parse_binary, print_debug_binary
from cfg_isc import parse_isc, print_debug_isc
# from display_cfg import display_cfgs
from draw_cfg import draw_cfg

######################################################
## Global Variables
######################################################

COND_EXEC_BLOCKLEN_THRESH = 6

app = None

# listISCFileNames = []
# listObjdumpFileNames = []
# listBinaryFileNames = []

class GDBMapTarget:
    def __init__(self, fileName, lineNum):
        self.fileName = fileName
        self.lineNum = lineNum

def printDebugMapCFG(listISCFunctions, listObjdumpFunctions, gdbMapping):
    for func in listObjdumpFunctions:
        print("\nFileName : %s" % (func.fileName))
        print("Function : %s" % (func.functionName))
        print "\t Stack Size = %d" % func.stackSize
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
    
    # gdbMappingDebug(gdbMapping)
    
    return gdbMapping


mappingStackISC = []  
mappingStackObj = []
gdbMapping = {}

def mapping(cfgISC, blockIndISC, cfgObj, blockIndObj, mergedLevelsISC):
#     raw_input("Press any key to continue ...")
    
    blockISC = cfgISC.listBlocks[blockIndISC]
    blockObj = cfgObj.listBlocks[blockIndObj]
    
    listSuccBlocksISC = cfgISC.successorBlocks(blockIndISC)
    listSuccBlocksObj = cfgObj.successorBlocks(blockIndObj)
    listSuccBlocksWOBackEdgeISC = cfgISC.successorBlocksWOBackEdges(blockIndISC)
    listSuccBlocksWOBackEdgeObj = cfgObj.successorBlocksWOBackEdges(blockIndObj)
    
    logging.debug("Matching ISC: %s and OBJ: %s" % (blockISC.name, blockObj.name))
    
    # If both blocks return, mapping found!
    if (blockISC.isReturning == 1 and blockObj.isReturning == 1):
        logging.debug("\t %s::%s Both blocks return! Matched!" % (blockISC.name, blockObj.name))
        # blockISC.mapsTo.append(blockIndObj)
        blockISC.mapISCTo(blockIndObj)        
        blockObj.mapsTo.append(blockIndISC)
        return 0
    
    # If one of the block returns, and other block has only one successor, which returns, mapping found!
    if (blockISC.isReturning != blockObj.isReturning):
        if (blockISC.isReturning == 1):
            if (len(listSuccBlocksObj) == 1):
                succBlockObj = cfgObj.listBlocks[listSuccBlocksObj[0]]
                if (succBlockObj.isReturning == 1):
                    logging.debug("/t ISC:%s returns, and is mapped to both OBJ:%s and OBJ:%s" 
                                  % (blockISC.name, blockObj.name, succBlockObj.name))
                    #blockISC.mapsTo.append(blockIndObj)
                    blockISC.mapISCTo(blockIndObj)
                    blockObj.mapsTo.append(blockIndISC)
                    succBlockObj.mapsTo.append(blockIndISC)
                    return 0
                else:
                    # Mapping not found!
                    return -1
            else:
                # Mapping not found!
                return -1
        elif (blockObj.isReturning == 1):
            if (len(listSuccBlocksISC) == 1):
                succBlockISC = cfgISC.listBlocks[listSuccBlocksISC[0]]
                if (succBlockISC.isReturning == 1):
                    logging.debug("/t OBJ:%s returns, and is mapped to ISC:%s" 
                                  % (blockObj.name, succBlockISC.name))
                    # blockISC.mapsTo.append(blockIndObj)
                    blockISC.mapISCTo(blockIndObj)
                    # succBlockISC.mapsTo.append(blockIndObj)
                    succBlockISC.mapISCTo(blockIndObj)
                    blockObj.mapsTo.append(listSuccBlocksISC[0])
                    return 0
                else:
                    # Mapping not found!
                    return -1
            else:
                # Mapping not found!
                return -1
            
    # Checking if current blockISC or blockObj is already in stack, ie. has already been seen, ie. this is a back edge
    stackEntryISC = find(lambda stackEntry: stackEntry[0] == blockIndISC, mappingStackISC[:-1])
    if stackEntryISC != None:
        # Back Edge Found!
        stackEntryObj = find(lambda stackEntry: stackEntry[0] == blockIndObj, mappingStackObj[:-1])
        if stackEntryObj != None:
            # Back edge found in Obj too. Do these match?
            if blockIndISC in stackEntryObj[1] and blockIndObj in stackEntryISC[1]:
                logging.debug("\t %s::%s Back Edge Found!" %
                              (blockISC.name, blockObj.name))
                # TODO: Is there something else to do here?
                return 0
            else:
                logging.debug("\t %s::%s Back Edge in ISC could not be matched with Back Edge in Obj!" %
                              (blockISC.name, blockObj.name))
                return -1
        else:
            # It may be that a block has been split in Obj
            if len(listSuccBlocksObj) == 1:
                succBlockIndObj = listSuccBlocksObj[0]
                stackEntryObj = find(lambda stackEntry: stackEntry[0] == succBlockIndObj, mappingStackObj[:-1])
                if stackEntryObj != None:
                    if blockIndISC in stackEntryObj[1] and succBlockIndObj in stackEntryISC[1]:
                        logging.debug("\t %s::%s Back Edge Found through split block in Obj!" %
                                      (blockISC.name, blockObj.name))
                        # TODO: Is there something else to do here?
                        return 0
                    else:
                        logging.debug("\t %s::%s Back Edge in ISC could not be matched with Back Edge in Obj!" %
                              (blockISC.name, blockObj.name))
                        return -1
                else:
                    logging.debug("\t %s::%s Back Edge in ISC but not in Obj!" %
                              (blockISC.name, blockObj.name))
                    return -1
            else:
                logging.debug("\t %s::%s Back Edge in ISC but not in Obj!" %
                          (blockISC.name, blockObj.name))
                return -1

    # Checking if current blockISC or blockObj is already in stack, ie. has already been seen, ie. this is a back edge
    stackEntryObj = find(lambda stackEntry: stackEntry[0] == blockIndObj, mappingStackObj[:-1])
    if stackEntryObj != None:
        # Back Edge Found!
        logging.debug("\t %s::%s Back Edge in Obj!" %
                      (blockISC.name, blockObj.name))
        stackEntryISC = find(lambda stackEntry: stackEntry[0] == blockIndISC, mappingStackISC[:-1])
        if stackEntryISC != None:
            # Back edge found in Obj too. Do these match?
            if blockIndISC in stackEntryObj[1] and blockIndObj in stackEntryISC[1]:
                logging.debug("\t %s::%s Back Edge Found!" %
                              (blockISC.name, blockObj.name))
                # TODO: Is there something else to do here?
                return 0
            else:
                logging.debug("\t %s::%s Back Edge in Obj could not be matched with Back Edge in ISC!" %
                              (blockISC.name, blockObj.name))
                return -1
        else:
            logging.debug("\t\t %s::%s No Back Edge in ISC, looking for split ISC block!" %
                          (blockISC.name, blockObj.name))
            # It may be that a block has been split in Obj
            for succBlockIndISC in  listSuccBlocksISC:
#                 succBlockIndISC = listSuccBlocksISC[0]
                stackEntryISC = find(lambda stackEntry: stackEntry[0] == succBlockIndISC, mappingStackISC[:-1])
                if stackEntryISC != None:
                    logging.debug("\t %s::%s Back Edge in Obj and split block back edge in ISC!" %
                              (blockISC.name, blockObj.name))
                    if succBlockIndISC in stackEntryObj[1] and blockIndObj in stackEntryISC[1]:
                        logging.debug("\t %s::%s Back Edge Found through split block in ISC!" %
                                      (blockISC.name, blockObj.name))
                        # Match current ISC block (split block) to predecessor of current Obj Block
                        # blockISC.mapsTo.append(mappingStackObj[-1][0])
                        blockISC.mapISCTo(mappingStackObj[-1][0])
                        # TODO: Is there something else to do here?
                        return 0
                    else:
                        logging.debug("\t %s::%s Back Edge in Obj could not be matched with Back Edge in ISC!" %
                              (blockISC.name, blockObj.name))
#                         return -1
                else:
                    logging.debug("\t %s::%s Back Edge in Obj but not in ISC!" %
                              (blockISC.name, blockObj.name))
#                     return -1
#             else:
            logging.debug("\t %s::%s Back Edge in Obj but not in ISC!" %
                      (blockISC.name, blockObj.name))
            return -1

    if (blockISC.flow != blockObj.flow):
        logging.debug("\t %s::%s Flow Values don't match!")
        return -1

    # If none of the blocks return, it means we have to continue the DFT
#     len(listSuccBlocksWOBackEdgeISC) != len(listSuccBlocksWOBackEdgeObj) and 
    if blockObj.hasConditionalExec == 1:
        
        # Check that length of each successor block is less than threshold for Conditional Execution
        lenLongestSuccBlock = 0
        for succBlockIndISC in listSuccBlocksWOBackEdgeISC:
            succBlockISC = cfgISC.listBlocks[succBlockIndISC]
            if lenLongestSuccBlock < succBlockISC.endLine - succBlockISC.startLine:
                lenLongestSuccBlock = succBlockISC.endLine - succBlockISC.startLine
        if lenLongestSuccBlock > COND_EXEC_BLOCKLEN_THRESH:
            logging.debug("\t %s::%s Length of successor blocks ISC greater than threshold to be considered as Conditional Execution" % 
                          (blockISC.name, blockObj.name))
        else:
            logging.debug("\t %s::%s Found Conditional Execution" % (blockISC.name, blockObj.name))
            # Case 1: 2 branches, one merges into other
            # Case 2: 2 branches with same successor
            # for each successor of blockISC
            case1Found = 0
            case2Found = 0
            for succ1BlockIndISC in listSuccBlocksWOBackEdgeISC:
                # list of successors of successor of blockISC
                listSuccSucc1BlocksISC = cfgISC.successorBlocks(succ1BlockIndISC)
                # for each successor of successor of blockISC
                for succSucc1BlockIndISC in listSuccSucc1BlocksISC:
                    # for each successor of blockISC other than succ1BlockIndISC
                    for succ2BlockIndISC in list(set(listSuccBlocksWOBackEdgeISC) - {succ1BlockIndISC}):
                        if succSucc1BlockIndISC == succ2BlockIndISC:
                            case1Found = 1
                            break
                        
                        # list of successors of other successor of blockIndISC
                        listSuccSucc2BlocksISC = cfgISC.successorBlocks(succ2BlockIndISC)
                        # for each successor of other successor of blockIndISC
                        for succSucc2BlockIndISC in listSuccSucc2BlocksISC:
                            # if successor of both successors of blockIndISC is same
                            if succSucc1BlockIndISC == succSucc2BlockIndISC:
                                case2Found = 1
                                break
                        
                        if case2Found == 1:
                            break
                    if case1Found == 1 or case2Found == 1:
                        break
                if case1Found == 1 or case2Found == 1:
                    break
            
            if case1Found == 1:
                logging.debug("\t\t %s::%s Conditional Execution Case 1" % (blockISC.name, blockObj.name))
                # call mapping on succ2BlockIndISC and blockObj
                mappingStackISC.append((succ1BlockIndISC, [blockIndObj]))
                mappingStackISC.append((succ2BlockIndISC, [blockIndObj]))
                mappingStackObj[-1][1].append(succ1BlockIndISC)
                mappingStackObj[-1][1].append(succ2BlockIndISC)
                if (mapping(cfgISC, succ2BlockIndISC, cfgObj, blockIndObj, mergedLevelsISC + 1) == 0):
                    logging.debug("\t\t\t %s::%s Mapping Found (CondExec: Case 1)!" % 
                                  (blockISC.name, blockObj.name))
                    # blockISC.mapsTo.append(blockIndObj)
                    blockISC.mapISCTo(blockIndObj)
                    # cfgISC.listBlocks[succ1BlockIndISC].mapsTo.append(blockIndObj)
                    cfgISC.listBlocks[succ1BlockIndISC].mapISCTo(blockIndObj)
                    # cfgISC.listBlocks[succ2BlockIndISC].mapsTo.append(blockIndObj)
                    cfgISC.listBlocks[succ2BlockIndISC].mapISCTo(blockIndObj)
                    blockObj.mapsTo.append(blockIndISC)
                    mappingStackISC.pop()
                    mappingStackISC.pop()
                    return 0
                else:
                    logging.warning("\t\t\t %s::%s Conditional Execution Case 1 was found, but could not be successfully mapped" % (blockISC.name, blockObj.name))
#                     return -1
            elif case2Found == 1:
                logging.debug("\t\t %s::%s Conditional Execution Case 2" % (blockISC.name, blockObj.name))
                # Call Mapping on succSucc1BlockIndISC and blockIndObj
                mappingStackISC.append((succ1BlockIndISC, [blockIndObj]))
                mappingStackISC.append((succ2BlockIndISC, [blockIndObj]))
                mappingStackISC.append((succSucc1BlockIndISC, [blockIndObj]))
                mappingStackObj[-1][1].append(succ1BlockIndISC)
                mappingStackObj[-1][1].append(succ2BlockIndISC)
                mappingStackObj[-1][1].append(succSucc1BlockIndISC)
                if (mapping(cfgISC, succSucc1BlockIndISC,
                            cfgObj, blockIndObj, mergedLevelsISC + 2) == 0):
                    logging.debug("\t\t\t %s::%s Mapping Found (CondExec: Case 2)!" % 
                                  (blockISC.name, blockObj.name))
                    # blockISC.mapsTo.append(blockIndObj)
                    # cfgISC.listBlocks[succ1BlockIndISC].mapsTo.append(blockIndObj)
                    # cfgISC.listBlocks[succ2BlockIndISC].mapsTo.append(blockIndObj)
                    # cfgISC.listBlocks[succSucc1BlockIndISC].mapsTo.append(blockIndObj)
                    blockISC.mapISCTo(blockIndObj)
                    cfgISC.listBlocks[succ1BlockIndISC].mapISCTo(blockIndObj)
                    cfgISC.listBlocks[succ2BlockIndISC].mapISCTo(blockIndObj)
                    cfgISC.listBlocks[succSucc1BlockIndISC].mapISCTo(blockIndObj)
                    blockObj.mapsTo.append(blockIndISC)
                    mappingStackISC.pop()
                    mappingStackISC.pop()
                    mappingStackISC.pop()
                    return 0
                else:
                    logging.warning("\t\t\t %s::%s Conditional Execution Case 2 was found, but could not be successfully mapped" % (blockISC.name, blockObj.name))
#                     return -1
            else:
                logging.warning("\t\t %s::%s Conditional Execution was found, but neither case matched!" % (blockISC.name, blockObj.name))
#                 return -1

    # Conditional Execution not found
    if len(listSuccBlocksISC) == len(listSuccBlocksObj):
        logging.debug("\t %s::%s length of successors is same, trying DFT" %
                      (blockISC.name, blockObj.name))
        allSuccBlocksISCMatchingFound = 1
        for succBlockIndISC in listSuccBlocksISC:
            succBlockISCMatchFoundUsingDFT = 0
            for succBlockIndObj in listSuccBlocksObj:
                if cfgObj.listBlocks[succBlockIndObj].mapsTo:
                    if succBlockIndISC in cfgObj.listBlocks[succBlockIndObj].mapsTo:
                        # Both have already been mapped.
                        logging.debug("\t\t %s::%s DFT: Successor blocks %s::%s have already been mapped to each other!" %
                                      (blockISC.name, blockObj.name,
                                       cfgISC.listBlocks[succBlockIndISC].name,
                                       cfgObj.listBlocks[succBlockIndObj].name))                        
                        succBlockISCMatchFoundUsingDFT = 1
                        break # to continue matching the next successor in ISC
                    else:
                        logging.debug("\t\t %s::%s DFT: Successor blocks Obj:%s have already been mapped to some other ISC block than current ISC:%s!" %
                                      (blockISC.name, blockObj.name,
                                       cfgObj.listBlocks[succBlockIndObj].name,
                                       cfgISC.listBlocks[succBlockIndISC].name))
                        continue
                else:
                    # Obj blocked hasn't yet been mapped. Try mapping
                    logging.debug("\t\t %s::%s Trying DFT on %s::%s" %
                          (blockISC.name, blockObj.name,
                           cfgISC.listBlocks[succBlockIndISC].name,
                           cfgObj.listBlocks[succBlockIndObj].name))
                    mappingStackISC.append((succBlockIndISC, [succBlockIndObj]))
                    mappingStackObj.append((succBlockIndObj, [succBlockIndISC]))
                    if (mapping(cfgISC, succBlockIndISC,
                                cfgObj, succBlockIndObj,
                                mergedLevelsISC) == 0):
                        # cfgISC.listBlocks[succBlockIndISC].mapsTo.append(succBlockIndObj)
                        cfgISC.listBlocks[succBlockIndISC].mapISCTo(succBlockIndObj)
                        cfgObj.listBlocks[succBlockIndObj].mapsTo.append(succBlockIndISC)
                        mappingStackISC.pop()
                        mappingStackObj.pop()
                        succBlockISCMatchFoundUsingDFT = 1
                        break
                    else:
                        succBlockISCMatchFoundUsingDFT = 0
                        mappingStackISC.pop()
                        mappingStackObj.pop()
                        continue # to try to match next successor of blockObj with current successor of blockISC
            
            if succBlockISCMatchFoundUsingDFT == 1:
                logging.debug("\t\t %s::%s DFT: Found matching for %s::%s" % 
                              (blockISC.name, blockObj.name,
                               cfgISC.listBlocks[succBlockIndISC].name,
                               cfgObj.listBlocks[succBlockIndObj].name))
                succBlockISCMatchFoundUsingDFT = 0
                continue # to match next blockISC
            else:
                logging.error("\t\t %s::%s DFT: Matching obj block for ISC block not found!" %
                              (blockISC.name, blockObj.name))
                allSuccBlocksISCMatchingFound = 0
                break
        
        if allSuccBlocksISCMatchingFound == 1:
            # Mapping was found for each successor block of blockISC
            # blockISC.mapsTo.append(blockIndObj)
            blockISC.mapISCTo(blockIndObj)
            blockObj.mapsTo.append(blockIndISC)
            return 0
        else:
            logging.debug("\t %s::%s Could not be matched using DFT" %
                          (blockISC.name, blockObj.name))
    
    return -1
#     # Trying to map using gdbMapping
#     deepestISCBlock = -1
#     deepestISCBlockNestingLevel = -1
#     logging.debug ("\t %s::%s Trying to match using gdb info" % (blockISC.name, blockObj.name))
#     blockObj.mapsTo = []
#     for lineNum in range(blockObj.startLine, blockObj.endLine):
#         if lineNum in gdbMapping:
#             ISCLineNum = gdbMapping[lineNum].lineNum
#             for i in range(len(cfgISC.listBlocks)):
#                 if (cfgISC.listBlocks[i].startLine <= ISCLineNum and
#                     cfgISC.listBlocks[i].endLine >= ISCLineNum):
#                     if i not in blockObj.mapsTo:
#                         blockObj.mapsTo.append(i)
#                     if blockIndObj not in cfgISC.listBlocks[i].mapsTo:
#                         cfgISC.listBlocks[i].mapsTo.append(blockIndObj)
#                     if deepestISCBlockNestingLevel < cfgISC.listBlocks[i].nestingLevel and i != blockIndISC:
#                         # The deepest ISC Block is not inserted in mappingStackISC
#                         #    because mapping will be called on this block, and
#                         #    it will be inserted by the next iteration of the
#                         #    mapping function. Insert the block in stack, which
#                         #    was previously thought of being deepest.
#                         if deepestISCBlock != -1:
#                             mappingStackISC.append(deepestISCBlock)
#                         deepestISCBlock = i
#                         deepestISCBlockNestingLevel < cfgISC.listBlocks[i].nestingLevel
#                         break
#                     else:
#                         mappingStackISC.append(i)
#                         continue
#     
#     if deepestISCBlock != -1:
#         mappingStackObj.pop() # popping blockIndObj from stack, as mapping is called on it again.
#         mergedLevelsISC = mergedLevelsISC + cfgISC.listBlocks[deepestISCBlock].nestingLevel - blockISC.nestingLevel
#         if mapping(cfgISC, deepestISCBlock, cfgObj, blockIndObj, mergedLevelsISC) == 0:
#             for i in range(len(blockObj.mapsTo)-1):
#                 # pop each entry from ISC to which the blockIndObj maps to
#                 mappingStackISC.pop()
#             return 0 # successful mapping

    
def map_cfg(listISCFileNames, listObjdumpFileNames, listBinaryFileNames):
    global mappingStackISC
    global mappingStackObj
    listISCFunctions = []
    listFunctionNames = []
    listObjdumpFunctions = []
    
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
        
#     for funcISC in listISCFunctions:
#         funcObj = find(lambda fn: fn.functionName == funcISC.functionName, listObjdumpFunctions)
#         display_cfgs(app, funcISC.cfg, funcObj.cfg, "%s" % funcISC.functionName)

    for binaryFileName in listBinaryFileNames:
        gdbMapping = getGDBMapping(binaryFileName, objdumpLineNumForAddress)

    for fnISC in listISCFunctions:
          
        cfgISC = fnISC.cfg
        fnObj = find(lambda fn: fn.functionName == fnISC.functionName, listObjdumpFunctions)
        cfgObj = fnObj.cfg
        
        mappingStackISC = [(0, [0])]  
        mappingStackObj = [(0, [0])]
        if mapping(cfgISC=cfgISC, blockIndISC=0, cfgObj=cfgObj, blockIndObj=0, mergedLevelsISC=0) == 0:
            logging.debug("Mapping Found!!!!")
            print mappingStackISC
            print mappingStackObj
        else:
            logging.debug("Fuck my life!!!")
        mappingStackISC.pop()
        mappingStackObj.pop()
        
        if mappingStackISC or mappingStackObj:
            logging.error("*** Stack is not empty after mapping function returns ***")
            
    printDebugMapCFG(listISCFunctions, listObjdumpFunctions, gdbMapping)

    return listISCFunctions, listObjdumpFunctions


if __name__ == "__main__":
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
    optparser.add_option("-p", "--output_path", action="store",
                         type="string", dest="outputPath", 
                         help="Output path to store graphs generated.",
                         metavar="PATH")
    
    (options, args) = optparser.parse_args()
    
    if (len(args) > 0):
        print "Addtional arguments are being ignored"
    
    listISCFileNames =  options.listISCFileNames
    listObjdumpFileNames = options.listObjdumpFileNames
    listBinaryFileNames = options.listBinaryFileNames
    outputPath = options.outputPath
    
    (listISCFunctions, listObjdumpFunctions) = map_cfg(listISCFileNames, listObjdumpFileNames, listBinaryFileNames)
    
    for funcISC in listISCFunctions:
        funcObj = find(lambda fn: fn.functionName == funcISC.functionName, listObjdumpFunctions)
#         display_cfgs(app, funcISC.cfg, funcObj.cfg, "%s" % funcISC.functionName)
        psISCFileName = draw_cfg(funcISC, outputPath)
        psObjFileName = draw_cfg(funcObj, outputPath)
        call(args = ["evince", psISCFileName, psObjFileName])
        
         
    