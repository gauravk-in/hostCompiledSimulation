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


def gdbMappingDebug(gdbMapping):
    for lineNum in gdbMapping:
        print ("line %d maps to %s:%d" % (lineNum, gdbMapping[lineNum].fileName, gdbMapping[lineNum].lineNum))

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
    
    gdbMappingDebug(gdbMapping)
    
    return gdbMapping

def map_cfg(listISCFileNames, listObjdumpFileNames, listBinaryFileNames):
    listISCFunctions = []
    listFunctionNames = []
    listObjdumpFunctions = []
    
    # Parse the ISC files
    for ISCFileName in listISCFileNames:
        listISCFunctions = listISCFunctions + parse_isc(ISCFileName)
        for function in listISCFunctions:
            listFunctionNames.append(function.functionName)
            print "parsed "+ISCFileName
    
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
        getGDBMapping(binaryFileName, objdumpLineNumForAddress)

    print_debug_isc (listISCFunctions)
    print_debug_binary (listObjdumpFunctions)


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
    