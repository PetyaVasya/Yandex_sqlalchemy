import datetime

from sqlalchemy import Column, Integer, String, DateTime, orm, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    chief = Column(Integer)
    members = orm.relation("User", back_populates='department')
    email = Column(String)
