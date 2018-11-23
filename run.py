import sys
from fattie.scanner import fattie_lexer
from VirtualBigMachine import BigMachine
from fattie.parser import parser_fattie, chubby
from fattie import easter_egg


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
        sys.exit(1)

    _eat(data)


def _eat(data, easter=False):
    parser = parser_fattie.parse(data, lexer=fattie_lexer, debug=False, tracking=True)
    if parser == "COMPILED":
        print("Compiled successfully ")
        chubby.make_output()

        if easter: print(easter_egg)


        # big_machine = BigMachine("fat.txt")
        # big_machine.process_quadruples()

    else:
        pass


if __name__ == '__main__':
    _main()
