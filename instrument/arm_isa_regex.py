import re

EndLine = "\s*;\s*(?P<comment>.*)$|$"

Cond = "eq|ne|cs|hs|lo|cc|mi|pl|hi|ls|ge|lt|gt|le"
Reg = "r0|r1|r2|r3|r4|r5|r6|r7|r8|r9|sl|fp|ip|sp|lr|pc"
ShiftOpcode = "(?:lsl|lsr|asr|ror|rrx)s?"
Operand2 = "#(?P<op2ImedVal>-?\d*)|(?P<op2Reg>%s)|(?P<op2RegShifted>%s),\s*(?:%s)\s*(?:#-?\d*|(?:%s))" % (Reg, Reg, ShiftOpcode, Reg)
re_movInst = re.compile("\s*(?:mov)s?(?:%s)?\s*(?P<destReg>%s),\s*(?:%s)(?:%s)" % 
                        (Cond, Reg, Operand2, EndLine))
re_mvnInst = re.compile("\s*(?:mvn)s?(?:%s)?\s*(?P<destReg>%s),\s*(?:%s)(?:%s)" % 
                        (Cond, Reg, Operand2, EndLine))

ArithOpcode = "(?P<arithOpcode>add|adc|sub|sbc|rsb|rsc|mul|mla)s?" # There are more that I have ignored for now
re_arithInst = re.compile("\s*(?:%s)(?:%s)?\s*(?P<destReg>%s),\s*(?P<op1Reg>%s),\s*(?:%s)(?:%s)" % 
                          (ArithOpcode, Cond, Reg, Reg, Operand2, EndLine))

ArithLongOpcode = "(?P<arithLongOpcode>umull|umlal|smull|smlal)"
re_arithLongInst = re.compile("\s*(?:%s)(?:%s)?\s*(?P<destRegLow>%s),\s*(?P<destRegHi>%s),\s*(?:%s),\s*(?:%s)(?:%s)" % 
                              (ArithLongOpcode, Cond, Reg, Reg, Reg, Reg, EndLine))

LogicOpcode = "(?P<logicOpcode>and|eor|orr|bic)s?"
re_logicInst = re.compile("\s*(?:%s)(?:%s)?\s*(?P<destReg>%s),\s*(?P<op1Reg>%s),\s*(?:%s)(?:%s)" % 
                          (LogicOpcode, Cond, Reg, Reg, Operand2, EndLine))

re_shiftInst = re.compile("\s*(?:%s)(?:%s)?\s*(?P<destReg>%s),\s*(?P<op1Reg>%s),\s*#(?P<op2ImedVal>\d*)(?:%s)" %
                          (ShiftOpcode, Cond, Reg, Reg, EndLine))

BranchOpcode = "(?P<branchOpcode>b|bl|bx|blx|bxj)"
BranchTarget = "(?P<branchTarget>[a-f0-9]*)"
Label = "\<(?P<labelFunction>\w*)(?:\+0x[a-f0-9]*)?\>"
re_branchInst = re.compile("\s*(?:%s)(?:%s)?\s*(?:(?:%s)|(?:%s))\s*(?:%s)?(?:%s)" % 
                           (BranchOpcode, Cond, Reg, BranchTarget, Label, EndLine))

# AMode2 = "\[(?P<lsop2BaseReg>%s)(?:(?:,\s*(?:(?P<imedOffset>#-?\d*)|(?P<offsetReg>-?%s(?:,\s*(?:%s)\s*#\d*)?)))?\])|(?:(?:\](?:,\s*(?:#\d*)|(?:%s(?:,\s*(?:%s),\s*#\d*)?))?))" % (Reg, Reg, ShiftOpcode, Reg, ShiftOpcode)

AMode2_1 = "\[(?P<am2_1BaseReg>%s)\]" % (Reg)
AMode2_2 = "\[(?P<am2_2BaseReg>%s),\s*#(?P<am2_2ImedOff>-?\d*)\]" % (Reg)
AMode2_3 = "\[(?P<am2_3BaseReg>%s),\s*(?P<am2_3OffsetReg>-?%s)\]" % (Reg, Reg)
AMode2_4 = "\[(?P<am2_4BaseReg>%s),\s*(?P<am2_4OffsetReg>%s),\s*(?:%s)\s*#\d*\]" % (Reg, Reg, ShiftOpcode)
AMode2_5 = "\[(?P<am2_5BaseReg>%s)\],\s*#(?P<am2_5ImedOff>-?\d*)" % (Reg)
AMode2_6 = "\[(?P<am2_6BaseReg>%s)\],\s*-?(?:%s)" % (Reg, Reg)
AMode2_7 = "\[(?P<am2_7BaseReg>%s)\],\s*(?:%s),\s*(?:%s)\s*#\d*" % (Reg, Reg, ShiftOpcode)

AMode2 = ("(?:%s)|(?:%s)|(?:%s)|(?:%s)|(?:%s)|(?:%s)|(?:%s)" % (AMode2_1, 
                                                                AMode2_2, 
                                                                AMode2_3, 
                                                                AMode2_4, 
                                                                AMode2_5,
                                                                AMode2_6, 
                                                                AMode2_7))

LoadStoreType = "t|b|bt|sb|h|sh|d"
LoadStoreOp2 = ("\[(?P<lsop2BaseReg>%s)(?:,\s*(?P<lsop2Index>%s))?\]" % (Reg, Operand2))
re_loadInst = re.compile("\s*ldrs?(?:%s)?(?:%s)?\s*(?P<destReg>%s),\s*(?:%s)(?:%s)" % 
                         (LoadStoreType, Cond,  Reg, AMode2, EndLine))
re_storeInst = re.compile("\s*strs?(?:%s)?(?:%s)?\s*(?P<destReg>%s),\s*(?:%s)(?:%s)" % 
                         (LoadStoreType, Cond, Reg, AMode2, EndLine))

re_cmpInst = re.compile("\s*(?:cmp|cmn)\s*(?:%s),\s*(?:%s)(?:%s)" % 
                        (Reg, Operand2, EndLine))

re_pushInst = re.compile("\s*push\s*\{(?P<pushRegs>(?:%s)(?:,\s*(?:%s))*)\}(?:%s)" % 
                         (Reg, Reg, EndLine))

re_popInst = re.compile("\s*pop\s*\{(?P<popRegs>(?:%s)(?:,\s*(?:%s))*)\}(?:%s)" % 
                         (Reg, Reg, EndLine))

IgnoredOpcode = "(?P<ignoredOpcode>stc|ldc|stm|tst)"
re_ignoredInst = re.compile("\s*(?:%s).*" % (IgnoredOpcode))