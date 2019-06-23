import json
import logging
from utils import process_and_tokenize_string
import time
import pickle

class Paragraph:
    paragraph_id = None
    data = None
    tokens = None

    def __init__(self, paragraph_id, data):
        self.paragraph_id = paragraph_id
        self.data = data
        self.tokens = process_and_tokenize_string(data)

    def get_text(self):
        return self.data


class Document:
    paragraphs = []
    doc_id = []

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

    def __init__(self):
        pass

    def create(self, file_path):
        start = time.time()
        self.logger.info("Creating documents...")
        with open(file_path) as f:
            docs_json = json.load(f)

        self.docs = [None] * len(docs_json)

        for key in docs_json.keys():
            self.docs[int(key)] = Document(int(key), docs_json[key])

        end = time.time()
        self.logger.info("Creating document complete. elapsed time: " + str(end - start) + " secs")

    def get_document_by_id(self, doc_id):
        return self.docs[doc_id]

    def save(self):
        f = open('data/document_store_v1', 'wb')
        pickle.dump(self.docs, f)
        f.close()
        self.logger.info("Successfully saved document store data to data/document_store_v1")

    def load(self):
        f = open('data/document_store_v1', 'rb')
        self.docs = pickle.load(f)
        f.close()
        self.logger.info("Successfully loaded document store data from data/document_store_v1")
