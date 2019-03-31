import re


class Movie:
    # examples of class variables
    popularity_total = 0
    movie_count = 0

    # class constructor example
    def __init__(self, details):
        self.id = details['id']
        self.title = details['title']
        self.release_date = details['release_date']
        self.popularity = details['popularity']
        # use regexp to remove "the" from title for sorting
        self.sort_title = re.sub(r"^(The )", "", details['title'])
        # examples of updating class variables
        Movie.popularity_total += details['popularity']
        Movie.movie_count += 1

    # example of class method
    def get_popularity_average(self):
        return self.popularity_total / self.movie_count
