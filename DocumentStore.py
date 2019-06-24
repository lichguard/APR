import json
import logging
from utils import process_and_tokenize_string
import time
import pickle


class Paragraph:

    def __init__(self, paragraph_id, data):
        self.paragraph_id = paragraph_id
        self.data = data
        self.tokens = process_and_tokenize_string(data)

    def get_text(self):
        return self.data


class Document:

    def __init__(self, doc_id=None, paragraphs_json=None):
        self.paragraphs = []
        self.tokens = []

        if doc_id is None:
            return

        self.paragraphs = [None] * len(paragraphs_json)
        for key in paragraphs_json.keys():
            self.doc_id = doc_id
            self.paragraphs[int(key)] = Paragraph(int(key), paragraphs_json[key])

        self.recalculate_tokens()

    def get_paragraph_by_id(self, para_id):
        return self.paragraphs[para_id]

    def get_text(self):
        return ' '.join([x.get_text() for x in self.paragraphs])
        # return "document " + str(self.doc_id)

    def recalculate_tokens(self):
        for p in self.paragraphs:
            self.tokens = self.tokens + p.tokens

    def get_tokens(self):
        return self.tokens


class DocumentManager:
    logger = logging.getLogger('DocumentManager')

    def __init__(self, file_name):
        self.file_name = file_name
        self.docs = None
        self.token_set = None

    def create(self):
        # time and log
        start = time.time()
        self.logger.info("Creating documents...")

        # load file from directory
        with open(self.file_name + ".json") as f:
            docs_json = json.load(f)

        # init variables
        self.docs = [None] * len(docs_json)
        self.token_set = set()

        # load documents and tokenize
        for key in docs_json.keys():
            progbar
            doc = Document(int(key), docs_json[key])
            self.docs[int(key)] = doc
            # bag of words
            self.token_set.update(doc.get_tokens())

        end = time.time()
        self.logger.info("Creating document complete. elapsed time: " + str(end - start) + " secs")

    def get_document_by_id(self, doc_id):
        return self.docs[doc_id]

    def load(self):
        f = open(self.file_name + "_ds.arp", 'rb')
        tmp_dict = pickle.load(f)
        f.close()
        self.__dict__.clear()
        self.__dict__.update(tmp_dict)
        self.logger.info("Successfully loaded document store data to " + self.file_name)

    def save(self):
        f = open(self.file_name + "_ds.arp", 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()
        self.logger.info("Successfully saved document store data from " + self.file_name)