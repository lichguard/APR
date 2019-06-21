import json

class Paragraph:
    paragraph_id = None
    data = None

    def __init__(self, paragraph_id, data):
        self.paragraph_id = paragraph_id
        self.data = data

    def get_text(self):
        return self.data


class Document:
    paragraphs = {}
    doc_id = None

    def __init__(self, doc_id, paragraphs_json):
        self.paragraphs = [None] * len(paragraphs_json)
        for key in paragraphs_json.keys():
            self.doc_id = doc_id
            self.paragraphs[int(key)] = Paragraph(int(key), paragraphs_json[key])

    def get_paragraph_by_id(self, para_id):
        return self.paragraphs[para_id]


class DocumentManager:
    docs = None

    def __init__(self):
        pass

    def create(self, file_path):

        with open(file_path) as f:
            docs_json = json.load(f)

        self.docs = [None] * len(docs_json)
        for key in docs_json.keys():
            self.docs[int(key)] = Document(int(key), docs_json[key])

    def get_document_by_id(self, doc_id):
        return self.docs[doc_id]
