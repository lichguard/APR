import logging
import time
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


def dummy_fun(doc):
    return doc


class TfIdf:
    logger = logging.getLogger('TfIdf')

    def __init__(self, tokens_by_docs):
        start = time.time()
        """
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
        """
        self.tf_idf_vectorizer = TfidfVectorizer(analyzer='word', tokenizer=dummy_fun,preprocessor=dummy_fun, token_pattern=None)
        self.tf_idf_vectorizer.fit(tokens_by_docs)

        end = time.time()
        self.logger.info("create_tf_idf complete. elapsed time: " + str(end - start) + " secs")
        # print(tf_idf_vectorizer.vocabulary_)
        # print(tf_idf_vectorizer.idf_))

    def query(self, query_tokens, source_docs):
        if not source_docs:
            return None

        start = time.time()
        self.logger.info("Executing tf_idf query")

        docs_vecotr = self.tf_idf_vectorizer.transform([doc.get_tokens() for doc in source_docs])
        query_vector = self.tf_idf_vectorizer.transform([query_tokens])

        cosine_similarities = linear_kernel(query_vector, docs_vecotr).flatten()

        end = time.time()
        self.logger.info("tf_idf query complete. elapsed time: " + str(end - start) + " secs")
        return cosine_similarities
