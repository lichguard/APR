from DocumentStore import *
from indexer import Indexer
from utils import *
import logging


def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


def run():
    ds = DocumentManager()
    ds.create("data\\document_passages.json")
    # ds.save()
    # ds.load()

    indexer = Indexer()
    indexer.index(ds)

    top_docs = indexer.execute_query("try to work smarter not harder working hard")

    # qs = QuestionManager()
    # qs.create("data\\dev.tsv")
    # doc = ds.get_document_by_id(1)
    # para = doc.get_paragraph_by_id(0)
    # print(doc.get_tokens())

    # print(str(qs.questions[0].question))


if __name__ == '__main__':
    main()
