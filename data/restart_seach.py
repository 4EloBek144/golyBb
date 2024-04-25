from flask_wtf import FlaskForm
from wtforms import SubmitField



class RestartFowm(FlaskForm):
    submit = SubmitField('Сброс')