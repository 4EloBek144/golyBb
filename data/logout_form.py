from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class LogoutForm(FlaskForm):
    submitYes = SubmitField('Выйти')
    submitNo = SubmitField('Остатся')