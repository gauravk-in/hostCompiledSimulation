import logging
from optparse import OptionParser
from subprocess import call
import linecache as lc

from load_store_info import *
from match_cfg import match_cfg
from gdb_info import *
from cGrammar import parse_statement

import re

re_term = re.compile("\w*")

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item


def instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames):
    
    (listISCFunctions, listObjdumpFunctions) = match_cfg(listISCFileNames, 
                                                         listObjdumpFileNames, 
                                                         listBinaryFileNames)
    
    listGlobalVariables = getGlobalVariablesInfoFromGDB(listBinaryFileNames)
    
    listLocalVariables = getLocalVariablesForAllFunc(listBinaryFileNames, listObjdumpFunctions)

    listLSInfo = identifyLoadStore(listISCFunctions,
                                   listObjdumpFunctions,
                                   listGlobalVariables,
                                   listLocalVariables)
    
    debugListLSInfo(listLSInfo)

    for funcISC in listISCFunctions:
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
#                     lineAnnotations = parse_statement(lineISC)
#                     if lineAnnotations == None:
#                         continue
#                     for annotation in lineAnnotations:
#                         for lsInfo in blockLSInfo:
#                             if lsInfo.var != None and annotation[0] == lsInfo.var.name:
#                                 print "Annotation :" + annotation[1]
                    listTerms = re_term.findall(lineISC)
                    for term in listTerms:
                        for lsInfo in blockLSInfo:
                            if lsInfo.var != None and lsInfo.var.name == term:
                                print "term %s found!" % term


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
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
        print "Additional arguments are being ignored"
    
    listISCFileNames =  options.listISCFileNames
    listObjdumpFileNames = options.listObjdumpFileNames
    listBinaryFileNames = options.listBinaryFileNames
    
    instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames)