import linecache as lc
from collections import deque
import copy

from arm_isa_regex import *
from armEmulate import *

re_instructionLineObj = re.compile('\s*([0-9a-f]*):\s*([0-9a-f]*)\s*(.*)')

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item
        
def findLocalVar(funcName, addRelSP, listLocalVariables):
    for var in listLocalVariables:
        assert (var.isLocal == True)
        if var.scope == funcName:
            if var.address <= addRelSP and (var.address + var.size) > addRelSP :
                return var
    return None


def findGlobalVar(address, listGlobalVariables):
    for var in listGlobalVariables:
        assert (var.isLocal == False)
        if var.address <= address and (var.address + var.size) > address:
            return var
    return None
        
def getGlobalVariableAddressTableForFunc(funcObj):
    re_instructionLineObj = re.compile('\s*([0-9a-f]*):\s*([0-9a-f]*)\s*(.*)')
    re_returnInst = re.compile('\s*(bx)\s*(lr)')
    
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

class FunctionInitState:
    def __init__(self, name, initRegState = None):
        self.name = name
        self.initRegState = initRegState

class LoadStoreInfo:
    def __init__(self):
        self.isLoad = False
        self.var = None
        self.isPCRelLoad = False
        self.PCRelAdd = -1
        self.isSpiltRegister = False
        self.spiltRegAdd = -1
        self.isAccuratelyMatched = False
        self.lineNumObj = -1
        
    def loadVar(self, var, lineNum):
        self.isLoad = True
        self.var = var
        self.isAccuratelyMatched = True
        self.lineNumObj = lineNum
        
    def storeVar(self, var, lineNum):
        self.isLoad = False
        self.var = var
        self.isAccuratelyMatched = True
        self.lineNumObj = lineNum
        
    def loadInaccurate(self, lineNum):
        self.isLoad = True
        self.var = None
        self.lineNumObj = lineNum
        self.isAccuratelyMatched = False
        
    def storeInaccurate(self, lineNum):
        self.isLoad = False
        self.var = None
        self.lineNumObj = lineNum
        self.isAccuratelyMatched = False
        
    def loadPCRel(self, PCRelAdd, lineNum):
        self.isLoad = True
        self.isPCRelLoad = True
        self.PCRelAdd = PCRelAdd
        self.lineNumObj = lineNum
        self.isAccuratelyMatched = True
        
    def spillReg(self, spiltRegAdd, lineNum):
        self.isLoad = False
        self.isSpiltRegister = True
        self.spiltRegAdd = spiltRegAdd
        self.lineNumObj = lineNum
        self.isAccuratelyMatched = True
        
    def readSpiltReg(self, spiltRegAdd, lineNum):
        self.isLoad = True
        self.isSpiltRegister = True
        self.spiltRegAdd = spiltRegAdd
        self.lineNumObj = lineNum
        self.isAccuratelyMatched = True
        
    def debug(self):
        if self.isAccuratelyMatched == True:
            if self.isLoad == True:
                if self.isPCRelLoad == False:
                    if self.isSpiltRegister == False:
                        print("Load "),
                        if self.var.isLocal == True:
                            print("LocalVar "),
                        else:
                            print("GlobalVar "),
                        print("%s at line %d" % (self.var.name, self.lineNumObj))
                    else: # isSpiltRegister == True
                        print("Reading Spilt Register from add %d in stack on line %d" %
                              (self.spiltRegAdd, self.lineNumObj))
                else: # isPCRelLoad == True
                    print("PC Relative Load from add %d on line %d" % 
                          (self.PCRelAdd, self.lineNumObj))
            else: # isLoad == False
                if self.isSpiltRegister == False:
                    print("Store "),
                    if self.var.isLocal == True:
                        print("LocalVar "),
                    else:
                        print("GlobalVar "),
                    print("%s at line %d" % (self.var.name, self.lineNumObj))
                else: # isSpiltRegister == True
                    print ("Spilling Register to add %d in stack on line %d" % 
                           (self.spiltRegAdd, self.lineNumObj))
        else:
            if self.isLoad == True:
                print("Inaccurately Matched Load at line %d" % self.lineNumObj)
            else:
                print("Inaccurately Matched Store at line %d" % self.lineNumObj)
                

def debugListLSInfo(listLSInfo):
    print ""
    for lsInfo in listLSInfo:
        lsInfo.debug()
    print ""

# TODO: Probably need to change the name of this function
def identifyLoadStore(listISCFunctions,
                        listObjdumpFunctions,
                        listGlobalVariables,
                        listLocalVariables):

    listEmulatedFunctions = []
    queuePendingFunction = deque([FunctionInitState("main")])
    
    currFuncSpilledRegister = {}
    
    listLSInfo = []
    
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
        currFuncListLSInfo = []
        
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
                                initRegState = copy.deepcopy(armEmu.reg)
                                logging.debug("Adding func %s to queue!" % branchToFunction)
                                queuePendingFunction.append(FunctionInitState(branchToFunction,
                                                                              initRegState))
                                continue
                    else:
                        logging.debug("Branch function does not have a label! (branch to same function)")
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
                            lsInfo = LoadStoreInfo()
                            lsInfo.storeVar(localVar, lineNumObj)
                            currFuncListLSInfo.append(lsInfo)
                            del lsInfo
                            logging.debug(" %d: Writing local var %s" %
                                          (lineNumObj, localVar.name))
                        else:
                            destRegVal = armEmu.reg[destReg].value
                            lsInfo = LoadStoreInfo()
                            lsInfo.spillReg((strAdd - armEmu.reg["sp"].value), lineNumObj)
                            currFuncListLSInfo.append(lsInfo)
                            del lsInfo
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
                            lsInfo = LoadStoreInfo()
                            lsInfo.storeVar(globalVar, lineNumObj)
                            currFuncListLSInfo.append(lsInfo)
                            del lsInfo
                            logging.debug(" %d: Writing Global Var %s" % 
                                          (lineNumObj, globalVar.name))
                            continue
                        else:
                            lsInfo = LoadStoreInfo()
                            lsInfo.storeInaccurate(lineNumObj)
                            currFuncListLSInfo.append(lsInfo)
                            del lsInfo
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
                        lsInfo = LoadStoreInfo()
                        lsInfo.loadPCRel(addInTable, lineNumObj)
                        currFuncListLSInfo.append(lsInfo)
                        del lsInfo
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
                                lsInfo = LoadStoreInfo()
                                lsInfo.loadVar(localVar, lineNumObj)
                                currFuncListLSInfo.append(lsInfo)
                                del lsInfo
                                logging.debug(" %d: Reading local var %s" %
                                              (lineNumObj, localVar.name))
                            else:
                                lsInfo = LoadStoreInfo()
                                lsInfo.readSpiltReg((ldrAdd - armEmu.reg["sp"].value), lineNumObj)
                                currFuncListLSInfo.append(lsInfo)
                                del lsInfo
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
                                lsInfo = LoadStoreInfo()
                                lsInfo.loadVar(globalVar, lineNumObj)
                                currFuncListLSInfo.append(lsInfo)
                                del lsInfo
                                logging.debug(" %d: Reading Global Var %s" % 
                                              (lineNumObj, globalVar.name))
                                continue
                            else:
                                lsInfo = LoadStoreInfo()
                                lsInfo.loadInaccurate(lineNumObj)
                                currFuncListLSInfo.append(lsInfo)
                                del lsInfo
                                logging.error(" %d: %s" % (lineNumObj, instObj))
                                continue
                        
            else:
                logging.error(" %d: Instruction does not match!")
                return -1
            
#         debugListLSInfo(currFuncListLSInfo)
        listLSInfo = listLSInfo + currFuncListLSInfo

    return listLSInfo

def findLoadStoreBetweenLines(listLSInfo, startLine, endLine):
    listLSInfoInBlock = []
    for lsInfo in listLSInfo:
        if lsInfo.lineNumObj in range(startLine, endLine+1):
            listLSInfoInBlock.append(lsInfo)
    return listLSInfoInBlock
