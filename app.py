from flask import Flask, Response, request
from ImdbIndexer import ImdbIndexer
import ImdbCrawler
import json
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

logging.info('Fetching Data')
movie_data = ImdbCrawler.get_movies_dataframe()

logging.info('Initializing DB')
imdb_indexer = ImdbIndexer(movie_data)


@app.route('/')
def home():
    return 'IMDB Search home!'


@app.route('/search')
def search_movies():
    search_term = request.args.get('search_term')
    result = imdb_indexer.find_by_search_term(search_term)
    response = Response(
        json.dumps(result),
        status=200,
        content_type='application/JSON'
    )
    return response


if __name__ == '__main__':
    app.run()
