from flask import Flask, send_from_directory, Response, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'Created by YcK'


@app.route('/fruits')
def fruits():
    data = [
        {'name': 'apple', 'picked': 2, 'left': 1},
        {'name': 'orange', 'picked': 3, 'left': 0},
        {'name': 'banana', 'picked': 1, 'left': 2},
        {'name': 'quince', 'picked': 3, 'left': 0},
        {'name': 'pomegranate', 'picked': 3, 'left': 0}
    ]

    return jsonify(data)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'static/favicon.ico', mimetype='image/x-icon')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
