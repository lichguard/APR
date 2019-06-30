import logging
import time
import pickle
from pathlib import Path
from sklearn import svm


class PassageClassifier:
    logger = logging.getLogger('PassageClassifier')

    def __init__(self, file_name='test'):
        self.svm_model = svm.SVC(kernel='linear', C=1)
        self.file_name = file_name

    def train(self, x, y):
        self.svm_model.fit(x, y)
        self.save()

    def predict(self, x):
        return self.svm_model.predict(x)

    def load(self):
        full_file_name = "data\\cache\\" + self.file_name + "_svm.arp"

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
        full_file_name = "data\\cache\\" + self.file_name + "_svm.arp"
        f = open(full_file_name, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()
        self.logger.info("Successfully saved indexer data from " + full_file_name)



