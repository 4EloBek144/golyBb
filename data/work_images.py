import sqlalchemy
from .db_session import SqlAlchemyBase


class Work_images(SqlAlchemyBase):
    __tablename__ = 'work_images'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    img_stats = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    imgdop1 = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    imgdop2 = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
