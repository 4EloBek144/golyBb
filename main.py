from flask import *
from flask_login import *
from data import db_session
from data.users import User
from data.news import News
from data.form_index import IndexTForm
from data.seach_form import SeachForm
from data.logout_form import LogoutForm
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.works_form import WorkLogin
import werkzeug

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


def load_work(name, img, text, tags):
    db_sess = db_session.create_session()
    work = News(
        name=name,
        user_id=current_user.id,
        img=img,
        text=text,
        tags=tags
    )
    db_sess.add(work)
    db_sess.commit()


@app.route('/seach', methods=['GET', 'POST'])
def perekidsearch():
    return redirect("/seach/1")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect("/")
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and werkzeug.security.check_password_hash(user.hashed_password, str(form.password.data)):
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
                user.hashed_password = werkzeug.security.generate_password_hash(form.password1.data)
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


@app.route('/profiel/<id>', methods=['GET', 'POST'])
def profiel(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(id=id).first()
    print(news.name)
    return render_template('profiel.html', news=user)


@app.route('/seach/<title>', methods=['GET', 'POST'])
def seach(title):
    form = SeachForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter_by(anonimus='False').all()
    kash = len(news) // 5
    if len(news) % 5 != 0:
        kash += 1
    newslist = []
    if len(news) - 5 * (int(title) - 1) > 4:
        vid = 5
        if len(news) // 5 == int(title) and len(news) % 5 == 0:
            next = False
        else:
            next = True
    elif len(news) - 5 * (int(title) - 1) > 0:
        vid = len(news) % 5
        next = False
    else:
        vid = '404'
        next = False
    if vid != '404':
        for i in range(vid):
            print(5 * (int(title) - 1) + i)
            newslist.append(news[5 * (int(title) - 1) + i])
        max_number_list = [i for i in range(1, kash + 1)]
        return render_template('seach.html', news=newslist, form=form, num_l=max_number_list,
                               m_num_l=int(title), next=next)
    else:
        return render_template('seach.html', news=newslist, form=form, num_l=[1],
                               message=f"Ошибка 404 (страницы {title} не существует по вашем критериям)",
                               m_num_l=int(title), next=next)


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


@app.route('/addwork', methods=['GET', 'POST'])
def addwork():
    form = WorkLogin()
    if form.validate_on_submit():
        load_work(form.name.data, form.img.data, form.text.data, form.tags.data)
        return redirect("/")
    return render_template('addwork.html', title='Создание поста', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
