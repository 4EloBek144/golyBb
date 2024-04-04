from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = TextAreaField('Логие', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password1 = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторный ввод пароля', validators=[DataRequired()])
    avatar = FileField('Аватар (не обязателен)')
    submit = SubmitField('Зарегистрироваться')
