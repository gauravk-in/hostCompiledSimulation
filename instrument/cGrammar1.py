from pyparsing import *
from _ast import For

IDENTIFIER = Word(alphas, alphanums+'_')
CONSTANT = Word(nums+'.')
STRING = quotedString
SIZEOF = "sizeof"

PTR_OP = Literal("->")
INC_OP = Literal("++")
DEC_OP = Literal("--")
LEFT_OP = Literal("<<")
RIGHT_OP = Literal(">>")
LE_OP = Literal("<=")
GE_OP = Literal(">=")
EQ_OP = Literal("==")
NE_OP = Literal("!=")

AND_OP = Literal("&&")
OR_OP = Literal("||")

MUL_ASSIGN = Literal("*=")
DIV_ASSIGN = Literal("/=")
MOD_ASSIGN = Literal("%=")
ADD_ASSIGN = Literal("+=")
SUB_ASSIGN = Literal("-=")
LEFT_ASSIGN = Literal("<<=")
RIGHT_ASSIGN = Literal(">>=")
AND_ASSIGN = Literal("&=")
XOR_ASSIGN = Literal("^=")
OR_ASSIGN = Literal("|=")

# TODO: TYPE_NAME

TYPEDEF = Literal("typedef")
EXTERN = Literal("extern")
STATIC = Literal("static")
AUTO = Literal("auto")
REGISTER = Literal("register")
CHAR = Literal("char")
SHORT = Literal("short")
INT = Literal("int")
LONG = Literal("long")
SIGNED = Literal("signed")
UNSIGNED = Literal("unsigned")
FLOAT = Literal("float")
DOUBLE= "double"
CONST = Literal("const")
VOLATILE = Literal("volatile")
VOID = Literal("void")
STRUCT = Literal("struct")
UNION = Literal("union")
ENUM = Literal("enum")

ELLIPSIS = Literal("...")

CASE = Literal("case")
DEFAULT = Literal("default")
IF = Literal("if")
ELSE = Literal("else")
SWITCH = Literal("switch")
WHILE = Literal("while")
DO = Literal("do")
FOR = Literal("for")
GOTO = Literal("goto")
CONTINUE = Literal("continue")
BREAK = Literal("break")
RETURN = Literal("return")

# TODO: Start Translation Unit

postfix_expression = Forward()
unary_expression = Forward()
cast_expression = Forward()
multiplicative_expression = Forward()
additive_expression = Forward()
shift_expression = Forward()
relational_expression = Forward()
equality_expression = Forward()
and_expression = Forward()
exclusive_or_expression = Forward()
logical_and_expression = Forward()
logical_or_expression = Forward()
conditional_expression = Forward()
assignment_expression = Forward()
expression = Forward()
declaration_specifiers = Forward()
init_declarator_list = Forward()
struct_declaration_list = Forward()
specifier_qualifier_list = Forward()
struct_declarator_list = Forward()
enumerator_list = Forward()
direct_declarator = Forward()
pointer = Forward()
type_qualifier_list = Forward()
parameter_type_list = Forward()
parameter_list = Forward()
identifier_list = Forward()
direct_abstract_declarator = Forward()
initializer_list = Forward()
declaration_list = Forward()
statement_list = Forward()
translation_unit = Forward()
primary_expression = Forward()
argument_expression_list = Forward()
unary_operator = Forward()
assignment_operator = Forward()
constant_expression = Forward()
declaration = Forward()
init_declarator = Forward()
storage_class_specifier = Forward()
type_specifier = Forward()
struct_or_union_specifier = Forward()
struct_or_union = Forward()
struct_declaration = Forward()
struct_declarator = Forward()
enum_specifier = Forward()
enumerator = Forward()
type_qualifier = Forward()
declarator = Forward()
parameter_declaration = Forward()
type_name = Forward()
abstract_declarator = Forward()
initializer = Forward()
statement = Forward()
labeled_statement = Forward()
compound_statement = Forward()
expression_statement = Forward()
selection_statement = Forward()
iteration_statement = Forward()
jump_statement = Forward()
external_declaration = Forward()
function_definition = Forward()
inclusive_or_expression = Forward()

primary_expression << ( IDENTIFIER 
                      | CONSTANT
                      | STRING
                      | ('(' + expression + ')')
                      )

postfix_expression<< ( primary_expression
                      | (postfix_expression + '[' + expression + ']')
                      | (postfix_expression + '(' + ')')
                      | (postfix_expression + '(' + argument_expression_list + ')')
                      | (postfix_expression + '.' + IDENTIFIER)
                      | (postfix_expression + PTR_OP + IDENTIFIER)
                      | (postfix_expression + INC_OP)
                      | (postfix_expression + DEC_OP)
                      )

argument_expression_list << ( assignment_expression
                           | (argument_expression_list + ',' + assignment_expression)
                           )

unary_expression << ( postfix_expression 
                     | (INC_OP + unary_expression)
                     | (DEC_OP + unary_expression)
                     | (unary_operator + cast_expression)
                     | (SIZEOF + unary_expression)
                     | (SIZEOF + '(' + type_name + ')')
                     )

unary_operator << oneOf("& * + - ~ !")

cast_expression << ( unary_expression
                    | ('(' + type_name + ')' + cast_expression)
                    )

multiplicative_expression << ( cast_expression
                              | (multiplicative_expression + '*' + cast_expression)
                              | (multiplicative_expression + '/' + cast_expression)
                              | (multiplicative_expression + '%' + cast_expression)
                              )

additive_expression << ( multiplicative_expression
                         | (additive_expression + '+' + multiplicative_expression)
                         | (additive_expression + '-' + multiplicative_expression)
                         )

shift_expression << ( additive_expression
                      | (shift_expression + LEFT_OP + additive_expression)
                      | (shift_expression + RIGHT_OP + additive_expression)
                      )

relational_expression << ( shift_expression
                           | (relational_expression + '<' + shift_expression)
                           | (relational_expression + '>' + shift_expression)
                           | (relational_expression + LE_OP + shift_expression)
                           | (relational_expression + GE_OP + shift_expression)
                           )

equality_expression << ( relational_expression
                         | (equality_expression + EQ_OP + relational_expression)
                         | (equality_expression + NE_OP + relational_expression)
                         )

and_expression << ( equality_expression
                    | (and_expression + '&' + equality_expression)
                    )

exclusive_or_expression <<( and_expression
                            | (exclusive_or_expression + '^' + and_expression)
                            )

logical_and_expression << ( inclusive_or_expression
                            | (logical_and_expression + AND_OP + inclusive_or_expression)
                            )

logical_or_expression << ( logical_and_expression
                           | (logical_or_expression + OR_OP + logical_and_expression)
                           )

conditional_expression << ( logical_or_expression
                            | (logical_or_expression + '?' + expression + ':' + conditional_expression)
                            )

assignment_expression << ( conditional_expression
                           | (unary_expression + assignment_operator + assignment_expression)
                           )
    
assignment_operator << ( '='
                        | MUL_ASSIGN
                        | DIV_ASSIGN
                        | MOD_ASSIGN
                        | ADD_ASSIGN
                        | SUB_ASSIGN
                        | LEFT_ASSIGN
                        | RIGHT_ASSIGN
                        | AND_ASSIGN
                        | XOR_ASSIGN
                        | OR_ASSIGN
                        )

expression << ( assignment_expression
                | (expression + ',' + assignment_expression)
                )

constant_expression << conditional_expression

# declaration << ( (declaration_specifiers + ';')
#                 | (declaration_specifiers + init_declarator_list + ';')
#                 )
# 
# declaration_specifiers << ( storage_class_specifier
#                             | (storage_class_specifier + declaration_specifiers)
#                             | type_specifier
#                             | (type_specifier + declaration_specifiers)
#                             | type_qualifier
#                             | (type_qualifier + declaration_specifiers)
#                             )
# 
# init_declarator_list << ( init_declarator
#                           | (init_declarator_list + ',' + init_declarator)
#                           )
# 
# init_declarator << ( declarator
#                     | (declarator + '=' + initializer)
#                     )

storage_class_specifier << ( TYPEDEF
                            | EXTERN
                            | STATIC
                            | AUTO
                            | REGISTER
                            )

type_specifier << ( VOID
                   | CHAR
                   | SHORT
                   | INT
                   | LONG
                   | FLOAT
                   | DOUBLE
                   | SIGNED
                   | UNSIGNED
                   | struct_or_union_specifier
                   | enum_specifier
                   | type_name
                   )

struct_or_union_specifier << ( (struct_or_union + IDENTIFIER + '{' + struct_declaration_list + '}')
                              | (struct_or_union + '{' + struct_declaration_list + '}')
                              | (struct_or_union + IDENTIFIER)
                              )

struct_or_union << ( STRUCT
                    | UNION
                    )

# struct_declaration_list << ( struct_declaration
#                              | (struct_declaration_list + struct_declaration)
#                              )
# 
# struct_declaration << specifier_qualifier_list +  struct_declarator_list +  ';'

specifier_qualifier_list << ( (type_specifier + specifier_qualifier_list)
                              | type_specifier
                              | (type_qualifier + specifier_qualifier_list)
                              | (type_qualifier)
                              )

# struct_declarator_list << ( struct_declarator
#                             | (struct_declarator_list + ',' + struct_declarator)
#                             )
# 
# struct_declarator << ( declarator
#                       | (':' + constant_expression)
#                       | (declarator + ':' + constant_expression)
#                       )
# 
# enum_specifier << ( (ENUM + '{' + enumerator_list + '}')
#                    | (ENUM + IDENTIFIER + '{' + enumerator_list + '}')
#                    | (ENUM + IDENTIFIER)
#                    )
# 
# enumerator_list << ( enumerator
#                      | (enumerator_list + ',' + enumerator)
#                      )
#  
# enumerator << ( IDENTIFIER
#                | (IDENTIFIER + '=' + constant_expression)
#                )

type_qualifier << ( CONST
                   | VOLATILE
                   )

# declarator << ( pointer + direct_declarator
#                | direct_declarator
#                )
# 
# direct_declarator << ( IDENTIFIER
#                        | ('(' + declarator + ')')
#                        | (direct_declarator + '[' + constant_expression + ']')
#                        | (direct_declarator + '[' + ']')
#                        | (direct_declarator + '(' + parameter_type_list + ')')
#                        | (direct_declarator + '(' + identifier_list + ')')
#                        | (direct_declarator + '(' + ')')
#                        )                       

pointer << ( '*'
             | ('*' +  type_qualifier_list)
             | ('*' + pointer)
             | ('*' + type_qualifier_list + pointer)
             )

type_qualifier_list << ( type_qualifier
                         | (type_qualifier_list + type_qualifier)
                         )

# parameter_type_list << ( parameter_list
#                          | (parameter_list + ',' + ELLIPSIS)
#                          )
# 
# parameter_list << ( parameter_declaration
#                     | (parameter_list + ',' + parameter_declaration)
#                     )
# 
# parameter_declaration << ( (declaration_specifiers + declarator)
#                           | (declaration_specifiers + abstract_declarator)
#                           | (declaration_specifiers)    
#                           )

# identifier_list << ( IDENTIFIER
#                      | (identifier_list + ',' + IDENTIFIER)
#                      )

type_name << ( specifier_qualifier_list
#               | (specifier_qualifier_list + abstract_declarator)
              )

# abstract_declarator << ( pointer
#                         | direct_abstract_declarator
#                         | (pointer + direct_abstract_declarator)
#                         )
#  
# direct_abstract_declarator << ( ('(' + abstract_declarator + ')')
#                                 | ('[' + ']')
#                                 | ('[' + constant_expression + ']')
#                                 | (direct_abstract_declarator + '[' + ']')
#                                 | (direct_abstract_declarator + '[' + constant_expression + ']')
#                                 | ('(' + ')')
#                                 | ('(' + parameter_type_list + ')')
#                                 | (direct_abstract_declarator + '(' + ')')
#                                 | (direct_abstract_declarator + '(' + parameter_type_list + ')')
#                                 )

# initializer << ( assignment_expression
#                 | ('{' + initializer_list + '}')
#                 | ('{' + initializer_list + ',' + '}')
#                 )
# 
# initializer_list << ( initializer
#                       | (initializer_list + ',' + initializer)
#                       )
# 
# statement << ( labeled_statement
#               | compound_statement
#               | expression_statement
#               | selection_statement
#               | iteration_statement
#               | jump_statement
#               )
# 
# labeled_statement << ( (IDENTIFIER + ':' + statement)
#                       | (CASE + constant_expression + ':' + statement)
#                       | (DEFAULT + ':' + statement)
#                       )
#  
# compound_statement << ( ('{' + '}')
#                        | ('{' + statement_list + '}')
#                        | ('{' + declaration_list + '}')
#                        | ('{' + declaration_list + statement_list + '}')
#                        )
#  
# declaration_list << ( declaration
#                       | (declaration_list + declaration)
#                       )
#  
# statement_list << ( statement
#                     | (statement_list +  statement)
#                     )

expression_statement << ( ';'
                         | (expression + ';')
                         )

# selection_statement << ( (IF + '(' + expression + ')' + statement)
#                         | (IF + '(' + expression + ')' + statement + ELSE + statement)
#                         | (SWITCH + '(' + expression + ')' + statement)
#                         )
# 
# iteration_statement << ( (WHILE + '(' + expression + ')' + statement)
#                         | (DO + statement + WHILE + '(' + expression + ')' + ';')
#                         | (FOR + '(' + expression_statement + expression_statement + ')' + statement)
#                         | (FOR + '(' + expression_statement + expression_statement + expression + ')' + statement)
#                         )
# 
# jump_statement << ( (GOTO + IDENTIFIER + ';')
#                    | (CONTINUE + ';')
#                    | (BREAK + ';')
#                    | (RETURN + ';')
#                    | (RETURN + expression + ';')
#                    )
# 
# translation_unit << ( external_declaration
#                       | (translation_unit + external_declaration)
#                       )
# 
# external_declaration << ( function_definition
#                          | declaration
#                          )
# 
# function_definition << ( (declaration_specifiers + declarator + declaration_list + compound_statement)
#                         | (declaration_specifiers + declarator + compound_statement)
#                         | (declarator + declaration_list + compound_statement)
#                         | (declarator + compound_statement)
#                         )

if __name__ == "__main__":
    str = "a = b"
#     print expression
    r = assignment_expression.parseString(str)
    print r