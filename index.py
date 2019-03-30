import requests
from flask import Flask, render_template, request

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


@app.route('/movies/', methods=['GET'])
def get_movies():
    page_num = int(request.args['page']) if request.args.get('page') else 1
    api_key = app.config['TMDB_API_KEY']
    res = requests.get(
        f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page_num}')
    error, data = return_error_or_data(res)
    if error:
        return render_template('error.html', error=error)
    return render_template('movies.html', movies=data['results'], page=page_num)


@app.route('/movie/<int:id>', methods=['GET'])
def get_movie(id):
    api_key = app.config['TMDB_API_KEY']
    res = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US')
    error, data = return_error_or_data(res)
    if error:
        return render_template('error.html', error=error)
    return render_template('movie.html', movie=data)
