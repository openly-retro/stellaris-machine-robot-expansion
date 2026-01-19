import sys
from antlr4 import *
from oxr_stellaris_grammarLexer import oxr_stellaris_grammarLexer as ExprLexer
from oxr_stellaris_grammarParser import oxr_stellaris_grammarParser as ExprParser
from oxr_stellaris_grammarVisitor import oxr_stellaris_grammarVisitor as VisitorInterp

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)

    tree = parser.expr()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        vinterp = VisitorInterp()
        vinterp.visit(tree)
    
    breakpoint()


    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main(sys.argv)