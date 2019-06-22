from DocumentStore import *
from indexer import Indexer
from utils import *
import logging


def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


def run():

    indexer = Indexer()
    ds = DocumentManager()
    ds.create("data\\document_passages.json")
    indexer.index(ds.docs)
    top_docs = indexer.execute_query("How did Italy get its name")
    print(top_docs.display())
    # qs = QuestionManager()
    # qs.create("data\\dev.tsv")


    # doc = ds.get_document_by_id(1)
    # para = doc.get_paragraph_by_id(0)
    # print(doc.get_tokens())

    # print(str(qs.questions[0].question))



if __name__ == '__main__':
    main()
