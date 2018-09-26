import sys
import ply.yacc as yacc
from fattie.scanner import tokens
from fattie.belly.exceptions import BigError

from fattie.chubby import Chubby

chubby = Chubby()

function_param = []


def p_program(p):
    '''program : empty_spaces program_vars program_functions main '''
    p[0] = "COMPILED"


def p_empty_spaces(p):
    ''' empty_spaces : empty_spaces NEW_LINE
                    | empty'''


def p_program_vars(p):
    '''program_vars : program_vars variable
                    | empty'''


def p_program_functions(p):
    '''program_functions : program_functions function
                         | empty'''


def p_main(p):
    '''main : MAIN ARROW sub_main'''


def p_sub_main(p):
    '''sub_main : sub_main NEW_LINE function_call block
                | empty'''


def p_function_call(p):
    '''function_call : ID EQUAL sub_function_call
                    | sub_function_call
                    | empty'''


def p_sub_function_call(p):
    '''sub_function_call : ID OPEN_PAREN sub_expression CLOSE_PAREN SEMICOLON'''


def p_sub_expression(p):
    '''sub_expression : expression
                    | expression COMMA sub_expression'''


def p_block(p):
    '''block : INDENT block_body DEDENT'''
    pass


def p_block_body(p):
    '''block_body : sub_block_body block_body
                  | empty'''
    pass


def p_sub_block_body(p):
    '''sub_block_body : statement
                      | variable'''


def p_statement(p):
    '''statement : sub_statement'''
    pass


def p_sub_statement(p):
    '''sub_statement : while
                     | for
                     | assignation NEW_LINE
                     | if
                     | special_fun NEW_LINE
                     | RETURN expression NEW_LINE'''
    pass


def p_while(p):
    '''while : WHILE expression ARROW NEW_LINE block'''
    pass


def p_for(p):
    '''for : FOR OPEN_PAREN expression TO expression CLOSE_PAREN ARROW NEW_LINE block'''
    pass


def p_assignation(p):
    '''assignation :  ID array_assignation EQUAL expression SEMICOLON'''


def p_array_assignation(p):
    '''array_assignation : OPEN_BRACKET expression CLOSE_BRACKET
                         | empty '''


def p_if(p):
    '''if : IF expression ARROW NEW_LINE block optional_else'''


def p_optional_else(p):
    '''optional_else :  ELSE  NEW_LINE  block
            | empty'''


def p_expression(p):
    '''expression : exp comparison'''


def p_exp(p):
    '''exp : term operator'''


def p_comparison(p):
    '''comparison : EQUALS comparison_exp
                   | LESS comparison_exp
                   | GREATER comparison_exp
                   | NOTEQUAL comparison_exp
                   | empty'''


def p_comparison_exp(p):
    '''comparison_exp : exp'''


def p_term(p):
    '''term : factor term_factor '''


def p_operator(p):
    '''operator : sign term operator
                | empty'''


def p_factor(p):
    '''factor :  sign OPEN_PAREN expression CLOSE_PAREN
              | sign var_cte'''


def p_term_factor(p):
    '''term_factor : TIMES factor term_factor
                   | DIVIDE  factor term_factor
                   | empty'''


def p_variable(p):
    '''variable : VAR type COLON var_id NEW_LINE'''


def p_var_id(p):
    '''var_id : ID variable_array more_variables'''


def p_more_variables(p):
    '''more_variables : more_variables COMMA ID variable_array
                      | empty'''


def p_variable_array(p):
    '''variable_array : OPEN_BRACKET CTEI CLOSE_BRACKET
                       | empty'''


def p_function(p):
    '''function : FUN function_id OPEN_PAREN  function_params  CLOSE_PAREN function_return_type ARROW NEW_LINE block'''

    try:
        chubby.add_function(p[2], p[5], function_param)
        function_param.clear()
    except BigError as e:
        print(p.lineneo(1))


def p_function_id(p):
    '''function_id : ID'''
    p[0] = p[1]


def p_function_params(p):
    '''function_params : more_params param
                       | empty'''


def p_param(p):
    '''param : type COLON ID '''
    function_param.append({"id": p[3], "value": p[1]})


def p_more_params(p):
    '''more_params : more_params param COMMA
                   | empty'''
    pass


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
                   | sleep
                   | empty'''


def p_input(p):  # TODO : Check the value inside input
    '''input : INPUT OPEN_PAREN  expression CLOSE_PAREN'''


def p_print(p):
    '''print :  PRINT OPEN_PAREN print_value CLOSE_PAREN'''


def p_print_value(p):
    '''print_value : print_value expression
                    | CTEC '''


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
            | MINUS'''


def p_var_cte(p):
    '''var_cte : ID sub_var_cte
               | CTEI
               | CTEF
               | CTEC'''


def p_sub_var_cte(p):
    '''sub_var_cte : OPEN_PAREN sub_expression CLOSE_PAREN
                   | OPEN_BRACKET expression CLOSE_BRACKET
                   | empty'''


def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | BOOLEAN'''

    p[0] = p[1]


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    # if p is None:
    #     print("Unexpected EOF")
    # else:
    print("ERROR /////////// Type -> " + p.type + " Value -> " + str(p.value))
    print(p)
    # print("Unexpected {} at line {}".format(p.value, p.lexer.lineno))


parser_fattie = yacc.yacc()

#
# if __name__ == '__main__':
#
#     if len(sys.argv) > 1:
#         file = sys.argv[1]
#         try:
#             f = open(file, 'r')
#             data = f.read()
#             f.close()
#             if parser_fattie.parse(data) == "COMPILED":
#                 print("Valid input")
#         except EOFError:
#             print(EOFError)
#     else:
#         print("No file to test found")
