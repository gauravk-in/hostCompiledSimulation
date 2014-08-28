import sys
import logging
from pyparsing import *



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


list_identifiers = []
list_annotations = []


################################################################3

list_type_names = ["short", "int", "long", "char", "float", "double", "void", "signed", "unsigned", "uintptr_t"]

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

    if tokens[0] not in list_type_names:
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
                annotation = (pointer_var_name, "simDCache(%s_addr, \"r\");" % (pointer_var_name))
                if annotation not in list_annotations:
                    list_annotations.append(annotation)
                deref_operator_seen = 0

        # Variable Access
        else:
            var_name = tokens[0]
            if (var_name not in list_identifiers):
                logging.debug(" Variable name = " + var_name)
                annotation = (var_name, "simDCache(%s_addr, \"r\");" % (var_name))
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

    if deref_operator_seen == 1 and deref_expression_lparen_seen == 1 and deref_index_seen == 1:
        deref_operator_seen = 0
        deref_expression_lparen_seen = 0
        deref_index_seen = 0
        base_pointer_var_seen = 0
        # TODO ANNOTATE Deref with Index here
        if deref_index_string != "":
            annotation = (base_pointer_var_name, "simDCache((%s_addr + (%s)), \"r\");" % (base_pointer_var_name, deref_index_string))
        else:
            annotation = (base_pointer_var_name, "simDCache(%s_addr, \"r\");" % (base_pointer_var_name))
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

    assert(array_index_lbrace_seen == 1)
    array_index_lbrace_seen = 0

    # TODO Annotate Array Indexed Access Here
    annotation = (array_name, "simDCache((%s_addr + (%s)), \"r\");" % (array_name, array_index_string))
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

    array_index_lbrace_seen = 1
    array_name = list_identifiers[-1]
    logging.debug(" Array Name = " + array_name)
    # TODO : Previous variable name was already annotated, assuming its a variable access. Delete the last entry in the list of annotations.
    del(list_annotations[-1])

# Removing Left Recursion
postfix_expression_1 = Forward()
postfix_expression_1 << ( (Literal("[").setParseAction(act_array_index_lbrace) + Combine(expression).setParseAction(act_array_index_expression) + Literal("]").setParseAction(act_array_index_rbrace))
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

    if tokens[0] is not "":
        if deref_operator_seen == 1 and deref_expression_lparen_seen == 1 and base_pointer_var_seen == 1 and deref_index_seen == 0:
            deref_index_seen = 1
            deref_index_string = tokens[0]
            logging.debug(" Deref Index String = " + deref_index_string)

    # Can happen when the derefed pointer was written in a paranthesis without an index. In this case, annotate deref pointer without index
    else:
        if deref_operator_seen == 1 and deref_expression_lparen_seen == 1 and base_pointer_var_seen == 1 and deref_index_seen == 0:
            deref_index_seen = 1
            deref_index_string = ""
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
relational_expression_1 << ( (LT_OP + shift_expression + relational_expression_1)
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
                            | (logical_or_expression)
                            )

assignment_expression = Forward()
assignment_expression << ( ((unary_expression) + ASSIGN_OP + (assignment_expression))
                           | (conditional_expression)
                           )

expression << ( assignment_expression )


# Full statement with ';'
statement = ( expression + SEMICOLON + stringEnd)
# statement.ignore(cStyleComment)

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
    global list_identifiers
    global list_annotations

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
    list_identifiers = []
    list_annotations = []

    r = statement.parseString(line)

    return list_annotations

def test():

    lines = [  "pcmdata[start - start_40] = *(short int*)((uintptr_t)ivtmp_28);"
             , "a = b + c;"
             , "diff = (int) *(short int *)((uintptr_t)indata + (uintptr_t)ivtmp_28) - valpred;"
             , "D_2252 = (unsigned int) j_76 + D_2263;"
             , "*outp = (signed char) (signed char) outputbuffer;"
             , "*(outp + i) = (signed char) (signed char) outputbuffer;"
             ]


    for line in lines:
        print ""
        print line
        annotations = parse_statement(line)
        print "Annotations:"
        for annotation in annotations:
            print "%s  ::  %s" % (annotation[0], annotation[1])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    deref_operator_seen = 0
    deref_expression_lparen_seen = 0
    base_pointer_var_seen = 0
    base_pointer_var_name = ""

    list_identifiers = []

    test()





























def parseStatement(line):

    logging.debug(" line: " + line)

    # Parse the Entire Statement
    try:
        r = statement.parseString(line)
    except ParseException, e:
        logging.error(" Parsing Statement: %s" % e.msg)
        return

    logging.debug(" Simplified Expression = " + "".join([str(e) for e in r])),
    logging.debug(" Destination = " + "".join([str(e) for e in r.dest]))
    logging.debug(" RHS = " + "".join([str(e) for e in r.value]))

    # Parse the Destination String
    try:
        r_dest = unary_expression.parseString(r.dest[0])
    except ParseException, e:
        logging.error(e.msg, e.line)
        logging.error(" Parsing Destination (LHS): %s" % e.msg)

    '''
    Analysing the Destination
    The Destination can only be either a dereferenced pointer, an indexed
    array element or a variable. Writing to a pointer itself is also
    basically writing to a variable.
    '''

    # If the destination variable, a dereferenced pointer?
    if r_dest.deref is not "":
        logging.debug(" \t Writing to address pointed by " + "".join([str(e) for e in r_dest.deref.deref_exp]))
        # Is the pointer being indexed?
        if r_dest.deref.deref_exp.prim.add is not "":
            ptr_name = r_dest.deref.deref_exp.prim.add.add_op[0][0]
            ptr_index = r_dest.deref.deref_exp.prim.add.add_op_rest[0]
            logging.debug(" Address in %s is indexed by %s" % (ptr_name, ptr_index))
            annotation = (ptr_name, "simDCache((%s_addr + (%s)), \"w\");" %
                          (ptr_name, ptr_index))
        else:
            ptr_name = r_dest.deref.deref_exp.prim[0]
            logging.debug(" Address in %s" % (ptr_name))
            annotation = (ptr_name,"simDCache((%s_addr), \"w\");" % (ptr_name))

    # If the destination variable and indexed element in an array
    elif r_dest.post.array_index is not "":
        array_name = r_dest.post.prim[0]
        array_index = r_dest.post.array_index[0]
        logging.debug(" Writing to element of array %s indexed by %s" % (array_name,
                                                                         array_index))
        annotation = (array_name, "simDCache((%s_addr + (%s)), \"w\");" % (array_name,
                                                                           array_index))

    # If destination is a variable
    else:
        var_name = r_dest.prim[0]
        logging.debug(" Writing to variable %s" % var_name)
        annotation = (var_name, "simDCache((%s_addr), \"w\");" % (var_name))

    print r.value
    # Parse the Value Expression
    try:
        r_value = expression.parseString(r.value[0])
    except ParseException, e:
        logging.error(e.msg, e.line)
        logging.error(" Parsing Destination (LHS): %s" % e.msg)

    print r_value.add.add_op.deref.deref_exp

    logging.debug(" Annotation = %s" % annotation[1])
    return annotation

