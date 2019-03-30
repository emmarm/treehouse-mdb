import unittest

from index import app


class IndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

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
        self.assertIn(b'<a href="/movies/?page=2">Next</a>', res.data)
        self.assertNotIn(b'<a href="/movies/?page=0">Previous</a>', res.data)

        res = self.app.get('/movies/?page=10')

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.data)
        self.assertIn(b'<a href="/movies/?page=11">Next</a>', res.data)
        self.assertIn(b'<a href="/movies/?page=9">Previous</a>', res.data)

        res = self.app.get('/movies/?page=9001')

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Page must be less than or equal to 1000", res.data)

    def test_get_movie(self):
        res = self.app.get('/movie/129')

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Spirited Away", res.data)


if __name__ == '__main__':
    unittest.main()
