import werkzeug.security
from flask import *
from flask_login import *
from data import db_session
from data.users import User
from data.works import Jobs
from data.login_form import LoginForm
from data.works_form import JobLogin
from data.reg_form import RegForm
import werkzeug


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/main.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def add_user(sr, nm, ag, pos, spec, add, mail, pas):
    db_sess = db_session.create_session()
    user = User(
        surname=sr,
        name=nm,
        age=ag,
        position=pos,
        speciality=spec,
        address=add,
        email=mail,
        hashed_password=pas
    )
    db_sess.add(user)
    db_sess.commit()


def load_job(lid_id, name, size, coll, is_f):
    db_sess = db_session.create_session()
    job = Jobs(
        team_leader=lid_id,
        job=name,
        work_size=size,
        collaborators=coll,
        is_finished=is_f
    )
    db_sess.add(job)
    db_sess.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and werkzeug.security.check_password_hash(user.hashed_password, str(form.password.data)):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = JobLogin()
    if form.validate_on_submit():
        load_job(form.user_id.data, form.job.data, form.size.data, form.collab.data, form.is_finished.data)
        return redirect("/")
    return render_template('addjob.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def adduser():
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user is None:
            add_user(form.sur.data, form.name.data, form.age.data, form.pos.data, form.spec.data, form.add.data, form.email.data, werkzeug.security.generate_password_hash(form.password.data))
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('register.html',
                               message="Почта уже занята",
                               form=form)
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')
def job_list():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs)
    return render_template("index.html", news=news)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
