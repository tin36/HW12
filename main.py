from flask import Flask, render_template
import json
def read_json(file_name):
    with open(file_name, 'r') as file:
        f = json.load(file)
        return f

settings = read_json('settings.json')
candidates = read_json('candidates.json')

app = Flask(__name__)

@app.route('/')
def main():
    if settings['online']:
        return ('Приложение работает'
        '<p><a href="/candidate/">Кандидаты</a></p>')
    else:
        return ('Приложение не работает'
        '<p><a href="/candidate/">Кандидаты</a></p>')

@app.route('/candidate/<id>')
def candidate(id):
    return render_template('index.html')
app.run(debug=True, port=60002)