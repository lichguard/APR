from indexer import Indexer
import logging
import json


def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


def run():
    #DOC_SOURCE_FILE = "document_passages_shorten_2"
    #DOC_SOURCE_FILE = "document_passages_shorten"
    DOC_SOURCE_FILE = "document_passages"
    query_string = "Who runs the administration of the euro?"
    reindex = True

    # load file from directory
    with open("data\\" + DOC_SOURCE_FILE + ".json") as f:
        docs_json = json.load(f)

    indexer = Indexer("data\\cache\\" + DOC_SOURCE_FILE + "_documents")
    indexer.index({x: ' '.join(docs_json[x].values()) for x in docs_json}, reindex)
    top_docs = indexer.execute_query(query_string)

    print("Documents: ")
    print(top_docs[0:10])

    if top_docs:
        passages = docs_json[str(top_docs[0].get_doc().get_id())]
        indexer = Indexer("data\\cache\\" + DOC_SOURCE_FILE + "_doc_" + str(top_docs[0].get_doc().get_id()) + "_passages")
        indexer.index(passages, reindex)
        top_docs = indexer.execute_query(query_string)

        print("Passages: ")
        print(passages)
        print(top_docs)
    # qs = QuestionManager()
    # qs.create("data\\dev.tsv")
    # doc = ds.get_document_by_id(1)
    # para = doc.get_paragraph_by_id(0)
    # print(doc.get_tokens())

    # print(str(qs.questions[0].question))


if __name__ == '__main__':
    main()
