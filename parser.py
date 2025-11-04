from sly import Parser
from lexer import MLexer


class Mparser(Parser):
    tokens = MLexer.tokens

    debugfile = 'parser.out'

    precedence = (
    # to fill ...
        ("left", '+', '-'),
    # to fill ...
    )

    v =                                                                                            0
    @_('instructions_opt')
    def program(p):
        pass

    @_('instructions')
    def instructions_opt(p):
        pass

    @_('')
    def instructions_opt(p):
        pass

    @_('instructions instruction')
    def instructions(p):
        pass

    @_('instruction')
    def instructions(p):
        pass


    # to finish the grammar
    # ....
