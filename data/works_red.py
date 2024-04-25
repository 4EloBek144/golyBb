from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField,  FileField, TextAreaField
from flask import *
from flask_login import *


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class WorkRed(FlaskForm):
    name = StringField('Название')
    img = FileField('Изображение персонажа')
    text = TextAreaField('Текст поста')
    tags = StringField('Теги (Пример "#dnd #robot #lvl3")')
    img_stat = FileField('Картинка статистики персонажа')
    img_dop1 = FileField('Дополнительная картинка 1')
    img_dop2 = FileField('Дополнительная картинка 2')
    submit = SubmitField('Создать')