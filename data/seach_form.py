from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField


class SeachForm(FlaskForm):
    text = StringField('Поиск')
    submit = SubmitField('Искать')