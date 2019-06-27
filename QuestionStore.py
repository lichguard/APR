import csv
from utils import process_and_tokenize_string


class Question:

    def __init__(self, qid, question, document_id=None, document_name=None, passages=None):
        self.qid = qid
        self.question = question
        self.document_id = int(document_id)
        self.document_name = document_name
        self.passages = passages

    def __str__(self):
        return str(self.qid) + "\t" + str(self.question) + "\t" + str(self.document_id) + "\t" + str(self.document_name) + "\t" + \
               str(self.passages) + "\n"

    def __repr__(self):
        return self.__str__()


class QuestionManager:
    questions = []

    def __init__(self):
        pass

    def create(self, file_path):
        self.questions = []
        with open(file_path) as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            # ignores header row
            next(rd)
            for row in rd:
                self.questions.append(Question(row[0], row[1], row[2], row[3],
                                           [x.strip() for x in str(row[4]).split(',')]))

