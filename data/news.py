import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'works'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    img = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tags = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    anonimus = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    img_stats = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    img_dop1 = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    img_dop2 = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)

    user = orm.relationship('User')
