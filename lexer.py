from flask import Flask, request, jsonify
from flask_cors import CORS
import ply.lex as lex

app = Flask(__name__)
CORS(app) 

# Lista de tokens
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

def tokenize(input_text):
    lexer.input(input_text)
    token_list = []
    token_count = {'IDENTIFIER': 0, 'DATA_TYPE': 0, 'KEYWORD': 0, 'ASSIGN': 0, 'SEMICOLON': 0, 'LOGICAL_OPERATOR': 0,
                   'INTEGER': 0, 'FLOAT': 0, 'STRING': 0, 'COLON': 0, 'OPEN_PAREN': 0, 'CLOSE_PAREN': 0, 'CONTENT': 0, 'ILLEGAL': 0}
    lexeme_dict = {}

    while True:
        tok = lexer.token()
        if not tok:
            break
        token_type = tok.type
        lexeme = tok.value

        if token_type in token_count:
            token_count[token_type] += 1

        if token_type in lexeme_dict:
            lexeme_dict[token_type].append(lexeme)
        else:
            lexeme_dict[token_type] = [lexeme]

    result_list = []
    for token_type, count in token_count.items():
        if token_type in lexeme_dict:
            result_list.append((token_type, tuple(lexeme_dict[token_type]), count))

    return result_list

@app.route('/api/tokenize', methods=['POST'])
def tokenize_endpoint():
    try:
        data = request.get_json()
        input_text = data['inputText']

        tokens_info = tokenize(input_text)

        print(tokens_info)
        return jsonify(tokens_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)