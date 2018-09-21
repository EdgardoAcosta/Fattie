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
    pass


def p_sub_block(p):
    '''sub_block : sub_block statement
                | empty'''
    pass


def p_statement(p):
    '''statement : while
                 | for
                 | assignation
                 | if
                 | special_fun'''


def p_while(p):
    '''while : WHILE expression ARROW block'''


def p_for(p):
    '''for : FOR OPEN_PAREN expression TO expression CLOSE_PAREN ARROW block'''


def p_assignation(p):
    '''assignation :  ID array_assignation EQUAL expression SEMICOLON'''


def p_array_assignation(p):
    '''array_assignation : OPEN_BRACKET expression CLOSE_BRACKET
                         | empty '''


def p_if(p):
    '''if : IF expression ARROW block else'''


def p_else(p):
    '''else :  ELSE  block
            | empty'''


def p_expression(p):
    '''expression : exp comparation'''


def p_exp(p):
    '''exp : term operator'''


def p_comparation(p):
    '''comparation : EQUAL
                   | LESS
                   | GREATER
                   | NOTEQUAL'''


def p_term(p):
    '''term : factor term_factor '''


def p_operator(p):
    '''operator : sign exp '''


def p_factor(p):
    '''factor :  sing OPEN_PAREN expression CLOSE_PAREN
              | sing sing var_cte'''


def p_term_factor(p):
    '''term_factor : TIMES term
                   | DIVIDE term
                   | empty'''


def p_variable(p):
    '''variable : VAR type ID sub_variable SEMICOLON'''


def p_sub_variable(p):
    '''sub_variable : COMMA variable
                    | OPEN_BRACKET CTEI CLOSE_BRACKET
                    | empty'''


def p_function(p):
    '''function : FUN ID OPEN_PAREN  function_variables  CLOSE_PAREN function_return_type ARROW block'''


def p_function_variables(p):
    '''function_variables : type COLON ID sub_function_variables
                          | empty'''


def p_sub_function_variables(p):
    '''sub_function_variables : COMMA function_variables
                              | empty'''


def p_function_return_type(p):
    '''function_return_type : COLON type
                            | empty'''


##########################SPECIAL FUNCTIONS#######################################
def p_special_fun(p):
    '''special_fun : input
                   | print
                   | move_up
                   | move_down
                   | move_right
                   | move_left
                   | angle
                   | color
                   | circle
                   | square
                   | clean
                   | draw
                   | start_point
                   | screen_sizes_x
                   | screen_sizes_y
                   | go
                   | fibonacci
                   | factorial
                   | sleep'''


def p_input(p):  # TODO : Check the value inside input
    '''input : INPUT OPEN_PAREN  expression CLOSE_PAREN'''


def p_print(p):  # TODO : Check the value inside print
    '''print :  PRINT OPEN_PAREN expression CLOSE_PAREN'''


def p_move_up(p):
    '''move_up :  MOVEUP OPEN_PAREN expression CLOSE_PAREN'''


def p_move_down(p):
    '''move_down :  MOVEDOWN OPEN_PAREN expression CLOSE_PAREN'''


def p_move_right(p):
    '''move_right :  MOVERIGHT OPEN_PAREN expression CLOSE_PAREN'''


def p_move_left(p):
    '''move_left :  MOVELEFT OPEN_PAREN expression CLOSE_PAREN'''


def p_angle(p):
    '''angle :  ANGLE OPEN_PAREN expression CLOSE_PAREN'''


def p_color(p):
    '''color :  COLOR OPEN_PAREN expression CLOSE_PAREN'''


def p_circle(p):
    '''circle :  CIRCLE OPEN_PAREN expression sub_circle CLOSE_PAREN'''


def p_sub_circle(p):
    '''sub_circle : COMMA expression COMMA expression
                  | COMMA expression
                  | empty'''


def p_square(p):
    '''square :  SQUARE OPEN_PAREN expression COMMA expression sub_square CLOSE_PAREN'''


def p_sub_square(p):
    '''sub_square :  COMMA expression
                  | empty'''


def p_clean(p):
    '''clean :  CLEAN OPEN_PAREN expression CLOSE_PAREN'''


def p_draw(p):
    '''draw :  DRAW OPEN_PAREN expression CLOSE_PAREN'''


def p_start_point(p):
    '''start_point : STARTPOSITION OPEN_PAREN expression COMMA expression CLOSE_PAREN'''


def p_screen_sizes_x(p):
    '''screen_sizes_x :  SCREENSIZESX OPEN_PAREN CLOSE_PAREN'''


def p_screen_sizes_y(p):
    '''screen_sizes_y :  SCREENSIZESY OPEN_PAREN CLOSE_PAREN'''


def p_go(p):
    '''go :  GO OPEN_PAREN expression COMMA expression CLOSE_PAREN'''


def p_fibonacci(p):
    '''fibonacci : FIBONACCI OPEN_PAREN expression CLOSE_PAREN'''


def p_factorial(p):
    '''factorial : FACTORIAL OPEN_PAREN expression CLOSE_PAREN'''


def p_sleep(p):
    '''sleep :  SLEEP OPEN_PAREN expression CLOSE_PAREN'''


##########################STATIC#################################################
def p_sign(p):
    '''sign : PLUS
            | MINUS
            | empty'''


def p_var_cte(p):
    '''var_cte : ID sub_var_cte
               | CTEI
               | CTEF
               | CTES'''


def p_sub_var_cte(p):
    '''sub_var_cte : OPEN_PAREN sub_expression CLOSE_PAREN
                   | OPEN_BRACKET expression CLOSE_BRACKET
                   | empty'''


def p_type(p):
    '''type :  INT
            | BOOLEAN
            | FLOAT
            | CHAR'''


def p_empty(p):
    '''empty :'''
    pass


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
