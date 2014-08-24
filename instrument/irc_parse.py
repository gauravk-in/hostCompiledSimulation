from pyparsing import *

Ident = Word(alphas, alphanums+'_')
Num = Word(nums+'.')
String = quotedString

MUL_ASSIGN = "*"
DIV_ASSIGN = "/"
MOD_ASSIGN = "%"
ADD_ASSIGN = "+"
SUB_ASSIGN = "-"
LEFT_ASSIGN = "<<="
RIGHT_ASSIGN = ">>="
AND_ASSIGN = "&="
XOR_ASSIGN ="^="
OR_ASSIGN = "|="

IncOp = "++"
DecOp = "--"

LPAREN = Suppress("(")
RPAREN = Suppress(")")

UnaryOp = ( "&" |
            "*" |
            "+" |
            "-" |
            "~" |
            "!"
            )

Sizeof = "sizeof"

StructUnion = ( "struct" |
                "union" )

StructDeclList = Forward()
StructDeclList << ( (StructDecl) |
                    (StructDeclList + StructDecl) 
                    )

StructDecl = ( SpecifierQualifierList + StructDeclaratorList + ';' )

StructDeclaratorList = Forward()



StructUnionSpecifier = ( (StructUnion + Ident + '{' + StructDeclList + '}') |
                         (StructUnion + '{' + StructDeclList + '}') |
                         (StructUnion + Ident)
                         )

TypeSpecifier = ( "void" |
                  "char" |
                  "short" |
                  "int" |
                  "long" |
                  "float" |
                  "double" |
                  "signed" |
                  "unsigned" |
                  StructUnionSpecifier |
                  EnumSpecifier |
                  TypeName
                  )

SpecifierQualifierList = Forward()
SpecifierQualifierList << ( TypeSpecifier + SpecifierQualifierList |
                            TypeSpecifier |
                            TypeQualifier + SpecifierQualifierList |
                            TypeQualifier
                            )

TypeName = ( SpecifierQualifierList | 
             (SpecifierQualifierList + AbstractDeclarator)
             )

CastExpression = ( UnaryExpression |
                   (LPAREN + TypeName + RPAREN + CastExpression)
                   )

UnaryExpression = Forward()
UnaryExpression << (PostExpression |
                    (IncOp + UnaryExpression) |
                    (DecOp + UnaryExpression) |
                    (UnaryOp + CastExpresssion) |
                    (Sizeof + UnaryExpression) |
                    (Sizeof + LPAREN + TypeName + RParen)
                    )

AssignOperator = ( '='
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

AssignExpression = Forward()
AssignExpression << ( CondExpression | 
                      (UnaryExpression + AssignOperator + AssignExpression)
                      )

Expression = Forward()
Expression << ( AssignExpression |
                (Expression + ',' + AssignExpression) 
                )


PrimExpression = ( Ident |
                    Num |
                    String |
                    (LPAREN + Expression + RPAREN )
                    )
                   
PostExpression = Forward()
PostExpression << ( PrimExpression |
                    
                    )

if __name__ == "__main__":
    str_varDecl = "unsigned short int a;"
     