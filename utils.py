import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import Stemmer
import re
from nltk.corpus import wordnet
from QuestionStore import QuestionManager
import json

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
english_stemmer = Stemmer.Stemmer('en')
stop_words = set(stopwords.words('english'))
stop_words.add(",")
stop_words.add(".")
stop_words.add("?")
wh_questions = ['who', 'what', 'how', 'where', 'when', 'why', 'which', 'whom', 'whose']


def dummy_func(doc):
    return doc


def load_questions(question_source_file):
    qs = QuestionManager()
    qs.create("data\\" + question_source_file)
    return qs


def load_json_from_file(doc_source_file):
    with open("data\\" + doc_source_file + ".json", 'r', encoding='utf-8') as f:
        docs_json = json.load(f)
    return docs_json


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
    tokens = split_strings(re.sub(r'[^a-zA-Z0-9\s]', '', data))
    tokens = remove_stop_words(tokens)
    return stem_tokens(tokens)
    # return english_stemmer.stemWords(word_tokenize(data.lower()))


def remove_stop_words(tokens):
    return [word for word in tokens if word not in stop_words]


def stem_tokens(tokens):
    return english_stemmer.stemWords(tokens)


def get_processed_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms += process_and_tokenize_string(l.name().replace('_', ' '))
    return synonyms


def split_strings(data):
    return word_tokenize(data.lower())


def generate_ngrams(tokens, n):
    result = []
    for j in range(1, n+1):
        ngrams = zip(*[tokens[i:] for i in range(j)])
        result += [" ".join(ngram) for ngram in ngrams]
    return result
