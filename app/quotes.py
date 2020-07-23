## Author: Aleem Juma

from app import app
import pandas as pd
import gensim.downloader as api

while True:
    try:
        model = api.load('glove-wiki-gigaword-50')
        break
    except:
        pass
q = pd.read_csv('app\\data\\quotes_all.csv', sep=';', skiprows=1, header=0)

# there are a few quote genres that don't occur in the model vocab
# replace them with appropriate words so the similarity search works
replace = {
    'movingon':'moving',
    'fathersday': 'fathers',
    'memorialday': 'memorial',
    'mothersday': 'mothers',
    'newyears': 'year',
    'saintpatricksday': 'patrick',
    'valentinesday': 'valentine'
}
q['GENRE'].replace(to_replace=replace, inplace=True)

def get_random_word():
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
        return [(word, 1.0)]
    if word in model.vocab.keys():
        similarities = [(choice, model.similarity(word, choice)) for choice in choices]
        return sorted(similarities, key=lambda x: x[1])[::-1][:n]
    else:
        app.logger.info(f'Not in model vocab: "{word}"')
        return [(get_random_word(), 1.0), (word, 0.0)]

def find_matching_quote(genre):
    '''
    Returns a matching quote and up to 5 of the most similar genres with similarity measures
    Paramters:
    genre      genre to match

    Returns:
    (str) Quote
    (list) List of tuples in the form (word (str), simliarity (float))
    '''
    matched_genres = get_closest_words(genre, q.GENRE.unique(), 5)
    closest = matched_genres[0][0]
    app.logger.info(f'Finding quote for: "{closest}"')
    matching_quote = q['QUOTE'][q['GENRE']==closest].sample(1).iloc[0]
    return matching_quote, matched_genres
