import logging
from optparse import OptionParser
from subprocess import call
import linecache as lc
from collections import OrderedDict

from load_store_info import *
from match_cfg import match_cfg
from gdb_info import *
from cGrammar import parse_statement
from irc_regex import *
from pipeline_sim import *
from annotation import *

import re

re_term = re.compile("\w*")

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item
    return None
    
def getListLocalVarInFunc(listLocalVariables, functionName):
    listLocalVarInFunc = []
    for localVar in listLocalVariables:
        if localVar.scope == functionName:
            listLocalVarInFunc.append(localVar)
    return listLocalVarInFunc

# TODO : Make a new function to instrument the additional global vars needed! 
# def annotateGlobalVar(listISCFileNames):

def annotateVarFuncDecl(listISCFileNames, listISCFunctions, listGlobalVariables, listLocalVariables):
    dictAnnotVarFuncDecl = {}
    
    SPInitAddress = 0x1234
    
    mainFunc = find(lambda fn: fn.functionName == "main", listISCFunctions)
    mainFuncFile = mainFunc.fileName
    
    for ISCFileName in listISCFileNames:
        ISCFile = open(ISCFileName, "r")
        currFunctionName = ""
        lineNum = 0
        inMultiLineVarInit = 0
        inMultiLineFuctionSignature = 0
        inFunction = 0
        isGlobalSPVarDeclared = 0
        
        for line in ISCFile:
            lineNum = lineNum + 1
            
            if line.startswith('#include "ir2c.h"'):
                annot_str = '#include "cacheSim.h"'
                annot = Annotation(annot_str, ISCFileName, lineNum, False)
                addAnnotationToDict(dictAnnotVarFuncDecl,
                                    lineNum,
                                    annot)
                annot_str = '#include "branchPred.h"'
                annot = Annotation(annot_str, ISCFileName, lineNum, False)
                addAnnotationToDict(dictAnnotVarFuncDecl,
                                    lineNum,
                                    annot)
                annot_str = '#include "power_estimator.h"'
                annot = Annotation(annot_str, ISCFileName, lineNum, False)
                addAnnotationToDict(dictAnnotVarFuncDecl,
                                    lineNum,
                                    annot)
                if not isGlobalSPVarDeclared:
                    isGlobalSPVarDeclared = 1
                    if ISCFileName == mainFuncFile:
                        annot_str = "unsigned long SP = 0x%x;" % (SPInitAddress)
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl,
                                            lineNum,
                                            annot)
                        annot_str = "unsigned long long memAccessCycles = 0;"
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl,
                                            lineNum,
                                            annot)
                        annot_str = "unsigned long long pipelineCycles = 0;"
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl,
                                            lineNum,
                                            annot)
                        annot_str = "struct csim_result_t csim_result;"
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl,
                                            lineNum,
                                            annot)
                    else:
                        annot_str = "extern unsigned long SP;"
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl,
                                            lineNum,
                                            annot)
                        annot_str = "extern unsigned long long memAccessCycles;"
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl,
                                            lineNum,
                                            annot)
                        annot_str = "extern unsigned long long pipelineCycles;"
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl,
                                            lineNum,
                                            annot)
                        annot_str = "extern struct csim_result_t csim_result;"
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl,
                                            lineNum,
                                            annot)
            
            if inMultiLineVarInit == 1:
                m = re_VarDeclInitMultiLineEnd.match(line)
                if m is not None:
                    logging.debug("%d: VarDecl MultiLine End " % (lineNum))
                    inMultiLineVarInit = 0
                    if inFunction:
                        listCurrFuncLocalVar = getListLocalVarInFunc(listLocalVariables, 
                                                                     currFunctionName)
                        var = find(lambda var: var.name == varName, listCurrFuncLocalVar)
                        if var:
                            annot_str = "unsigned long %s_addr = 0x%x;" % (varName, var.address)
                            annot = Annotation(annot_str, ISCFileName, lineNum, False)
                            addAnnotationToDict(dictAnnotVarFuncDecl, 
                                                lineNum,
                                                annot)
                    else: # not inFunction
                        var = find(lambda var: var.name == varName, listGlobalVariables)
                        if var:
                            annot_str = "unsigned long %s_addr = 0x%x;" % (varName, var.address)
                            annot = Annotation(annot_str, ISCFileName, lineNum, False)
                            addAnnotationToDict(dictAnnotVarFuncDecl, 
                                                lineNum,
                                                annot)
                    continue
                else:
                    continue
                
            if inMultiLineFuctionSignature == 1:
                m = re_FuncDefArgLine.match(line)
                if m is not None:
                    if not m.group("openBrace").isspace():
                        inMultiLineFunctionSignature = 0
                    # replace the multi line signature with blank lines, 
                    # the annotation for function has already been added
                    annot_str = ""
                    annot = Annotation(annot_str, ISCFileName, lineNum, True)
                    addAnnotationToDict(dictAnnotVarFuncDecl,
                                        lineNum,
                                        annot)
                    continue
    
            m = re_VarDeclInitOneLine.match(line)
            if m is not None:
                varName = m.group("varName")
                if inFunction:
                    listCurrFuncLocalVar = getListLocalVarInFunc(listLocalVariables, 
                                                                 currFunctionName)
                    var = find(lambda var: var.name == varName, listCurrFuncLocalVar)
                    if var:
                        annot_str = "unsigned long %s_addr = 0x%x;" % (varName, var.address)
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl, 
                                            lineNum,
                                            annot)
                else: # not inFunction
                    var = find(lambda var: var.name == varName, listGlobalVariables)
                    if var:
                        annot_str = "unsigned long %s_addr = 0x%x;" % (varName, var.address)
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl, 
                                            lineNum,
                                            annot)
                continue
            
            m = re_VarDeclInitMultiLine.match(line)
            if m is not None:
                varName = m.group("varName")
                logging.debug("%d: VarDecl InitMultiLine: \"%s\"" % (lineNum, varName))
                inMultiLineVarInit = 1;
                continue
            
            m = re_VarDecl.match(line)
            if m is not None:
                varName = m.group("varName")
                if inFunction:
                    listCurrFuncLocalVar = getListLocalVarInFunc(listLocalVariables, 
                                                                 currFunctionName)
                    var = find(lambda var: var.name == varName, listCurrFuncLocalVar)
                    if var:
                        annot_str = "unsigned long %s_addr = 0x%x;" % (varName, var.address)
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl, 
                                            lineNum,
                                            annot)
                else: # not inFunction
                    var = find(lambda var: var.name == varName, listGlobalVariables)
                    if var:
                        annot_str = "unsigned long %s_addr = 0x%x;" % (varName, var.address)
                        annot = Annotation(annot_str, ISCFileName, lineNum, False)
                        addAnnotationToDict(dictAnnotVarFuncDecl, 
                                            lineNum,
                                            annot)
                continue
            
            m = re_FuncDefStart.match(line)
            if m is not None:
                inFunction = 1
                currFunctionName = m.group("name")
                currFuncRetType = m.group("retType")
                if m.group("endComma") is not None:
                    inMultiLineFuctionSignature = 1
                else:
                    assert(m.group("openBrace") is not None)
                logging.debug(" Function : " + currFunctionName)
                
                funcISC = find(lambda fn: fn.functionName == currFunctionName,
                               listISCFunctions)
                if funcISC.listParams:
                    # Create a list of new parameters for the annotated function signature
                    #     Add <name>_addr parameter for each param that is a pointer
                    newFuncParamsList = []
                    for param in funcISC.listParams:
                        newFuncParamsList.append(param.type + param.name + param.len)
                        if param.isPointer:
                            newFuncParamsList.append("unsigned long " + param.name + "_addr")
                    
                    # create the new annotation
                    annotatedFuncDecl = currFuncRetType + " " + currFunctionName + " ("
                    for param in newFuncParamsList[:-1]:
                        annotatedFuncDecl = annotatedFuncDecl + param + ", "
                    annotatedFuncDecl = annotatedFuncDecl + newFuncParamsList[-1] + ") {"
                    
                    annot = Annotation(annotatedFuncDecl,
                                       ISCFileName,
                                       lineNum,
                                       replace = True)
                    addAnnotationToDict(dictAnnotVarFuncDecl, 
                                        lineNum,
                                        annot)
                continue
            
            m = re_FuncDeclStart.match(line)
            if m is not None:
                currFunctionName = m.group("name")
                currFuncRetType = m.group("retType")
                assert(m.group("openBrace") is not None)
                logging.debug(" Function : " + currFunctionName)
                
                funcISC = find(lambda fn: fn.functionName == currFunctionName,
                               listISCFunctions)
                if funcISC.listParams:
                    # Create a list of new parameters for the annotated function signature
                    #     Add <name>_addr parameter for each param that is a pointer
                    newFuncParamsList = []
                    for param in funcISC.listParams:
                        newFuncParamsList.append(param.type + param.name + param.len)
                        if param.isPointer:
                            newFuncParamsList.append("unsigned long " + param.name + "_addr")
                    
                    # create the new annotation
                    annotatedFuncDecl = currFuncRetType + " " + currFunctionName + " ("
                    for param in newFuncParamsList[:-1]:
                        annotatedFuncDecl = annotatedFuncDecl + param + ", "
                    annotatedFuncDecl = annotatedFuncDecl + newFuncParamsList[-1] + ");"
                    
                    annot = Annotation(annotatedFuncDecl,
                                       ISCFileName,
                                       lineNum,
                                       replace = True)
                    addAnnotationToDict(dictAnnotVarFuncDecl, 
                                        lineNum,
                                        annot)
                continue
            
            m = re_functionCallStatement.match(line)
            if m is not None:
                funcName = m.group("name")
                funcParams = m.group("params")
                logging.debug("Found Function Call to %s, params (%s)\n" % (funcName, funcParams))
                funcISC = find(lambda fn: fn.functionName == funcName, listISCFunctions)
                if (funcISC is None):
                    logging.error(" ISC Function : %s not found in listISCFunctions!\n" % (funcName))
                    continue
                listParamsInCall = funcParams.split(",")
                listParamsInAnnotCall = []
                paramInd = -1
                
                skipLine = 0
                for param in funcISC.listParams:
                    paramInd = paramInd + 1
                    listParamsInAnnotCall.append(listParamsInCall[paramInd])
                    if param.isPointer:
                        m = re.match("\s*&?(?P<varName>\w*)", listParamsInCall[paramInd])
                        if m is None:
                            logging.error("%s:%d: Can't instrument, too complicated!" % (ISCFileName, lineNum))
                            skipLine = 1
                            break
                        paramVarName = m.group("varName")
                        listParamsInAnnotCall.append(paramVarName + "_addr")
                
                if skipLine:
                    continue
                
                annot_str = funcName + " ("
                for param in listParamsInAnnotCall[:-1]:
                    annot_str = annot_str + param + ", "
                annot_str = annot_str + listParamsInAnnotCall[-1] + ");"
                annot = Annotation(annot_str,
                                   ISCFileName,
                                   lineNum,
                                   True)
                addAnnotationToDict(dictAnnotVarFuncDecl, lineNum, annot)
                continue
            
            m = re_BlockEndRBrace.match(line)
            if m is not None and inFunction == 1:
                inFunction = 0
                currFunctionName = ""
                continue
        ISCFile.close()
        
    debugDictAnnot(dictAnnotVarFuncDecl)
    return dictAnnotVarFuncDecl
    
    # TODO : Annotate Push Pop Operations for DCache Access to Stack!
    
def annotateLoadStore(listISCFunctions, listObjdumpFunctions, listLSInfo, listGlobalVariables, listLocalVariables):
    dictAnnotLoadStore = {}
    
    for funcISC in listISCFunctions:
        lineNumISC = funcISC.startLine
        currFuncListParamsToAnnot = []
        for param in funcISC.listParams:
            if param.isPointer:
                currFuncListParamsToAnnot.append(param.name)
                
        if funcISC.functionName == "main":
            annot_str = "cacheSimInit(&csim_result);"
            annot = Annotation(annot_str, funcISC.fileName, funcISC.cfg.listBlocks[0].startLine-1, False)
            addAnnotationToDict(dictAnnotLoadStore, funcISC.cfg.listBlocks[0].startLine-1, annot)
            annot_str = "branchPred_init();"
            annot = Annotation(annot_str, funcISC.fileName, funcISC.cfg.listBlocks[0].startLine-1, False)
            addAnnotationToDict(dictAnnotLoadStore, funcISC.cfg.listBlocks[0].startLine-1, annot)
            annot_str = "power_estimator_init();"
            annot = Annotation(annot_str, funcISC.fileName, funcISC.cfg.listBlocks[0].startLine-1, False)
            addAnnotationToDict(dictAnnotLoadStore, funcISC.cfg.listBlocks[0].startLine-1, annot)
            
        funcObj = find(lambda fn: fn.functionName == funcISC.functionName, listObjdumpFunctions)
        annot_str = "SP = SP + 0x%x;" % (funcObj.stackSize)
        annot = Annotation(annot_str, funcISC.fileName, funcISC.cfg.listBlocks[0].startLine-1, False)
        addAnnotationToDict(dictAnnotLoadStore, funcISC.cfg.listBlocks[0].startLine-1, annot)
        
        for blockObj in funcObj.cfg.listBlocks:
            mappedBlocksISCInd = blockObj.mapsTo
            if len(mappedBlocksISCInd) == 0:
                logging.error("Func %s ObjBlock %s does not have a mapping!" %
                              (funcObj, blockObj.name))
                continue
            
            blockLSInfo = findLoadStoreBetweenLines(listLSInfo, blockObj.startLine, blockObj.endLine)
#             print blockLSInfo
            for blockISCInd in mappedBlocksISCInd:
                blockISC = funcISC.cfg.listBlocks[blockISCInd]
                
                for i in range(len(blockLSInfo)):
                    lsInfo = blockLSInfo.pop(0)
                    if lsInfo.isLoad and lsInfo.isPCRelLoad:
                        annot_str = "memAccessCycles += simDCache(0x%x, 1, &csim_result);  // PC Relative Load" % (lsInfo.PCRelAdd)
                        annot = Annotation(annot_str, funcISC.fileName, blockISC.startLine-1, False)
                        addAnnotationToDict(dictAnnotLoadStore, 
                                            blockISC.startLine-1,
                                            annot)
                        continue
                    elif lsInfo.isSpiltRegister:
                        if lsInfo.isLoad:
                            annot_str = "memAccessCycles += simDCache((SP + 0x%x), 1, &csim_result);  // Reading Spilt Register" % (lsInfo.spiltRegAdd)
                            annot = Annotation(annot_str, funcISC.fileName, blockISC.startLine-1, False)
                            addAnnotationToDict(dictAnnotLoadStore, 
                                                blockISC.startLine-1,
                                                annot)
                            continue
                        else:
                            annot_str = "memAccessCycles += simDCache((SP + 0x%x), 1, &csim_result);  // Spilling Register" % (lsInfo.spiltRegAdd)
                            annot = Annotation(annot_str, funcISC.fileName, blockISC.startLine-1, False)
                            addAnnotationToDict(dictAnnotLoadStore, 
                                                blockISC.startLine-1,
                                                annot)
                            continue
                    else:
                        blockLSInfo.append(lsInfo)
                
                for lineNumISC in range(blockISC.startLine, blockISC.endLine + 1):
                    lineISC = lc.getline(funcISC.fileName, lineNumISC)
                    logging.debug("%s:%d: %s" % (funcISC.fileName, lineNumISC, lineISC))
                    lineAccesses = parse_statement(lineISC)
                    if lineAccesses == None:
                        continue
                    while lineAccesses:
                        access = lineAccesses.pop()
                        if access.varName in currFuncListParamsToAnnot:
                            if access.isIndexed:
                                if access.ifIndexedIsArray:
                                    param = find(lambda p: p.name == access.varName, funcISC.listParams)
                                    annot_str = "memAccessCycles += simDCache(%s_addr + (sizeof(%s) * (%s)), %d, &csim_result);" % (access.varName, param.type, access.index, access.isRead)
                                else:
                                    param = find(lambda p: p.name == access.varName, funcISC.listParams)
                                    annot_str = "memAccessCycles += simDCache(%s_addr + (%s), %d, &csim_result);" % (access.varName, access.index, access.isRead)
                            else:
                                annot_str = "memAccessCycles += simDCache(%s_addr, %d, &csim_result);" % (access.varName, access.isRead)
                            annot = Annotation(annot_str, funcISC.fileName, lineNumISC, False)
                            annot.debug()
                            addAnnotationToDict(dictAnnotLoadStore, 
                                                lineNumISC,
                                                annot)

                        else:
                            lenBlockLSInfo = len(blockLSInfo)
                            for i in range(lenBlockLSInfo):
                                lsInfo = blockLSInfo.pop(0)
                                if lsInfo.var != None and access.varName == lsInfo.var.name and access.isRead == lsInfo.isLoad:
                                    var = find(lambda var: var.name == access.varName, listGlobalVariables + listLocalVariables)
                                    if access.isIndexed:
                                        if access.ifIndexedIsArray:
                                            if var.isLocal:
                                                annot_str = "memAccessCycles += simDCache((SP + %s_addr + (%d * (%s))), %d, &csim_result);" % (access.varName, var.size/var.length, access.index, access.isRead)
                                            else:
                                                annot_str = "memAccessCycles += simDCache(%s_addr + (%d * (%s)), %d, &csim_result);" % (access.varName, var.size/var.length, access.index, access.isRead)
                                        else:
                                            if var.isLocal:
                                                annot_str = "memAccessCycles += simDCache((SP + %s_addr + (%s)), %d, &csim_result);" % (access.varName, access.index, access.isRead)
                                            else:
                                                annot_str = "memAccessCycles += simDCache(%s_addr + (%s), %d, &csim_result);" % (access.varName, access.index, access.isRead)
                                    else:
                                        if var.isLocal:
                                            annot_str = "memAccessCycles += simDCache((SP + %s_addr), %d, &csim_result);" % (access.varName, access.isRead)
                                        else:
                                            annot_str = "memAccessCycles += simDCache(%s_addr, %d, &csim_result);" % (access.varName, access.isRead)
                                    annot = Annotation(annot_str, funcISC.fileName, lineNumISC-1, False)
                                    annot.debug()
                                    addAnnotationToDict(dictAnnotLoadStore, 
                                                        lineNumISC-1,
                                                        annot)
                                    break
                                else:
                                    blockLSInfo.append(lsInfo)
            
            # Annotate Instruction Cache Access
            re_instruction = re.compile('\s*(?P<address>[0-9a-f]*):\s*(?P<opcode>[0-9a-f]*)\s*(?P<instruction>.*)')
            objBlockStartLine = lc.getline(funcObj.fileName, blockObj.startLine)
            m = re_instruction.match(objBlockStartLine)
            assert(m is not None and m.group("address") is not None)
            blockStartAddress = int(m.group("address"), 16)
            objBlockEndLine = lc.getline(funcObj.fileName, blockObj.endLine)
            m = re_instruction.match(objBlockEndLine)
            assert(m is not None and m.group("address") is not None)
            blockEndAddress = int(m.group("address"), 16)
            blockSizeBytes = (blockEndAddress + 4 - blockStartAddress)
            blockSizeRounded = ((blockSizeBytes + 3) / 4) * 4
            annot_str = "// Simulating I Cache for obj block %s" % (blockObj.name)
            annot = Annotation(annot_str, funcISC.fileName, blockISC.startLine-1, False)
            addAnnotationToDict(dictAnnotLoadStore,
                                blockISC.startLine-1,
                                annot)
            annot_str = "memAccessCycles += simICache(0x%x, %d, &csim_result);" % (blockStartAddress, blockSizeRounded)
            annot = Annotation(annot_str, funcISC.fileName, blockISC.startLine-1, False)
            addAnnotationToDict(dictAnnotLoadStore,
                                blockISC.startLine-1,
                                annot)
            annot_str = "estimate_power(\"%s\", pipelineCycles, memAccessCycles, csim_result.L2Hits, (csim_result.prefetches + csim_result.L2Misses));" % (blockISC.name)
            annot = Annotation(annot_str, funcISC.fileName, blockISC.startLine-1, False)
            addAnnotationToDict(dictAnnotLoadStore,
                                blockISC.startLine-1,
                                annot)
            
            flag = 0
            for lsInfo in blockLSInfo:
                if flag == 0:
                    flag = 1
                    logging.error(" Unmapped LS from %s:%s :" % (funcObj.fileName, blockObj.name))
                logging.error(" \t%s" % lsInfo.debug_str())
                annot_str = "// TODO: UnmappedLS: %s" % (lsInfo.debug_str())
                annot = Annotation(annot_str, funcISC.fileName, blockISC.startLine - 1, False) 
                addAnnotationToDict(dictAnnotLoadStore, blockISC.startLine-1, annot)
            
        if funcISC.functionName == "main":
            returnLineNumber = funcISC.endLine + 1
            while True:
                returnLineNumber = returnLineNumber - 1
                line = lc.getline(funcISC.fileName, returnLineNumber)
                m = re_returnStatement.match(line)
                if m is not None:
                    annot_str = 'printf("memAccessCycles = \%llu\\n", memAccessCycles);'
                    annot = Annotation(annot_str, funcISC.fileName, returnLineNumber-1, False)
                    addAnnotationToDict(dictAnnotLoadStore, returnLineNumber-1, annot)
                    annot_str = 'printf("pipelineCycles = \%llu\\n", pipelineCycles);'
                    annot = Annotation(annot_str, funcISC.fileName, returnLineNumber-1, False)
                    addAnnotationToDict(dictAnnotLoadStore, returnLineNumber-1, annot)
                    annot_str = 'cacheSimFini(&csim_result);'
                    annot = Annotation(annot_str, funcISC.fileName, returnLineNumber-1, False)
                    addAnnotationToDict(dictAnnotLoadStore, returnLineNumber-1, annot)
                    annot_str = 'power_estimator_fini();'
                    annot = Annotation(annot_str, funcISC.fileName, returnLineNumber-1, False)
                    addAnnotationToDict(dictAnnotLoadStore, returnLineNumber-1, annot)
                    break
                else:
                    continue
                
    debugDictAnnot(dictAnnotLoadStore)
    return dictAnnotLoadStore

def generateOutputFileName(insOutputPath, inFileName):
    re_fileName = re.compile("(?P<path>/?(?:\w*/)*)(?P<fileName>\w*)\.(?P<fileExt>\w*)")
    m = re_fileName.match(inFileName)
    assert(m is not None)
    inFilePath = m.group("path")
    inFileNameWOExt = m.group("fileName")
    inFileExt = m.group("fileExt")
    if insOutputPath is None:
        insOutputPath = inFilePath
    return insOutputPath + inFileNameWOExt + "." + inFileExt



def unionDict(dict1, dict2):
    '''
    Both Dictionaries have lists as values!!!
    '''
    dict = {}
    for key in list(set(dict1.keys() + dict2.keys())):
        if key in dict1 and key in dict2:
            dict[key] = dict1[key] + dict2[key]
            continue
        
        if key in dict1 and key not in dict2:
            dict[key] = dict1[key]
            continue
        
        if key in dict2 and key not in dict1:
            dict[key] = dict2[key]
            continue
            
    return dict
            

def generateAnnotatedSourceFiles(dictAnnot, listISCFileNames, insOutputPath):
    for inFileName in listISCFileNames:
        outFileName = generateOutputFileName(insOutputPath, inFileName)
        inFile = open(inFileName, "r")
        outFile = open(outFileName, "w")
        lineNum = 0
        for line in inFile:
            lineNum = lineNum + 1
            
            if line.isspace():
                outFile.write("\n")
                continue
            
            re_indent = re.compile("(?P<indent>\s*)")
            m = re_indent.match(line)
            assert(m is not None)
            indent = m.group("indent")
            
            assert dictAnnot
            
            if lineNum not in dictAnnot:
                outFile.write(line)
                continue
            
            replaceLine = False
            
            if lineNum in dictAnnot:
                for annot in dictAnnot[lineNum]:
                    if annot.fileName == inFileName and annot.replace == True:
                        replaceLine = True
                        
            if replaceLine == False:
                outFile.write(line)
                
            for annot in dictAnnot[lineNum]:
                if annot.fileName == inFileName:
                    outFile.write(indent + annot.annotation + "\n")
                    
        inFile.close()
        outFile.close()
        print ("Output to file : %s" % outFileName)
            

def instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames, insOutputPath):
    
    (listISCFunctions, listObjdumpFunctions) = match_cfg(listISCFileNames, 
                                                         listObjdumpFileNames, 
                                                         listBinaryFileNames)
    
    listGlobalVariables = getGlobalVariablesInfoFromGDB(listBinaryFileNames)
    
    listLocalVariables = getLocalVariablesForAllFunc(listBinaryFileNames, listObjdumpFunctions)

    listLSInfo = identifyLoadStore(listISCFunctions,
                                   listObjdumpFunctions,
                                   listGlobalVariables,
                                   listLocalVariables)
    
#     debugListLSInfo(listLSInfo)

    dictAnnotVarFuncDecl = annotateVarFuncDecl(listISCFileNames, listISCFunctions, listGlobalVariables, listLocalVariables)
    
    dictAnnotLoadStore = annotateLoadStore(listISCFunctions, listObjdumpFunctions, listLSInfo, listGlobalVariables, listLocalVariables)

    dictAnnotPipeline = annot_pipeline_sim(listISCFunctions, listObjdumpFunctions)
    debugDictAnnot(dictAnnotPipeline)

    dictAnnot = unionDict(dictAnnotVarFuncDecl, dictAnnotLoadStore)
    dictAnnot = unionDict(dictAnnot, dictAnnotPipeline)

    generateAnnotatedSourceFiles(dictAnnot, listISCFileNames, insOutputPath)

if __name__ == "__main__":

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
    optparser.add_option("-p", "--outpath", action="store",
                         type="string", dest="insOutputPath", 
                         help="Output Path to store the annotated source files.",
                         metavar="PATH")
    
    (options, args) = optparser.parse_args()
    
    if (len(args) > 0):
        print "Additional arguments are being ignored"
    
    listISCFileNames =  options.listISCFileNames
    listObjdumpFileNames = options.listObjdumpFileNames
    listBinaryFileNames = options.listBinaryFileNames
    insOutputPath = options.insOutputPath
    
    instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames, insOutputPath)