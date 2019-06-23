import json
import logging
from utils import process_and_tokenize_string
import time
import pickle


class Paragraph:
    paragraph_id = None
    data = None
    tokens = None
    file_name = 'data/document_store_v1'

    def __init__(self, paragraph_id, data):
        self.paragraph_id = paragraph_id
        self.data = data
        self.tokens = process_and_tokenize_string(data)

    def get_text(self):
        return self.data


class Document:
    paragraphs = []
    doc_id = None

    def __init__(self, doc_id=None, paragraphs_json=None):
        if doc_id is None:
            return
        self.paragraphs = [None] * len(paragraphs_json)
        for key in paragraphs_json.keys():
            self.doc_id = doc_id
            self.paragraphs[int(key)] = Paragraph(int(key), paragraphs_json[key])

    def get_paragraph_by_id(self, para_id):
        return self.paragraphs[para_id]

    def get_text(self):
        return ' '.join([x.get_text() for x in self.paragraphs])
        # return "document " + str(self.doc_id)

    def get_tokens(self):
        tokens = []
        for p in self.paragraphs:
            tokens = tokens + p.tokens
        return tokens


class DocumentManager:
    logger = logging.getLogger('DocumentManager')
    docs = None
    token_set = None

    def __init__(self):
        pass

    def create(self, file_path):
        # time and log
        start = time.time()
        self.logger.info("Creating documents...")

        # load file from directory
        with open(file_path) as f:
            docs_json = json.load(f)

        # init variables
        self.docs = [None] * len(docs_json)
        self.token_set = set()

        # load documents and tokenize
        for key in docs_json.keys():
            doc = Document(int(key), docs_json[key])
            self.docs[int(key)] = doc
            # bag of words
            self.token_set.update(doc.get_tokens())

        end = time.time()
        self.logger.info("Creating document complete. elapsed time: " + str(end - start) + " secs")

    def get_document_by_id(self, doc_id):
        return self.docs[doc_id]

    def save(self):
        f = open(self.file_name, 'wb')
        pickle.dump(self.docs, f)
        f.close()

        self.logger.info("Successfully saved document store data to " + self.file_name)

    def load(self):
        f = open(self.file_name, 'rb')
        self.docs = pickle.load(f)
        f.close()

        self.logger.info("Successfully loaded document store data from " + self.file_name)
