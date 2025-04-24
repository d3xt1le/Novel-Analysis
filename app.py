from flask import Flask, render_template, request, jsonify
from analysis import top_n_words_in_novel, novel_metadata, STOPWORDS_LANGUAGES

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    num_words = int(data.get('num_words', 10))

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    if not isinstance(num_words, int) or num_words <= 0:
        return jsonify({'error': 'num_words must be a positive integer'}), 400

    try:
        top_n_words = top_n_words_in_novel(url, num_words)
        metadata = novel_metadata(url)
        return jsonify({'results': top_n_words, 'metadata': metadata})

    except Exception as error:
        return jsonify({'error': str(error)}), 500


if __name__ == '__main__':
    app.run(debug=True)
