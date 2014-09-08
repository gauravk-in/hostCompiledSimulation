import sys
import logging
from pyparsing import *
from irc_regex import *


IDENTIFIER = Word(alphas, alphanums+'_')
CONSTANT = Word(nums+'.')
STRING_LITERAL = quotedString

LPAREN = Literal("(")
RPAREN = Literal(")")

ASSIGN_OP = Literal("=")
ADD_OP = Literal("+")
SUB_OP = Literal("-")
MUL_OP = Literal("*")
DIV_OP = Literal("/")
MOD_OP = Literal("%")
INC_OP = Literal("++")
DEC_OP = Literal("--")
OR_OP = Literal("||")
AND_OP = Literal("&&")
BITXOR_OP = Literal("^")
BITOR_OP = Literal("|")
BITAND_OP = Literal("&")

EQ_OP = Literal("==")
NE_OP = Literal("!=")
GT_OP = Literal(">")
GE_OP = Literal(">=")
LT_OP = Literal("<")
LE_OP = Literal("<=")

RIGHT_OP = Literal(">>")
LEFT_OP = Literal("<<")

PTR_OP = Literal("->")

POINTER = Literal("*")
SEMICOLON = Literal(";")
SIZEOF = Literal("sizeof")

# Type Specifiers
SHORT = Literal("short")
INT = Literal("int")
LONG = Literal("long")
CHAR = Literal("char")
FLOAT = Literal("float")
DOUBLE = Literal("double")
VOID = Literal("void")
SIGNED = Literal("signed")
UNSIGNED = Literal("unsigned")
# EXTRA
UINTPTR = Literal("uintptr_t")

# Type Qualifiers
CONST = Literal("const")
VOLATILE = Literal("volatile")
STRUCT = Literal("struct")
UNION = Literal("union")
ENUM = Literal("enum")

AUTO = Literal("auto")
REGISTER = Literal("register")

extra_type_specifier = ( UINTPTR )

'''
State Management Variables
'''

deref_operator_seen = 0
deref_expression_lparen_seen = 0
base_pointer_var_seen = 0
base_pointer_var_name = ""
pointer_var_name = ""
var_name = ""
deref_index_seen = 0
deref_index_string = ""
array_name = ""
array_index_lbrace_seen = 0
array_index_string = ""
assign_operator_seen = 0
isConditionalStatement = 0

list_identifiers = []
list_annotations = []
currStatementAccesses = []

def addAccessToList(newAccess):
    global currStatementAccesses
    
    for access in currStatementAccesses:
        if access.varName == newAccess.varName:
            return
    
    currStatementAccesses.append(newAccess)


################################################################3

list_type_names = ["short", "int", "long", "char", "float", "double", "void", "signed", "unsigned", "uintptr_t"]
list_keywords = ["if", "else", "switch", "case", "for", "while", "do", "return"]


# TODO: Extend this : struct_or_union, enum
type_specifier = ( SHORT
                   | INT
                   | LONG
                   | CHAR
                   | FLOAT
                   | DOUBLE
                   | VOID
                   | SIGNED
                   | UNSIGNED
                   | extra_type_specifier
                   )

type_qualifier = ( CONST
                   | VOLATILE
                   )

unary_operator = oneOf("+ - & ~ !")
DEREF_OP = Literal("*")

specifier_qualifier_list = Forward()
specifier_qualifier_list << ( ( type_specifier + specifier_qualifier_list )
                             | type_specifier
                             | ( type_qualifier + specifier_qualifier_list )
                             | type_qualifier
                             )

# TODO: Extend this
abstract_declarator = ( POINTER )

type_name = ( (specifier_qualifier_list + abstract_declarator)
              | specifier_qualifier_list 
              )

def act_identifier(tokens):
    global deref_operator_seen
    global deref_expression_lparen_seen
    global base_pointer_var_seen
    global base_pointer_var_name
    global pointer_var_name
    global var_name
    global list_identifiers
    global list_annotations
    global currStatementAccesses

    if tokens[0] not in list_type_names and tokens[0] not in list_keywords:
        # Deref Operation
        if deref_operator_seen == 1:
            # Deref Operation with Index
            if deref_expression_lparen_seen == 1:
                if base_pointer_var_seen == 0:
                    base_pointer_var_name = tokens[0]
                    base_pointer_var_seen = 1
                    logging.debug(" Base Pointer Var Name = " + base_pointer_var_name)
                # else ignore

            # Deref Operation without Index
            else: # if deref_expression_lparen_seen == 0:
                pointer_var_name = tokens[0]
                logging.debug(" Pointer Var Name = " + pointer_var_name)
                # TODO Annotate Deref without Index here.
                annotation = (pointer_var_name, "simDCache((%s_addr), %d);" % (pointer_var_name, assign_operator_seen))
                addAccessToList(Access(pointer_var_name, False, "", assign_operator_seen))
                if annotation not in list_annotations:
                    list_annotations.append(annotation)
                deref_operator_seen = 0

        # Variable Access
        else:
            var_name = tokens[0]
            if (var_name not in list_identifiers):
                logging.debug(" Variable name = " + var_name)
                annotation = (var_name, "simDCache((%s_addr), %d);" % (var_name, assign_operator_seen))
                addAccessToList(Access(var_name, False, "", assign_operator_seen))
                if annotation not in list_annotations:
                    list_annotations.append(annotation)
                # TODO Annotate Variable Access Here.

            list_identifiers.append(tokens[0])


def act_rparen_expression(tokens):
    global deref_operator_seen
    global deref_expression_lparen_seen
    global deref_index_seen
    global base_pointer_var_seen
    global list_annotations
    global currStatementAccesses

    if deref_operator_seen == 1 and deref_expression_lparen_seen == 1 and deref_index_seen == 1:
        deref_operator_seen = 0
        deref_expression_lparen_seen = 0
        deref_index_seen = 0
        base_pointer_var_seen = 0
        # TODO ANNOTATE Deref with Index here
        annotation = (base_pointer_var_name, "simDCache((%s_addr%s), %d);" % (base_pointer_var_name, deref_index_string, assign_operator_seen))
        addAccessToList(Access(base_pointer_var_name, 
                                            True, 
                                            deref_index_string, 
                                            assign_operator_seen))
#         if deref_index_string != "":
#             annotation = (base_pointer_var_name, "simDCache((%s_addr + (%s)), %d);" % (base_pointer_var_name, deref_index_string, assign_operator_seen))
#         else:
#             annotation = (base_pointer_var_name, "simDCache(%s_addr, %d);" % (base_pointer_var_name, assign_operator_seen))
        if annotation not in list_annotations:
            list_annotations.append(annotation)


def act_lparen_expression(tokens):
    global deref_operator_seen
    global deref_expression_lparen_seen

    if deref_operator_seen == 1:
        deref_expression_lparen_seen = 1

expression = Forward()
primary_expression = ( IDENTIFIER.setParseAction(act_identifier)
                       ^ CONSTANT
                       ^ STRING_LITERAL
                       ^ ((LPAREN.setParseAction(act_lparen_expression) + expression + RPAREN.setParseAction(act_rparen_expression)))
                       )

def act_array_index_rbrace(tokens):
    global array_index_lbrace_seen
    global list_annotations
    global currStatementAccesses

    assert(array_index_lbrace_seen == 1)
    array_index_lbrace_seen = 0

    # TODO Annotate Array Indexed Access Here
    annotation = (array_name, "simDCache((%s_addr + (%s)), %d);" % (array_name, array_index_string, assign_operator_seen))
    addAccessToList(Access(array_name, 
                           True, 
                           array_index_string, 
                           assign_operator_seen))
    if annotation not in list_annotations:
        list_annotations.append(annotation)

def act_array_index_expression(tokens):
    global array_index_lbrace_seen
    global array_index_string

    if array_index_lbrace_seen == 1:
        array_index_string = tokens[0]
        logging.debug(" Array Index = " + array_index_string)

def act_array_index_lbrace(tokens):
    global array_index_lbrace_seen
    global base_pointer_var_name
    global list_identifiers
    global list_annotations
    global array_name
    global currStatementAccesses

    array_index_lbrace_seen = 1
    array_name = list_identifiers[-1]
    logging.debug(" Array Name = " + array_name)
    # TODO : Previous variable name was already annotated, assuming its a variable access. Delete the last entry in the list of annotations.
    del(list_annotations[-1])
    del(currStatementAccesses[-1])
    
# TODO : Check if PTR_OP and Literal(".") must be handled more carefully     

# Removing Left Recursion
postfix_expression_1 = Forward()
postfix_expression_1 << ( (Literal("[").setParseAction(act_array_index_lbrace) + Combine(expression).setParseAction(act_array_index_expression) + Literal("]").setParseAction(act_array_index_rbrace))
                          | (PTR_OP + IDENTIFIER + postfix_expression_1)
                          | (Literal(".") + IDENTIFIER + postfix_expression_1)
                          | Empty()
                          )
postfix_expression = ( (primary_expression) + postfix_expression_1)

def act_deref_operator(tokens):
    global deref_operator_seen
    deref_operator_seen = 1

cast_expression = Forward()
unary_expression = Forward()
unary_expression << ( postfix_expression
                      | (INC_OP + unary_expression)
                      | (DEC_OP + unary_expression)
                      | (unary_operator + cast_expression)
                      | (DEREF_OP.setParseAction(act_deref_operator) + Combine(cast_expression))
                      | (SIZEOF + unary_expression)
                      | (SIZEOF + LPAREN + type_name + RPAREN)
                      )  

cast_expression << ( ((LPAREN + type_name + RPAREN).suppress() + cast_expression)
                     | unary_expression
                     )

# Left Factored
multiplicative_expression_1 = Forward()
multiplicative_expression_1 << ( (MUL_OP + cast_expression + multiplicative_expression_1)
                                 | (DIV_OP + cast_expression + multiplicative_expression_1)
                                 | (MOD_OP + cast_expression + multiplicative_expression_1)
                                 | Empty()
                                 )
multiplicative_expression = ( cast_expression + multiplicative_expression_1)

def act_add_second_operand_onwards(tokens):
    global deref_operator_seen
    global deref_expression_lparen_seen
    global base_pointer_var_seen
    global deref_index_seen
    global deref_index_string

    if deref_operator_seen == 1 and deref_expression_lparen_seen == 1 and base_pointer_var_seen == 1 and deref_index_seen == 0:
        deref_index_seen = 1
        deref_index_string = tokens[0]
        logging.debug(" Deref Index String = " + deref_index_string)


# Left Factored
additive_expression_1 = Forward()
additive_expression_1 << ( (ADD_OP + multiplicative_expression + (additive_expression_1))
                           | (SUB_OP + multiplicative_expression + (additive_expression_1))
                           | Empty()
                           )
additive_expression = ( multiplicative_expression + Combine(additive_expression_1).setParseAction(act_add_second_operand_onwards) )

shift_expression_1 = Forward()
shift_expression_1 << ( (LEFT_OP + additive_expression + shift_expression_1)
                        | (RIGHT_OP + additive_expression + shift_expression_1)
                        | Empty()
                        )
shift_expression = ( (additive_expression + shift_expression_1) )

relational_expression_1 = Forward()
relational_expression_1 << ( (GT_OP + shift_expression + relational_expression_1)
                            | (LT_OP + shift_expression + relational_expression_1)
                            | (GE_OP + shift_expression + relational_expression_1)
                            | (LE_OP + shift_expression + relational_expression_1)
                            | Empty()
                            )

relational_expression = ( (shift_expression + relational_expression_1))

equality_expression_1 = Forward()
equality_expression_1 << ( (EQ_OP + relational_expression + equality_expression_1)
                           | (NE_OP + relational_expression + equality_expression_1)
                           | Empty()
                           )
equality_expression = ( (relational_expression + equality_expression_1) )

and_expression_1 = Forward()
and_expression_1 << ( (BITAND_OP + equality_expression + and_expression_1)
                      | Empty()
                      )
and_expression = ( (equality_expression + and_expression_1) )

exclusive_or_expression_1 = Forward()
exclusive_or_expression_1 << ( (BITXOR_OP + and_expression + exclusive_or_expression_1)
                               | empty()
                               )
exclusive_or_expression = ( (and_expression + exclusive_or_expression_1) )

inclusive_or_expression_1 = Forward()
inclusive_or_expression_1 << ( (BITOR_OP + exclusive_or_expression + inclusive_or_expression_1)
                               | Empty()
                               )
inclusive_or_expression = ( (exclusive_or_expression + inclusive_or_expression_1) )


logical_and_expression_1 = Forward()
logical_and_expression_1 << ( (AND_OP + inclusive_or_expression + logical_and_expression_1)
                              | Empty()
                              )
logical_and_expression = ( (inclusive_or_expression + logical_and_expression_1) )

logical_or_expression_1 = Forward()
logical_or_expression_1 << ( (OR_OP + logical_and_expression + logical_or_expression_1)
                             | Empty()
                             )
logical_or_expression = ( (logical_and_expression + logical_or_expression_1) )

# def print_conditional_expression(tokens):
#     print "Conditional Expression = ",
#     print tokens

conditional_expression = Forward()
conditional_expression << ( (logical_or_expression + Literal("?") + expression + Literal(":") + conditional_expression)
                            ^ (logical_or_expression)
                            )

def act_assign_op(tokens):
    global assign_operator_seen
    if (assign_operator_seen == 1):
        # TODO: Should only occur once?
        logging.warning (" WARNING: 2 Assignment Operations found! Is that right? ***")
    logging.debug(" Found Assignment Operator!")
    assign_operator_seen = 1

assignment_expression = Forward()
assignment_expression << ( ((unary_expression) + ASSIGN_OP.setParseAction(act_assign_op) + (assignment_expression))
                           ^ (conditional_expression)
                           )

expression << ( assignment_expression )


# Full statement with ';'
expression_statement = ( expression + SEMICOLON + stringEnd)

IF = Literal("if")
ELSE = Literal("else")

def actConditionalStatement(tokens):
    global isConditionalStatement
    global assign_operator_seen
    isConditionalStatement = 1
    assign_operator_seen = 1

selection_statement = ( IF.setParseAction(actConditionalStatement) + LPAREN + expression + RPAREN )

statement = ( expression_statement 
              | selection_statement )

def ignore_statement(line):
    m = re_Comment.match(line)
    if m is not None:
        logging.debug("One Line Comment : %s" % line)
        return True
    
    m = re_elseStatement.match(line)
    if m is not None:
        logging.debug("Else Statement : %s" % line)
        return True
    
    m = re_gotoStatement.match(line)
    if m is not None:
        logging.debug("Goto Statement. : %s" % line)
        return True
    
    m = re_functionCallStatement.match(line)
    if m is not None:
        logging.debug("Function Call. : %s" % line)
        return True
    
    m = re_returnStatement.match(line)
    if m is not None:
        logging.debug("Function Call. : %s" % line)
        return True
    
    if line.isspace():
        return True

class Access:
    def __init__(self, varName, isIndexed, index, isRead):
        self.varName = varName
        self.isIndexed = isIndexed
        self.index = index
        self.isRead = isRead
        
    def debug(self):
        if self.isRead:
            if self.isIndexed:
                logging.debug("Read var %s indexed by %s" % (var.name, var.index))
            else:
                logging.debug("Read var %s without index" % (var.name))
        else: # if not self.isRead:
            if self.isIndexed:
                logging.debug("Write var %s indexed by %s" % (var.name, var.index))
            else:
                logging.debug("Write var %s without index" % (var.name))    
            

def parse_statement(line):
    global deref_operator_seen
    global deref_expression_lparen_seen
    global base_pointer_var_seen
    global base_pointer_var_name
    global pointer_var_name
    global var_name
    global deref_index_seen
    global deref_index_string
    global array_name
    global array_index_lbrace_seen
    global array_index_string
    global isConditionalStatement
    global list_identifiers
    global list_annotations
    global assign_operator_seen
    global currStatementAccesses

    if ignore_statement(line):
        return None

    deref_operator_seen = 0
    deref_expression_lparen_seen = 0
    base_pointer_var_seen = 0
    base_pointer_var_name = ""
    pointer_var_name = ""
    var_name = ""
    deref_index_seen = 0
    deref_index_string = ""
    array_name = ""
    array_index_lbrace_seen = 0
    array_index_string = ""
    assign_operator_seen = 0
    isConditionalStatement = 0
    list_identifiers = []
    list_annotations = []
    currStatementAccesses = []
    
    r = statement.parseString(line)

    assert (len(list_annotations) == len(currStatementAccesses))

#     return list_annotations
    return currStatementAccesses

def test():

    lines = [  "pcmdata[start - start_40] = *(short int*)((uintptr_t)ivtmp_28);"
             , "a = b + c;"
             , "diff = (int) *(short int *)((uintptr_t)indata + (uintptr_t)ivtmp_28) - valpred;"
             , "*outp = (signed char) (signed char) outputbuffer;"
             , "*(outp + i) = (signed char) (signed char) outputbuffer;"
             , "valpred = state->valprev;"
             , "valpred = state.valprev;"
             , "valpred_41 = (valpred_34 > -32768) ? valpred_35 : -32768;"
             , "if (a == b)"
             ]
    
    expected_annotations = [[("start", "simDCache((start_addr), 0);" ),
                             ("start_40", "simDCache((start_40_addr), 0);"),
                             ("pcmdata", "simDCache((pcmdata_addr + (start-start_40)), 0);"),
                             ("ivtmp_28", "simDCache((ivtmp_28_addr), 1);")
                             ],
                            [("a", "simDCache((a_addr), 0);"),
                             ("b", "simDCache((b_addr), 1);"),
                             ("c", "simDCache((c_addr), 1);")
                             ],
                            [("diff", "simDCache((diff_addr), 0);"),
                             ("indata", "simDCache((indata_addr+ivtmp_28), 1);"),
                             ("valpred", "simDCache((valpred_addr), 1);")
                             ],
                            [("outp", "simDCache((outp_addr), 0);"),
                             ("outputbuffer", "simDCache((outputbuffer_addr), 1);")
                             ],
                            [("outp", "simDCache((outp_addr+i), 0);"),
                             ("outputbuffer", "simDCache((outputbuffer_addr), 1);")
                             ],
                            [("valpred", "simDCache((valpred_addr), 0);"),
                             ("state", "simDCache((state_addr), 1);"),
                             ("valprev", "simDCache((valprev_addr), 1);")
                             ],
                            [("valpred", "simDCache((valpred_addr), 0);"),
                             ("state", "simDCache((state_addr), 1);"),
                             ("valprev", "simDCache((valprev_addr), 1);")
                             ],
                            [("valpred_41", "simDCache((valpred_41_addr), 0);"),
                             ("valpred_34", "simDCache((valpred_34_addr), 1);"),
                             ("valpred_35", "simDCache((valpred_35_addr), 1);")
                             ],
                            [("a", "simDCache((a_addr), 1);"),
                             ("b", "simDCache((b_addr), 1);")]                            
                            ]


    for i in range(len(lines)):
        line = lines[i]
        print ""
        print line
        annotations = parse_statement(line)       
        print "Annotations:"
        for annotation in annotations:
            print "%s  ::  %s" % (annotation[0], annotation[1])
        if annotations != expected_annotations[i]:
            logging.error(" ERROR : Annotation for %d does not match expected value! ***" % i)
            return -1


    print "Tests passed!"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    deref_operator_seen = 0
    deref_expression_lparen_seen = 0
    base_pointer_var_seen = 0
    base_pointer_var_name = ""

    list_identifiers = []

    test()

