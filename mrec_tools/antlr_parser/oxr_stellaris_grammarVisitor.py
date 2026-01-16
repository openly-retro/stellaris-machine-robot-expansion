# Generated from oxr_stellaris_grammar.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .oxr_stellaris_grammarParser import oxr_stellaris_grammarParser
else:
    from oxr_stellaris_grammarParser import oxr_stellaris_grammarParser

# This class defines a complete generic visitor for a parse tree produced by oxr_stellaris_grammarParser.

class oxr_stellaris_grammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by oxr_stellaris_grammarParser#content.
    def visitContent(self, ctx:oxr_stellaris_grammarParser.ContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#expr.
    def visitExpr(self, ctx:oxr_stellaris_grammarParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#assignment.
    def visitAssignment(self, ctx:oxr_stellaris_grammarParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#comparison.
    def visitComparison(self, ctx:oxr_stellaris_grammarParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#listitem.
    def visitListitem(self, ctx:oxr_stellaris_grammarParser.ListitemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#key.
    def visitKey(self, ctx:oxr_stellaris_grammarParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#val.
    def visitVal(self, ctx:oxr_stellaris_grammarParser.ValContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#attrib.
    def visitAttrib(self, ctx:oxr_stellaris_grammarParser.AttribContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#accessor.
    def visitAccessor(self, ctx:oxr_stellaris_grammarParser.AccessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#block.
    def visitBlock(self, ctx:oxr_stellaris_grammarParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#equation.
    def visitEquation(self, ctx:oxr_stellaris_grammarParser.EquationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#number.
    def visitNumber(self, ctx:oxr_stellaris_grammarParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by oxr_stellaris_grammarParser#name.
    def visitName(self, ctx:oxr_stellaris_grammarParser.NameContext):
        return self.visitChildren(ctx)



del oxr_stellaris_grammarParser