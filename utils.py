import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
import Stemmer

nltk.download('stopwords')
english_stemmer = Stemmer.Stemmer('en')
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def process(s):
    """
    This function converts sentences into tokens

    Parameters:
        s (String): this function accepts a string that represents a sentence

    Returns:
        Array: An array of tokens that after stemming with no stop words
    """

    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(s)

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(ps.stem(w))

    return filtered_sentence


def process_and_tokenize_string(data):
    # return data.split(" ")

    tokens = english_stemmer.stemWords(word_tokenize(data.lower()))
    return [word for word in tokens if word not in stop_words]
    # return english_stemmer.stemWords(word_tokenize(data.lower()))



