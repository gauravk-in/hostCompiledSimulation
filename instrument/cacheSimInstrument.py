import re
import logging
from optparse import OptionParser
from subprocess import call
import linecache as lc

from instrument import *
from match_cfg import match_cfg


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


def mapRegToVar(dictGlobalVarAddInReg, fileNameObj, lsLineNum, regName):
    if regName in dictGlobalVarAddInReg:
        globalVar = dictGlobalVarAddInReg[regName]
        return globalVar
    else:
        READ_BACKWARDS_INST_THRESHOLD = 20
        lineNum = lsLineNum
        # Check if register can be mapped to a global variable by reading instructions above
        while lineNum > (lsLineNum - READ_BACKWARDS_INST_THRESHOLD):
            lineNum = lineNum - 1
            line = lc.getline(fileNameObj, lineNum)
            m = re_instructionLineObj.match(line)
            if m is not None:
                inst = m.group(3)
                instAdd = int(m.group(1), 16)
                m = re_instObj.match(inst)
                if m is not None:
                    targetReg = m.group(2)
                    operands = m.group(3)
                    if targetReg == regName:
                        # find all operands that are registers (\w{2})
                        listRegOperands = re.findall("\s*,\s*(\w{2})", operands)
                        for regOperand in listRegOperands:
                            if regOperand in dictGlobalVarAddInReg:
                                globalVar = dictGlobalVarAddInReg[regOperand]
                                return globalVar
                    else:
                        continue
                else:
                    break
            else:
                break

        logging.debug("\t %d: Could not map register \"%s\" to a global var." % 
                                  (lsLineNum, regName))
        
    # if here, the register could not be matched to a global var using above analysis
    return None

def instrument_cache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames):
    '''
    Algorithm
    To make our process simple, we are planning to use only Global Variables.
    We will modify the benchmark program, to make all local variables as global.
    This will only be possible, if the function is not recursive and won't have
    a huge impact on performance unless there are a number of functions that are
    called, and each have a large number of local variables.
    
    1. Extract info of Global Variables from GDB.
    2. Perform Matching of Control Flow Graphs.
    3. For each funcObj in list of Objdump functions,
        a. Find corresponding funcISC.
        b. For each line in funcObj,
            1. look for load and store instructions. Each load and store
               should be either,
                a. PC Relative Load/Store (Global Variable)
                b. Stack Pointer Relative Load/Store (Local Variable)
                PS. This is when we don't consider heap/dynamically allocated
                    memory.
            2. PC Relative Load/Store:
                a. Find the address of the address of global variable.
                b. Find name of the global variable being fetched from memory.
                c. In the mapping basic block in ISC, look for an instruction
                    where this global variable is being accessed. If found,
                    1. Look if this variable is an array and is being accessed
                        with an index.
                        a. TODO: Find a good way, to check if the current basic
                            block is part of a loop.
                        b. If yes, we need to find the index variable in the
                            source code.
                        c. Annotate the memory access at appropriate line in
                            the source code.
                    
    
    '''
    
    (listISCFunctions, listObjdumpFunctions) = match_cfg(listISCFileNames, 
                                                         listObjdumpFileNames, 
                                                         listBinaryFileNames)
    
    listGlobalVariables = getGlobalVariablesInfoFromGDB(listBinaryFileNames)    
    
    for funcObj in listObjdumpFunctions:
        
        dictGlobalVarAtPCRelativeAdd = {}
        dictGlobalVarAddInReg = {}
        
        fileNameObj = funcObj.fileName
        funcISC = find(lambda fn: fn.functionName == funcObj.functionName, listISCFunctions)
        fileNameISC = funcISC.fileName
        
        logging.debug("")
        logging.debug(" Function: %s" % funcObj.functionName)
        
        # Read addresses of all global variables attached at the end of the
        #     function, by reading backwards until return instruction is found
        
        logging.debug(" Table of Global Variable Addresses:")
        lineNumObj = funcObj.endLine
        while True:
            lineObj = lc.getline(fileNameObj, lineNumObj)
            m = re_instructionLineObj.match(lineObj)
            if m is not None:
                inst = m.group(3)
                m1 = re_returnInst.match(inst)
                if m1 is not None:
                    break
                else:
                    instAdd = int(m.group(1), 16)
                    globalVarAdd = int(m.group(2), 16)
                    globalVar = find(lambda var: var.address == globalVarAdd,
                                     listGlobalVariables)
                    if globalVar is not None:                
                        dictGlobalVarAtPCRelativeAdd[instAdd] = globalVar
                        logging.debug("\t \"%s\" at address %x." % (globalVar.name, globalVar.address))
                    else:
                        logging.error("\t Global Var with address %x not found." % globalVarAdd)
                    lineNumObj = lineNumObj - 1
            else:
                break
        
        logging.debug(" Load Store Instructions:")
        for lineNumObj in range(funcObj.startLine, funcObj.endLine+1):
            lineObj = lc.getline(fileNameObj, lineNumObj)
            m = re_instructionLineObj.match(lineObj)
            if m is not None:
                instAdd = int(m.group(1), 16)
                instObj = m.group(3)
                
                # Load PC Relative - Global Variables
                m = re_loadPCRelative.match(instObj)
                if m is not None:
                    globalVarAddInReg = m.group(1)
                    globalVarTabAddress = int(m.group(2), 16)
                    if globalVarTabAddress in dictGlobalVarAtPCRelativeAdd:                    
                        globalVar = dictGlobalVarAtPCRelativeAdd[globalVarTabAddress]
                    else:
                        logging.debug("\t %d: PC Relative Address was loaded, but corresponding global var was not found. Ignoring!")
                        continue
                    dictGlobalVarAddInReg[globalVarAddInReg] = globalVar
                    logging.debug("\t %d: %s = address of global var \"%s\"" % 
                                  (lineNumObj, globalVarAddInReg, globalVar.name))
                    continue
                
                m = re_loadStoreSPRelative.match(instObj)
                if m is not None:
                    lsOpcode = m.group(1)
                    lsReg = m.group(2)
                    if m.group(3) is None:
                        lsSPIndexVal = 0
                    else:
                        lsSPIndexVal = int(m.group(3))
                    logging.debug("\t %d: Local Variable was accessed at address sp+%d." %
                                  (lineNumObj, lsSPIndexVal))
                    continue
                
                # TODO: Look for SP relative address being loaded into a register
                #     It can be done by moving sp to a register, or by
                #     adding/subtracting from sp and storing to a register.
                #     Map the address to a local variable
                    
                m = re_loadStoreInst.match(instObj)
                if m is not None:
                    lsOpcode = m.group(1)
                    lsReg = m.group(2)
                    lsAddReg1 = m.group(3)
                    lsAddReg2 = m.group(4)
                    if lsAddReg2 == None:
                        # See if we know address of which global var is stored in lsAddReg1
                        # TODO: Look for above instructions to see where lsAddReg1 comes from.
                        globalVar = mapRegToVar(dictGlobalVarAddInReg, 
                                                fileNameObj, 
                                                lineNumObj, 
                                                lsAddReg1)
                        if globalVar is None:
                            logging.error("\t %s:%d: Could not match load/store instruction with variable"
                                          (fileNameObj, lineNumObj))
                            return -1
                        else:
                            baseAddReg = lsAddReg1
                        
                        # TODO: Verify the global variable being accessed by looking at source code
                        logging.debug("\t %d: %s = value of global var \"%s\" (pointed to by %s)" % 
                                      (lineNumObj, lsReg, globalVar.name, baseAddReg))
                    else:
                        globalVar = mapRegToVar(dictGlobalVarAddInReg, 
                                                fileNameObj, 
                                                lineNumObj, 
                                                lsAddReg1)
                        
                        if globalVar is not None:
                            baseAddReg = lsAddReg1
                            indexReg = lsAddReg2
                        else:
                            
                            globalVar = mapRegToVar(dictGlobalVarAddInReg, 
                                                    fileNameObj, 
                                                    lineNumObj, 
                                                    lsAddReg2)
                            if globalVar is not None:
                                baseAddReg = lsAddReg2
                                indexReg = lsAddReg1
                            else:
                                logging.error("\t %d: Could not match load/store instruction with variable" %
                                              (lineNumObj))
                                
                        if globalVar.length == 1:
                            logging.error("From objdump, it looks like an indexed access of array, but global variable is not an array (based on info from GDB)!")
                            quit
                            
                        # TODO: Look for Indexed array access in matching block in Source Code
                        logging.debug("\t %d: %s = value of element in global var %s (pointed to by %s, indexed by %s)." % 
                                          (lineNumObj, lsReg, globalVar.name, baseAddReg, indexReg))


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

#     getGlobalVariablesInfoFromGDB(listBinaryFileNames)
    
#     instrument_cache(listISCFileNames, listISCFunctions, 
#                      listObjdumpFileNames, listObjdumpFunctions,
#                      listBinaryFileNames)
#     
    instrument_cache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames)
