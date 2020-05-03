from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, IntegerField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from main import User, db_session


class LoginForm(FlaskForm):
    email = StringField('Логин/Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

    def validate(self):
        if not super().validate():
            return False
        session = db_session.create_session()
        user = session.query(User).filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('Такого пользователя не существует')
            return False
        if not user.check_password(self.password.data):
            self.password.errors.append('Неверный пароль')
            return False
        return True


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])

    def validate(self):
        if not super().validate():
            return False
        session = db_session.create_session()
        user = session.query(User).filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Пользователь с такой почтой существует')
            return False
        if self.password.data != self.password_again.data:
            self.password_again.errors.append('Пароли не совпадают')
            return False
        return True


class JobForm(FlaskForm):
    team_leader = IntegerField("Team leader id", validators=[DataRequired()])
    job = StringField("Job title", validators=[DataRequired()])
    work_size = IntegerField("Work size", validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    is_finished = BooleanField("Is finished")
