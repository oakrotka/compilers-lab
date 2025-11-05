from sly import Parser
from lexer import MLexer

class Mparser(Parser):
    tokens = MLexer.tokens

    debugfile = 'parser.out'

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
        ('nonassoc', 'double_index'),
        ('left', 'single_index'),
        ('nonassoc', 'matrix_declaration'),
    )

    # general statement forms
    @_('statement statement_list')
    def statement_list(self, p):
        return ('statement_list', p.statement, p.statement_list)

    @_('statement')
    def statement_list(self, p):
        return p.statement

    @_('expr ";"', 'assign ";"', 'instruction ";"', 'named_block')
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

    @_('asignee assigner expr')
    def assign(self, p):
        return (p.assigner, p.asignee, p.expr)

    @_('ID', 'index')
    def asignee(self, p):
        return p[0]

    @_('"="', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN')
    def assigner(self, p):
        return p[0]

    # expressions
    @_('binary', 'index')
    def expr(self, p):
        return p.binary

    @_('binary "+" negation',    'binary "-" negation',
       'binary "*" negation',    'binary "/" negation',
       'binary "<" negation',    'binary ">" negation',
       'binary DOTADD negation', 'binary DOTSUB negation',
       'binary DOTMUL negation', 'binary DOTDIV negation',
       'binary LE negation',     'binary GE negation',
       'binary NE negation',     'binary EQ negation')
    def binary(self, p):
        return (p[1], p.binary, p.negation)

    @_('negation')
    def binary(self, p):
        return p.negation

    @_('"-" transposition %prec UMINUS')
    def negation(self, p):
        return ('-', p.transposition)

    @_('transposition')
    def negation(self, p):
        return p.transposition

    @_('transposition "\'"')  # more than one transposition at a time, why not
    def transposition(self, p):
        return ('\'', p.transposition)

    @_('primary')
    def transposition(self, p):
        return p.primary

    @_('ID', 'INTNUM', 'FLOATNUM', 'STRING')
    def primary(self, p):
        return (p[0],)

    @_('"(" expr ")"')
    def primary(self, p):
        return p.expr

    @_('EYE "(" expr ")"', 'ZEROS "(" expr ")"', 'ONES "(" expr ")"')
    def primary(self, p):
        return (p[0], p.expr)

    @_('"[" matrix "]" %prec matrix_declaration')
    def primary(self, p):
        return p.matrix

    @_('expr "[" indexer "," indexer "]" %prec double_index')
    def index(self, p):
        return ('index_matrix', p.expr, p[2], p[4])

    # other expressions
    @_('expr "[" indexer "]" %prec single_index')
    def index(self, p):
        return ('index_array', p.expr, p.indexer)

    @_('expr', 'range_expr')
    def indexer(self, p):
        return p[0]

    @_('expr ":" expr')
    def range_expr(self, p):
        return (p[1], p[0], p[2])

    # matrix initialization
    @_('varlist ";" matrix')
    def matrix(self, p):
        return ('matrix', p.varlist, p.matrix)

    @_('varlist', 'varlist ";"')
    def matrix(self, p):
        return ('varlist', p.varlist, None)

    @_('expr "," varlist')
    def varlist(self, p):
        return ('varlist', p.expr, p.varlist)

    @_('expr', 'expr ","')
    def varlist(self, p):
        return p.expr
