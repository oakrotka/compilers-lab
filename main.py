import sys
from lexer import MLexer
from parser import Mparser


if __name__ == '__main__':
    lexer = MLexer()
    parser = Mparser()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    parser.parse(lexer.tokenize(text))
