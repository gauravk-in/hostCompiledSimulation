import re
import logging
# from cGrammar import parse_statement

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
TypeSpecifiers = "char|int|float|double|short|long"
OptionalSpecifiers = "signed|unsigned"
StorageClass = "(?:static|extern|auto|register)"
UserDefined = "struct\s*[\w_]*"
IRCSpecific = "uintptr_t"
DataTypes = "((?:(?:%s)|(?:%s)|(?:%s)|(?:%s)|(?:%s))\s*)+(?:\*)*" % (StorageClass, OptionalSpecifiers, TypeSpecifiers, UserDefined, IRCSpecific)
VarSpec = "(?P<varType>%s)\s*(?P<varName>\w*)\s*(?P<varLen>(?:\[.*\])*)?" % (DataTypes)
VarSpecInitOneLine = "(?:%s)\s*=\s*((?:\{.*\})|(?:.*))" % (VarSpec)
VarSpecInitMultiLine = "(?:%s)\s*=\s*(?:\{.*)" % (VarSpec)
VarSpecInitMultiLineEnd = "\s*.*}\s*"
re_VarDecl = re.compile("\s*(?:%s)\s*;" % (VarSpec))
re_VarDeclInitOneLine = re.compile("\s*(?:%s)\s*;" % (VarSpecInitOneLine))
re_VarDeclInitMultiLine = re.compile("\s*(?:%s)" % (VarSpecInitMultiLine))
re_VarDeclInitMultiLineEnd = re.compile("\s*(?:%s)\s*;" % (VarSpecInitMultiLineEnd))

# Function Definition Start
VarSpec_ = "(?:%s)\s*(?:\w*)\s*(?:(?:\[.*\])*)?" % (DataTypes)
FuncParams = "(?:(?:%s)(?:\s*,\s*(?:%s))*)" % (VarSpec_, VarSpec_)
RetTypes = "(?:%s)|void" % (DataTypes)
re_FuncDefStart = re.compile("\s*(?P<retType>%s)?\s*(?P<name>\w*)\s*\((?P<params>%s)?\)\s*(?P<openBrace>\{)?" % (RetTypes, FuncParams))

# Label
re_Label = re.compile("\s*(?P<label>\w*):")

# If Statement
re_ifStatement = re.compile("\s*if\s*\(.*\)")
re_elseStatement = re.compile("\s*else\s*")

# Goto Instructions
re_gotoStatement = re.compile("\s*goto\s*\w*;")

# Struct Declaration Start
re_structDecl = re.compile("\s*struct\s*\w*\s*{.*};$")
re_structDeclMultiLine = re.compile("\s*struct\s*\w*\s*{\s*$")

# Extra
re_BlockStartLBrace = re.compile("^\s*\{\s*$")
re_BlockEndRBrace = re.compile("^\s*\}\s*$")
re_returnStatement = re.compile("^\s*return\s*.*;\s*$")
re_functionCallStatement = re.compile("\s*\w*\s*\(.*\);\s*")
# [&\s,\w\[\]\(\)\*]

# 
# # Assignment/Arithmetic
# Var = "(?:\s*\w*\s*)"
# Const = "(?:\s*\d*\s*)"
# Oper = "(?:\+|\-|\*|/)"
# re_Assign = re.compile("\s*.*\s*=\s*.*;")

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
    
    elif line.isspace():
        return True
    
    elif re_BlockStartLBrace.match(line):
        return True
    
    elif re_BlockEndRBrace.match(line):
        return True

    elif re_returnStatement.match(line):
        return True
    
    elif re_functionCallStatement.match(line):
        return True
    
    return False
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
#     fileName = "examples/adpcm/my_ctop_IR.c"
#     fileName = "examples/adpcm/adpcm_IR.c"
    fileName = "examples/sieve/erat_sieve_no_print_IR.c"

    file = open(fileName, "r")
    
    inMultiLineVarInit = 0
    inStructDeclaration = 0
    
    lineNum = 0
    
    for line in file:
        lineNum = lineNum + 1
        
        if shouldIgnore(line, lineNum):
            continue
        
        if inMultiLineVarInit == 1:
            m = re_VarDeclInitMultiLineEnd.match(line)
            if m is not None:
                logging.debug("%d: VarDecl MultiLine End " % (lineNum))
                inMultiLineVarInit = 0
                continue
            else:
                continue

        m = re_VarDeclInitOneLine.match(line)
        if m is not None:
            varName = m.group("varName")
            logging.debug("%d: VarDecl InitOneLine: \"%s\"" % (lineNum, varName))
            continue
        
        m = re_VarDeclInitMultiLine.match(line)
        if m is not None:
            varName = m.group("varName")
            logging.debug("%d: VarDecl InitMultiLine: \"%s\"" % (lineNum, varName))
            inMultiLineVarInit = 1;
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
        
        m = re_ifStatement.match(line)
        if m is not None:
            logging.debug("%d: If Statement." % lineNum)
            continue
        
        m = re_elseStatement.match(line)
        if m is not None:
            logging.debug("%d: Else Statement." % lineNum)
            continue
        
        m = re_gotoStatement.match(line)
        if m is not None:
            logging.debug("%d: Goto Statement." % lineNum)
            continue
        
        print ""
        logging.info("%d: %s" % (lineNum, line[0:-1]))
        annotations = parse_statement(line)
        for annotation in annotations:
            print "%s  ::  %s" % (annotation[0], annotation[1])
        
        continue
        