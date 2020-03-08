from flask import Flask
from flask import render_template, redirect

from loginform import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "veryverysecretkeywhichyoucantbreak"


@app.route('/<string:title>')
@app.route('/index/<string:title>')
def index(title):
    return render_template("base.html", title=title)


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


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)


