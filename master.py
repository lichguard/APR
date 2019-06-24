from DocumentStore import DocumentManager
from indexer import Indexer
import logging


def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


DOC_SOURCE_FILE = "data\\document_passages"


def run():

    ds = DocumentManager(DOC_SOURCE_FILE)
    #ds.create()
    #ds.save()
    ds.load()

    indexer = Indexer(ds)
    #indexer.index()
    #indexer.save()
    indexer.load()

    top_docs = indexer.execute_query("What is a municipality?")

    # qs = QuestionManager()
    # qs.create("data\\dev.tsv")
    # doc = ds.get_document_by_id(1)
    # para = doc.get_paragraph_by_id(0)
    # print(doc.get_tokens())

    # print(str(qs.questions[0].question))


if __name__ == '__main__':
    main()
