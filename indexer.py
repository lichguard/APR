from DocumentStore import *
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import logging
import time
import operator
from sklearn.metrics.pairwise import linear_kernel
from utils import process_and_tokenize_string
import marisa_trie
from operator import itemgetter
import numpy as np


class TopDocs:
    scores = {}

    def update(self, doc_id, score):
        if doc_id not in self.scores.keys():
            self.scores[doc_id] = score
        else:
            self.scores[doc_id] += score

    def __str__(self):
        output = "\n"
        for key in self.scores.keys():
            output += "doc_id: " + str(key) + " score: " + str(self.scores[key])
            # self.document_store.docs[key].get_text() + " \n"
        return output

    def display(self):
        return sorted(self.scores.items(), key=operator.itemgetter(1), reverse=True)


class PostingList:
    logger = logging.getLogger('PostingList')
    token2docs = None
    token_trie_tree = None

    def __init__(self, document_store):
        start = time.time()
        self.logger.info("Creating posting list (inverse index)...")

        self.token_trie_tree = marisa_trie.Trie(document_store.token_set)
        self.token2docs = [defaultdict(list) for _ in range(len(document_store.token_set))]

        for doc in document_store.docs:
            for idx, token in enumerate(doc.get_tokens()):
                trie_token_index = self.token_trie_tree[token]
                self.token2docs[trie_token_index][doc.doc_id].append(idx)

        end = time.time()
        self.logger.info("create_inverse_index. elapsed time: " + str(end - start) + " secs")

    # returns a set of unique ids e.g. (1,5,2,5)
    def get_relevant_docs_ids(self, question_doc):
        relevant_docs = set()
        for token in question_doc.get_tokens():
            if token in self.token_trie_tree.keys():
                relevant_docs.update(self.token2docs[self.token_trie_tree[token]].keys())
        return relevant_docs


class TfIdf:
    logger = logging.getLogger('TfIdf')
    tf_idf_vectorizer = None

    def __init__(self, document_store):
        start = time.time()
        class StemmedTfidfVectorizer(TfidfVectorizer):
            def build_analyzer(self):
                # analyzer = super(TfidfVectorizer, self).build_analyzer()
                # return lambda doc: english_stemmer.stemWords(analyzer(doc))
                return lambda doc: doc.get_tokens()

            def build_preprocessor(self):
                preprocessor = super(TfidfVectorizer, self).build_preprocessor()
                return lambda doc: (preprocessor(doc.get_text()))

        self.tf_idf_vectorizer = StemmedTfidfVectorizer(strip_accents='ascii', stop_words='english', analyzer='word', ngram_range=(1, 1))
        self.tf_idf_vectorizer.fit(document_store.docs)
        end = time.time()
        self.logger.info("create_tf_idf complete. elapsed time: " + str(end - start) + " secs")
        # print(tf_idf_vectorizer.vocabulary_)
        # print(tf_idf_vectorizer.idf_))

    def query(self, query_doc, source_docs):
        start = time.time()
        self.logger.info("Executing tf_idf query")

        docs_vecotr = self.tf_idf_vectorizer.transform(source_docs)
        query_vector = self.tf_idf_vectorizer.transform([query_doc])

        cosine_similarities = linear_kernel(query_vector, docs_vecotr).flatten()

        end = time.time()
        self.logger.info("tf_idf query complete. elapsed time: " + str(end - start) + " secs")
        return cosine_similarities


class Indexer:
    """
      A class used to index DocumentStore

      Attributes
      ----------
      logger : Logger
          a formatted string to print out what the animal says
      posting_list : PostingList
          a formatted string to print out what the animal says
      document_store : DocumentStore
          will be written
      tf_idf_vectorizer : StemmedTfidfVectorizer
          the sound that the animal makes
      tf_idf : sparse matrix, [n_samples, n_features]]
          the number of legs the animal has (default 4)

      Methods
      -------
      index(DocumentStore)
          Prints the animals name and what sound it makes
      """
    logger = logging.getLogger('Indexer')

    posting_list = None
    document_store = None
    tf_idf = None

    def __init__(self, document_store):
        self.document_store = document_store

    def index(self):
        start = time.time()
        self.logger.info("Indexing...")

        self.posting_list = PostingList(self.document_store)
        self.tf_idf = TfIdf(self.document_store)

        end = time.time()
        self.logger.info("Indexing complete. elapsed time: " + str(end - start) + " secs")

    def execute_query(self, query):
        start = time.time()
        self.logger.info("Executing query: " + str(query))
        self.logger.debug("query tokenizing: " + str(process_and_tokenize_string(query)))

        # create question doc from query string
        question_document = Document()
        question_document.paragraphs.append(Paragraph(0, query))

        relevant_doc_ids = self.posting_list.get_relevant_docs_ids(question_document)
        tf_idf_scores = self.tf_idf.query(question_document, self.document_store.docs)

        self.logger.info(relevant_doc_ids)
        self.logger.info(tf_idf_scores.argsort()[::-1])

        end = time.time()
        self.logger.info("execute_query complete. elapsed time: " + str(end - start) + " secs")