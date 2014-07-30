import re
import logging
from optparse import OptionParser
from subprocess import call

from instrument import *
from map_cfg import map_cfg


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item


def debugListGlobalVariables(listGlobalVariables):
    print ""
    for globVar in listGlobalVariables:
        print ("%s\t\t0x%x\t\t(type=%s; length=%d) - %s:%d" % 
               (globVar.name, globVar.address, globVar.type, globVar.length, 
                globVar.file, globVar.lineNum))
    print ""


def getGlobalVariablesInfoFromGDB(listBinaryFileNames):
    
    re_AllDefinedVariables = re.compile("All Defined Variables:")
    re_File = re.compile("File\s(.*):")
    re_Variable = re.compile("((?:[\w_]*\s)*)([\w_]*)(?:\[([0-9]*)\])*;")
    re_VarAdd = re.compile("Symbol \"([\w_]*)\" is static storage at address ([0-9a-fA-Fx]*).")
    
    listGlobalVariables = []
    
    for fileName in listBinaryFileNames:
        
        # Fetch Global Variable Names from this file
        gdbXFileName = fileName + ".globalVarNames.gdbx"
        gdbXFile = open(gdbXFileName, 'w')
        
        command = "info variables\n"
        gdbXFile.write(command)
        gdbXFile.write("quit\n")
        gdbXFile.close()
        
        gdbGlobalVarNamesOutputFileName = fileName + ".globalVarNames.gdbo"
        gdbGlobalVarNamesOutputFile = open(gdbGlobalVarNamesOutputFileName, 'w')
        call(args=["gdb", "--quiet", "--command="+gdbXFileName, fileName], 
             stdout=gdbGlobalVarNamesOutputFile)
        gdbGlobalVarNamesOutputFile.close()
        
        gdbGlobalVarNamesOutputFile = open(gdbGlobalVarNamesOutputFileName, 'r')
        currFileName = ""
        currListGlobalVariables = []
        for line in gdbGlobalVarNamesOutputFile:
            m = re_File.match(line)
            if m is not None:
                currFileName = m.group(1)
            
            m = re_Variable.match(line)
            if m is not None:
                dataType = m.group(1)
                varName = m.group(2)
                if m.group(3) is not None:
                    varLen = int(m.group(3))
                else:
                    varLen = 0
                
                currListGlobalVariables.append(GlobalVariable(name=varName,
                                                          type=dataType,
                                                          length=varLen,
                                                          file=currFileName))
        gdbGlobalVarNamesOutputFile.close()
        
        # Fetch addresses for Global Variables in this file
        gdbXGlobalVarAddFileName = fileName + ".globalVarAdd.gdbx"
        gdbXGlobalVarAddFile = open(gdbXGlobalVarAddFileName, 'w')
            
        for var in currListGlobalVariables:
            gdbXGlobalVarAddFile.write("info address %s\n" % (var.name))
        
        gdbXGlobalVarAddFile.write("quit\n")
        gdbXGlobalVarAddFile.close()
        
        gdbGlobalVarAddOutputFileName = fileName + ".globalVarAdd.gdbo"
        gdbGlobalVarAddOutputFile = open(gdbGlobalVarAddOutputFileName, 'w')
        call(args=["gdb", "--quiet", "--command="+gdbXGlobalVarAddFileName, fileName], 
             stdout=gdbGlobalVarAddOutputFile)
        gdbGlobalVarAddOutputFile.close()
        
        gdbGlobalVarAddOutputFile = open(gdbGlobalVarAddOutputFileName, 'r')
        for line in gdbGlobalVarAddOutputFile:
            m = re_VarAdd.match(line)
            if m is not None:
                var = find(lambda v: v.name == m.group(1), currListGlobalVariables)
                var.setAddress(int(m.group(2), 16))
        
        listGlobalVariables = listGlobalVariables + currListGlobalVariables
    
    debugListGlobalVariables(listGlobalVariables)
    return listGlobalVariables


re_loadPCRelative = re.compile("\s*ldr\s*[\w]\2,\s*\[pc,\s#[\d]*\]\s*;\s*[a-fA-F0-9]*\s*<\w*+0x[a-fA-F0-9]*>")


def instrument_cache(listISCFileNames, listISCFunctions, 
                     listObjdumpFileNames, listObjdumpFunctions,
                     listBinaryFileNames):
    '''
    Algorithm
    '''
    getGlobalVariablesInfoFromGDB(listBinaryFileNames)


if __name__ == "__main__":
#     listISCFileNames = []
#     listObjdumpFileNames = []
#     app = QtGui.QApplication(sys.argv)

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
        print "Additional arguments are being ignored"
    
    listISCFileNames =  options.listISCFileNames
    listObjdumpFileNames = options.listObjdumpFileNames
    listBinaryFileNames = options.listBinaryFileNames
    
#     (listISCFunctions, listObjdumpFunctions) = map_cfg(listISCFileNames, 
#                                                        listObjdumpFileNames, 
#                                                        listBinaryFileNames)

    getGlobalVariablesInfoFromGDB(listBinaryFileNames)
    
#     instrument_cache(listISCFileNames, listISCFunctions, 
#                      listObjdumpFileNames, listObjdumpFunctions,
#                      listBinaryFileNames)
#     