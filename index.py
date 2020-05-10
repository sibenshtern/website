import os

from flask import Flask
from flask import render_template, redirect

from data.loginform import LoginForm
from data.registerform import RegisterForm

from data import database_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/<string:title>')
@app.route('/index/<string:title>')
def index(title):
    session = database_session.create_session()
    jobs = session.query(Jobs).all()

    names = {
        user.id: ' '.join([user.surname, user.name])
        for user in session.query(User).all()
    }

    params = {"title": title, "jobs": jobs, "names": names}
    return render_template("jobs_list.html", **params)


@app.route('/')
@app.route('/index')
def index_too():
    return render_template("base.html", title="Mission MARS")


@app.route('/list_prof/<list_type>')
def show_professions_list(list_type):
    return render_template("professions_list.html", list_type=list_type,
                           title="Список профессий", professions=[
                            "Инженер - исследователь", "Пилот",
                            "Строитель", "Экзобиолог", "Врач",
                            "Инженер по терраформированию", "Климатолог",
                            "Специалист по радиационной защите",
                            "Астрогеолог", "Гляциолог",
                            "Инженер жизнеобеспечения", "Метеоролог",
                            "Оператор марсохода", "Киберинженер", "Штурман",
                            "Пилот дронов"
                            ])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return redirect('/success')

    return render_template("login.html", title="Авторизация", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        login = form['login'].data
        surname = form['surname'].data
        name = form['name'].data
        age = form['age'].data
        position = form['position'].data
        speciality = form['speciality'].data
        address = form['address'].data
        email = form['email'].data
        password = form['password'].data

        session = database_session.create_session()

        user = User()
        user.login = login
        user.surname = surname
        user.name = name
        user.age = age
        user.position = position
        user.speciality = speciality
        user.address = address
        user.email = email
        user.hashed_password = password
        session.add(user)

        session.commit()

        return redirect('/success')

    return render_template("register.html", title="Регистрация", form=form)


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


@app.route('/distribution')
def distribution_page():
    users = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур']
    return render_template('distribution.html', users=users)


def run_app():
    database_session.global_init('db/database.sqlite')
    port = os.environ.get('PORT', 5000)
    app.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
    run_app()
