from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, TextAreaField, StringField, FileField
from wtforms.validators import DataRequired
from flask import *
from flask_login import *


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class WorkLogin(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    img = FileField('Изображение', validators=[DataRequired()])
    text = TextAreaField('Текст поста', validators=[DataRequired()])
    tags = StringField('Теги', validators=[DataRequired()])
    submit = SubmitField('Создать')
