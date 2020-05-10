import os

from flask import Flask
from flask import render_template, redirect, abort

from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user

from data.loginform import LoginForm
from data.registerform import RegisterForm
from data.add_job_form import AddJobForm

from data import database_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    session = database_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def job_list():
    session = database_session.create_session()
    jobs = session.query(Jobs).all()

    names = {
        user.id: ' '.join([user.surname, user.name])
        for user in session.query(User).all()
    }

    params = {"title": "Mission MARS", "jobs": jobs, "names": names}
    return render_template("jobs_list.html", **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = database_session.create_session()
        user = session.query(User).filter(
            User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session = database_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            params = {
                "title": "Регистрация", "form": form,
                "message": "Такой пользователь уже есть"
            }
            return render_template('register.html', **params)

        user = User()
        user.surname = form['surname'].data
        user.name = form['name'].data
        user.age = form['age'].data
        user.position = form['position'].data
        user.speciality = form['speciality'].data
        user.address = form['address'].data
        user.email = form['email'].data
        user.set_password(form['password'].data)
        session.add(user)
        session.commit()
        return redirect('/login')

    params = {
        "title": "Регистрация", "form": form,
        "message": False
    }
    return render_template("register.html", **params)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()

    if form.validate_on_submit():
        session = database_session.create_session()

        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        session.add(job)
        session.commit()

        return redirect('/')

    params = {
        "title": "Добавить работу",
        "form": form
    }
    return render_template("add_job.html", **params)


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = AddJobForm()
    session = database_session.create_session()
    job: Jobs = session.query(Jobs).get(job_id)

    if job is None:
        abort(404)
    elif job.team_leader != current_user.id and not current_user.id == 1:
        abort(404)

    if form.validate_on_submit():
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        session.commit()
        return redirect('/')

    form.team_leader.data = job.team_leader
    form.job.data = job.job
    form.work_size.data = job.work_size
    form.collaborators.data = job.collaborators
    form.is_finished.data = job.is_finished

    params = {
        "title": "Редактировать задачу", "form": form
    }
    return render_template("add_job.html", **params)


@app.route('/del_job/<int:job_id>')
@login_required
def delete_job(job_id):
    session = database_session.create_session()
    job: Jobs = session.query(Jobs).get(job_id)

    if job is None:
        abort(404)
    elif job.team_leader != current_user.id and not current_user.id == 1:
        abort(404)
    else:
        session.delete(job)
        session.commit()

    return redirect('/')


def run_app():
    database_session.global_init('db/database.sqlite')
    port = os.environ.get('PORT', 5000)
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == '__main__':
    run_app()
