from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField, EmailField
from flask import *
from flask_login import *


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class Profred(FlaskForm):
    email = EmailField('Почта')
    login = StringField('Логин')
    password = PasswordField('Пароль')
    avatar = FileField('Аватар')
    submit = SubmitField('Подтвердить')
