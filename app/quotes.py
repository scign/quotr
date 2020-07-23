## Author: Aleem Juma

import os
from app import app
import pandas as pd
import gensim.downloader as api

# sometimes the model needs a couple of tries to load
while True:
    try:
        model = api.load('glove-wiki-gigaword-50')
        break
    except:
        pass
# read in the quotes database
q = pd.read_csv(os.path.join('app','data','quotes_all.csv'), sep=';', skiprows=1, header=0)

# there are a few quote genres that don't occur in the model vocab
# replace them with appropriate words so the similarity search works
replace = {
    'movingon':'moving',
    'fathersday': 'fathers',
    'memorialday': 'memorial',
    'mothersday': 'mothers',
    'newyears': 'year',
    'saintpatricksday': 'ireland',
    'valentinesday': 'valentine'
}
q['GENRE'].replace(to_replace=replace, inplace=True)

def get_random_word():
    '''
    Returns a random category label from the data
    '''
    random_word = q['GENRE'].sample(1).iloc[0]
    return random_word

def get_closest_words(word, choices, n=1):
    '''
    Returns the n closest matches in the model vocab
    Parameters:
    word       word to search
    choices    available matches
    n          number of results to return

    Returns:
    A list of n tuples in the form (word (str), similarity (float))
    '''
    app.logger.info(f'Finding closest words to "{word}"')
    if word in choices:
        # if the word is already in the list return the same word with 100% match
        return [(word, 1.0)]
    if word in model.vocab.keys():
        # if not in the list, find the closest words
        similarities = [(choice, model.similarity(word, choice)) for choice in choices]
        # sort, reverse, and return the top n (word,similarity) tuples
        return sorted(similarities, key=lambda x: x[1])[::-1][:n]
    else:
        app.logger.info(f'Not in model vocab: "{word}"')
        # if the requested label isn't in the model vocab, return a random genre
        return [(get_random_word(), 1.0), (word, 0.0)]

def find_matching_quote(genre):
    '''
    Returns a matching quote and up to 5 of the most similar genres with similarity measures
    Paramters:
    genre      genre to match

    Returns:
    (str) Quote
    (str) Author
    (list) List of tuples in the form (word (str), simliarity (float))
    '''
    # find closest matches
    matched_genres = get_closest_words(genre, q.GENRE.unique(), 5)
    # get the best one
    closest = matched_genres[0][0]
    app.logger.info(f'Finding quote for: "{closest}"')
    # get a quote from that genre
    matching_quote = q[q['GENRE']==closest].sample(1).iloc[0]
    quote = matching_quote.QUOTE
    author = matching_quote.AUTHOR
    # return the quote and the genres
    return quote, author, matched_genres
