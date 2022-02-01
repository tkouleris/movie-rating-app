from flask import render_template, redirect, url_for, request
from flask_login import login_user

from app import app, db
from app.forms import RegisterForm
from app.models import Movie, User


@app.route('/', methods=['GET'])
def index_page():
    movies = None
    query = request.args.get('query')
    if query is None:
        movies = Movie.query.all()
    else:
        movies = Movie.query.filter(Movie.title.like("%" + query + "%")).all()
    print(movies)
    return render_template('index.html', movies=movies)


@app.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    attempted_user = User.query.filter_by(username=username).first()
    if attempted_user and attempted_user.check_password_correction(attempted_password=password):
        login_user(attempted_user)
    return redirect(url_for('index_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('index_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(err_msg)
    return render_template('register.html', form=form)
