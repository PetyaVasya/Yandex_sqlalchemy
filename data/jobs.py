import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer)
    job = Column(String)
    work_size = Column(Integer)
    collaborators = Column(String)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_finished = Column(Boolean)