import logging
import time
import pickle
from gensim.corpora import Dictionary
from pathlib import Path
from passages.toppassage import TopPassage
from passages.passage import Passage
from utils import process_and_tokenize_string, progbar, dummy_func
from passages.scoretype import ScoreType
# import cProfile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel


class Indexer:
    """
      A class used to index DocumentStore

      Attributes
      ----------
      logger : Logger
          a formatted string to print out what the animal says
      posting_list : PostingList
          a formatted string to print out what the animal says
      document_store : Document
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

    def __init__(self, file_name=None):
        self.posting_list = None
        self.tf_idf = None
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

            if self.file_name:
                self.save()

    def create_from_docs(self, docs_json):
        # time and log
        start = time.time()
        self.logger.info("Creating documents...")

        # init variables
        self.docs = [None] * len(docs_json)

        # load documents and tokenize
        for i, key in enumerate(docs_json.keys()):
            progbar(i, len(self.docs), 20)
            doc = Passage(int(key),0, docs_json[key])
            self.docs[int(key)] = doc

        end = time.time()
        self.logger.info("Creating document complete. elapsed time: " + str(end - start) + " secs")

    def execute_query(self, query):
        start = time.time()
        self.logger.info(" Executing Query: '" + str(query) + "'")
        self.logger.debug(" Query tokens: " + str(process_and_tokenize_string(query)))

        # create question doc from query string
        query_tokens = process_and_tokenize_string(query)
        top_docs = [TopPassage(doc) for doc in self.docs]

        vectorizer = CountVectorizer(ngram_range=(1, 1),  tokenizer=dummy_func, preprocessor=dummy_func)
        vectorizer.fit(self.tokens_by_docs)

        query_vector = vectorizer.transform(query_tokens)

        for i in range(len(top_docs)):
            progbar(i, len(top_docs), 20)

            doc_vector = vectorizer.transform(top_docs[i].passage.get_tokens())

            cosine_similarities = linear_kernel(query_vector, [doc_vector]).flatten()

            top_docs[i].update_score(ScoreType.language_model, cosine_similarities)
            top_docs[i].calculate_score()

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

