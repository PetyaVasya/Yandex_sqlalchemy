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
            session.close()
            return False
        if not user.check_password(self.password.data):
            self.password.errors.append('Неверный пароль')
            session.close()
            return False
        session.close()
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
            session.close()
            return False
        if self.password.data != self.password_again.data:
            self.password_again.errors.append('Пароли не совпадают')
            session.close()
            return False
        session.close()
        return True


class JobForm(FlaskForm):
    team_leader = IntegerField("Team leader id", validators=[DataRequired()])
    job = StringField("Job title", validators=[DataRequired()])
    work_size = IntegerField("Work size", validators=[DataRequired()])
    collaborators = StringField("Collaborators")
    is_finished = BooleanField("Is finished")

    def validate(self):
        if not super().validate():
            return False
        session = db_session.create_session()
        if not session.query(User).filter(User.id == self.team_leader.data).first():
            self.team_leader.errors.append("Такого пользователя не существует")
            session.close()
            return False
        if not self.collaborators.data:
            session.close()
            return True
        for collaborator in self.collaborators.data.split(", "):
            try:
                if not session.query(User).filter(User.id == int(collaborator)).first():
                    self.collaborators.errors.append(
                        f"Пользователя с id {collaborator} не существует")
                    session.close()
                    return False
            except ValueError:
                self.collaborators.errors.append(f"Пользователя с id {collaborator} не существует")
                session.close()
                return False
        session.close()
        return True


class DepartmentForm(FlaskForm):
    chief_id = IntegerField("Chief id", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    members = StringField("Members ids")
    email = EmailField("Email", validators=[DataRequired()])

    def validate(self):
        if not super().validate():
            return False
        session = db_session.create_session()
        if not session.query(User).filter(User.id == self.chief_id.data).first():
            self.chief_id.errors.append("Такого пользователя не существует")
            session.close()
            return False
        if not self.members.data:
            session.close()
            return True
        for member in self.members.data.split(", "):
            try:
                if not session.query(User).filter(User.id == int(member)).first():
                    self.members.errors.append(
                        f"Пользователя с id {member} не существует")
                    session.close()
                    return False
            except ValueError:
                self.members.errors.append(f"Пользователя с id {member} не существует")
                session.close()
                return False
        session.close()
        return True
