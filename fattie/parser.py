import sys
import ply.yacc as yacc
from fattie.chubby import Chubby
from fattie.scanner import tokens
from fattie.belly.types import Types
from fattie.belly.builder import Builder
from fattie.belly.quadruple import Operator
from fattie.belly.exceptions import BigError
from fattie.belly.heavyfunction import HeavyFunction
from fattie.belly.fluffyvariable import FluffyVariable

from fattie import cube

chubby = Chubby()

function_param = []  # Function to store parameters of a function
more_variable = []  # Variable to store the ID of variables in same row
fn_builder = Builder(HeavyFunction)
var_builder = Builder(FluffyVariable)

precedence = (
    ('left', 'MINUS'),
    ('right', 'UMINUS')
)


# <editor-fold desc="Program">
def p_program(p):
    '''program : empty_spaces n_goto_main program_vars n_program_vars program_functions main '''
    p[0] = "COMPILED"
    chubby.print_all()
    # chubby.print_quadruple()


# Generate quadruple to jump to main
def p_n_goto_main(p):
    '''n_goto_main : '''
    chubby.jump_main()


def p_empty_spaces(p):
    ''' empty_spaces : empty_spaces NEW_LINE
                    | empty'''


def p_program_vars(p):
    '''program_vars : program_vars variable
                    | empty'''


def p_n_program_vars(p):
    '''n_program_vars : '''
    try:
        global more_variable
        for j in more_variable:
            chubby.add_global_variable(j)
        more_variable.clear()
    except BigError as e:
        e.print(p.lineno(-1))


def p_program_functions(p):
    '''program_functions : program_functions function
                         | empty'''


# </editor-fold>


# <editor-fold desc="Main">
def p_main(p):
    '''main : MAIN ARROW NEW_LINE n_main block'''
    chubby.end_main()


def p_n_main(p):
    '''n_main : '''
    try:
        chubby.jump_fill_main()
    except BigError as e:
        e.print(p.lineno(0))


def p_function_call(p):
    '''function_call : ID n_find_fn_name n_era OPEN_PAREN call_params CLOSE_PAREN'''

    try:
        chubby.gosub()
    except BigError as e:
        e.print(p.lineno(2))


def p_n_find_fn_name(p):
    '''n_find_fn_name : '''
    try:
        chubby.function_validate(p[-1])
    except BigError as e:
        e.print(p.lineno(-1))


def p_n_era(p):
    '''n_era : '''
    chubby.function_create_era()


def p_call_params(p):
    '''call_params : expression sub_expression
                   | empty'''
    try:
        chubby.function_validate_params((p[1] is not None))
    except BigError as e:
        e.print(p.lineno(-1))


def p_sub_expression(p):
    '''sub_expression : sub_expression COMMA params
                      | empty'''


def p_params(p):
    '''params : expression
              | empty'''

    try:
        chubby.function_validate_params((p[1] is not None))
    except BigError as e:
        e.print(p.lineno(-1))


# </editor-fold>


# <editor-fold desc="Block">
def p_block(p):
    '''block : INDENT block_body sub_block_body DEDENT'''
    pass


def p_block_body(p):
    '''block_body : block_body sub_block_body
                  | empty'''
    pass


def p_sub_block_body(p):
    '''sub_block_body : statement
                      | block_variable'''
    pass


def p_block_variable(p):
    '''block_variable : variable'''
    try:
        global more_variable
        for var in more_variable:
            chubby.add_local_variable(var)
        more_variable.clear()
    except BigError as e:
        e.print(p.lineno(1))


def p_statement(p):
    '''statement : while
                 | assignation NEW_LINE
                 | if
                 | special_fun NEW_LINE
                 | function_call NEW_LINE
                 | RETURN expression n_return NEW_LINE'''


def p_statement_err(p):
    '''statement : error'''
    print("Statement error - {}".format(p.lineno(0)))


def p_n_return(p):
    '''n_return : '''
    try:
        chubby.function_return()
    except BigError as e:
        e.print(p.lineno(0))


# </editor-fold>


# <editor-fold desc="Basic Functions">

def p_block_statement(p):
    '''block_statement : INDENT sub_block_statement statement DEDENT'''
    pass


def p_sub_block_statement(p):
    '''sub_block_statement : sub_block_statement statement
                           | empty '''
    pass


def p_while(p):
    '''while : WHILE expression n_while ARROW NEW_LINE block_statement'''
    chubby.fill_jumps_while()


def p_n_while(p):
    '''n_while : '''
    try:
        chubby.jump_false()
    except BigError as e:
        e.print(p.lineno(-1))


def p_assignation(p):
    '''assignation : ID n_var_cte_id variable_array EQUAL n_equal expression'''
    try:
        chubby.create_assignation()
    except BigError as e:
        e.print(p.lineno(1))


def p_n_equal(p):
    '''n_equal : '''
    chubby.add_operator(Operator.EQUAL)


def p_if(p):
    '''if : IF expression n_if ARROW NEW_LINE block_statement optional_else'''
    try:
        chubby.fill_jumps_if()
    except BigError as e:
        e.print(p.lineno(0))


def p_n_if(p):
    '''n_if : '''
    try:
        chubby.jump_false()
    except BigError as e:
        e.print(p.lineno(0))


def p_optional_else(p):
    '''optional_else : ELSE n_else NEW_LINE block_statement
                     | empty'''


def p_n_else(p):
    '''n_else : '''
    chubby.print_test("ELSE")


# </editor-fold>


# <editor-fold desc="Expression">
def p_expression(p):
    '''expression : exp comparison'''
    p[0] = p[1]


def p_exp(p):
    '''exp : term operator'''
    p[0] = p[1]


def p_comparison(p):
    '''comparison : EQUALS exp
                  | LESS exp
                  | GREATER exp
                  | NOTEQUAL exp
                  | empty'''
    if p[1] is not None:
        try:
            chubby.add_operator(chubby.text_to_operator(p[1]))
            chubby.check_operator_stack([Operator.LESS, Operator.GETRET, Operator.EQUALS, Operator.NOTEQUAL])
        except BigError as e:
            e.print(p.lineno(1))


def p_term(p):
    '''term : factor n_factor term_factor '''


# Number 5
def p_n_factor(p):
    '''n_factor : '''
    try:
        chubby.check_operator_stack([Operator.TIMES, Operator.DIVIDE])
    except BigError as e:
        e.print(p.lineno(0))


def p_operator(p):
    '''operator : sign n_operator exp
                | empty'''
    try:
        chubby.check_operator_stack([Operator.PLUS, Operator.MINUS])
    except BigError as e:
        e.print(p.lineno(1))


def p_n_operator(p):
    '''n_operator : '''

    if not p[-1] is None:
        try:
            chubby.add_operator(chubby.text_to_operator(p[-1]))
        except BigError as e:
            e.print(p.lineno(0))


def p_factor(p):
    '''factor : unary sub_factor '''


def p_unary(p):
    '''unary : MINUS %prec UMINUS
             | empty'''

    if p[1] is not None:
        chubby.add_operator(Operator.UMINUS)


def p_sub_factor(p):
    '''sub_factor : OPEN_PAREN expression CLOSE_PAREN
                  | var_cte'''


def p_term_factor(p):
    '''term_factor : TIMES term
                   | DIVIDE term
                   | empty'''

    if not p[1] is None:
        chubby.add_operator(chubby.text_to_operator(p[1]))


# </editor-fold>


# <editor-fold desc="Variables">
def p_variable(p):
    '''variable : VAR var_id NEW_LINE'''


def p_var_id(p):
    '''var_id : type save_type COLON  ID variable_array more_variables'''
    var_builder.put('id_var', p[4])
    more_variable.append(var_builder.build())
    var_builder.clear()


def p_save_type(p):
    '''save_type : '''
    try:
        value = chubby.text_to_type(p[-1])

        var_builder.put('type_var', value)
    except BigError as e:
        e.print(p.lineno(-1))
        # raise BigError("{} is not a valid type".format(p[-1]))


def p_more_variables(p):
    '''more_variables : more_variables COMMA ID variable_array
                      | empty'''

    if len(p) > 2:
        var_builder.put('id_var', p[3])
        more_variable.append(var_builder.build())


# Array and Matrix value assignation
def p_variable_array(p):
    '''variable_array : array
                      | matrix
                      | empty'''
    p[0] = p[1]


def p_array(p):
    '''array : OPEN_BRACKET expression CLOSE_BRACKET'''
    dimension = p[2]
    print("Array {} , dimension {}".format(p[-1], dimension))


def p_matrix(p):
    '''matrix : OPEN_BRACKET expression CLOSE_BRACKET OPEN_BRACKET expression CLOSE_BRACKET'''
    dimension = p[2]  # * p[5]
    print("Matrix {} , dimension {}".format(p[-1], dimension))


# </editor-fold>


# <editor-fold desc="Function">
def p_function(p):
    '''function : FUN function_id  OPEN_PAREN function_params CLOSE_PAREN function_return_type ARROW n_function NEW_LINE block'''

    fn_builder.clear()
    chubby.function_end()

    # Release var table for function (n_point =  7)
    # chubby.print_local_variables()
    chubby.clean_variables_from_function()
    chubby.reset_addr()


def p_n_function(p):
    '''n_function : '''

    try:
        global function_param

        fun = fn_builder.build()
        # Add function to function table
        chubby.add_function(fun)
        # Save params as a local variable of the function|
        try:
            global more_variable
            for var in more_variable:
                chubby.add_local_variable(var)
            more_variable.clear()
            function_param = []
        except BigError as e:
            e.print(p.lineno(1))

    except BigError as e:
        e.print(p.lineno(-1))


def p_function_id(p):
    '''function_id : ID'''
    p[0] = p[1]
    fn_builder.put('id_function', p[1])


def p_function_params(p):
    '''function_params : more_params param
                       | empty'''

    fn_builder.put('params', function_param)


def p_param(p):
    '''param : type save_type COLON ID '''
    var_builder.put('id_var', p[4])

    more_variable.append(var_builder.build())
    function_param.append(var_builder.build())
    var_builder.clear()


def p_more_params(p):
    '''more_params : more_params param COMMA
                   | empty'''
    pass


def p_function_return_type(p):
    '''function_return_type : COLON type
                            | empty'''

    value_return = p[2]
    if p[1] is None:
        value_return = None

    fn_builder.put('return_type', value_return)


# </editor-fold>


# <editor-fold desc="Special functions">
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
                   | go
                   | fibonacci
                   | factorial
                   | sleep'''


def p_input(p):
    '''input : INPUT OPEN_PAREN expression CLOSE_PAREN'''


def p_print(p):
    '''print : PRINT OPEN_PAREN  expression print_value  CLOSE_PAREN'''


def p_print_value(p):
    '''print_value : print_value COMMA expression
                   | empty'''


def p_move_up(p):
    '''move_up :  MOVEUP OPEN_PAREN  expression CLOSE_PAREN'''


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
    '''draw :  DRAW OPEN_PAREN expression'''


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


# </editor-fold>


# <editor-fold desc="Static Functions">
def p_sign(p):
    '''sign : PLUS
            | MINUS'''

    p[0] = p[1]


def p_var_cte(p):
    '''var_cte : ID n_var_cte_id sub_var_cte
               | function_call
               | constant
               | screen_sizes_x
               | screen_sizes_y'''
    # p[0] = p[1]


def p_constants(p):
    '''constant : ctei
                | ctef
                | ctec'''


def p_ctei(p):
    '''ctei : CTEI'''
    chubby.add_constants(p[1], Types.INT)


def p_ctef(p):
    '''ctef : CTEF'''
    chubby.add_constants(p[1], Types.FLOAT)


def p_ctec(p):
    '''ctec : CTEC'''
    chubby.add_constants(p[1], Types.FLOAT)


def p_n_var_cte_id(p):
    '''n_var_cte_id : '''
    try:
        var = chubby.find_variable(p[-1])
        chubby.add_operand(var)
    except BigError as e:
        e.print(p.lineno(-1))
        raise e


def p_sub_var_cte(p):
    '''sub_var_cte : OPEN_BRACKET expression CLOSE_BRACKET
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
    if not isinstance(p, BigError):
        print("Unexpected {} at line {}".format(p.value, p.lexer.lineno))


# </editor-fold>


parser_fattie = yacc.yacc()
