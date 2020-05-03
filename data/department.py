import datetime

from sqlalchemy import Column, Integer, String, DateTime, orm, ForeignKey
from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    chief_id = Column(Integer)
    chief = orm.relation("User")
    members = orm.relation("User", back_populates='department')
    email = Column(String)
