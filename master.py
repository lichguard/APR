from documents.document_indexer import Indexer as Documents_Indexer
from passages.passage_indexer import Indexer as Passages_Indexer
import logging
import json
from QuestionStore import QuestionManager
from utils import process_and_tokenize_string

def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


def create_document_indexer(doc_source_file, reindex):
    # load file from directory
    with open("data\\" + doc_source_file + ".json") as f:
        docs_json = json.load(f)

    indexer = Documents_Indexer(doc_source_file + "_documents")
    #indexer.index({x: ' '.join(docs_json[x].values()) for x in docs_json}, reindex)
    return docs_json, indexer


def create_passages_indexer(doc_id, docs_json, doc_source_file, reindex):
    doc_id = str(doc_id)
    passages = docs_json[doc_id]
    indexer = Passages_Indexer(doc_source_file + "_doc_" + doc_id + "_passages")
    indexer.index(passages, reindex)
    return indexer


def run():
    #doc_source_file = "document_passages_shorten_2"
    #doc_source_file = "document_passages_shorten"
    doc_source_file = "document_passages"
    query_string = "What is the rationale of support of the Common Era?"
    reindex = False

    docs_json, docs_indexer = create_document_indexer(doc_source_file, reindex)

    #top_docs = docs_indexer.execute_query(query_string)
    #print("Documents: ")
    #print(top_docs[0:10])

    doc_id = 204  # str(top_docs[0].get_doc().get_id())
    passage_indexer = create_passages_indexer(doc_id, docs_json,doc_source_file, reindex)
    top_passages = passage_indexer.execute_query(query_string)
    print("Passages: ")
    print(top_passages)


def score_documents_retrival(docs_json, indexer):

    count = 0
    questions = 10
    qs = QuestionManager()
    qs.create("data\\train.tsv")

    for i in range(questions):
        top_docs = indexer.execute_query(qs.questions[i].question)
        if qs.questions[i].document_id == top_docs[0].doc.get_id():
            print("Success! Expected: " + str(qs.questions[i].document_id) + " Result: " + str(top_docs[0].doc.get_id()))
            count += 1
        else:
            print("Fail! Expected: " + str(qs.questions[i].document_id) + " Result: " + str(top_docs[0].doc.get_id()))

    print("Final tally: " + str(count) + " correct out of " + str(questions) + "(" + str(count/questions) + ")")


def printquestions(docs_json):
    qs = QuestionManager()
    qs.create("data\\train.tsv")
    for i in range(200):
        print(" ")
        print(i)
        print(process_and_tokenize_string(qs.questions[i].question))
        print(process_and_tokenize_string(docs_json[str(qs.questions[i].document_id)][str(qs.questions[i].passages[0])]))



if __name__ == '__main__':
    main()
