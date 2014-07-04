#-----------------------------------------------------------------
# map_cfg.py: Map Control Flow Graphs from Binary and ISC
#-----------------------------------------------------------------

from optparse import OptionParser
from cfg_binary import parse_binary, print_debug_binary
from cfg_isc import parse_isc, print_debug_isc
import logging

from collections import deque

listISCFileNames = []
listObjdumpFileNames = []





def map_cfg(listISCFileNames, listObjdumpFileNames):
    listISCFunctions = []
    listFunctionNames = []
    listObjdumpFunctions = []
    
    # Parse the ISC files
    for ISCFileName in listISCFileNames:
        listISCFunctions = listISCFunctions + parse_isc(ISCFileName)
        for function in listISCFunctions:
            listFunctionNames.append(function.functionName)
    
    # Parse the objdump files
    for ObjdumpFileName in listObjdumpFileNames:
        listObjdumpFunctions = listObjdumpFunctions + parse_binary(ObjdumpFileName, 
                                                                   listFunctionNames)
        
    # Check that we found all functions in ISC in Objdump
    if len(listISCFunctions) != len(listObjdumpFunctions):
        raise ParseError("all functions in ISC file not found in Objdump file!")
    
    for function in listISCFunctions:
        logging.debug("Computing flow for function %s from file %s" % (function.functionName, function.fileName))
        function.cfg.computeFlow()
        
    for function in listObjdumpFunctions:
        logging.debug("Computing flow for function %s from file %s" % (function.functionName, function.fileName))
        function.cfg.computeFlow()

    print_debug_isc (listISCFunctions)
    print_debug_binary (listObjdumpFunctions)


if __name__ == "__main__":
#     listISCFileNames = []
#     listObjdumpFileNames = []
    logging.basicConfig(level=logging.DEBUG)
    optparser = OptionParser()
    optparser.add_option("-i", "--isc", action="append", dest="listISCFileNames",
                         type="string", help="ISC Filenamel. For multiple files, use -i <filename> multiple times.",
                         metavar="FILE")
    optparser.add_option("-o", "--objdump", action="append",
                         type="string", dest="listObjdumpFileNames", 
                         help="Objdump Filename. For multiple files, use -o <filename> multiple times.",
                         metavar="FILE")
    
    (options, args) = optparser.parse_args()
    
    if (len(args) > 0):
        print "Addtional arguments are being ignored"
    
    listISCFileNames =  options.listISCFileNames
    listObjdumpFileNames = options.listObjdumpFileNames
    
    map_cfg(listISCFileNames, listObjdumpFileNames)
    