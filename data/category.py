from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    jobs = orm.relation('Jobs')
