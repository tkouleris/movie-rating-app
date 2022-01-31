from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import app, db, login_manager
from app.models import Movie


@login_manager.user_loader
@app.route('/')
def index_page():
    movies = None
    query = request.args.get('query')
    if query is None:
        movies = Movie.query.all()
    else:
        movies = Movie.query.filter(Movie.title.like("%" + query + "%")).all()

    return render_template('index.html', movies=movies)


@app.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    print("LOGIN ACTION")
    print(username)
    print(password)
    return redirect(url_for('index_page'))
