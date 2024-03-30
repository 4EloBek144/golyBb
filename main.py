from flask import *
from flask_wtf import *
from flask_login import *
from wtforms import EmailField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.news import News
from data import news_api
from data.form_index import IndexTForm
from data.seach_form import SeachForm
from data.logout_form import LogoutForm
from data.login_form import LoginForm
from data.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/main.db")
number_list = 1
max_number_list = [1, 2, 3, 4, 5, 6, 7]


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect("/")
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.login.data).first():
            return render_template('register.html',
                                   message="Данный логин уже занят.",
                                   form=form)
        elif db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   message="Данная почта уже занята.",
                                   form=form)
        for i in form.password1.data:
            if i in '#@$%^&*?:;№/\\|,.`~(){}[]':
                return render_template('register.html',
                                       message="""Пароль не должен содержать
                                ( # @ $ % ^ & * ? : ; № / \\ | , . ` ~ ( ) [ ] { } )""",
                                       form=form)
        else:
            if form.password1.data != form.password2.data:
                return render_template('register.html',
                                       message="Пароли не совпадают.",
                                       form=form)
            else:
                user = User()
                user.name = form.login.data
                user.email = form.email.data
                user.works = None
                user.hashed_password = form.password1.data
                db_sess.add(user)
                db_sess.commit()
                login_user(user, remember=True)
                return redirect("/")

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/main', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def main():
    formindex = IndexTForm()
    return render_template('main.html', formindex=formindex)


@app.route('/profiel', methods=['GET', 'POST'])
def profiel():
    db_sess = db_session.create_session()
    news = db_sess.query(News).first()
    return render_template('profiel.html', news=news)

@app.route('/seach', methods=['GET', 'POST'])
def seach():
    form = SeachForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    theposts = None
    max_number_list = [1, 2, 3, 4, 5, 6, 7]
    return render_template('seach.html', news=news, form=form, theposts=theposts, num_l=max_number_list,
                           m_num_l=number_list)


@app.route('/postslist', methods=['GET', 'POST'])
def seacht():
    return render_template('seach.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutForm()
    if request.method == 'POST':
        if 'submitYes' in request.form.keys():
            logout_user()
            return redirect("/")
        if 'submitNo' in request.form.keys():
            return redirect("/")
    return render_template('logout.html', title='Выход из аккаунта', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
