from sly import Parser
from lexer import MLexer

import AST

class Mparser(Parser):
    tokens = MLexer.tokens

    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', IFX),
        ('nonassoc', ELSE),
        ('nonassoc', EQ, NE),
        ('nonassoc', "<", ">", LE, GE),
        ('nonassoc', DOTADD, DOTSUB),
        ('nonassoc', '+', '-'),
        ('nonassoc', DOTMUL, DOTDIV),
        ('nonassoc', '*', '/'),
        ('right', UMINUS),
        ('left', UTRANSPOSE),
    )

    # general statement forms
    @_('statement block')
    def block(self, p):
        return AST.Block(p.lineno, p.statement, p.block)

    @_('statement')
    def block(self, p):
        return AST.Block(p.lineno, p.statement)

    @_('assign ";"', 'instruction ";"', 'named_block')
    def statement(self, p):
        return p[0]

    @_('"{" block "}"')
    def statement(self, p):
        return p.block

    # loops etc
    @_('while_loop', 'for_loop', 'if_stmt')
    def named_block(self, p):
        return p[0]

    @_('WHILE "(" expr ")" statement')
    def while_loop(self, p):
        return AST.WhileLoop(p.lineno, p.expr, p.statement)

    @_('FOR ID "=" range_expr statement')
    def for_loop(self, p):
        return AST.ForLoop(p.lineno, p.ID, p.range_expr, p.statement)

    @_('IF "(" expr ")" statement %prec IFX')
    def if_stmt(self, p):
        return AST.Conditional(p.lineno, p.expr, p.statement)

    @_('IF "(" expr ")" statement ELSE statement')
    def if_stmt(self, p):
        return AST.Conditional(p.lineno, p.expr, p[4], p[6])

    # instructions
    @_('BREAK')
    def instruction(self, p):
        return AST.BreakStatement(p.lineno)

    @_('CONTINUE')
    def instruction(self, p):
        return AST.ContinueStatement(p.lineno)

    @_('RETURN')
    def instruction(self, p):
        return AST.ReturnStatement(p.lineno)

    @_('PRINT varlist')
    def instruction(self, p):
        return AST.PrintStatement(p.lineno, p.varlist)

    @_('assignee assigner expr')
    def assign(self, p):
        return AST.Assignment(p.lineno, p.assigner, p.assignee, p.expr)

    @_('ID')
    def assignee(self, p):
        return p.ID

    @_('ID index_bracket')
    def assignee(self, p):
        return AST.Ref(p.lineno, p.ID, p.index_bracket)

    @_('"="', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN')
    def assigner(self, p):
        return p[0]

    # helper/misc constructs
    @_('expr ":" expr')
    def range_expr(self, p):
        return AST.Range(p.lineno, p[0], p[2])

    @_('"[" indexer "]"')
    def index_bracket(self, p):
        return AST.Index(p.lineno, p.indexer)

    @_('"[" indexer "," indexer "]"')
    def index_bracket(self, p):
        return AST.Index(p.lineno, p[1], p[3])

    @_('expr')
    def indexer(self, p):
        return p[0]

    @_('expr "," varlist')
    def varlist(self, p):
        return AST.Varlist(p.lineno, p.expr, p.varlist)

    @_('expr', 'expr ","')
    def varlist(self, p):
        return AST.Varlist(p.lineno, p.expr)

    # expressions
    @_('expr index_bracket')
    def expr(self, p):
        return AST.Ref(p.lineno, p.expr, p.index_bracket)

    @_('binary')
    def expr(self, p):
        return p[0]

    @_('binary relation_operator unary')
    def binary(self, p):
        return AST.RelExpr(p.lineno, p.relation_operator, p.binary, p.unary)

    @_('binary binary_operator unary')
    def binary(self, p):
        return AST.NumExpr(p.lineno, p.binary_operator, p.binary, p.unary)

    @_('binary matrix_operator unary')
    def binary(self, p):
        return AST.MatExpr(p.lineno, p.matrix_operator, p.binary, p.unary)

    @_('unary')
    def binary(self, p):
        return p.unary

    @_('"<"', '">"','LE', 'GE', 'NE', 'EQ')
    def relation_operator(self, p):
        return p[0]

    @_('"+"', '"-"', '"*"', '"/"')
    def binary_operator(self, p):
        return p[0]

    @_('DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV')
    def matrix_operator(self, p):
        return p[0]

    @_('"-" unary %prec UMINUS')
    def unary(self, p):
        return AST.UnExpr(p.lineno, '-', p.unary)

    @_('unary "\'" %prec UTRANSPOSE')
    def unary(self, p):
        return AST.UnExpr(p.lineno, '\'', p.unary)

    @_('primary')
    def unary(self, p):
        return p.primary

    @_('INTNUM')
    def primary(self, p):
        return AST.IntNum(p.lineno, int(p[0]))

    @_('FLOATNUM')
    def primary(self, p):
        return AST.FloatNum(p.lineno, float(p[0]))

    @_('ID')
    def primary(self, p):
        return AST.Variable(p.lineno, p.ID)

    @_('STRING')
    def primary(self, p):
        return AST.String(p.lineno, p[0])

    @_('"(" expr ")"')
    def primary(self, p):
        return p.expr

    @_('EYE "(" expr ")"', 'ZEROS "(" expr ")"', 'ONES "(" expr ")"')
    def primary(self, p):
        return AST.FunctionCall(p.lineno, p[0], p.expr)

    @_('"[" matrix "]"')
    def primary(self, p):
        return p.matrix

    # matrix initialization
    @_('varlist ";" matrix')
    def matrix(self, p):
        return AST.Vector(p.lineno, p.varlist, p.matrix)

    @_('varlist', 'varlist ";"')
    def matrix(self, p):
        return AST.Vector(p.lineno, p.varlist)
