from flask import Flask
from flask import render_template, redirect

from data.loginform import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "veryverysecretkeywhichyoucantbreak"


@app.route('/<string:title>')
@app.route('/index/<string:title>')
def index(title):
    return render_template("base.html", title=title)


@app.route('/')
@app.route('/index')
def index_too():
    return render_template("base.html", title="Mission MARS")


@app.route('/list_prof/<list_type>')
def show_professions_list(list_type):
    return render_template("professions_list.html", list_type=list_type,
                           title="Список профессий")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return redirect('/success')

    return render_template("login.html", title="Авторизация", form=form)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    params = {
        "title": "Анкета",
        "surname": "Wathy",
        "name": "Mark",
        "education": "выше среднего",
        "profession": "штурман марсохода",
        "sex": "male",
        "motivation": "Всегда мечтал застрять на Марсе!",
        "ready": "True"
    }
    return render_template("answer.html", **params)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)


