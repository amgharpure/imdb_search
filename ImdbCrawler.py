from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import logging
import pandas as pd
import json


def get_cleaned_movie(movie_bs4):
    """Get a dictionary of a movie from its bs4 object"""

    # parse directors and stars arrays
    movie_directors_array = []
    movie_stars_array = []
    array = movie_directors_array
    try:
        for content in movie_bs4.find_all('p')[2].contents:
            # switch array to stars array after seeing its NavigableString el
            if type(content) == NavigableString:
                if 'Stars' in content:
                    array = movie_stars_array
            else:
                # check for ghost span if NOT a NavigableString
                if 'class' in content.attrs and\
                        'ghost' in content.attrs['class']:
                    continue
                # add to array if not a ghost span
                array.append(content.text)
    except (KeyError, Exception) as e:
        logging.error(f'Error parsing directors and stars: {e=}, {type(e)=}')

    # parse remaining movie fields
    movie_name = None
    movie_year = None
    movie_genres = None
    try:
        movie_name = movie_bs4.h3.a.text
        movie_year = int(movie_bs4.find(class_='lister-item-year').text[-5:-1])
        movie_genres = movie_bs4.find(class_='genre')\
            .text.replace('\n', '').replace(' ', '').split(',')
    except Exception as e:
        logging.error(f'Error parsing movie details: {e=}, {type(e)=}')

    cleaned_movie = {
        'name': movie_name,
        'year': movie_year,
        'directors': movie_directors_array,
        'stars': movie_stars_array,
        'genres': movie_genres
    }
    return cleaned_movie


def get_fake_top_1000_api_response():
    """Returns fake cleaned movie data"""
    fake_top_5_movies = json.loads(
        '[{"name": "Jai Bhim", "year": 2021, "directors": ["T.J. Gnanavel"], '
        '"stars": ["Suriya", "Lijo Mol Jose", "Manikandan", "Rajisha '
        'Vijayan"], "genres": ["Crime", "Drama"]}, {"name": "The Shawshank '
        'Redemption", "year": 1994, "directors": ["Frank Darabont"], '
        '"stars": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William '
        'Sadler"], "genres": ["Drama"]}, {"name": "The Godfather", "year": '
        '1972, "directors": ["Francis Ford Coppola"], "stars": ["Marlon '
        'Brando", "Al Pacino", "James Caan", "Diane Keaton"], "genres": ['
        '"Crime", "Drama"]}, {"name": "Soorarai Pottru", "year": 2020, '
        '"directors": ["Sudha Kongara"], "stars": ["Suriya", "Paresh Rawal", '
        '"Urvashi", "Aparna Balamurali"], "genres": ["Drama"]}, {"name": '
        '"The Dark Knight", "year": 2008, "directors": ["Christopher '
        'Nolan"], "stars": ["Christian Bale", "Heath Ledger", "Aaron '
        'Eckhart", "Michael Caine"], "genres": ["Action", "Crime", '
        '"Drama"]}]')
    return fake_top_5_movies


def get_movies_data(count=100, start=1):
    """Calls imdb (top 1000) api based on count and offset(start) """
    url = "https://www.imdb.com/search/title/?groups=top_1000&sort" \
          "=user_rating,desc&count={count}&start={" \
          "start}&ref_=adv_nxt".format(count=count, start=start)
    response = requests.get(url)

    # parse response using bs4
    soup = BeautifulSoup(response.content, "html.parser")
    movie_list_bs4 = soup.find_all("div", attrs={"lister-item-content"})

    # get cleaned movies (list of dictionaries)
    cleaned_movies = [get_cleaned_movie(movie) for movie in movie_list_bs4]
    return cleaned_movies


def get_top_1000_movies():
    """Returns list of top 1000 imdb movies"""
    movies_list = []
    count = 100
    for start_ix in range(1, 1000, 100):
        movies_list += get_movies_data(count, start_ix)
    return movies_list


def get_movies_dataframe():
    """returns a dataframe containing the top 1000 imdb movies"""
    top_1000_movies = get_top_1000_movies()
    movie_df = pd.DataFrame.from_dict(top_1000_movies)
    return movie_df
