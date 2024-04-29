from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.register import RegisterForm
from data.login_form import LoginForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            try:
                file = request.files['file'].read()
                photo = request.files['file'].filename
                with open(f'static/img/{photo}', 'wb') as f:
                    f.write(file)
                with open('db/avatars.txt', mode='w', encoding='utf8') as f:
                    f.write(photo)
                return render_template("main.html", photo=f'static/img/{photo}')
            except:
                photo = 'ava.webp'
                with open('db/avatars.txt', mode='w', encoding='utf8') as f:
                    f.write(photo)
                return render_template("main.html", photo=f'static/img/{photo}')
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("main.html", photo=f'static/img/{photo}', title='"Пчёлки" Детский сад и Семейный Клуб')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/Короткий_день')
def short():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("short.html", photo=f'static/img/{photo}', title='Детский сад короткого дня')

@app.route('/Полный_день')
def full():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("full.html", photo=f'static/img/{photo}', title='Детский сад полного дня')

@app.route('/Правила_посещения')
def rules():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("rules.html", photo=f'static/img/{photo}', title='Правила посещения детского сада')

@app.route('/Семейный_клуб')
def club():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("club.html", photo=f'static/img/{photo}', title='Семейный клуб | Доп.занятия')

@app.route('/Танцы')
def dance():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("dance.html", photo=f'static/img/{photo}', title='Танцевальная студия')

@app.route('/ИЗО')
def draw():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("draw.html", photo=f'static/img/{photo}', title='ИЗО студия')

@app.route('/Дошколята')
def doshkol():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("doshkol.html", photo=f'static/img/{photo}', title='Дошколята')

@app.route('/Логопед')
def logoped():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("logoped.html", photo=f'static/img/{photo}', title='Логопед-дефектолог')

@app.route('/Программирование')
def scratch():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("scratch.html", photo=f'static/img/{photo}', title='Программирование Scratch Junior')

@app.route('/Робототехника')
def roboto():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("roboto.html", photo=f'static/img/{photo}', title='Робототехника')

@app.route('/День_рождения')
def birth():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("birth.html", photo=f'static/img/{photo}', title='День рождения')

@app.route('/Тхэквондо')
def tek():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("teknchess.html", photo=f'static/img/{photo}', title='Тхэквондо')

@app.route('/Шахматы')
def chess():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("teknchess.html", photo=f'static/img/{photo}', title='Шахматы')

@app.route('/Академический_рисунок')
def academ():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("academ.html", photo=f'static/img/{photo}', title='Академический рисунок')

@app.route('/Мастерилка')
def masterilka():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("masterilka.html", photo=f'static/img/{photo}', title='Мастерилка')

@app.route('/Отзывы')
def response():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("response.html", photo=f'static/img/{photo}', title='Отзывы')

@app.route('/Сотрудники')
def employee():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("employee.html", photo=f'static/img/{photo}', title='Сотрудники')

@app.route('/Достижения')
def awards():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("awards.html", photo=f'static/img/{photo}', title='Достижения')

@app.route('/Галерея')
def gallery():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("gallery.html", photo=f'static/img/{photo}', title='Галерея')

@app.route('/Контакты')
def contact():
    with open('db/avatars.txt', mode='r', encoding='utf8') as f:
        photo = str(f.readline())
    return render_template("contact.html", photo=f'static/img/{photo}', title='Контакты')

def main():
    db_session.global_init("db/users.sqlite")
    app.run()


if __name__ == '__main__':
    main()
