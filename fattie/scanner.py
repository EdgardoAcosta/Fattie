import ply.lex as lex
from fattie.belly.indents import Indents

# Reserved words
reserved = {
    "main": "MAIN",
    "fun": "FUN",
    "var": "VAR",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",

    "input": "INPUT",
    "print": "PRINT",
    "moveUp": "MOVEUP",
    "moveDown": "MOVEDOWN",
    "moveRight": "MOVERIGHT",
    "moveLeft": "MOVELEFT",
    "color": "COLOR",
    "circle": "CIRCLE",
    "square": "SQUARE",
    "clean": "CLEAN",
    "draw": "DRAW",
    "startPosition": "STARTPOSITION",
    "screenSizes": "SCREENSIZES",
    "go": "GO",
    "fibonacci": "FIBONACCI",
    "factorial": "FACTORIAL",
    "sleep": "SLEEP",

    # "and": "AND",
    # "or": "OR",
    # "not": "NOT",
    "Boolean": "BOOLEAN",
    "Int": "INT",
    "Float": "FLOAT",
    "Char": "CHAR",
    "True": "TRUE",
    "False": "FALSE",

    "equals": "EQUALS",
    "less": "LESS",
    "greater": "GREATER",
    "notequal": "NOTEQUAL",
    "return": "RETURN"

}

# Token declaration
tokens = [
             'ID', 'CTEI', 'CTEF', 'CTEC', 'EQUAL', 'COLON', 'COMMA', 'NEW_LINE', 'OPEN_BRACKET',
             'CLOSE_BRACKET', 'OPEN_PAREN', 'CLOSE_PAREN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'INDENT', 'DEDENT',
             'ARROW'
         ] + list(reserved.values())

t_EQUAL = r'\='
t_COLON = r'\:'
t_COMMA = r'\,'
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_ARROW = r'\=\>'
t_ignore = ' '


def t_comment(t):
    r'\$.*'

    t.lexer.lineno += 1


def t_ignore_multi_comment(t):
    r'\$\*(.|\n)*\*\$'
    pass


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')

    if t.type == 'TRUE':
        t.value = True
    elif t.type == 'FALSE':
        t.value = False

    return t


# Define a float number
def t_CTEF(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


# Define a variable int
def t_CTEI(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


# Define a variable Chart
def t_CTEC(t):
    r'\".*\"'
    t.value = t.value[1:-1]
    return t


# Define a new line or multiple new lines
def t_NEW_LINE(t):
    r'\n\s*[\t ]*'
    t.lexer.lineno += t.value.count('\n')
    t.value = len(t.value) - 1 - t.value.rfind('\n')
    return t


def first_word(s):
    whites = [' ', '\t', '\n']
    low = 0
    for l in s:
        if l in whites:
            break
        low += 1

    return s[0:low]


def t_error(t):
    # raise SyntaxError(t)
    print("Unexpected \"{}\" at line {}".format(first_word(t.value), t.lexer.lineno))


fattie_lexer = Indents(lex.lex())
