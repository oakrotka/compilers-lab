import sys
from lexer import MLexer
from parser import Mparser
import tree_printer
from type_checker import TypeChecker
from interpreter import Interpreter

def print_parser(p):
    block = False

    if type(p) == tuple and p[0] == 'statement_list':
        print('statement list:')
        block = True

    while type(p) == tuple and p[0] == 'statement_list':
        print_parser(p[1])
        p = p[2]

    p.printTree()

def run(code, lexer, parser, checker):
    tokens = list(lexer.tokenize(code))
    for tok in tokens:
        # print(f"({tok.lineno}): {tok.type}({tok.value})")
        pass

    ast = parser.parse(t for t in tokens)
    # print_parser(ast)
    checker.visit(ast)
    if checker.correct:
        try:
            interpreter.visit(ast)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    lexer = MLexer()
    parser = Mparser()
    checker = TypeChecker()
    interpreter = Interpreter()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, "r") as file:
            code = file.read()
        run(code, lexer, parser, checker)
    else:
        while True:
            try:
                run(input('M> '), lexer, parser, checker)
            except EOFError:
                break
