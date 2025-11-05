from sly import Lexer

class MLexer(Lexer):
    literals = {
        '+', '-', '*', '/', '=', '<', '>', '(', ')', '[', ']', '{', '}', ':', '\'', ',', ';'
    }
    tokens = {
        ID, INTNUM, FLOATNUM, STRING,
        DOTADD, DOTSUB, DOTMUL, DOTDIV,
        ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
        LE, GE, NE, EQ,
        IF, ELSE, FOR, WHILE,
        BREAK, CONTINUE, RETURN,
        EYE, ZEROS, ONES,
        PRINT
    }

    ignore_whitespace = r'[ \t]+'
    ignore_comment = r'#[^\n]*'
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    LE = r'<='
    GE = r'>='
    NE = r'!='
    EQ = r'=='

    ID = r'[_a-zA-Z][_\w0-9]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT

    @_(r'([0-9]+\.[0-9]*?|\.[0-9]+)([eE][-+]?[0-9]+)?', r'[0-9]+[eE][-+]?[0-9]+')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'[0-9]+')
    def INTNUM(self, t):
        self.lineno += len([t for t in t.value if t == '\n'])
        t.value = int(t.value)
        return t

    @_(r'"[^"]*"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        self.lineno += t.value.count('\n')
        return t

if __name__ == '__main__':
    import sys, pathlib
    src = pathlib.Path(sys.argv[1]).read_text()

    lexer = MLexer()
    for tok in lexer.tokenize(src):
        print(f"({tok.lineno}): {tok.type}({tok.value})")
