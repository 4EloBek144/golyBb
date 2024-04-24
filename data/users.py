import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import *
from flask import url_for


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def check_password(self, password):
        return password == self.hashed_password

    def get_id(self):
        return str(self.id)

    def getName(self):
        return self.__user['name'] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user['email'] if self.__user else "Без email"

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(
                        app.root_path + url_for('static', filename='../static/image/basic/NonePicture.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = self.__user['avatar']

        return img
