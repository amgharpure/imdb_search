import pandas as pd
from collections import defaultdict


def get_cleaned_text(text):
    """Returns cleaned text (convert to string, change to lowercase, etc)"""
    cleaned_text = str(text)
    cleaned_text = cleaned_text.lower()
    return cleaned_text


class ImdbIndexer:
    def __init__(self, movie_data=None):
        self._movie_index = defaultdict(set)
        self._set_data(movie_data)
        self._create_index()

    def _set_data(self, movie_data):
        """Sets movie dataframe"""
        if movie_data is not None:
            self._movie_df = movie_data

    def _load_top_movies(self):
        """Loads movie dataframe from a file"""
        movie_df = pd.read_csv('./movies.csv')
        self._set_data(movie_df)

    def _create_index(self):
        """Creates the in-memory index from the movie dataframe"""
        for ix, row in self._movie_df.iterrows():
            name = row['name']
            # index name
            self._update_index(name, name)
            # index directors
            for director in row['directors']:
                self._update_index(director, name)
            # index stars
            for star in row['stars']:
                self._update_index(star, name)
            # index genres
            for genre in row['genres']:
                self._update_index(genre, name)
            # index release year
            self._update_index(row['year'], name)

    def _update_index(self, key, val):
        """update the in-memory index"""
        cleaned_key = get_cleaned_text(key)
        for part in cleaned_key.split(' '):
            self._movie_index[part].add(val)

    def get_items_by_key(self, key):
        """Returns item from movie index by key"""
        if key in self._movie_index:
            return self._movie_index[key]
        return set()

    def find_by_keys(self, keys=[]):
        """Returns items from movie index that match with all keys"""
        sets = [self.get_items_by_key(key) for key in keys]
        search_result = set.intersection(*sets)
        search_result = list(search_result)
        return search_result

    def find_by_search_term(self, search_term):
        """Returns items from movie index based on search term"""
        cleaned_search_term = get_cleaned_text(search_term)
        keys = cleaned_search_term.split(' ')
        search_result = self.find_by_keys(keys)
        search_result = list(search_result)
        return search_result
