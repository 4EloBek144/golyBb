import sqlite3

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
from data.works_red import WorkRed
from data.profile_red import Profred
import werkzeug

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/main.db")

db_sess = db_session.create_session()
news = db_sess.query(News).filter(News.anonimus != 'True').all()
db_sess.close()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def load_work(name, img, text, tags, img_stat, img_dop1, img_dop2):
    db_sess = db_session.create_session()
    work = News(
        name=name,
        user_id=current_user.id,
        img=img,
        text=text,
        tags=tags,
        img_stat=img_stat,
        img_dop1=img_dop1,
        img_dop2=img_dop2
    )
    db_sess.add(work)
    db_sess.commit()


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
        for i in form.password1.data:
            if i in '#@$%^&*?:;№/\\|,.`~(){}[]':
                return render_template('register.html',
                                       message="""Пароль не должен содержать
                                ( # @ $ % ^ & * ? : ; № / \\ | , . ` ~ ( ) [ ] { } )""",
                                       form=form)
        if db_sess.query(User).filter(User.name == form.login.data).first():
            return render_template('register.html',
                                   message="Данный логин уже занят.",
                                   form=form)
        elif db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   message="Данная почта уже занята.",
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
                user.image = None
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


@app.route('/profile/')
def check():
    return redirect(f'/profile/{current_user.id}')


@app.route('/profile/<id>', methods=['GET', 'POST'])
def profiel(id):
    admin = False
    if current_user.is_authenticated and int(id) == int(current_user.id):
        admin = True
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    news = db_sess.query(News).filter(News.user_id == id, News.anonimus != 'True').all()
    db_sess.close()
    n1 = []
    for i in range(len(news)):
        if str(news[i].user_id) == str(id):
            n1.append(news[i])
    return render_template('profiel_normal.html', news=n1, admin=admin, user=user)


@app.route('/seach/<title>', methods=['GET', 'POST'])
def seach(title):
    global news
    forme = SeachForm()
    db_sess = db_session.create_session()
    if request.method == 'POST' and 'submit' in request.form.keys():
        text = forme.text.data
        if len(text) > 0 and text.count(' ') != len(text):
            news = []
            tags = []
            name = []
            for i in text.split():
                if i[0] == '#':
                    tags.append(i)
                else:
                    name.append(i)
            if name:
                for i in name:
                    kash = db_sess.query(News).filter(
                        News.name.like(f'%{i}%'),
                        News.anonimus != 'True',
                        News.tags.like("%" + "%".join(tags) + "%")).all()
                for i in kash:
                    if i not in news:
                        news.append(i)
            elif text == '' or text == ' ':
                db_sess = db_session.create_session()
                news = db_sess.query(News).filter(News.anonimus != 'True').all()
                db_sess.close()


            elif tags:
                news = db_sess.query(News).filter(
                    News.anonimus != 'True',
                    News.tags.like("%" + "%".join(tags) + "%")).all()

        else:
            db_sess = db_session.create_session()
            news = db_sess.query(News).filter(News.anonimus != 'True').all()
            db_sess.close()

        flash('error', 'error')

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
            newslist.append(news[5 * (int(title) - 1) + i])
        max_number_list = [i for i in range(1, kash + 1)]
        return render_template('seach.html', news=newslist, form=forme, num_l=max_number_list,
                               m_num_l=int(title), next=next)
    else:
        return render_template('seach.html', news=newslist, form=forme, num_l=[1],
                               message=f"Ошибка 404 (страницы {title} не существует по вашем критериям)",
                               m_num_l=int(title), next=next)


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            db_sess = db_session.create_session()
            ext = file.filename.rsplit('.', 1)[1]
            if file and (ext == "png" or ext == "PNG" or ext == 'jpg'):
                try:
                    binary = sqlite3.Binary(file.read())
                    kash = db_sess.query(User).filter(User.id == current_user.id).first()
                    kash.image = binary
                    db_sess.commit()
                    db_sess.close()
                except:
                    flash('error', 'error')
            else:
                flash("Ошибка обновления аватара", "error")

    return redirect(url_for(f'profiel', id=current_user.id))


@app.route('/project/<id>', methods=['GET', 'POST'])
def project(id):
    db_sess = db_session.create_session()
    post = db_sess.query(News).filter(News.id == id).first()
    st, d1, d2 = False, False, False
    if post.img_dop1:
        d1 = True

    if post.img_dop2:
        d2 = True

    if post.img_stats:
        st = True
    names = db_sess.query(User.name).filter(User.id == post.user_id).first()
    db_sess.close()
    return render_template('project.html', post=post, st=st, d1=d1, d2=d2, name=names[0])


@app.route('/helper')
def helper():
    return render_template('helpers.html')


@app.route('/useravatar/<id>', methods=['GET', 'POST'])
def useravatar(id):
    db_sess = db_session.create_session()
    kash = db_sess.query(User).filter(User.id == id).first()
    img = None
    if not kash.image:
        try:
            with app.open_resource(
                    app.root_path + url_for('static', filename='../static/image/basic/NonePicture.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            print("Не найден аватар по умолчанию: " + str(e))
    else:
        img = kash.image
    copy = make_response(img)
    copy.headers['Content-Type'] = 'image/png'
    db_sess.close()
    return copy


@app.route('/workavatar/<id>', methods=['GET', 'POST'])
def workavatar(id):
    db_sess = db_session.create_session()
    kash = db_sess.query(News).filter(News.id == id).first()
    img = None
    if not kash.img:
        try:
            with app.open_resource(
                    app.root_path + url_for('static', filename='../static/image/basic/NonePicture.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            print("Не найден аватар по умолчанию: " + str(e))
    else:
        img = kash.img
    copy = make_response(img)
    copy.headers['Content-Type'] = 'image/png'
    db_sess.close()
    return copy


@app.route('/workstats/<id>', methods=['GET', 'POST'])
def workstats(id):
    db_sess = db_session.create_session()
    kash = db_sess.query(News).filter(News.id == id).first()
    img = None
    if not kash.img_stats:
        try:
            with app.open_resource(
                    app.root_path + url_for('static', filename='../static/image/basic/NonePicture.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            print("Не найден аватар по умолчанию: " + str(e))
    else:
        img = kash.img_stats
    copy = make_response(img)
    copy.headers['Content-Type'] = 'image/png'
    db_sess.close()
    return copy


@app.route('/workdop1/<id>', methods=['GET', 'POST'])
def workdop1(id):
    db_sess = db_session.create_session()
    kash = db_sess.query(News).filter(News.id == id).first()
    img = None
    if not kash.img_dop1:
        try:
            with app.open_resource(
                    app.root_path + url_for('static', filename='../static/image/basic/NonePicture.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            print("Не найден аватар по умолчанию: " + str(e))
    else:
        img = kash.img_dop1
    copy = make_response(img)
    copy.headers['Content-Type'] = 'image/png'
    db_sess.close()
    return copy


@app.route('/workdop2/<id>', methods=['GET', 'POST'])
def workdop2(id):
    db_sess = db_session.create_session()
    kash = db_sess.query(News).filter(News.id == id).first()
    img = None
    if not kash.img_dop2:
        try:
            with app.open_resource(
                    app.root_path + url_for('static', filename='../static/image/basic/NonePicture.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            ("Не найден аватар по умолчанию: " + str(e))
    else:
        img = kash.img_dop2
    copy = make_response(img)
    copy.headers['Content-Type'] = 'image/png'
    db_sess.close()
    return copy


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutForm()
    if current_user.is_authenticated:
        if request.method == 'POST':
            if 'submitYes' in request.form.keys():
                logout_user()

                return redirect("/")
            if 'submitNo' in request.form.keys():
                return redirect("/")
    else:
        return redirect("/")
    return render_template('logout.html', title='Выход из аккаунта', form=form)


@app.route('/addwork', methods=['GET', 'POST'])
@login_required
def addwork():
    global news
    form = WorkLogin()
    if request.method == 'POST' and 'submit' in request.form.keys():
        if 'img' not in request.files:
            flash('Не могу прочитать файл персонажа')

        if 'img_stat' not in request.files:
            flash('Не могу прочитать файл персонажа')
        if 'img_dop1' not in request.files:
            flash('Не могу прочитать файл персонажа')
        if 'img_dop2' not in request.files:
            flash('Не могу прочитать файл персонажа')
        img = request.files['img']
        img_stat = request.files['img_stat']
        img_dop1 = request.files['img_dop1']
        img_dop2 = request.files['img_dop2']

        if img.filename == '':
            img = None
        else:
            img = sqlite3.Binary(img.read())

        if img_stat.filename == '':
            img_stat = None
        else:
            img_stat = sqlite3.Binary(img_stat.read())

        if img_dop1.filename == '':
            img_dop1 = None
        else:
            img_dop1 = sqlite3.Binary(img_dop1.read())

        if img_dop2.filename == '':
            img_dop2 = None
        else:
            img_dop2 = sqlite3.Binary(img_dop2.read())

        db_sess = db_session.create_session()
        work = News(
            name=form.name.data,
            user_id=current_user.id,
            img=img,
            text=form.text.data,
            tags=form.tags.data,
            img_stats=img_stat,
            img_dop1=img_dop1,
            img_dop2=img_dop2,
            anonimus=False
        )
        db_sess.add(work)
        db_sess.commit()

        db_sess = db_session.create_session()
        news = db_sess.query(News).filter_by(anonimus='False').all()
        db_sess.close()

        return redirect("/")

    return render_template('addwork.html', title='Создание поста', form=form)


@app.route('/project_redact/<id>', methods=['GET', 'POST'])
@login_required
def project_redact(id):
    form = WorkRed()
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(id)
    if request.method == 'POST' and 'submit' in request.form.keys():
        if 'img' not in request.files:
            flash('Не могу прочитать файл персонажа')

        if 'img_stat' not in request.files:
            flash('Не могу прочитать файл персонажа')
        if 'img_dop1' not in request.files:
            flash('Не могу прочитать файл персонажа')
        if 'img_dop2' not in request.files:
            flash('Не могу прочитать файл персонажа')
        img = request.files['img']
        img_stat = request.files['img_stat']
        img_dop1 = request.files['img_dop1']
        img_dop2 = request.files['img_dop2']

        if img.filename == '':
            img = None
        else:
            img = sqlite3.Binary(img.read())

        if img_stat.filename == '':
            img_stat = None
        else:
            img_stat = sqlite3.Binary(img_stat.read())

        if img_dop1.filename == '':
            img_dop1 = None
        else:
            img_dop1 = sqlite3.Binary(img_dop1.read())

        if img_dop2.filename == '':
            img_dop2 = None
        else:
            img_dop2 = sqlite3.Binary(img_dop2.read())

        old_stat = [news.name, news.img, news.text, news.tags, news.img_stats, news.img_dop1, news.img_dop2]
        new_stat = [form.name.data, img, form.text.data, form.tags.data, img_stat, img_dop1, img_dop2]
        conf_stat = []
        try:
            db_sess.delete(news)
            for i in range(7):
                if new_stat[i] == '' or new_stat[i] is None:
                    conf_stat.append(old_stat[i])
                else:
                    conf_stat.append(new_stat[i])

            work = News(
                id=int(news.id),
                name=conf_stat[0],
                user_id=int(news.user_id),
                img=conf_stat[1],
                text=conf_stat[2],
                tags=conf_stat[3],
                img_stats=conf_stat[4],
                img_dop1=conf_stat[5],
                img_dop2=conf_stat[6],
                anonimus=False
            )
            db_sess.add(work)
            db_sess.commit()
            db_sess.close()
        except Exception:
            return render_template('addwork.html', title='Редактирование проекта', form=form,
                                   message='Неверный формат ввода')

        return redirect(f"/profile/{news.user_id}")

    return render_template('addwork.html', title='Редактирование проекта', form=form)


@app.route('/project_delete/<id>', methods=['GET', 'POST'])
@login_required
def project_delete(id):
    global news
    form = LogoutForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id).first()
    if not news:
        return jsonify({'error': 'Not found'})
    if current_user.is_authenticated:
        if request.method == 'POST':
            if 'submitYes' in request.form.keys():
                db_sess.delete(news)
                db_sess.commit()
                db_sess = db_session.create_session()
                news = db_sess.query(News).filter(News.anonimus != 'True').all()
                db_sess.close()
                return redirect(f"/profile/{current_user.id}")

            if 'submitNo' in request.form.keys():
                return redirect(f"/profile/{current_user.id}")
    else:
        return redirect("/")
    return render_template('project_delete.html', title='Удаление работы', form=form)


@app.route('/profile/profile_red', methods=['GET', 'POST'])
@login_required
def profile_red():
    form = Profred()
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    if request.method == 'POST':
        try:
            img = request.files['avatar']
            if form.email.data != '':
                user.email = form.email.data
            if form.login.data != '':
                user.name = form.login.data
            if form.password.data != '':
                user.hashed_password = werkzeug.security.generate_password_hash(form.password.data)
            if allowed_file(img.filename):
                user.image = sqlite3.Binary(img.read())

            db_sess.commit()
            db_sess.close()
            return redirect(f"/profile/{current_user.id}")
        except Exception:
            return render_template('profile_red.html', title='Редактирование профиля', form=form,
                                   message='Неверный формат ввода')
    return render_template('profile_red.html', title='Редактирование профиля', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
