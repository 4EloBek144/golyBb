from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class SeachForm(FlaskForm):
    text = TextAreaField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Искать')