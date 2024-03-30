from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class SeachForm(FlaskForm):
    text = TextAreaField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Искать')