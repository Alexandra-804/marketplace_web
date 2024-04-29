import markupsafe
from flask import Flask, url_for, request, render_template, redirect
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from data import db_session
from data.db_session import SqlAlchemyBase
from data.users import User
from data import categories
from forms.user import RegisterForm
from data.categories import Category
from forms import user
from data.notes import Notes
from forms.category import CategoryForm
from forms.note import NoteForm
from datetime import *


app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/maestro.db')
    app.run(debug=True)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html', message="Вы успешно вышли из системы")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == request.form.get('login')).first()
        # user.set_password('password')
        # print(user.hashed_password)
        if user:
            if user.check_password(request.form.get('password')):
                login_user(user)

                return render_template('base.html', message="Вы успешно вошли в систему", login=user.name)
            else:
                return render_template('base.html', message="Неправильный пароль")
        else:
            return render_template('base.html', message="Неправильный логин")
    # return render_template('base.html', message="")
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                about=form.about.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return render_template('/index.html', message='Пользователь был успешно зарегистрирован')
        # return render_template('register.html', title='Регистрация', form=form)
    else:
        return render_template('register.html', title='Регистрация', form=form)


@app.route('/create_category', methods=['GET', 'POST'])
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        category = Category(
            name=form.name.data,
        )
        db_sess.add(category)
        db_sess.commit()
        print('Категория создана')
    return redirect('/categories')


@app.route('/categories', methods=['GET'])
def categories():
    form = CategoryForm()
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    return render_template('categories.html', categories=categories, form=form)

@app.route('/delete_category/<int:id>')
def deletecategory(id):
    db_sess = db_session.create_session()
    category = db_sess.query(Category).filter(Category.id == id).first()
    db_sess.delete(category)
    db_sess.commit()
    print('Категория удалена')
    return redirect('/categories')

@app.route('/watch_notes/<int:catid>')
def tasks():
    form = NoteForm()
    db_sess = db_session.create_session()
    notes = db_sess.query(NoteForm).all()
    return render_template('categories.html', categories=categories, form=form)

@app.route('/notes', methods=['GET'])
def notes():
    form = NoteForm()

    db_sess = db_session.create_session()
    notes = db_sess.query(Notes).all()
    categories = db_sess.query(Category).all()
    form = NoteForm(categories=categories)
    return render_template('notes.html', notes=notes, form=form)


@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        note = NoteForm(
            category_id=form.category_id.data,
            title=form.title.data,
            price=form.price.data,
            amount=form.amount.data,
            about=form.about.data,
            )
        db_sess.add(note)
        db_sess.commit()
        print('Запись создана')
    return redirect('/notes')


@app.route('/delete_note/<int:id>')
def delete_note(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Notes).filter(Notes.id == id).first()
    db_sess.delete(task)
    db_sess.commit()
    print('Запись удалена')
    return redirect('/watch_notes')


if __name__ == '__main__':
    main()