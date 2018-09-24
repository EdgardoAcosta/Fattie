import sys
from fattie.parser import parser_fattie
from fattie.scanner import fattie_lexer


def _main():
    data = ''

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            with open(file, 'r') as src_file:
                data = src_file.read()
        except EOFError:
            print(EOFError)
    else:
        print("No file to test found")
        for line in sys.stdin:
            data = data + line

    _compile(data)


def _compile(data):
    par = parser_fattie.parse(data, lexer=fattie_lexer, debug=False, tracking=True)
    print(par)

if __name__ == '__main__':
    _main()
