import sys
import logging
from pyparsing import *


IDENTIFIER = Word(alphas, alphanums+'_')("ident")
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

extra_type_specifier = ( UINTPTR)

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

expression = Forward()
primary_expression = ( IDENTIFIER 
                       | CONSTANT
                       | STRING_LITERAL
                       | (LPAREN + expression + RPAREN)
                       )

# Removing Left Recursion
postfix_expression_1 = Forward()
postfix_expression_1 << ( (Literal("[") + Combine(expression)("array_index") + Literal("]"))
                          | Empty()
                          )
postfix_expression = ( Combine(primary_expression)("prim") + postfix_expression_1) 

cast_expression = Forward()
unary_expression = Forward()
unary_expression << ( postfix_expression("post")
                      | (INC_OP + unary_expression) 
                      | (DEC_OP + unary_expression)
                      | (unary_operator + cast_expression)
                      | (DEREF_OP + Combine(cast_expression)("deref_exp"))("deref")
                      | (SIZEOF + unary_expression)
                      | (SIZEOF + LPAREN + type_name + RPAREN)
                      )  

cast_expression << ( unary_expression
                     ^ ((LPAREN + type_name + RPAREN).suppress() + cast_expression)
                     )

# Left Factored
multiplicative_expression_1 = Forward()
multiplicative_expression_1 << ( (MUL_OP + cast_expression("mul_op") + multiplicative_expression_1("mul_op_rest"))
                                 | (DIV_OP + cast_expression("mul_op") + multiplicative_expression_1("mul_op_rest"))
                                 | (MOD_OP + cast_expression("mul_op") + multiplicative_expression_1("mul_op_rest"))
                                 | Empty()
                                 )
multiplicative_expression = ( cast_expression("mul_op") + multiplicative_expression_1("mul_op_rest"))

# Left Factored
additive_expression_1 = Forward()
additive_expression_1 << ( (ADD_OP + multiplicative_expression("add_op") + Combine(additive_expression_1)("add_op_rest"))
                           | (SUB_OP + multiplicative_expression("add_op") + Combine(additive_expression_1)("add_op_rest"))
                           | Empty()
                           )
additive_expression = ( multiplicative_expression("add_op") + Combine(additive_expression_1)("add_op_rest") )


assignment_expression = Forward()
assignment_expression << ( (Combine(unary_expression)("dest") + ASSIGN_OP + Combine(assignment_expression)("value"))
                           | (additive_expression)("add")
                           )


expression << ( assignment_expression )

# Full statement with ';'
statement = ( expression + SEMICOLON + stringEnd)
# statement.ignore(cStyleComment)

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

    logging.debug(" Annotation = %s" % annotation[1])
    return annotation

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    lines = [ 
             "pcmdata[start - start_40] = *(short int*)((uintptr_t)ivtmp_28);"
             , "a = b + c;"
             , "diff = (int) *(short int *)((uintptr_t)indata + (uintptr_t)ivtmp_28) - valpred;"
             , "D_2252 = (unsigned int) j_76 + D_2263;"
             , "*outp = (signed char) (signed char) outputbuffer;"
             , "*(outp + i) = (signed char) (signed char) outputbuffer;"
             ]
    
    annotations = [ 
                   "simDCache((pcmdata_addr + (start-start_40)), \"w\");"
                   , "simDCache((a_addr), \"w\");"
                   , "simDCache((diff_addr), \"w\");"
                   , "simDCache((D_2252_addr), \"w\");"
                   , "simDCache((outp_addr, \"w\");"
                   , "simDCache((outp_addr + (+i)), \"w\");"
                   ]
    
    for i in range(len(lines)):
        print ""
        annotation = parseStatement(lines[i])
        if annotation[1] != annotations[i]:
            logging.error(" Line %d does not give expected results!" % i)
            exit
    
    print "\n\n All Tests Passed!"
        
    