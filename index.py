import requests
from flask import Flask, session, render_template, request
import jsonpickle

from models import Movie
from utils import return_error_or_data

app = Flask(__name__)
app.config.from_object('config')


# most basic example
@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello'


# example using param variables
@app.route('/hello/<string:name>', methods=['GET'])
def say_hello(name):
    return 'Hello, {}'.format(name.title())


# '/movies/' returns page 1, use '/movies/?page=<int>' to get a different page
@app.route('/movies/', methods=['GET'])
def get_movies():
    page = int(request.args['page']) if request.args.get('page') else 1
    movies = []
    if 'page' in session and session['page'] == page:
        # get saved movie list from session
        movies = [jsonpickle.decode(movie) for movie in session['movies']]
    else:
        # get movies from popular movies endpoint
        api_key = app.config['TMDB_API_KEY']
        res = requests.get(
            f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}')
        error, data = return_error_or_data(res)
        if error:
            return render_template('error.html', error=error)
        # if not error, make movies into Movie instances and save to session
        movies = [Movie(movie) for movie in data['results']]
        session['page'] = page
        # session requires json format, use jsonpickle to encode complex objects to json
        session['movies'] = [jsonpickle.encode(
            movie_obj) for movie_obj in movies]
        session.modified = True
    return render_template('movies.html', movies=movies, page=page)


@app.route('/movie/<int:id>', methods=['GET'])
def get_movie(id):
    movie = None
    if 'movies' in session:
        # check if movie exists in saved movies - decode from json using jsonpickle and use next() function to return match or None if no match
        movies = [jsonpickle.decode(movie) for movie in session['movies']]
        movie = next((m for m in movies if m.id == id), None)
    if not movie or 'movies' not in session:
        # if movie didn't exist in saved movies or no movies saved in session
        api_key = app.config['TMDB_API_KEY']
        # use details endpoint to get info for movie by id
        res = requests.get(
            f'https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US')
        error, data = return_error_or_data(res)
        if error:
            return render_template('error.html', error=error)
        movie = Movie(data)
    return render_template('movie.html', movie=movie)
