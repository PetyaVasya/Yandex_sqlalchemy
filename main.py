import os
from datetime import datetime

from flask import Flask, render_template, redirect
from flask_login import current_user, LoginManager
from forms import RegisterForm
from data import db_session, __all_models

Jobs = __all_models.jobs.Jobs
User = __all_models.users.User

UPLOAD_FOLDER = 'static/img'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.sqlite")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title="Колонизация марса")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def init_users():
    session = db_session.create_session()
    session.query(User).delete()
    session.add_all((
        User(
            surname="Scott",
            name="Ridley",
            age=21,
            position="captain",
            speciality="research engineer",
            address="module_1",
            email="scott_chief@mars.org"
        ),
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
