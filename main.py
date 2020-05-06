import os
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from flask_restful import Api
from sqlalchemy import or_

from data import db_session, __all_models
import forms
from data.department import Department
from data.jobs import Jobs
from data.users import User
from api.jobs_api import jobs_api
from api.users_api import users_api
from api_v2 import users_resource
from api_v2 import jobs_resource

UPLOAD_FOLDER = 'static/img'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.register_blueprint(jobs_api, url_prefix="/api")
app.register_blueprint(users_api, url_prefix="/api")
login_manager = LoginManager()
login_manager.init_app(app)

api_v2 = Api(app)
api_v2.add_resource(users_resource.UserListResource, '/api/v2/users')
api_v2.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
api_v2.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api_v2.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    return render_template('index.html', title="Колонизация марса", jobs=session.query(Jobs).all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            position=form.position.data,
            speciality=form.speciality.data,
            age=form.age.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect(url_for("login"))
    return render_template('form.html', title='Registration', form=form, form_title="Registration")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template('form.html', title='Authorisation', form=form,
                           form_title="Authorisation")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/addjob", methods=["GET", "POST"])
def add_job():
    form = forms.JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(job=form.job.data, is_finished=form.is_finished.data,
                   team_leader=form.team_leader.data, collaborators=form.collaborators.data,
                   start_date=datetime.now(), work_size=form.work_size.data)
        session.add(job)
        session.commit()
        return redirect(url_for("index"))
    return render_template('form.html', title='Edit job', form=form, form_title="Add a job")


@app.route("/adddepartment", methods=["GET", "POST"])
def add_department():
    form = forms.DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        department = Department(title=form.title.data, email=form.email.data,
                                chief_id=form.chief_id.data)
        department.members = form.members.data
        session.add(department)
        session.commit()
        return redirect(url_for("departments"))
    return render_template('form.html', title='Edit department', form=form,
                           form_title="Add a department")


@app.route("/jobs/<int:id>", methods=["GET", "POST"])
@login_required
def edit_job(id):
    form = forms.JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        job: Jobs = session.query(Jobs).filter(Jobs.id == id).filter(
            or_(current_user.id == 1, Jobs.leader == current_user)).first()
        if job:
            form.job.data = job.job
            form.collaborators.data = job.collaborators
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        job: Jobs = session.query(Jobs).filter(Jobs.id == id).filter(
            or_(current_user.id == 1, Jobs.leader == current_user)).first()
        if job:
            job.job = form.job.data
            job.collaborators = form.collaborators.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.is_finished = form.is_finished.data
            session.commit()
            return redirect(url_for("index"))
        else:
            abort(404)
    return render_template('form.html', title='Edit job', form=form, form_title="Edit job")


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    session = db_session.create_session()
    job: Jobs = session.query(Jobs).filter(Jobs.id == id).filter(
        or_(current_user.id == 1, Jobs.leader == current_user)).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect(url_for("index"))


@app.route("/departments")
def departments():
    session = db_session.create_session()
    dments = session.query(Department).all()
    return render_template("departments.html", title="List of departments", departments=dments)


@app.route("/departments/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
    form = forms.DepartmentForm()
    if request.method == "GET":
        session = db_session.create_session()
        department: Department = session.query(Department).filter(Department.id == id).filter(
            or_(current_user.id == 1, Department.chief == current_user)).first()
        if department:
            form.title.data = department.title
            form.members.data = ", ".join(map(lambda x: str(x.id), department.members))
            form.chief_id.data = department.chief_id
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        department: Department = session.query(Department).filter(Department.id == id).filter(
            or_(current_user.id == 1, Department.chief == current_user)).first()
        if department:
            department.title = form.title.data
            department.members.clear()
            for member in session.query(User).filter(
                    User.id.in_(map(int, form.members.data.split(", ")))).all():
                department.members.append(member)
            department.chief_id = form.chief_id.data
            department.work_size = form.email.data
            session.commit()
            return redirect(url_for("departments"))
        else:
            abort(404)
    return render_template('form.html', title='Edit department', form=form,
                           form_title="Edit department")


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    session = db_session.create_session()
    department: Department = session.query(Department).filter(Department.id == id).filter(
        or_(current_user.id == 1, Department.chief == current_user)).first()
    if department:
        session.delete(department)
        session.commit()
    else:
        abort(404)
    return redirect(url_for("departments"))


def init_users():
    session = db_session.create_session()
    session.query(User).delete()
    captain = User(
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        email="scott_chief@mars.org"
    )
    captain.set_password("1")
    session.add_all((
        captain,
        User(
            surname="Kirda",
            name="Vasya",
            age=11,
            position="member",
            speciality="cleaner",
            address="module_2",
            email="azaza@mars.org"
        ),
        User(
            surname="Patla",
            name="Masha",
            age=42,
            position="member",
            speciality="scientist",
            address="module_1",
            email="scientist@mars.org"
        ),
        User(
            surname="Vasha",
            name="Natasha",
            age=18,
            position="member",
            speciality="nothing",
            address="module_2",
            email="vasha_natasha_123@mail.ru"
        )
    ))
    session.commit()


def init_jobs():
    session = db_session.create_session()
    session.query(Jobs).delete()
    session.add(
        Jobs(
            team_leader=1,
            job="deployment of residential modules 1 and 2",
            work_size=15,
            collaborators="2, 3",
            start_date=datetime.now(),
            is_finished=False,
        )
    )
    session.commit()


if __name__ == "__main__":
    db_session.global_init("db/db.sqlite3")
    init_users()
    init_jobs()
    app.run()
