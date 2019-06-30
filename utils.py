import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import Stemmer
import re


nltk.download('stopwords')
english_stemmer = Stemmer.Stemmer('en')
stop_words = set(stopwords.words('english'))
stop_words.add(",")
stop_words.add(".")
stop_words.add("?")

wh_questions = ['who', 'what', 'how', 'where', 'when', 'why', 'which', 'whom', 'whose']

def dummy_func(doc):
    return doc


def progbar(curr, total, full_progbar=20):
    frac = (curr+1) / total
    filled_progbar = round(frac * full_progbar)
    print('\r', '█' * filled_progbar + '-' * (full_progbar - filled_progbar), '[{:>7.2%}]'.format(frac), end='')


def process_and_tokenize_string(data):
    """
    This function converts sentences into tokens

    Parameters:
        data (String): this function accepts a string that represents a sentence

    Returns:
        list: A list of tokens that after stemming with no stop words
    """

    #     return data.split(" ")
    tokens = english_stemmer.stemWords(split_strings(re.sub(r'[^a-zA-Z0-9\s]', '', data)))
    return [word for word in tokens if word not in stop_words]
    # return english_stemmer.stemWords(word_tokenize(data.lower()))


def split_strings(data):
    return word_tokenize(data.lower())


def generate_ngrams(tokens, n):
    result = []
    for j in range(1, n+1):
        ngrams = zip(*[tokens[i:] for i in range(j)])
        result += [" ".join(ngram) for ngram in ngrams]
    return result
