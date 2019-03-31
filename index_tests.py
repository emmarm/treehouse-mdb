import unittest
import flask

from index import app
from models import Movie


class IndexTests(unittest.TestCase):
    def setUp(self):
        # set up test client as app, set testing to True
        self.app = app.test_client()
        self.app.testing = True

    # test routes
    def test_hello(self):
        res = self.app.get('/hello')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"Hello")

    def test_say_hello(self):
        res = self.app.get('/hello/treehouse')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"Hello, Treehouse")

    def test_get_movies(self):
        res = self.app.get('/movies/')

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.data)
        self.assertIn(b'page=2">Next</a>', res.data)
        self.assertNotIn(b'page=0">Previous</a>', res.data)

        res = self.app.get('/movies/?page=10')

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.data)
        self.assertIn(b'page=11">Next</a>', res.data)
        self.assertIn(b'page=9">Previous</a>', res.data)

        res = self.app.get('/movies/?page=9001')

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Page must be less than or equal to 1000", res.data)

        # sets up test client, can access session data
        with app.test_client() as c:
            c.get('/movies/')
            assert 'movies' in flask.session
            assert flask.session['page'] == 1
            assert len(flask.session['movies']) > 0

        # access info about request object
        with app.test_request_context('/movies/?page=5'):
            assert flask.request.path == '/movies/'
            assert flask.request.args['page'] == '5'

    def test_get_movie(self):
        res = self.app.get('/movie/129')

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Spirited Away", res.data)

        with app.test_request_context('/movie/129'):
            assert flask.request.path == '/movie/129'

    # test model instances created correctly
    def test_movie_model(self):
        movie = Movie({
            'id': 1,
            'title': 'The Best Movie',
            'release_date': '2000-1-1',
            'popularity': 50
        })
        assert movie.id == 1
        assert movie.title == 'The Best Movie'
        assert movie.release_date == '2000-1-1'
        assert movie.popularity == 50
        assert movie.sort_title == 'Best Movie'


# initialize unittest
if __name__ == '__main__':
    unittest.main()
