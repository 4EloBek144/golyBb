import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'works'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tags = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())

    user = orm.relationship('User')
