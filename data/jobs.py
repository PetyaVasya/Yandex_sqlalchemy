import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, orm
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase, create_session
from .users import User


class Jobs(SqlAlchemyBase):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey("user.id"))
    leader = orm.relation('User')
    job = Column(String)
    work_size = Column(Integer)
    collaborators = Column(String)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_finished = Column(Boolean)
