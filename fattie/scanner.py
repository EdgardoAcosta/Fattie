import ply.lex as lex
from core.indents import Indents

# Reserved words
reserved = {
    "main": "MAIN",
    "to": "TO",
    "_input": "INPUT",
    "_print": "PRINT",
    "_moveUp": "MOVEUP",
    "_moveDown": "MOVEDOWN",
    "_moveRight": "MOVERIGHT",
    "_moveLeft": "MOVELEFT",
    "_angle": "ANGLE",
    "_color": "COLOR",
    "_circle": "CIRCLE",
    "_square": "SQUARE",
    "clean": "CLEAN",
    "draw": "DRAW",
    "_startPosition": "STARTPOSITION",
    "_screenSizesX": "SCREENSIZESX",
    "_screenSizesY": "SCREENSIZESY",
    "_go": "GO",
    "_fibonacci": "FIBONACCI",
    "_factorial": "FACTORIAL",
    "_sleep": "SLEEP",

    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "Boolean": "BOOLEAN",
    "Int": "INT",
    "Float": "FLOAT",
    "Char": "CHAR",
    "fun": "FUN",
    "var": "VAR",
    "if": "IF",
    "else": "ELSE",
    "True": "TRUE",
    "False": "FALSE",
    "while": "WHILE",
    "for": "FOR",
    "equals": "EQUALS",
    "less": "LESS",
    "greater": "GREATER",
    "notequal": "NOTEQUAL",
    "return": "RETURN"

}

# Token declaration
tokens = [
             'ID', 'CTEI', 'CTEF', 'CTEC', 'EQUAL', 'SEMICOLON', 'COLON', 'COMMA', 'NEW_LINE', 'OPEN_BRACKET',
             'CLOSE_BRACKET', 'OPEN_PAREN', 'CLOSE_PAREN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'INDENT', 'DEDENT',
             'ARROW'
         ] + list(reserved.values())

t_EQUAL = r'\='
t_SEMICOLON = r'\;'
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


def t_ignore_SINGLE_COMMENT(t):
    r'\#.*\n'
    t.lexer.lineno += 1


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    # print(t.type + t.value)
    return t


# Define a float number
def t_CTEF(t):
    r'[0-9]*\.[0-9]+|[0-9]+'
    t.value = float(t.value)
    return t


# Define a variable int
def t_CTEI(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


# Todo: Check rexe for char
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
    raise SyntaxError(t)
    # print("Unexpected \"{}\" at line {}".format(first_word(t.value), t.lexer.lineno))


fattie_lexer = Indents(lex.lex())
