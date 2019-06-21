import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def process(s):

    ps = PorterStemmer()

    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(s)

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(ps.stem(w))

    return filtered_sentence
