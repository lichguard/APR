from utils import process_and_tokenize_string


class Document:

    def __init__(self, _id=None, text=None):
        self.tokens = process_and_tokenize_string(text)
        self.text = text
        self._id = _id

    def get_text(self):
        return self.text

    def get_tokens(self):
        return self.tokens

    def get_id(self):
        return self._id
