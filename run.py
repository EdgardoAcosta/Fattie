import sys
from fattie.parser import parser_fattie, chubby
from fattie.scanner import fattie_lexer


def _main():
    data = ''
    # Check if file exist for test
    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            with open(file, 'r') as src_file:
                data = src_file.read()
        except EOFError:
            print(EOFError)
    else:
        print("No file to test found")
        print("-> ")
        for line in sys.stdin:
            data = data + line
    _eat(data)


def _eat(data):
    parser = parser_fattie.parse(data, lexer=fattie_lexer, debug=False, tracking=True)
    if parser == "COMPILED":
        print("Compiled successfully ")
        chubby.make_output()
    else:
        pass


if __name__ == '__main__':
    _main()
