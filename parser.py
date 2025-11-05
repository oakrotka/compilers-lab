from sly import Parser
from lexer import MLexer

class Mparser(Parser):
    tokens = MLexer.tokens

    # debugfile = 'parser.out'

    precedence = (
        ('nonassoc', IFX),
        ('nonassoc', ELSE),
        ('nonassoc', EQ, NE),
        ('nonassoc', "<", ">", LE, GE),
        ('left', DOTADD, DOTSUB),
        ('left', '+', '-'),
        ('left', DOTMUL, DOTDIV),
        ('left', '*', '/'),
        ('right', UMINUS),
        ('left', UTRANSPOSE),
    )

    # general statement forms
    @_('statement statement_list')
    def statement_list(self, p):
        return ('statement_list', p.statement, p.statement_list)

    @_('statement')
    def statement_list(self, p):
        return p.statement

    @_('assign ";"', 'instruction ";"', 'named_block')
    def statement(self, p):
        return p[0]

    @_('"{" statement_list "}"')
    def statement(self, p):
        return p.statement_list

    # loops etc
    @_('while_loop', 'for_loop', 'if_stmt')
    def named_block(self, p):
        return p[0]

    @_('WHILE "(" expr ")" statement')
    def while_loop(self, p):
        return (p.WHILE, p.expr, p.statement)

    @_('FOR ID "=" range_expr statement')
    def for_loop(self, p):
        return (p.FOR, p.ID, p.range_expr, p.statement)

    @_('IF "(" expr ")" statement %prec IFX')
    def if_stmt(self, p):
        return (p.IF, p.expr, p.statement, None)

    @_('IF "(" expr ")" statement ELSE statement')
    def if_stmt(self, p):
        return (p.IF, p.expr, p[4], p[6])

    # instructions
    @_('BREAK', 'CONTINUE')
    def instruction(self, p):
        return (p[0],)

    @_('PRINT varlist', 'RETURN varlist')
    def instruction(self, p):
        return (p[0], p.varlist)

    @_('assignee assigner expr')
    def assign(self, p):
        return (p.assigner, p.assignee, p.expr)

    @_('ID')
    def assignee(self, p):
        return p[0]

    @_('ID index_bracket')
    def assignee(self, p):
        return ('index', p.ID, p.index_bracket)

    @_('"="', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN')
    def assigner(self, p):
        return p[0]

    # helper/misc constructs
    @_('expr ":" expr')
    def range_expr(self, p):
        return (p[1], p[0], p[2])

    @_('"[" indexer "]"')
    def index_bracket(self, p):
        return ('index_array', p.indexer)

    @_('"[" indexer "," indexer "]"')
    def index_bracket(self, p):
        return ('index_matrix', p[1], p[3])

    @_('expr', 'range_expr')
    def indexer(self, p):
        return p[0]

    @_('expr "," varlist')
    def varlist(self, p):
        return ('varlist', p.expr, p.varlist)

    @_('expr', 'expr ","')
    def varlist(self, p):
        return p.expr

    # expressions
    @_('expr index_bracket')
    def expr(self, p):
        return ('index', p.expr, p.index_bracket)

    @_('binary')
    def expr(self, p):
        return p[0]

    @_('binary binary_operator unary')
    def binary(self, p):
        return (p[1], p[0], p[2])

    @_('unary')
    def binary(self, p):
        return p.unary

    @_('"+"', '"-"', '"*"', '"/"', '"<"', '">"',
       'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
       'LE', 'GE', 'NE', 'EQ')
    def binary_operator(self, p):
        return p[0]

    @_('"-" unary %prec UMINUS')
    def unary(self, p):
        return ('-', p.unary)

    @_('unary "\'" %prec UTRANSPOSE')
    def unary(self, p):
        return ('\'', p.unary)

    @_('primary')
    def unary(self, p):
        return p.primary

    @_('INTNUM', 'FLOATNUM')
    def primary(self, p):
        return ('num', p[0])

    @_('ID')
    def primary(self, p):
        return ('id', p.ID)

    @_('STRING')
    def primary(self, p):
        return ('string', p[0])

    @_('"(" expr ")"')
    def primary(self, p):
        return p.expr

    @_('EYE "(" expr ")"', 'ZEROS "(" expr ")"', 'ONES "(" expr ")"')
    def primary(self, p):
        return (p[0], p.expr)

    @_('"[" matrix "]"')
    def primary(self, p):
        return p.matrix

    # matrix initialization
    @_('varlist ";" matrix')
    def matrix(self, p):
        return ('matline', p.varlist, p.matrix)

    @_('varlist', 'varlist ";"')
    def matrix(self, p):
        return ('matline', p.varlist, None)
