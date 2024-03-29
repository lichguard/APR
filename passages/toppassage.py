from collections import defaultdict
from passages.scoretype import ScoreType


class TopPassage:

    def __init__(self, passage):
        self.passage = passage
        self.scores = defaultdict(float)
        self.score = 0

    def get_passage(self):
        return self.passage

    def update_score(self, score_type, score):
        self.scores[score_type] = score

    def calculate_score(self):
        self.score = 0
        self.score += self.scores[ScoreType.ngram] * 0.8
        self.score += self.scores[ScoreType.expanded_ngram] * 0.2

    def get_score(self):
        return self.score

    def __str__(self):
        output = "Document:  " + str(self.passage.get_doc_id()) + " Passage: " + str(self.passage.get_id()) + " Score " + str(self.score)
        for key in self.scores.keys():
            output += "\t" + str(key) + " score: " + str(self.scores[key])
        return output

    def __repr__(self):
        return "\n" + str(self)
