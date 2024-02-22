from flask import Flask, request, jsonify
from flask_cors import CORS
from tokenizer import tokenize

app = Flask(__name__)
CORS(app)

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
