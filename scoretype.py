from enum import Enum


class ScoreType(Enum):
    tf_idf = 0
    jaccard = 1
    proximity = 2
