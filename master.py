from DocumentStore import DocumentManager
from indexer import Indexer
import logging


DOC_SOURCE_FILE = "data\\document_passages"
query_string = "How quickly did information technology advance following the invention of the transistor?"
reindex = True


def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


def run():
    ds = DocumentManager(DOC_SOURCE_FILE)
    if reindex:
        ds.create()
        ds.save()
    else:
        ds.load()

    indexer = Indexer(ds)
    if reindex:
        indexer.index()
        indexer.save()
    else:
        indexer.load()

    top_docs = indexer.execute_query(query_string)
    print(top_docs[0:10])
    if top_docs:
        print("Doc id: " + str(top_docs[0].doc.doc_id))
        print(top_docs[0].doc.get_text())
    # qs = QuestionManager()
    # qs.create("data\\dev.tsv")
    # doc = ds.get_document_by_id(1)
    # para = doc.get_paragraph_by_id(0)
    # print(doc.get_tokens())

    # print(str(qs.questions[0].question))


if __name__ == '__main__':
    main()
