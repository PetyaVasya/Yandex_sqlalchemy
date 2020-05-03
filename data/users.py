import datetime

from sqlalchemy import Column, Integer, String, DateTime, orm, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    age = Column(Integer)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    about = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    modified_date = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    news = orm.relation("News", back_populates='user')
    department_id = Column(Integer, ForeignKey("department.id"))
    department = orm.relation('Department')
    jobs = orm.relation("Jobs", back_populates='leader')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @hybrid_property
    def fullname(self):
        return f"{self.surname} {self.name}"
