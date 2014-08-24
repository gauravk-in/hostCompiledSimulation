import re
import logging

# Comments
re_CommentStart = re.compile("\s*/\*.*")
re_CommentEnd = re.compile(".*\*/")
CommentOneLine = "\s*//.*"
CommentLine = "\s*/\*.*\*/"
re_Comment = re.compile("(?:(?:%s)|(?:%s))" % (CommentOneLine, CommentLine))

# Pre-processor directives
PreProcDir = "\s*#(?:include|define|ifndef|endif).*"
re_PreProcDir = re.compile("(?:%s)" % PreProcDir)

# Variable Declarations
TypeSpecifiers = "char|int|float|double"
OptionalSpecifiers = "signed|unsigned|short|long"
StorageClass = "(?:static|extern|auto|register)"
UserDefined = "struct\s*[\w_]*"
IRCSpecific = "uintptr_t"
DataTypes = "(?:%s)?\s*(?:%s\s*)*\s*(?:(?:%s)|(?:%s)|(?:%s))?\s*(?:\*)*" % (StorageClass, OptionalSpecifiers, TypeSpecifiers, UserDefined, IRCSpecific)
VarSpec = "(?P<varType>%s)\s*(?P<varName>\w*)\s*(?P<varLen>(?:\[.*\])*)?" % (DataTypes)
re_VarDecl = re.compile("\s*(?:%s);" % (VarSpec))

# Function Definition Start
VarSpec_ = "(?:%s)\s*(?:\w*)\s*(?:(?:\[.*\])*)?" % (DataTypes)
FuncParams = "(?:(?:%s)(?:\s*,\s*(?:%s))*)" % (VarSpec_, VarSpec_)
RetTypes = "(?:%s)|void" % (DataTypes)
re_FuncDefStart = re.compile("\s*(?P<retType>%s)?\s*(?P<name>\w*)\s*\((?P<params>%s)?\)\s*(?P<openBrace>\{)?" % (RetTypes, FuncParams))

# Label
re_Label = re.compile("\s*(?P<label>\w*):")

# Assignment/Arithmetic
Var = "(?:\s*\w*\s*)"
Const = "(?:\s*\d*\s*)"
Oper = "(?:\+|\-|\*|/)"
re_Assign = re.compile("\s*.*\s*=\s*.*;")

inMultiLineComment = False

def inComment(line, lineNum):
    global inMultiLineComment
    
    if inMultiLineComment == True:
        m = re_CommentEnd.match(line)
        if m is not None:
            inMultiLineComment = False
#             logging.debug("%d: Comment end" % lineNum)
        return True
    
    m = re_Comment.match(line)
    if m is not None:
#         logging.debug("%d: One Line Comment" % lineNum)
        return True
    
    m = re_CommentStart.match(line)
    if m is not None:
        inMultiLineComment = True
#         logging.debug("%d: Comment start" % lineNum)
        return True
    else:
        return False
    
def isPreProcDir(line, lineNum):
    m = re_PreProcDir.match(line)
    if m is not None:
#         logging.debug("%d: Preprocessor Directive" % lineNum)
        return True
    else:
        return False
    
    
def shouldIgnore(line, lineNum):
    if inComment(line, lineNum):
        return True
    
    elif isPreProcDir(line, lineNum):
        return True
    
    elif line == "":
#         logging.debug("%d: Empty Line" % lineNum)
        return True
    
    return False
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
#     fileName = "examples/adpcm/my_ctop_IR.c"
    fileName = "examples/adpcm/adpcm_IR.c"
    file = open(fileName, "r")
    
    lineNum = 0
    
    for line in file:
        lineNum = lineNum + 1
        
        if shouldIgnore(line, lineNum):
            continue
        
        m = re_VarDecl.match(line)
        if m is not None:
            varName = m.group("varName")
            logging.debug("%d: VarDecl: \"%s\"" % (lineNum, varName))
            continue
        
        m = re_FuncDefStart.match(line)
        if m is not None:
            funcName = m.group("name")
            logging.debug("%d: FuncDef: \"%s\"" % (lineNum, funcName))
            continue
        
        m = re_Label.match(line)
        if m is not None:
            label = m.group("label")
            logging.debug("%d: Label: \"%s\"" % (lineNum, label))
            continue
        
        m =

        continue
        