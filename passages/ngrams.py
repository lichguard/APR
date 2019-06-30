import logging
import time
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from utils import dummy_func


class Ngrams:
    logger = logging.getLogger('Ngrams')

    def __init__(self, tokens_by_docs):
        start = time.time()
        self.vectorizer = CountVectorizer(ngram_range=(1, 7),  tokenizer=dummy_func, preprocessor=dummy_func, binary=True)
        self.vectorizer.fit(tokens_by_docs)
        end = time.time()
        self.logger.info("completed in " + str(end - start) + " secs")

    def query(self, query_tokens, source_docs):
        if not source_docs:
            return None

        start = time.time()
        self.logger.info("Executing ngram query on " + str(len(source_docs)) + " items")

        docs_vecotor = self.vectorizer.transform([doc.get_tokens() for doc in source_docs])
        query_vector = self.vectorizer.transform([query_tokens])

        cosine_similarities = linear_kernel(query_vector, docs_vecotor).flatten()

        end = time.time()
        self.logger.info("completed in " + str(end - start) + " secs")
        return cosine_similarities
