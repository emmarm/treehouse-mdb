import re


class Movie:
    popularity_total = 0
    movie_count = 0

    def __init__(self, details):
        self.id = details['id']
        self.title = details['title']
        self.release_date = details['release_date']
        self.popularity = details['popularity']
        self.sort_title = re.sub(r"^(The )", "", details['title'])
        Movie.popularity_total += details['popularity']
        Movie.movie_count += 1

    def get_popularity_average(self):
        return self.popularity_total / self.movie_count
