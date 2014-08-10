import logging
from optparse import OptionParser
from subprocess import call
import linecache as lc

from instrument import *
from match_cfg import match_cfg
from armEmulate import *


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
                    varLen = 1
                
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

re_instructionLineObj = re.compile('\s*([0-9a-f]*):\s*([0-9a-f]*)\s*(.*)')
re_loadPCRelative = re.compile("\s*ldr\w*\s*([\w]{2}),\s*\[pc,\s#[\d]*\]\s*;\s*([a-fA-F0-9]*)\s*<\w*\+0x[a-fA-F0-9]*>")
re_loadStoreSPRelative = re.compile("\s*((?:str\w*)|(?:ldr\w*))\s*(\w{2}),\s*\[sp(?:,\s*#(\d*))?\]")
re_returnInst = re.compile('\s*(bx)\s*(lr)')
re_loadStoreInst = re.compile("\s*((?:ldr)|(?:str))\s*(\w{2}),\s*\[(\w{2})(?:,\s*(\w{2}))?(?:,\s*(.*))?\]")
re_addSubInst = re.compile("\s*((?:add)|(?:sub))(?:\w{2})?\s*(\w{2}),\s*(.*),\s*(.*)")
re_instObj = re.compile("\s*(\w*)\s*(\w*)((?:,\s*[\w\[\]\#]*)*)")


def getGlobalVariableAddressTableForFunc(funcObj):
    dictGlobVarAddAtTableAddress = {}
    lineNumObj = funcObj.endLine
    while True:
        lineObj = lc.getline(funcObj.fileName, lineNumObj)
        m = re_instructionLineObj.match(lineObj)
        if m is not None:
            inst = m.group(3)
            m1 = re_returnInst.match(inst)
            if m1 is not None:
                break
            else:
                instAdd = int(m.group(1), 16)
                globalVarAdd = int(m.group(2), 16)
                dictGlobVarAddAtTableAddress[instAdd] = globalVarAdd
                lineNumObj = lineNumObj - 1
        else:
            break
    
    return dictGlobVarAddAtTableAddress


def instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames):
    
    (listISCFunctions, listObjdumpFunctions) = match_cfg(listISCFileNames, 
                                                         listObjdumpFileNames, 
                                                         listBinaryFileNames)
    
    listGlobalVariables = getGlobalVariablesInfoFromGDB(listBinaryFileNames)
    
    for funcObj in listObjdumpFunctions:
        funcISC = find(lambda fn: fn.functionName == funcObj.functionName, listISCFunctions)
        assert(funcISC is not None)
        dictGlobVarAddAtTableAddress = getGlobalVariableAddressTableForFunc(funcObj)
        armEmu = ArmEmulator(dictGlobVarAddAtTableAddress)
        
        for lineNumObj in range(funcObj.startLine, funcObj.endLine + 1):
            lineObj = lc.getline(funcObj.fileName, lineNumObj)
            
            m = re_instructionLineObj.match(lineObj)
            if m is not None:
                instAdd = m.group(1)
                instObj = m.group(3)
                ret = armEmu.emulate(instObj)
                if ret == -1:
                    logging.debug("\t %d: Instruction could not be emulated!" % lineNumObj)
                    return -1
                
                m = re_loadInst.match(instObj)
                if m is not None:
                    for baseRegLabel in ["am2_1BaseReg", 
                                         "am2_2BaseReg", 
                                         "am2_3BaseReg", 
                                         "am2_4BaseReg", 
                                         "am2_5BaseReg", 
                                         "am2_6BaseReg", 
                                         "am2_7BaseReg"]:
                        if m.group(baseRegLabel) is not None:
                            break
                    baseReg = m.group(baseRegLabel)
                    if baseReg == "pc":
                        comment = m.group("comment")
                        m_comment = re.match("\s*([0-9a-f]*)\s*\<.*\>", comment)
                        assert(m_comment)
                        addInTable = int(m_comment.group(1), 16)
                        assert(addInTable in dictGlobVarAddAtTableAddress)
                        address = dictGlobVarAddAtTableAddress[addInTable]
                        globalVar = find(lambda var: var.address == address,
                                         listGlobalVariables)
                        if globalVar is None:
                            logging.debug(" PC Relative Load not for Global Var, probably for long value!")
                            continue
                        
                        logging.debug(" %d: Load Address of Global Var %s" % 
                                      (lineNumObj, globalVar.name))
                        continue
                    else:
                        baseRegVal = armEmu.reg[baseReg].value
                        globalVar = find(lambda var: var.address == baseRegVal,
                                         listGlobalVariables)
                        if globalVar is not None:
                            logging.debug(" %d: Loading content of Global Var %s" % 
                                          (lineNumObj, globalVar.name))
                            continue
                        elif baseRegVal > armEmu.reg["sp"]:
                            logging.debug(" %d: Accessing some local variable" %
                                          (lineNumObj))
                            # TODO: Which Local Variable?
                            continue
                        else:
                            logging.debug(" %d: %s" % (lineNumObj, instObj))
                            continue
                        
            else:
                logging.error(" %d: Instruction does not match!")
                return -1
            
        armEmu.printRegisters()


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
    
    instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames)