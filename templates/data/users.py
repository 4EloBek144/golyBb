import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import *


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)