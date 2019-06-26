from indexer import Indexer
import logging
import json
from QuestionStore import QuestionManager


def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


def run():
    #DOC_SOURCE_FILE = "document_passages_shorten_2"
    #DOC_SOURCE_FILE = "document_passages_shorten"
    DOC_SOURCE_FILE = "document_passages"
    query_string = "What significance did Bulgaria have in the ending of World War I?"
    reindex = False

    # load file from directory
    with open("data\\" + DOC_SOURCE_FILE + ".json") as f:
        docs_json = json.load(f)

    indexer = Indexer("data\\cache\\" + DOC_SOURCE_FILE + "_documents")
    indexer.index({x: ' '.join(docs_json[x].values()) for x in docs_json}, reindex)

    count = 0 
    questions = 10
    qs = QuestionManager()
    qs.create("data\\train.tsv")

    for i in range(questions):
        top_docs = indexer.execute_query(qs.questions[i].question)
        if qs.questions[i].document_id == top_docs[0].doc.get_id():
            print("Success!")
            count += 1
        else:
            print("correct: " + str(qs.questions[i].document_id))
            print("given: " + str(top_docs[0].doc.get_id()))
            print("Fail!")
            
    print("Final tally: " + str(count) + " correct out of " + str(questions) + "(" + str(count/questions) + ")")

    """
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
    """


if __name__ == '__main__':
    main()
