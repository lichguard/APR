from DocumentStore import *
from sklearn.feature_extraction.text import TfidfVectorizer
import Stemmer
from collections import defaultdict
import logging
import time
import operator


class TopDocs:
    scores = {}
    document_store = None

    def __init__(self, ds):
        self.document_store = ds

    def update(self, doc_id, score):
        if doc_id not in self.scores.keys():
            self.scores[doc_id] = score
        else:
            self.scores[doc_id] += score

    def __str__(self):
        output = "\n"
        for key in self.scores.keys():
            output += "doc_id: " + str(key) + " score: " + str(self.scores[key])
            # self.document_store[key].get_text() + " \n"
        return output

    def display(self):
        return sorted(self.scores.items(), key=operator.itemgetter(1), reverse=True)


class Indexer:
    # create logger with 'Indexer'
    logger = logging.getLogger('Indexer')

    inv_index = None
    docs = None
    english_stemmer = Stemmer.Stemmer('en')
    tf_idf = None

    def index(self, docs):
        start = time.time()
        self.logger.info("Indexing...")
        self.docs = docs
        self.create_inverse_index()
        self.create_tf_idf()
        end = time.time()
        self.logger.info("Indexing complete. elapsed time: " + str(end - start) + " secs")

    def create_inverse_index(self):
        """
        This function creates an inverted index

        Parameters:
            docs ([Document]): this function accepts a DocumentManager that has data.

        Example:
        {"word1": [1,76,346], "word2": [123,646,222]}
        """
        start = time.time()
        self.logger.info("Creating inverse index...")
        self.inv_index = defaultdict(set)
        for idx, doc in enumerate(self.docs):
            for token in doc.get_tokens():
                self.inv_index[token].add(idx)
        end = time.time()
        self.logger.info("create_inverse_index. elapsed time: " + str(end - start) + " secs")

    def create_tf_idf(self):
        start = time.time()
        class StemmedTfidfVectorizer(TfidfVectorizer):
            def build_analyzer(self):
                # analyzer = super(TfidfVectorizer, self).build_analyzer()
                # return lambda doc: english_stemmer.stemWords(analyzer(doc))
                return lambda doc: doc.get_tokens()

            def build_preprocessor(self):
                preprocessor = super(TfidfVectorizer, self).build_preprocessor()
                return lambda doc: (preprocessor(doc.get_text()))

        self.tf_idf = StemmedTfidfVectorizer(strip_accents='ascii', stop_words='english', analyzer='word', ngram_range=(1, 1))
        self.tf_idf.fit_transform(self.docs)
        end = time.time()
        self.logger.info("create_tf_idf complete. elapsed time: " + str(end - start) + " secs")
        # print(tfidf.vocabulary_)
        # print(tfidf.idf_)

    def execute_query(self, query):
        start = time.time()
        self.logger.info("Executing query: " + str(query))
        top_docs = TopDocs(self.docs)

        tokenize_query = process_and_tokenize_string(query)
        for token in tokenize_query:
            if token not in self.inv_index.keys():
                continue

            for doc_id in self.inv_index[token]:
                top_docs.update(doc_id, self.tf_idf.idf_[self.tf_idf.vocabulary_[token]])

        end = time.time()
        self.logger.info("execute_query complete. elapsed time: " + str(end - start) + " secs")
        self.logger.info(str(top_docs))

        return top_docs
