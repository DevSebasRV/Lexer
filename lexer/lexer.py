
import ply.lex as lex

# Definiciones de tokens y lógica relacionada
tokens = (
    'IDENTIFIER',
    'ASSIGN',
    'SEMICOLON',
    'DATA_TYPE',
    'KEYWORD',
    'LOGICAL_OPERATOR',
    'INTEGER',
    'FLOAT',
    'STRING',
    'COLON',
    'OPEN_PAREN',
    'CLOSE_PAREN',
    'CONTENT',
    'ILLEGAL'
)

# Definición de patrones para los tokens
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LOGICAL_OPERATOR = r'<|>|==|<=|>=|!='
t_COLON = r':'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_CONTENT = r'C'
t_ignore = ' \t\n'

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-z][a-z]*'
    keywords = {'int', 'float', 'string', 'if', 'else', 'def', 'while'}
    if t.value.lower() in keywords:
        if t.value.lower() in {'int', 'float', 'string'}:
            t.type = 'DATA_TYPE'
        else:
            t.type = 'KEYWORD'
    else:
        t.type = 'IDENTIFIER'
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_error(t):
    t.type = 'ILLEGAL'
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

lexer = lex.lex()
