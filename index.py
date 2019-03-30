import requests

from flask import Flask
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
    api_key = app.config['TMDB_API_KEY']
    res = requests.get(
        f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1')
    movie_list = res.json()['results']
    print(movie_list)
    return movie_list[0]['title']
