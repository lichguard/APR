from collections import defaultdict
import operator
from documents.scoretype import ScoreType


class TopDoc:

    def __init__(self, doc):
        self.doc = doc
        self.scores = defaultdict(float)
        self.score = 0

    def get_doc(self):
        return self.doc

    def update_score(self, score_type, score):
        self.scores[score_type] = score

    def calculate_score(self):
        self.score = 0
        self.score += self.scores[ScoreType.tf_idf] * 0.8
        self.score += self.scores[ScoreType.proximity] * 0.2

    def __str__(self):
        output = "(doc " + str(self.doc.get_id()) + ", score " + str(self.score) + ")"
        for key in self.scores.keys():
            output += "\t" + str(key) + " score: " + str(self.scores[key])
        return output

    def __repr__(self):
        return "\n" + str(self)

    def display(self):
        return sorted(self.scores.items(), key=operator.itemgetter(1), reverse=True)
