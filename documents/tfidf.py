import logging
import time
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import dummy_func


class TfIdf:
    logger = logging.getLogger('TfIdf')

    def __init__(self, tokens_by_docs):
        start = time.time()
        self.vectorizer = TfidfVectorizer(analyzer='word', tokenizer=dummy_func, preprocessor=dummy_func)
        self.vectorizer.fit(tokens_by_docs)
        end = time.time()
        self.logger.info("completed in " + str(end - start) + " secs")

    def query(self, query_tokens, source_docs):
        if not source_docs:
            return None

        start = time.time()
        self.logger.info("Executing tf_idf query on " + str(len(source_docs)) + " items")
        docs_vector = self.vectorizer.transform([doc.get_tokens() for doc in source_docs])
        query_vector = self.vectorizer.transform([query_tokens])
        cosine_similarities = cosine_similarity(query_vector, docs_vector).flatten()
        end = time.time()
        self.logger.info("completed in " + str(end - start) + " secs")
        return cosine_similarities

    def get_tokens_value(self, query_tokens=None):
        vector = self.vectorizer.transform([query_tokens])
        token_vector = {}
        for i, index in enumerate(vector.indices):
            token_vector[self.vectorizer.get_feature_names()[index]] = vector.data[i]
        return token_vector
