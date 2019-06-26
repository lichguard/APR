import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import Stemmer

nltk.download('stopwords')
english_stemmer = Stemmer.Stemmer('en')
stop_words = set(stopwords.words('english'))
stop_words.add(",")
stop_words.add(".")
stop_words.add("?")


def progbar(curr, total, full_progbar):
    frac = curr / total
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
    tokens = english_stemmer.stemWords(word_tokenize(data.lower()))
    return [word for word in tokens if word not in stop_words]
    # return english_stemmer.stemWords(word_tokenize(data.lower()))


