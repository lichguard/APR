from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import defaultdict


def process(s):
    """
    This function converts sentences into tokens

    Parameters:
        s (String): this function accepts a string that represents a sentence

    Returns:
        Array: An array of tokens that after stemming with no stop words
    """
    ps = PorterStemmer()

    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(s)

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(ps.stem(w))

    return filtered_sentence


def create_inverse_index(ds):
    """
    This function creates an inverted index

    Parameters:
        ds (DocumentManager): this function accepts a DocumentManager that has data.

    Returns:
        Dictionary: A dictionary with with words as key and the corresponding list composed of integers that
        refers to the document the word was found

    Example:
    {"word1": [1,76,346], "word2": [123,646,222]}
    """
    inv_index = defaultdict(list)
    for idx, doc in enumerate(ds.docs):
        for token in doc.get_tokens():
            inv_index[token].append(idx)
