import ply.yacc as yacc
import sys
from fattie.scanner import tokens


def p_program(p):
    '''program : variable function main
                | main'''
    p[0] = "COMPILED"


def p_main(p):
    '''main : MAIN ARROW
            | MAIN ARROW sub_main'''


def p_sub_main(p):
    '''sub_main : function_call block sub_main
                | empty'''


def p_function_call(p):
    '''function_call : ID EQUAL sub_function_call
                    | sub_function_call'''


def p_sub_function_call(p):
    '''sub_function_call : ID OPEN_PAREN sub_expression CLOSE_PAREN SEMICOLON'''


def p_sub_expression(p):
    '''sub_expression : expression
                    | expression COMMA sub_expression'''


def p_block(p):
    '''block : INDENT sub_block DEDENT'''


def p_sub_block(p):
    '''sub_block : statement
                | sub_block'''


if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if yacc.parse(data) == "COMPILED":
                print("Valid input")
        except EOFError:
            print(EOFError)
    else:
        print("No file to test found")
