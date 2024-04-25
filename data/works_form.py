from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField
from wtforms.validators import DataRequired
from flask import *
from flask_login import *


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class WorkLogin(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    img = FileField('Изображение персонажа', validators=[DataRequired()])
    text = StringField('Текст поста', validators=[DataRequired()])
    tags = StringField('Теги (Пример "#dnd #robot #3lvl")', validators=[DataRequired()])
    img_stat = FileField('Картинка статистики персонажа', validators=[DataRequired()])
    img_dop1 = FileField('Дополнительная картинка 1', validators=[DataRequired()])
    img_dop2 = FileField('Дополнительная картинка 2', validators=[DataRequired()])
    submit = SubmitField('Создать')
