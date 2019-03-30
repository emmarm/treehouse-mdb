import requests
from flask import Flask, render_template, request

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
    page_num = 1
    if request.args.get('page'):
        page_num = int(request.args.get('page'))
    api_key = app.config['TMDB_API_KEY']
    res = requests.get(
        f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page_num}')
    json = res.json()
    error = ''
    if res.status_code != 200:
        error = json['errors'][0] if 'errors' in json else json['status_message']
    if error:
        return render_template('error.html', error=error)
    movie_list = json['results']
    return render_template('movies.html', movies=movie_list, page=page_num)


@app.route('/movie/<int:id>', methods=['GET'])
def get_movie(id):
    api_key = app.config['TMDB_API_KEY']
    res = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US')
    json = res.json()
    error = ''
    if res.status_code != 200:
        error = json['errors'][0] if 'errors' in json else json['status_message']
    if error:
        return render_template('error.html', error=error)
    return render_template('movie.html', movie=json)
