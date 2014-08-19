import re
import logging
from arm_isa_regex import *

class Register:
    def __init__(self, name):
        self.name = name
        self.isValid = False
        self.value = 0
    
    def setInvalid(self):
        self.isValid = False
    
    def setValue(self, value):
        self.valid = True
        self.value = value

# List of names of General Purpose Registers
listGPRegNames = ["r0",
                  "r1",
                  "r2",
                  "r3",
                  "r4",
                  "r5",
                  "r6",
                  "r7",
                  "r8",
                  "r9",
                  "sl",
                  "fp",
                  "ip",
                  "sp",
                  "lr",
                  "pc"]


INIT_STACK_POINTER_VAL = 0xffffffff

class ArmEmulator:
    def __init__(self, dictGlobVarAddAtTableAddress, listInitRegisterState = None):
        if listInitRegisterState == None:
            self.reg = {}
            for regName in listGPRegNames:
                self.reg[regName] = Register(regName)
        else:
            self.reg = listInitRegisterState
            
        # For our emulation purpose, we don't care what the actual value of SP
        #     is. However, we do want to initialize the SP so that we can
        #     identify local variable load/store operations.
        self.reg["sp"].setValue(INIT_STACK_POINTER_VAL)
        self.dictGlobVarAddAtTableAddress = dictGlobVarAddAtTableAddress

    def printRegisters(self):
        for regName in listGPRegNames:
            if self.reg[regName].isValid:
                print "%s = %d" % (regName, self.reg[regName].value)
            else:
                print "%s = Invalid" % (regName)

    def setDictGlobVarTable(self, dictGlobVarAddAtTableAddress):
        self.dictGlobVarAddAtTableAddress = dictGlobVarAddAtTableAddress

    def emulate(self, inst):
        m = re_movInst.match(inst)
        if m is not None:
            destReg = m.group("destReg")
            if m.group("op2ImedVal") is not None:
                self.reg[destReg].setValue(int(m.group("op2ImedVal")))
                logging.debug("\t %s = %d" % (destReg, self.reg[destReg].value))
                return 0
            
            elif m.group("op2Reg") is not None:
                self.reg[destReg].setValue(self.reg[m.group("op2Reg")].value)
                logging.debug("\t %s = %s (= %d)" % (destReg, m.group("op2Reg"), 
                                                  self.reg[destReg].value))
                return 0
            
            elif m.group("op2RegShifted") is not None:
                self.reg[destReg].setInvalid()
                logging.debug("\t Move: with Shifted Operand: Ignored!")
                return 0
            
            else:
                logging.error("\t Move: instruction does not match any format! ***")
                return -1
            
        m = re_mvnInst.match(inst)
        if m is not None:
            destReg = m.group("destReg")
            if m.group("op2ImedVal") is not None:
                self.reg[destReg].setValue(~int(m.group("op2ImedVal")))
                logging.debug("\t %s = %d" % (destReg, self.reg[destReg].value))
                return 0
            
            elif m.group("op2Reg") is not None:
                self.reg[destReg].setValue(~self.reg[m.group("op2Reg")].value)
                logging.debug("\t %s = %s (= %d)" % (destReg, m.group("op2Reg"), 
                                                  self.reg[destReg].value))
                return 0
            
            elif m.group("op2RegShifted") is not None:
                self.reg[destReg].setInvalid()
                logging.debug("\t Move: with Shifted Operand: Ignored!")
                return 0
            
            else:
                logging.error("\t Move: instruction does not match any format! ***")
                return -1
            
        m = re_arithInst.match(inst)
        if m is not None:
            opcode = m.group("arithOpcode")
            destReg = m.group("destReg")
            op1Reg = m.group("op1Reg")
            
            if opcode in ["add", "adc"]:
                if m.group("op2ImedVal") is not None:
                    self.reg[destReg].setValue(self.reg[op1Reg].value + int(m.group("op2ImedVal")))
                    logging.debug("\t %s = %s + %d ( = %d )" % (destReg, op1Reg, 
                                                                int(m.group("op2ImedVal")),
                                                                self.reg[destReg].value))
                    return 0
                
                elif m.group("op2Reg") is not None:
                    self.reg[destReg].setValue(self.reg[op1Reg].value + self.reg[m.group("op2Reg")].value)
                    logging.debug("\t %s = %s + %s ( = %d )" % (destReg, op1Reg, 
                                                                m.group("op2Reg"),
                                                                self.reg[destReg].value))
                    return 0
                
                elif m.group("op2RegShifted") is not None:
                    self.reg[destReg].setValue(self.reg[op1Reg].value + self.reg[m.group("op2RegShifted")].value)
                    logging.debug("\t Add: with shifted operand2: approximated! ( = %d)" % (self.reg[destReg].value))
                    return 0
                
                else:
                    logging.error("\t Add: operand 2 does not match expected format! ***")
                    return -1
                
            elif opcode in ["sub", "sbc", "rsb", "rsc"]:
                if m.group("op2ImedVal") is not None:
                    self.reg[destReg].setValue(self.reg[destReg].value - int(m.group("op2ImedVal")))
                    logging.debug("\t %s = %s - %d ( = %d )" % (destReg, op1Reg, 
                                                                int(m.group("op2ImedVal")),
                                                                self.reg[destReg].value))
                    return 0
                
                elif m.group("op2Reg") is not None:
                    self.reg[destReg].setValue(self.reg[destReg].value - self.reg[m.group("op2Reg")].value)
                    logging.debug("\t %s = %s - %s ( = %d )" % (destReg, op1Reg, 
                                                                m.group("op2Reg"),
                                                                self.reg[destReg].value))
                    return 0
                
                elif m.group("op2RegShifted") is not None:
                    self.reg[destReg].setValue(self.reg[op1Reg].value - self.reg[m.group("op2RegShifted")].value)
                    logging.debug("\t Sub: with shifted operand2: approximated! ( = %d)" % (self.reg[destReg].value))
                    return 0
                
                else:
                    logging.error("\t Sub: operand 2 does not match expected format! ***")
                    return -1
                
            else:
                # All other arithmetic instructions, like mul etc.
                # These instructions shouldn't matter for us, so ignore them.
                self.reg[destReg].setInvalid()
                logging.debug("\t Arithmetic: Instruction ignored!")
                return 0
            
        m = re_arithLongInst.match(inst)
        if m is not None:
            destRegHi = m.group("destRegHi")
            destRegLow = m.group("destRegLow")
            self.reg[destRegHi].setInvalid()
            self.reg[destRegLow].setInvalid()
            logging.debug("\t Arithmetic long: Ignored!.")
            return 0
        
        m = re_shiftInst.match(inst)
        if m is not None:
            destReg = m.group("destReg")
            self.reg[destReg].setInvalid()
            logging.debug("\t Shift: Ignored!.")
            return 0
        
        m = re_logicInst.match(inst)
        if m is not None:
            destReg = m.group("destReg")
            self.reg[destReg].setInvalid()
            logging.debug("\t Logical: Ignored!")
            return 0
            
            
        m = re_branchInst.match(inst)
        if m is not None:
            # Ignore the branch instructions
            logging.debug("\t Branch: Ignored!")
            return 0
            
        m = re_loadInst.match(inst)
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
            destReg = m.group("destReg")
            srcBaseReg = m.group(baseRegLabel)
            
            if srcBaseReg == "pc":
                # PC Relative Load Instruction to load an address of Global Variable to register
                #     Note: It could also be loading some long value which was stored at the end
                #     of the function!
                comment = m.group("comment")
                m = re.match("\s*(?P<address>[a-f0-9]*)\s*", comment)
                if m is not None:
                    address = int(m.group("address"), 16)
                else:
                    logging.error("\t Load: PC Relative: comment could not be matched! ***")
                    return -1
                if address in self.dictGlobVarAddAtTableAddress:
                    globVarAddress = self.dictGlobVarAddAtTableAddress[address]
                    self.reg[destReg].setValue(globVarAddress)
                    logging.debug("\t %s = %d (address of global var)" % 
                                  (destReg, self.reg[destReg].value))
                    return 0
                else:
                    logging.error("\t Load: PC Relative: address could not be found in table!")
                    return -1
                
            else:
                # Ignoring other load instructions
                logging.debug("\t Load: Ignored! (not PC Relative).")
                return 0
            
        m = re_storeInst.match(inst)
        if m is not None:
            logging.debug("\t Store: Ignored!")
            return 0
        
        m = re_cmpInst.match(inst)
        if m is not None:
            logging.debug("\t Compare: Ignored!")
            return 0

        m = re_pushInst.match(inst)
        if m is not None:
            pushRegs = m.group("pushRegs")
            numRegs = pushRegs.count(',') + 1
            self.reg["sp"].setValue(self.reg["sp"].value + (numRegs * 4))
            logging.debug("\t Push: sp incremented by %d ( = %d )" % 
                          ((numRegs * 4), self.reg["sp"].value))
            return 0
            
        m = re_popInst.match(inst)
        if m is not None:
            popRegs = m.group("popRegs")
            numRegs = popRegs.count(',') + 1
            self.reg["sp"].setValue(self.reg["sp"].value - (numRegs * 4))
            logging.debug("\t Pop: sp decremented by %d ( = %d )" % 
                          ((numRegs * 4), self.reg["sp"].value))
            return 0
        
        m = re_ignoredInst.match(inst)
        if m is not None:
            opcode = m.group("ignoredOpcode")
            logging.debug("\t %s: Ignored!" % opcode)
            return 0
        
        # If here, instruction was unable to be matched!
        logging.error("\t Could Not match the instruction! ********************")
        logging.error("\t %s" % inst)
        return -1

        