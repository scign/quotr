## Author: Aleem Juma

from flask import render_template, request
from app import app
from app.quotes import get_random_word, find_matching_quote

@app.route('/', methods=['GET','POST'])
def index():
    genres = [get_random_word() for _ in range(4)]
    genre = request.args.get('genre', default=genres[0])
    app.logger.info(f'Request received: "{genre}"')
    quote, matches = find_matching_quote(genre)
    return render_template('quote_finder.html', genres=genres, quote=quote, matches=matches)
