import linecache as lc
from arm_isa_regex import *
from annotation import *

ALU_LAT = 1
MUL_LAT = 1
LDST_LAT = 1

ALU_RES_LAT = 1 - ALU_LAT
MUL_RES_LAT = 4 - MUL_LAT
LDST_RES_LAT = 3 - LDST_LAT

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item

def annot_pipeline_sim(listISCFunctions, 
                          listObjdumpFunctions):
    '''
    In this function, we simulate pipeline for each basic block in the Objdump.
    
    We assume that :
     * Each basic block is independent, and is cold started ie. no instruction
       midway in pipeline.
     * For each Load/Store Instruction L1 Data Hit occurs.
     
    Pipeline Structure
     * 8 stage pipeline
       * 2 Instruction Fetch Stages
       * 2 Instruction Decode Stages
       * 4 Parallel Stages for 
         * Arithmetic Operations :  SH,   ALU,  SAT,  WB
         * Multiply Operations :    MAC1, MAC2, MAC3
         * Load Store Unit :        ADD,  DC1,  DC2,  WB
         
    Definitions:
     * Result Latency : Number of cycles required for the result of this
       instruction to be available at the start of ALU, MAC2 or DC1 stages
       of the next instruction.
     * Early Reg : Register required at the start of SH, MAC1 or ADD stages. 
       One cycle must be added to result latency of instruction producing this
       register for interlock calculations.
     * Late Reg : Register required in second stage of execution pipeline. One
       cycle must be subtracted from result latency of instruction producing
       this register for interlock calculations.
     
     Load/Store Instructions
      * Result Latency : 3 cycles
     ADD/MOV Inst:
      * Result Latency : 1 cycle
     MUL Inst
      * Result Latency : avg. 4 cycles (varies)
    '''
    dictAnnotPipeline = {}
    
    for funcObj in listObjdumpFunctions:
        funcISC = find(lambda fn: fn.functionName == funcObj.functionName, 
                       listISCFunctions) 
        
        for blockObj in funcObj.cfg.listBlocks:
            #initialize some state registers
            prevOpLoadStore = False
            prevDestReg = None
            currBlockCycles = 7; # For filling the pipeline on cold start
            
            for lineNumObj in range(blockObj.startLine, blockObj.endLine + 1):
                lineObj = lc.getline(funcObj.fileName, lineNumObj)
                
                # Initialize some state Registers
                opcode = ""
                destReg = ""
                op1Reg = ""
                op2 = ""
                op2RegIsShifted = False
                
                m = re_instruction.match(lineObj)
                assert(m is not None)
                instObj = m.group("instruction")
                
                m = re_arithInst.match(instObj)
                if m is not None:
                    opcode = m.group("arithOpcode")
                    destReg = m.group("destReg")
                    op1Reg = m.group("op1Reg")
                    if m.group("op2RegShifted") is not None:
                        op2 = m.group("op2RegShifted")
                        op2RegIsShifted = True
                    elif m.group("op2Reg") is not None:
                        op2 = m.group("op2Reg")
                        op2RegIsShifted = False
                    else:
                        assert(m.group("op2ImedVal") is not None)
                        op2 = ""
                        op2RegIsShifted = False
                    
                    if opcode not in ["mul", "mla"]:
                        # Add Instruction
                        currBlockCycles= currBlockCycles + ALU_LAT
                        prevResLat = ALU_RES_LAT
                    else:
                        # Multiply Instruction
                        currBlockCycles = currBlockCycles + MUL_LAT
                        prevResLat = MUL_RES_LAT
                    
                    # Calculation Interlock for Add and Mul Instructions
                    if prevDestReg is not None:
                        if op2 is not "":
                            if (op2RegIsShifted == True):
                                if (op2 == prevDestReg):
                                    # Early Reg!
                                    currBlockCycles = currBlockCycles + prevResLat + 1
                                elif (op1Reg == prevDestReg):
                                    # Late Reg!
                                    currBlockCycles = currBlockCycles + prevResLat - 1
                                else:
                                    # No interlock
                                    pass
                            else: # (op2RegIsShifted == False)
                                if (op1Reg == prevDestReg or
                                    op2 == prevDestReg):
                                    # Early Reg!
                                    currBlockCycles = currBlockCycles + prevResLat + 1
                                else:
                                    # No interlock
                                    pass
                    
                    prevDestReg = destReg
                    continue

                m = re_movInst.match(instObj)
                if m is not None:
                    destReg = m.group("destReg")
                    if m.group("op2RegShifted") is not None:
                        op2 = m.group("op2RegShifted")
                        op2RegIsShifted = True
                    elif m.group("op2Reg") is not None:
                        op2 = m.group("op2Reg")
                        op2RegIsShifted = False
                    else:
                        assert(m.group("op2ImedVal") is not None)
                        op2 = ""
                        op2RegIsShifted = False
                    
                    currBlockCycles= currBlockCycles + ALU_LAT
                    
                    # Calculation Interlock for Add and Mul Instructions
                    if prevDestReg is not None:
                        if op2 is not "":
                            if (op2 == prevDestReg):
                                # Early Reg!
                                currBlockCycles = currBlockCycles + prevResLat + 1
                            else:
                                # No interlock
                                pass
                        
                    prevDestReg = destReg
                    prevResLat = ALU_RES_LAT
                    continue
            
                m = re_mvnInst.match(instObj)
                if m is not None:
                    destReg = m.group("destReg")
                    if m.group("op2RegShifted") is not None:
                        op2 = m.group("op2RegShifted")
                        op2RegIsShifted = True
                    elif m.group("op2Reg") is not None:
                        op2 = m.group("op2Reg")
                        op2RegIsShifted = False
                    else:
                        assert(m.group("op2ImedVal") is not None)
                        op2 = ""
                        op2RegIsShifted = False
                    
                    currBlockCycles= currBlockCycles + ALU_LAT
                    
                    # Calculation Interlock for Add and Mul Instructions
                    if prevDestReg is not None:
                        if op2 is not "":
                            if (op2 == prevDestReg):
                                # Early Reg!
                                currBlockCycles = currBlockCycles + prevResLat + 1
                            else:
                                # No interlock
                                pass
                        
                    prevDestReg = destReg
                    prevResLat = ALU_RES_LAT
                    continue

                m = re_arithLongInst.match(instObj)
                if m is not None:
                    # Long Arithmetic Instructions
                    currBlockCycles = currBlockCycles + 2 * MUL_RES_LAT
                    prevDestReg = None
                    prevResLat = 0
                    # TODO: This needs to be improved!
                    continue
                
                m = re_logicInst.match(instObj)
                if m is not None:
                    # Logical Instruction
                    # opcode = m.group("logicOpcode")
                    destReg = m.group("destReg")
                    op1Reg = m.group("op1Reg")
                    if m.group("op2RegShifted") is not None:
                        op2 = m.group("op2RegShifted")
                        op2RegIsShifted = True
                    elif m.group("op2Reg") is not None:
                        op2 = m.group("op2Reg")
                        op2RegIsShifted = False
                    else:
                        assert(m.group("op2ImedVal") is not None)
                        op2 = ""
                        op2RegIsShifted = False
                        
                    currBlockCycles = currBlockCycles + ALU_RES_LAT
                    
                    # Calculating Interlock
                    if prevDestReg is not None:
                        if op2 is not "":
                            if (op2RegIsShifted == True):
                                if (op2 == prevDestReg):
                                    # Early Reg!
                                    currBlockCycles = currBlockCycles + prevResLat + 1
                                elif (op1Reg == prevDestReg):
                                    # Late Reg!
                                    currBlockCycles = currBlockCycles + prevResLat - 1
                                else:
                                    # No interlock
                                    pass
                            else: # (op2RegIsShifted == False)
                                if (op1Reg == prevDestReg or
                                    op2 == prevDestReg):
                                    # Early Reg!
                                    currBlockCycles = currBlockCycles + prevResLat + 1
                                else:
                                    # No interlock
                                    pass
                    
                    prevDestReg = destReg
                    prevResLat = ALU_RES_LAT
                    continue
                
                # Calculating Interlock
                m = re_shiftInst.match(instObj)
                if m is not None:
                    # Shift Instruction
                    # opcode = m.group("shiftOpcode")
                    destReg = m.group("destReg")
                    op1Reg = m.group("op1Reg")
                        
                    currBlockCycles = currBlockCycles + ALU_RES_LAT    
                    
                    # Calculation Interlock
                    if prevDestReg is not None:
                        if prevDestReg == op1Reg:
                            # Early Reg!
                            currBlockCycles = currBlockCycles + prevResLat + 1
                        else:
                            # No Interlock!
                            pass
                    
                    prevDestReg = destReg
                    prevResLat = ALU_RES_LAT
                    continue
                
                m = re_branchInst.match(instObj)
                if m is not None:
                    # Branch Instruction
                    currBlockCycles = currBlockCycles + ALU_RES_LAT
                    prevDestReg = None
                    prevResLat = 0
                    # TODO: May need to be improved! 
                    continue
                
                m = re_cmpInst.match(instObj)
                if m is not None:
                    # Compare Instruction
                    op1Reg = m.group("op1Reg")
                    if m.group("op2RegShifted") is not None:
                        op2 = m.group("op2RegShifted")
                        op2RegIsShifted = True
                    elif m.group("op2Reg") is not None:
                        op2 = m.group("op2Reg")
                        op2RegIsShifted = False
                    else:
                        assert(m.group("op2ImedVal") is not None)
                        op2 = ""
                        op2RegIsShifted = False
                        
                    currBlockCycles = currBlockCycles + ALU_RES_LAT
                    
                    # Calculating Interlock
                    if prevDestReg is not None:
                        if op2 is not "":
                            if (op2RegIsShifted == True):
                                if (op2 == prevDestReg):
                                    # Early Reg!
                                    currBlockCycles = currBlockCycles + prevResLat + 1
                                elif (op1Reg == prevDestReg):
                                    # Late Reg!
                                    currBlockCycles = currBlockCycles + prevResLat - 1
                                else:
                                    # No interlock
                                    pass
                            else: # (op2RegIsShifted == False)
                                if (op1Reg == prevDestReg or
                                    op2 == prevDestReg):
                                    # Early Reg!
                                    currBlockCycles = currBlockCycles + prevResLat + 1
                                else:
                                    # No interlock
                                    pass
                    
                    prevDestReg = None
                    prevResLat = 0
                    continue
                
                m = re_pushInst.match(instObj)
                if m is not None:
                    pushRegs = m.group("pushRegs")
                    listPushRegs = pushRegs.split(",")
                    currBlockCycles = currBlockCycles + len(listPushRegs)
                    prevDestReg = None
                    prevResLat = 0
                    # TODO: May need to be fixed!
                    continue
                
                m = re_popInst.match(instObj)
                if m is not None:
                    pushRegs = m.group("popRegs")
                    listPushRegs = pushRegs.split(",")
                    currBlockCycles = currBlockCycles + len(listPushRegs)
                    prevDestReg = None
                    prevResLat = 0
                    # TODO: May need to be fixed!
                    continue
                
                m = re_ignoredInst.match(instObj)
                if m is not None:
                    currBlockCycles = currBlockCycles + LDST_LAT
                    prevDestReg = None
                    prevResLat = 0
                    # TODO: Has to be improved!!!
                    continue
                
                m = re_loadInst.match(instObj)
                if m is not None:
                    destReg = m.group("destReg")
                    for baseRegLabel in ["am2_1BaseReg", 
                                 "am2_2BaseReg", 
                                 "am2_3BaseReg", 
                                 "am2_4BaseReg", 
                                 "am2_5BaseReg", 
                                 "am2_6BaseReg", 
                                 "am2_7BaseReg"]:
                        if m.group(baseRegLabel) is not None:
                            break
                    op1Reg = m.group(baseRegLabel)
                    op2 = ""
                    if op1Reg == "am2_3BaseReg":
                        op2 = m.group("am2_3OffsetReg")
                        op2RegIsShifted = False
                    elif op1Reg == "am2_4BaseReg":
                        op2 = m.group("am2_4OffsetReg")
                        op2RegIsShifted = True
                    elif op1Reg == "am2_6BaseReg":
                        op2 = m.group("am2_6OffsetReg")
                        op2RegIsShifted = False
                    elif op1Reg == "am2_7BaseReg":
                        op2 = m.group("am2_7OffsetReg")
                        op2RegIsShifted = True
                                                            
                    currBlockCycles = currBlockCycles + LDST_LAT
                    
                    if prevDestReg is not None:
                        if op2 is not "":
                            if (op2RegIsShifted == True):
                                if (op2 == prevDestReg):
                                    # Early Reg!
                                    currBlockCycles = currBlockCycles + prevResLat + 1
                                elif (op1Reg == prevDestReg):
                                    # Late Reg!
                                    currBlockCycles = currBlockCycles + prevResLat - 1
                                else:
                                    # No interlock
                                    pass
                            else: # (op2RegIsShifted == False)
                                if (op1Reg == prevDestReg or
                                    op2 == prevDestReg):
                                    # Early Reg!
                                    currBlockCycles = currBlockCycles + prevResLat + 1
                                else:
                                    # No interlock
                                    pass

                    prevDestReg = destReg
                    prevResLat = LDST_RES_LAT
                    continue
                
                m = re_storeInst.match(instObj)
                if m is not None:
                    currBlockCycles = currBlockCycles + LDST_LAT
                    prevDestReg = None
                    prevResLat = 0
                    continue
                
                print "%d : Instruction Could not be identified!" % (lineNumObj)
                
            # Block Done!
            blockIndISC = blockObj.mapsTo[0]
            blockISC = funcISC.cfg.listBlocks[blockIndISC]
            annot_str = "pipelineCycles += %d;" % (currBlockCycles)
            annot = Annotation(annot_str,
                               funcISC.fileName,
                               blockISC.startLine,
                               replace = False)
            print ("Adding annotation to %s:%d : %s" % (funcISC.fileName,
                                                        blockISC.startLine-1,
                                                        annot_str))
            addAnnotationToDict(dictAnnotPipeline, 
                                blockISC.startLine-1,
                                annot)
        # Function Done!
    
    # All Functions Done!
    return dictAnnotPipeline

if __name__ == "__main__":
    pass