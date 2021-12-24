from flask import Flask, render_template, request
import json

def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        f = json.load(file)
        return f

settings = read_json('settings.json')
candidates = read_json('candidates.json')

app = Flask(__name__)

@app.route('/')
def main():
    if settings['online']:
        return ('Приложение работает'
        '<p><a href="/list/">Кандидаты</a></p>'
        '<p><a href="/search/">Поиск</a></p>'
        '<p><a href="/skills/">Навыки</a></p>')
    else:
        return ('Приложение не работает'
        '<p><a href="/list/">Кандидаты</a></p>')


@app.route('/list/')
def candidates_list():


    return render_template('list.html', candidates=candidates)


@app.route('/candidate/<int:candidate_tp>/')
def candidate_tp(candidate_tp):
    for i in candidates:
        if i['id'] == candidate_tp:
            name = i['name']
            position = i['position']
            picture = i['picture']
            skills = i['skills']
            s = skills.split(', ')
            return render_template('candidate_tp.html', s=s, name=name, position=position, picture=picture, skills=skills)

@app.route("/search/")
def search():
    s = request.args.get('s')
    if s is None:
        return "Введите параметры для поиска"
    if settings['case-sensitive']:
        s = s.lower()
    else:
        s = s
    locl = []
    for i in candidates:
        if s in i['name']:
            locl.append(i['name'])


    if len(locl) <1:
        return "Кандидаты не найдены"

    return render_template('search.html', locl=locl, candidates=candidates)
@app.route('/skills/')
def skill():

    l = []
    for i in candidates:
        for z in i['skills'].split(', '):
            l.append(z)
    s = set(l)

    return render_template('skills.html', s=s,  candidates=candidates, skill=skill)

@app.route('/skills/<skill>/')
def skills(skill):
    limit = settings['limit']

    locl = []
    index = 0
    for i in candidates:

        if index == limit:
            break
        else:
            if skill in i['skills']:
                locl.append(i['name'])
                index += 1
    return render_template('skills_result.html', limit=limit, locl=locl, candidates=candidates, skills=skills)

app.run(debug=True, port=60002)