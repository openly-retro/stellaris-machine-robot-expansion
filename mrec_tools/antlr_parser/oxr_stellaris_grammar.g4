// $antlr-format alignTrailingComments true, columnLimit 150, minEmptyLines 1, maxEmptyLinesToKeep 1, reflowComments false, useTab false
// $antlr-format allowShortRulesOnASingleLine false, allowShortBlocksOnASingleLine true, alignSemicolons hanging, alignColons hanging

grammar oxr_stellaris_grammar;

content
    : expr+ EOF
    ;

expr
    : assignment+
    | listitem
    | comparison+
    ;

assignment
    : key '=' val
    ;

comparison
    : key ('>'|'<='|'<'|'>=') val
    ;

listitem
    : key
    ;

key
    : name
    | attrib
    | INTEGER
    ;

val
    : name
    | number
    | FLOAT
    | BOOLEAN
    | block
    | INTEGER
    | STATICVAR
    | INLINESCRIPTREF
    | equation
    | attrib
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
    : '@[' ( name | MATHSYMBOL )* ']'
    ;

number
    : INTEGER
    | FLOAT
    ;

name
    : STRING
    | IDENTIFIER
    | EVENTTARGET
    ;


INTEGER
    : [+-]? DIGIT+
    ;

FLOAT
    : INTEGER+ '.' DIGIT*
    | '.' DIGIT+
    ;

BOOLEAN
    : ('yes'|'no')
    ;

MATHSYMBOL
    : ('+'|'-'|'*'|'('|')') ;

fragment DIGIT
    : [0-9]
    ;

IDENTIFIER
    : [a-zA-Z_]+
    ;

EVENTTARGET
    : IDENTIFIER ':' IDENTIFIER
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
