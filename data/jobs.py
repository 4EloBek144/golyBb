import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Works(SqlAlchemyBase):
    __tablename__ = 'works'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tegs = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relationship('User')
