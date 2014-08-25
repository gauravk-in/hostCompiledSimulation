import sys

from pyparsing import *
from logging.config import IDENTIFIER

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
#                         | (LPAREN + expression + RPAREN)
                       )

unary_operator = oneOf("+ - & * ~ !")


cast_expression = Forward()
unary_expression = Forward()
unary_expression << ( primary_expression
                      | (INC_OP + unary_expression) 
                      | (DEC_OP + unary_expression)
                      | (unary_operator + cast_expression)
                      | (SIZEOF + unary_expression)
                      | (SIZEOF + LPAREN + type_name + RPAREN)
                      )  

cast_or_parenthesized_expression = ( (expression + RPAREN)
                                     ^ (type_name + RPAREN + cast_expression)
                                     )

cast_expression << ( unary_expression
                     | (LPAREN + cast_or_parenthesized_expression)
                     )

# Left Factored
multiplicative_expression_1 = Forward()
multiplicative_expression_1 << ( (MUL_OP + cast_expression + multiplicative_expression_1)
                                 | (DIV_OP + cast_expression + multiplicative_expression_1)
                                 | (MOD_OP + cast_expression + multiplicative_expression_1)
                                 | Empty()
                                 )
multiplicative_expression = ( cast_expression + multiplicative_expression_1)

# Left Factored
additive_expression_1 = Forward()
additive_expression_1 << ( (ADD_OP + multiplicative_expression + additive_expression_1)
                           | (SUB_OP + multiplicative_expression + additive_expression_1)
                           | Empty()
                           )
additive_expression = ( multiplicative_expression + additive_expression_1 )


assignment_expression = Forward()
assignment_expression << ( (unary_expression + ASSIGN_OP + assignment_expression)
                           | (additive_expression)
                           )


expression << ( assignment_expression )

# Full statement with ';'
statement = ( expression + SEMICOLON + stringEnd)

if __name__ == "__main__":
    str = "diff = (int) *(short int *) ((uintptr_t)indata + (uintptr_t)ivtmp_28) - valpred;"
    r = statement.parseString(str)
    print r
    