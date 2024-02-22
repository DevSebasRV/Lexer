from lexer import lexer

def tokenize(input_text):
    lexer.input(input_text)
    lexeme_dict = {}

    while True:
        tok = lexer.token()
        if not tok:
            break
        token_type = tok.type
        lexeme = tok.value

        if token_type in lexeme_dict:
            lexeme_dict[token_type].append(lexeme)
        else:
            lexeme_dict[token_type] = [lexeme]

    result_list = []
    for token_type, lexemes in lexeme_dict.items():
        result_list.append((token_type, tuple(lexemes), len(lexemes)))

    return result_list

