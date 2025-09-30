// $antlr-format alignTrailingComments true, columnLimit 150, minEmptyLines 1, maxEmptyLinesToKeep 1, reflowComments false, useTab false
// $antlr-format allowShortRulesOnASingleLine false, allowShortBlocksOnASingleLine true, alignSemicolons hanging, alignColons hanging

grammar oxr_stellaris_grammar;

content
    : expr+ EOF
    ;

expr
    : assignment+
    ;

assignment
    : key ('=' | '>' | '<')+ val
    ;

key
    : name
    | attrib
    ;

val
    : name
    | attrib
    | block
    | STATICVAR
    | INLINESCRIPTREF
    | equation
    ;

attrib
    : name accessor (attrib | name)
    ;

accessor
    : '.'
    | '@'
    | ':'
    ;

block
    : '{' (expr* | name) '}'
    ;

equation
    : '@[' ( name | MATHSYMBOL )* ']' ;

name
    : IDENTIFIER
    | STRING
    | INTEGER
    ;

IDENTIFIER
    : IDENITIFIERHEAD IDENITIFIERBODY*
    ;

INTEGER
    : [+-]? INTEGERFRAG
    ;

MATHSYMBOL
    : ('+'|'-'|'*'|'('|')') ;

fragment INTEGERFRAG
    : [0-9]+
    ;

fragment IDENITIFIERHEAD
    : [a-zA-Z]
    ;

fragment IDENITIFIERBODY
    : IDENITIFIERHEAD
    | [0-9_]
    ;

STRING
    : '"' ~["\r\n]* '"'
    ;

STATICVAR
    : '@' [a-zA-Z_0-9]+
    ;

INLINESCRIPTREF
    : [a-zA-Z/_]+ ;

COMMENT
    : '#' ~[\r\n]* -> channel(HIDDEN)
    ;

SPACE
    : [ \t\f] -> channel(HIDDEN)
    ;

NL
    : [\r\n] -> channel(HIDDEN)
    ;
