import datetime

from sqlalchemy import Column, Integer, String, DateTime, orm, ForeignKey, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase, create_session
from .users import User


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    chief_id = Column(Integer)
    members = orm.relation("User", back_populates='department')
    email = Column(String)

    @hybrid_property
    def chief(self):
        session = create_session()
        user = session.query(User).filter(User.id == self.chief_id).first()
        session.close()
        return user

    @chief.expression
    def chief(cls):
        return select([User]).where(User.id == cls.chief_id)

    @chief.setter
    def chief(self, user):
        self.chief_id = user.id
