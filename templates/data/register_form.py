from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Логие', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password1 = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторный ввод пароля', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')