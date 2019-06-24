from DocumentStore import *
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import logging
import time
import operator
from sklearn.metrics.pairwise import linear_kernel
from utils import process_and_tokenize_string, progbar
import marisa_trie
from enum import Enum
import cProfile


class ScoreType(Enum):
    tf_idf = 0
    token_count = 1
    proximity_score = 2


class TopDoc:

    def __init__(self, doc):
        self.doc = doc
        self.scores = defaultdict(int)
        self.score = 0

    def get_doc_id(self):
        return self.doc.doc_id

    def update_score(self, score_type, score):
        self.scores[score_type] = score

    def calculate_score(self):
        self.score = 0
        self.score += self.scores[ScoreType.tf_idf] * 0.6
        self.score += self.scores[ScoreType.token_count] * 0.1
        self.score += self.scores[ScoreType.proximity_score] * 0.3

    def __str__(self):
        output = "id " + str(self.doc.doc_id) + ", score " + str(self.score)
        for key in self.scores.keys():
            output += "\t" + str(key) + " score: " + str(self.scores[key])
        return output

    def __repr__(self):
        return "\n" + str(self)

    def display(self):
        return sorted(self.scores.items(), key=operator.itemgetter(1), reverse=True)


class PostingList:
    logger = logging.getLogger('PostingList')

    def __init__(self, document_store):

        # pr = cProfile.Profile()
        # pr.enable()
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
        # pr.disable()
        # after your program ends
         # pr.print_stats(sort="calls")

    # returns a set of unique ids e.g. (1,5,2,5)
    def get_relevant_docs_ids(self, query_doc):
        relevant_docs = set()
        for token in query_doc.get_tokens():
            if token in self.token_trie_tree:
                relevant_docs.update(self.token2docs[self.token_trie_tree[token]].keys())
        return relevant_docs

    def get_tokens_intersection_count(self, query_tokens, source_doc):
        count = 0
        for token in query_tokens:
            if token in self.token_trie_tree:
                if source_doc.doc_id in self.token2docs[self.token_trie_tree[token]].keys():
                    count += 1

        return count

    def get_proximity_score(self, query_tokens, source_doc):
        positions = []
        query_tokens = set(query_tokens)
        # find all relevant positions
        for token in query_tokens:
            if token in self.token_trie_tree:
                if source_doc.doc_id in self.token2docs[self.token_trie_tree[token]].keys():
                    positions += self.token2docs[self.token_trie_tree[token]][source_doc.doc_id]

        doc_tokens = source_doc.get_tokens()
        max_count = 0
        window = 10
        for position in positions:
            count = 0
            used_tokens = set()
            for position_index in range(position-window, position+window, 1):
                if position_index < 0 or position_index >= len(doc_tokens):
                    continue
                else:
                    token = doc_tokens[position_index]
                    if token in query_tokens and token not in used_tokens:
                        count += 1
                        used_tokens.add(token)
            if count > max_count:
                max_count = count
        return max_count


class TfIdf:
    logger = logging.getLogger('TfIdf')

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
        if not source_docs:
            return None

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

    def __init__(self, document_store):
        self.document_store = document_store
        self.posting_list = None
        self.tf_idf = None

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
        question_document.recalculate_tokens()

        relevant_doc_ids = self.posting_list.get_relevant_docs_ids(question_document)
        relevant_docs = [self.document_store.docs[i] for i in relevant_doc_ids]
        top_docs = [TopDoc(self.document_store.docs[i]) for i in relevant_doc_ids]

        tf_idf_scores = self.tf_idf.query(question_document, relevant_docs)

        for i in range(len(top_docs)):
            progbar(i, len(top_docs), 20)

            top_docs[i].update_score(ScoreType.tf_idf, tf_idf_scores[i])

            top_docs[i].update_score(ScoreType.token_count, self.posting_list.get_tokens_intersection_count(question_document.get_tokens(), top_docs[i].doc) / len(question_document.get_tokens()))

            top_docs[i].update_score(ScoreType.proximity_score, self.posting_list.get_proximity_score(question_document.get_tokens(), top_docs[i].doc) / len(question_document.get_tokens()))

            top_docs[i].calculate_score()

        top_docs.sort(key=lambda x: x.score, reverse=True)
        self.logger.info(str(top_docs))

        end = time.time()
        self.logger.info("execute_query complete. elapsed time: " + str(end - start) + " secs")
