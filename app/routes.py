from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from sqlalchemy import text

from app import app, db
from app.forms import RegisterForm
from app.models import Movie, User, Ratings


@app.route('/', methods=['GET'])
def index_page():
    movies = None
    query = request.args.get('query')
    if query is None:
        movies = Movie.query.all()
    else:
        movies = Movie.query.filter(Movie.title.like("%" + query + "%")).all()
    for movie in movies:
        sql = text("SELECT AVG(rating) AS AvgRate FROM ratings WHERE movie_id = "+str(movie.id))
        result = db.engine.execute(sql)
        results_as_dict = result.mappings().all()
        movie.avgrate = results_as_dict[0].AvgRate
        userRate = Ratings.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
        movie.userRate = " - "
        if userRate:
            movie.userRate = userRate.rating

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


@app.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    return redirect(url_for('index_page'))


@app.route('/rate', methods=['POST'])
def rate_movie_action():
    movie_id = request.form.get('movie_id')
    movie_rate = request.form.get('movie_rate')
    Ratings.query.filter_by(user_id=current_user.id, movie_id=movie_id).delete()
    db.session.commit()
    rating = Ratings(user_id=current_user.id, movie_id=movie_id, rating=movie_rate)
    db.session.add(rating)
    db.session.commit()
    return redirect(url_for('index_page'))
