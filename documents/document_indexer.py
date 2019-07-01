import logging
import time
import pickle
from gensim.corpora import Dictionary
from pathlib import Path
from documents.topdoc import TopDoc
from documents.document import Document
from utils import process_and_tokenize_string, progbar
from documents.scoretype import ScoreType
from documents.postinglist import PostingList
from documents.tfidf import TfIdf
# import cProfile
from statistics import mean

class Indexer:
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

            self.posting_list = PostingList(self.tokens_by_docs, self.dictionary)
            self.tf_idf = TfIdf(self.tokens_by_docs)
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
            doc = Document(int(key), docs_json[key])
            self.docs[int(key)] = doc

        end = time.time()
        self.logger.info("Creating document complete. elapsed time: " + str(end - start) + " secs")

    def execute_query(self, query):
        start = time.time()
        self.logger.info(" Executing Query: '" + str(query) + "'")
        self.logger.debug(" Query tokens: " + str(process_and_tokenize_string(query)))

        # create question doc from query string
        query_tokens = process_and_tokenize_string(query)
        #ngrams = generate_ngrams(query_tokens,3)
        query_tokens_tfidf = self.tf_idf.get_tokens_value(query_tokens)
        avg = mean(query_tokens_tfidf.values())
        query_tokens_tfidf = {k: v for k, v in query_tokens_tfidf.items() if v >= avg}

        relevant_doc_ids = self.posting_list.get_relevant_docs_ids(query_tokens_tfidf.keys())

        relevant_docs = [self.docs[i] for i in relevant_doc_ids]
        top_docs = [TopDoc(self.docs[i]) for i in relevant_doc_ids]

        self.logger.debug("filtered: " + str(len(top_docs)) + " docs ( pool: " + str(len(self.docs)) + ") with tokens " + str(query_tokens_tfidf))
        tf_idf_scores = self.tf_idf.query(query_tokens, relevant_docs)


        for i in range(len(top_docs)):
            progbar(i, len(top_docs), 20)

            top_docs[i].update_score(ScoreType.tf_idf, tf_idf_scores[i])

            top_docs[i].update_score(ScoreType.proximity,
                                     self.posting_list.get_proximity_score(
                    query_tokens, top_docs[i].doc, 6) * 0.5
                                     +
                                     self.posting_list.get_proximity_score(
                     query_tokens, top_docs[i].doc, 10) * 0.4
                                     +
                                     self.posting_list.get_proximity_score(
                    query_tokens, top_docs[i].doc, 40) * 0.1
                                     )

            top_docs[i].calculate_score()
        print(' ')
        top_docs.sort(key=lambda x: x.score, reverse=True)

        end = time.time()
        self.logger.info("execute_query complete. elapsed time: " + str(end - start) + " secs")
        return top_docs

    def load(self):
        full_file_name = "data\\cache\\" + self.file_name + "_documents.arp"

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
        full_file_name = "data\\cache\\" + self.file_name + "_documents.arp"
        f = open(full_file_name, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()
        self.logger.info("Successfully saved indexer data from " + full_file_name)

