import os

import requests

from flask import Flask
from flask import render_template, redirect, abort, jsonify, url_for

from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user

from flask_restful import Api

from data.loginform import LoginForm
from data.registerform import RegisterForm
from data.add_job_form import AddJobForm
from data.add_department_form import AddDepartmentForm

from data import database_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department

from users_resource import UsersResource, UsersListResource
from jobs_api import blueprint as jobs_blueprint

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
UPLOAD_FOLDER = 'static/carousel-images'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(UsersListResource, '/api/v2/users')

app.register_blueprint(jobs_blueprint, url_prefix='/api')

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


@app.route('/departments')
def show_departments():
    session = database_session.create_session()
    departments = session.query(Department).all()

    names = {
        user.id: ' '.join([user.surname, user.name])
        for user in session.query(User).all()
    }

    params = {
        'title': "Департаменты", 'names': names, 'departments': departments
    }
    return render_template('departments.html', **params)


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


@app.route('/add_department', methods=['GET', 'POST'])
def add_department_page():
    form = AddDepartmentForm()

    if form.validate_on_submit():
        session = database_session.create_session()

        department = Department()
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data

        session.add(department)
        session.commit()

        return redirect('/departments')

    params = {
        "title": "Добавить департамент",
        "form": form
    }
    return render_template("add_department.html", **params)


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


@app.route('/edit_department/<int:department_id>', methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    form = AddDepartmentForm()
    session = database_session.create_session()
    department: Department = session.query(Department).get(department_id)

    if department is None:
        abort(404)
    elif department.chief != current_user.id and not current_user.id == 1:
        abort(404)

    if form.validate_on_submit():
        department.chief = form.chief.data
        department.title = form.title.data
        department.members = form.members.data
        department.email = form.email.data
        session.commit()
        return redirect('/departments')

    form.chief.data = department.chief
    form.title.data = department.title
    form.members.data = department.members
    form.email.data = department.email

    params = {
        "title": "Редактировать департамент", "form": form
    }
    return render_template("add_department.html", **params)


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


@app.route('/del_department/<int:department_id>')
@login_required
def delete_department(department_id):
    session = database_session.create_session()
    department: Department = session.query(Department).get(department_id)

    if department is None:
        abort(404)
    elif department.chief != current_user.id and not current_user.id == 1:
        abort(404)
    else:
        session.delete(department)
        session.commit()

    return redirect('/departments')


@app.route('/users_show/<int:user_id>')
def shows_user(user_id):
    def get_map_url(toponym, zoom):
        request_params = {
            'll': ','.join(toponym['Point']['pos'].split()),
            'l': 'sat',
            'z': zoom,
            'size': "450,450"
        }

        response = requests.get(
            "http://static-maps.yandex.ru/1.x/", params=request_params
        )
        if not response:
            raise Exception(f'Request failed. {response.url}')

        return response.url

    def get_toponym_by_geocoder(geocode: str) -> dict:
        request_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": geocode,
            "format": "json"
        }

        response = requests.get(
            "http://geocode-maps.yandex.ru/1.x/",
            request_params)
        if not response:
            raise Exception(
                f'Response failed. Status code: {response.status_code}'
            )
        else:
            json_response = response.json()
            toponym = json_response['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']
            return toponym

    user: dict = requests.get(url_for(f'/users_show/{user_id}')).json()

    if user is None:
        abort(404)

    map_url = get_map_url(get_toponym_by_geocoder(user['city_from']), 14)
    return render_template("users_show.html", user=user, map_url=map_url)


@app.errorhandler(404)
def error_handler_404(error):
    return jsonify({'message': 'Error', 'status_code': 404})


def run_app():
    database_session.global_init('db/database.sqlite')
    port = os.environ.get('PORT', 5000)
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == '__main__':
    run_app()
