from DocumentStore import *
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import logging
import time
import operator
from sklearn.metrics.pairwise import linear_kernel


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
            # self.document_store[key].get_text() + " \n"
        return output

    def display(self):
        return sorted(self.scores.items(), key=operator.itemgetter(1), reverse=True)


class Indexer:
    logger = logging.getLogger('Indexer')

    inv_index = None
    docs = None
    tf_idf_vectorizer = None
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

        self.tf_idf_vectorizer = StemmedTfidfVectorizer(strip_accents='ascii', stop_words='english', analyzer='word', ngram_range=(1, 1))
        self.tf_idf = self.tf_idf_vectorizer.fit_transform(self.docs)
        end = time.time()
        self.logger.info("create_tf_idf complete. elapsed time: " + str(end - start) + " secs")
        # print(tfidf.vocabulary_)
        # print(tfidf.idf_)

    def execute_query(self, query):
        start = time.time()
        self.logger.info("Executing query: " + str(query))
        question_document = Document()
        question_document.paragraphs.append(Paragraph(0, query))
        question_tf_idf_vector = self.tf_idf_vectorizer.transform([question_document])

        self.logger.info("question_tf_idf_vector: " + str(question_tf_idf_vector.data))
        cosine_similarities = linear_kernel(question_tf_idf_vector, self.tf_idf).flatten()
        self.logger.info("cosine_similarities: " + str(cosine_similarities))
        related_docs_indices = cosine_similarities.argsort()[:-5:-1]
        self.logger.info("related_docs_indices: " + str(related_docs_indices))

        end = time.time()
        self.logger.info("execute_query complete. elapsed time: " + str(end - start) + " secs")
