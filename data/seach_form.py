from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class SeachForm(FlaskForm):
    text = StringField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Искать')