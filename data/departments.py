import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import *


class Department(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Department'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)

    user = orm.relationship('User')
