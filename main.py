import sys
from lexer import MLexer
from parser import Mparser
import TreePrinter

def print_parser(p):
    block = False

    if type(p) == tuple and p[0] == 'statement_list':
        print('statement list:')
        block = True

    while type(p) == tuple and p[0] == 'statement_list':
        print_parser(p[1])
        p = p[2]

    p.printTree()

def run(code, lexer, parser):
    tokens = list(lexer.tokenize(code))
    # for tok in tokens:
    #     print(f"({tok.lineno}): {tok.type}({tok.value})")

    result = parser.parse(t for t in tokens)
    print_parser(result)


if __name__ == '__main__':
    lexer = MLexer()
    parser = Mparser()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, "r") as file:
            code = file.read()
        run(code, lexer, parser)
    else:
        while True:
            try:
                run(input('M> '), lexer, parser)
            except EOFError:
                break
