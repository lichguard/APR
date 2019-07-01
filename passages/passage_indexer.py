import logging
import time
import pickle
from gensim.corpora import Dictionary
from pathlib import Path
from passages.toppassage import TopPassage
from passages.passage import Passage
from utils import process_and_tokenize_string, progbar, get_processed_synonyms, wh_questions, split_strings, remove_stop_words
from passages.scoretype import ScoreType
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from passages.ngrams import Ngrams
# import cProfile


class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight = None
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
                np.mean([self.word2vec[w] * self.word2weight[w]
                         for w in words if w in self.word2vec] or
                        [np.zeros(self.dim)], axis=0)
                for words in X
            ])


class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])


class PassageIndexer:
    logger = logging.getLogger('Indexer')

    def __init__(self, file_name=None):
        self.posting_list = None
        self.ngrams = None
        self.dictionary = None
        self.tokens_by_docs = None
        self.docs = None
        self.file_name = file_name

    def index(self, docs, reindex=True):
        if not reindex:
            reindex = not self.load()

        if reindex:
            self.create_from_docs(docs)

            self.tokens_by_docs = [doc.get_tokens() for doc in self.docs]
            self.dictionary = Dictionary(self.tokens_by_docs)
            self.ngrams = Ngrams(self.tokens_by_docs)

            #if self.file_name:
            #    self.save()

    def create_from_docs(self, docs_json):
        # time and log
        start = time.time()
        self.logger.info("Creating documents...")

        # init variables
        self.docs = []

        # load documents and tokenize
        for doc_id in docs_json.keys():
            passage_json = docs_json[doc_id]
            for i, key in enumerate(passage_json.keys()):
                doc = Passage(int(key), int(doc_id), passage_json[key])
                self.docs.append(doc)

        end = time.time()
        self.logger.info("Creating document complete. elapsed time: " + str(end - start) + " secs")

    def execute_query(self, query):
        start = time.time()
        query_tokens = process_and_tokenize_string(query)
        unprocessed_query_tokens = split_strings(query)
        self.logger.info(" Executing Query: '" + str(query) + "'  ---- tokens:" +   str(query_tokens) )
        top_docs = [TopPassage(doc) for doc in self.docs]
        question_class = -1
        for i, wh in enumerate(wh_questions):
            if wh in unprocessed_query_tokens:
                question_class = i
                break

        #pos_list = nltk.pos_tag(unprocessed_query_tokens)
        tokens_synonyms = []
        for token in remove_stop_words(unprocessed_query_tokens):
            tokens_synonyms += get_processed_synonyms(token)

        #print(tokens_synonyms)

        ngrams_vector = self.ngrams.query(query_tokens, self.docs)
        expanded_ngram_vector = self.ngrams.query(tokens_synonyms, self.docs)

        for i in range(len(top_docs)):
            progbar(i, len(top_docs))
            top_docs[i].update_score(ScoreType.ngram, ngrams_vector[i])
            top_docs[i].update_score(ScoreType.expanded_ngram, expanded_ngram_vector[i])

            top_docs[i].calculate_score()
        print(' ')
        top_docs.sort(key=lambda x: x.score, reverse=True)

        end = time.time()
        self.logger.info("execute_query complete. elapsed time: " + str(end - start) + " secs")
        return top_docs

    def load(self):
        full_file_name = "data\\cache\\" + self.file_name + "_passages.arp"

        my_file = Path(full_file_name)
        if not my_file.is_file():
            self.logger.info(full_file_name + " was not found, reindexing...")
            return False
        else:
            f = open(full_file_name, 'rb')
            tmp_dict = pickle.load(f)
            f.close()
            self.__dict__.clear()
            self.__dict__.update(tmp_dict)
            self.logger.info("Successfully loaded indexer data to " + full_file_name)
            return True

    def save(self):
        full_file_name = "data\\cache\\" + self.file_name + "_passages.arp"
        f = open(full_file_name, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()
        self.logger.info("Successfully saved indexer data from " + full_file_name)



