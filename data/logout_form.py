from flask_wtf import FlaskForm
from wtforms import SubmitField


class LogoutForm(FlaskForm):
    submitYes = SubmitField('Да')
    submitNo = SubmitField('Нет')
