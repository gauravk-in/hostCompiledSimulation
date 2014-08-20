import logging
from optparse import OptionParser
from subprocess import call
import linecache as lc
from collections import deque

from match_cfg import match_cfg
from armEmulate import *
from gdb_info import *


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item
        

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

def findLocalVar(funcName, addRelSP, listLocalVariables):
    for var in listLocalVariables:
        if var.funcName == funcName:
            if var.address <= addRelSP and (var.address + var.size) > addRelSP :
                return var
    return None

def findGlobalVar(address, listGlobalVariables):
    for var in listGlobalVariables:
        if var.address <= address and (var.address + var.size) > address:
            return var
    return None

class FunctionInitState:
    def __init__(self, name, initRegState = None):
        self.name = name
        self.initRegState = initRegState

# TODO: Probably need to change the name of this function
def instrumentCache(listISCFileNames, listObjdumpFileNames, listBinaryFileNames):
    
    (listISCFunctions, listObjdumpFunctions) = match_cfg(listISCFileNames, 
                                                         listObjdumpFileNames, 
                                                         listBinaryFileNames)
    
    listGlobalVariables = getGlobalVariablesInfoFromGDB(listBinaryFileNames)
    
    listLocalVariables = getLocalVariablesForAllFunc(listBinaryFileNames, listObjdumpFunctions)
    
    listEmulatedFunctions = []
    queuePendingFunction = deque([FunctionInitState("main")])
    
    currFuncSpilledRegister = {}
    
    while queuePendingFunction:
        func = queuePendingFunction.popleft()
        logging.debug("")
        logging.debug("Starting Emulation of Func %s" % func.name)
        funcObj = find(lambda fn: fn.functionName == func.name, listObjdumpFunctions)
        assert(funcObj is not None)
        funcISC = find(lambda fn: fn.functionName == func.name, listISCFunctions)
        assert(funcISC is not None)
        listEmulatedFunctions.append(func.name)
        
        dictGlobVarAddAtTableAddress = getGlobalVariableAddressTableForFunc(funcObj)
        armEmu = ArmEmulator(dictGlobVarAddAtTableAddress, func.initRegState)
        
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
                
                '''
                Branch Instruction
                  - If branch is to another function, add the called function to
                    queue of pending functions.
                  - Ignore all other branch instructions.
                '''
                m = re_branchInst.match(instObj)
                if m is not None:
                    branchToFunction = m.group("labelFunction")
                    if branchToFunction is not None:
                        if branchToFunction == (funcObj.functionName or 
                                                branchToFunction in listEmulatedFunctions):
                            continue
                        else:
                            funcInQueue = find(lambda fn: fn.name == branchToFunction, queuePendingFunction)
                            if funcInQueue is not None:
                                continue
                            else:
                                initRegState = armEmu.reg
                                logging.debug("Adding func %s to queue!" % branchToFunction)
                                queuePendingFunction.append(FunctionInitState(branchToFunction,
                                                                              initRegState))
                                continue
                    else:
                        logging.error("labelFunction in branch instruction could not be matched!")
                        continue
                
                '''
                Store Instruction
                  - Calculate the address in the store instruction.
                  - If the address is in Stack, 
                      - Writing to a local variable. Look up the list of local
                        variables, and find which one.
                      - Spilling Registers. Keep a dictionary mapping address 
                        (relative to SP) and the content of the spilled register
                  - If address not in stack, it could be accessing Global
                    Variable. Look up table of Global Variables, and if no match
                    found, report error.
                '''
                m = re_storeInst.match(instObj)
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
                    baseRegVal = armEmu.reg[baseReg].value
                    destReg = m.group("destReg")
                    # Calculate store address based on addressing mode used.
                    if m.group("am2_2ImedOff") is not None:
                        strAdd = baseRegVal + int(m.group("am2_2ImedOff"))
                    elif m.group("am2_3OffsetReg") is not None:
                        strAdd = baseRegVal + armEmu.reg[m.group("am2_3OffsetReg")].value
                    else:
                        strAdd = baseRegVal
                    
                    if baseRegVal >= armEmu.reg["sp"].value:
                        localVar = findLocalVar(funcObj.functionName, 
                                                strAdd - armEmu.reg["sp"].value, 
                                                listLocalVariables)
                        if localVar is not None:
                            logging.debug(" %d: Writing local var %s" %
                                          (lineNumObj, localVar.name))
                        else:
                            destRegVal = armEmu.reg[destReg].value
                            currFuncSpilledRegister[strAdd - armEmu.reg["sp"].value] = destRegVal
                            logging.debug(" %d: Spilling Register %s to address %d ( = %d)" % 
                                          (lineNumObj, destReg, 
                                           (strAdd - armEmu.reg["sp"].value),
                                           destRegVal))
                        continue
                    else:
                        globalVar = findGlobalVar(strAdd,
                                              listGlobalVariables)
                        if globalVar is not None:
                            logging.debug(" %d: Writing Global Var %s" % 
                                          (lineNumObj, globalVar.name))
                            continue
                        else:
                            logging.error(" %d: %s" % (lineNumObj, instObj))
                            continue
                
                '''
                Load Instruction
                  - If the base address is PC,
                      - PC Relative Load instruction is used for Global Variables
                        or Values more than 32 bit long. Check if the value
                        loaded matches with address of a global variable.
                  - If base address is not PC, calculate the address to be
                    be loaded from. If the address is in stack, it may be
                      - trying to load a local variable. Match the address to 
                        a local variable. 
                      - reading from a spilled register. Fetch the value of 
                        the spilled register stored at the address.
                  - If the address is not in stack, it must be trying to load
                    content of a global variable. Match the address to a global
                    variable. If matching is not found, report error.
                '''
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
                    destReg = m.group("destReg")
                    # PC Relative Load Instruction
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
                        # Calculate load address based on addressing mode used.
                        if m.group("am2_2ImedOff") is not None:
                            ldrAdd = baseRegVal + int(m.group("am2_2ImedOff"))
                        elif m.group("am2_3OffsetReg") is not None:
                            ldrAdd = baseRegVal + armEmu.reg[m.group("am2_3OffsetReg")].value
                        else:
                            ldrAdd = baseRegVal
                        
                        if baseRegVal >= armEmu.reg["sp"].value:
                            localVar = findLocalVar(funcObj.functionName, 
                                                    ldrAdd - armEmu.reg["sp"].value, 
                                                    listLocalVariables)
                            if localVar is not None:
                                logging.debug(" %d: Reading local var %s" %
                                              (lineNumObj, localVar.name))
                            else:
                                armEmu.reg[destReg].setValue(currFuncSpilledRegister[ldrAdd - armEmu.reg["sp"].value])
                                logging.debug(" %d: Reading Spilled Register in %s from address %d ( = %d)" % 
                                              (lineNumObj, destReg, 
                                               (ldrAdd - armEmu.reg["sp"].value),
                                               armEmu.reg[destReg].value))
                            continue
                        else:
                            globalVar = findGlobalVar(ldrAdd,
                                                  listGlobalVariables)
                            if globalVar is not None:
                                logging.debug(" %d: Reading Global Var %s" % 
                                              (lineNumObj, globalVar.name))
                                continue
                            else:
                                logging.error(" %d: %s" % (lineNumObj, instObj))
                                continue
                        
            else:
                logging.error(" %d: Instruction does not match!")
                return -1



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