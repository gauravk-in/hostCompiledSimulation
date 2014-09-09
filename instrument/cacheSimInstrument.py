import logging
from optparse import OptionParser
from subprocess import call
import linecache as lc

from load_store_info import *
from match_cfg import match_cfg
from gdb_info import *
from cGrammar import parse_statement
from irc_regex import *
from collections import OrderedDict

import re

re_term = re.compile("\w*")

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item
    return None
    
class Annotation:
    def __init__(self, annotation, fileName, lineNum, replace = False):
        self.fileName = fileName
        self.lineNum = lineNum
        self.annotation = annotation
        self.replace = replace
        
    def debug(self):
        logging.debug("%s:%d: %s" % (self.fileName, self.lineNum, self.annotation))
    
def getListLocalVarInFunc(listLocalVariables, functionName):
    listLocalVarInFunc = []
    for localVar in listLocalVariables:
        if localVar.scope == functionName:
            listLocalVarInFunc.append(localVar)
    return listLocalVarInFunc

def debugDictAnnot(dictAnnot):
    for lineNum in dictAnnot.iterkeys():
        for annot in dictAnnot[lineNum]:
            annot.debug()

def addAnnotationToDict(dict, lineNum, annot):
    if lineNum not in dict:
        dict[lineNum] = [annot]
    else:
        for a in dict[lineNum]:
            if a.annotation == annot.annotation and a.fileName == annot.fileName:
                return
        dict[lineNum].append(annot)

def annotateVarFuncDecl(listISCFileNames, listISCFunctions, listGlobalVariables, listLocalVariables):
    dictAnnotVarFuncDecl = OrderedDict({})
    
    for ISCFileName in listISCFileNames:
        ISCFile = open(ISCFileName, "r")
        currFunctionName = ""
        lineNum = 0
        inMultiLineVarInit = 0
        inMultiLineFuctionSignature = 0
        inFunction = 0
        for line in ISCFile:
            lineNum = lineNum + 1
            
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
                    annotatedFuncDecl = annotatedFuncDecl + newFuncParamsList[-1] + ")"
                    
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
                    annotatedFuncDecl = annotatedFuncDecl + newFuncParamsList[-1] + ")"
                    
                    annot = Annotation(annotatedFuncDecl,
                                       ISCFileName,
                                       lineNum,
                                       replace = True)
                    addAnnotationToDict(dictAnnotVarFuncDecl, 
                                        lineNum,
                                        annot)
                continue
            
            m = re_BlockEndRBrace.match(line)
            if m is not None and inFunction == 1:
                inFunction = 0
                currFunctionName = ""
                continue
        ISCFile.close()
        
    debugDictAnnot(dictAnnotVarFuncDecl)
    return dictAnnotVarFuncDecl
    
def annotateLoadStore(listISCFunctions, listObjdumpFunctions, listLSInfo, listGlobalVariables, listLocalVariables):
    dictAnnotLoadStore = OrderedDict({})
    
    for funcISC in listISCFunctions:
        lineNumISC = funcISC.startLine
        currFuncListParamsToAnnot = []
        for param in funcISC.listParams:
            if param.isPointer:
                currFuncListParamsToAnnot.append(param.name)
        
        funcObj = find(lambda fn: fn.functionName == funcISC.functionName, listObjdumpFunctions)
        for blockObj in funcObj.cfg.listBlocks:
            mappedBlocksISCInd = blockObj.mapsTo
            blockLSInfo = findLoadStoreBetweenLines(listLSInfo, blockObj.startLine, blockObj.endLine)
#             print blockLSInfo
            for blockISCInd in mappedBlocksISCInd:
                blockISC = funcISC.cfg.listBlocks[blockISCInd]
                for lineNumISC in range(blockISC.startLine, blockISC.endLine + 1):
                    lineISC = lc.getline(funcISC.fileName, lineNumISC)
                    print "%s:%d: %s" % (funcISC.fileName, lineNumISC, lineISC),
                    lineAccesses = parse_statement(lineISC)
                    if lineAccesses == None:
                        continue
                    while lineAccesses:
                        access = lineAccesses.pop()
                        if access.varName in currFuncListParamsToAnnot:
                            if access.isIndexed:
                                param = find(lambda p: p.name == access.varName, funcISC.listParams)
                                annot_str = "simDCache(%s_addr + (sizeof(%s) * (%s)), %d);" % (access.varName, param.type, access.index, access.isRead)
                            else:
                                annot_str = "simDCache(%s_addr, %d);" % (access.varName, access.isRead)
                            annot = Annotation(annot_str, funcISC.fileName, lineNumISC, False)
                            annot.debug()
                            addAnnotationToDict(dictAnnotLoadStore, 
                                                lineNumISC,
                                                annot)

                        else:
                            lenBlockLSInfo = len(blockLSInfo)
                            for i in range(lenBlockLSInfo):
                                lsInfo = blockLSInfo.pop(0)
                                if lsInfo.var != None and access.varName == lsInfo.var.name:
                                    if access.isIndexed:
                                        var = find(lambda var: var.name == access.varName, listGlobalVariables + listLocalVariables)
                                        annot_str = "simDCache(%s_addr + (%d * (%s)), %d);" % (access.varName, var.size/var.length, access.index, access.isRead)
                                    else:
                                        annot_str = "simDCache(%s_addr, %d);" % (access.varName, access.isRead)
                                    annot = Annotation(annot_str, funcISC.fileName, lineNumISC, False)
                                    annot.debug()
                                    addAnnotationToDict(dictAnnotLoadStore, 
                                                        lineNumISC,
                                                        annot)
                                    break
                                else:
                                    blockLSInfo.append(lsInfo)
            
            print "******* LS Info could not be mapped in block %s" % blockObj.name
            for lsInfo in blockLSInfo:
                lsInfo.debug()
            print "*******"
                                
    debugDictAnnot(dictAnnotLoadStore)
    return dictAnnotLoadStore

def generateOutputFileName(outputPath, inFileName):
    re_fileName = re.compile("(?P<path>/?(?:\w*/)*)(?P<fileName>\w*)\.(?P<fileExt>\w*)")
    m = re_fileName.match(inFileName)
    assert(m is not None)
    inFilePath = m.group("path")
    inFileNameWOExt = m.group("fileName")
    inFileExt = m.group("fileExt")
    if outputPath is None:
        outputPath = inFilePath
    return outputPath + inFileNameWOExt + "_ins." + inFileExt

def generateAnnotatedSourceFiles(dictAnnotVarFuncDecl, dictAnnotLoadStore, listISCFileNames, outputPath):
    for inFileName in listISCFileNames:
        outFileName = generateOutputFileName(outputPath, inFileName)
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
            
            assert dictAnnotLoadStore
            assert dictAnnotVarFuncDecl
            
            if lineNum not in dictAnnotVarFuncDecl and lineNum not in dictAnnotLoadStore:
                outFile.write(line)
                continue
            
            replaceLine = False
            
            if lineNum in dictAnnotVarFuncDecl:
                for annot in dictAnnotVarFuncDecl[lineNum]:
                    if annot.fileName == inFileName and annot.replace == True:
                        replaceLine = True
                        
            if lineNum in dictAnnotLoadStore:
                for annot in dictAnnotLoadStore[lineNum]:
                    if annot.fileName == inFileName and annot.replace == True:
                        replaceLine = True
            
            if replaceLine == False:
                outFile.write(line)
                
            if lineNum in dictAnnotVarFuncDecl:
                for annot in dictAnnotVarFuncDecl[lineNum]:
                    if annot.fileName == inFileName:
                        outFile.write(indent + annot.annotation + "\n")
                        
            if lineNum in dictAnnotLoadStore:
                for annot in dictAnnotLoadStore[lineNum]:
                    if annot.fileName == inFileName:
                        outFile.write(indent + annot.annotation + "\n")
                    
        inFile.close()
        outFile.close()
        print ("Output to file : %s" % outFileName)
            

def instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames, outputPath):
    
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

    generateAnnotatedSourceFiles(dictAnnotVarFuncDecl, dictAnnotLoadStore, listISCFileNames, outputPath)

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
                         type="string", dest="outputPath", 
                         help="Output Path to store the annotated source files.",
                         metavar="PATH")
    
    (options, args) = optparser.parse_args()
    
    if (len(args) > 0):
        print "Additional arguments are being ignored"
    
    listISCFileNames =  options.listISCFileNames
    listObjdumpFileNames = options.listObjdumpFileNames
    listBinaryFileNames = options.listBinaryFileNames
    outputPath = options.outputPath
    
    instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames, outputPath)