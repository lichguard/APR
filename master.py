from documents.document_indexer import Indexer as Documents_Indexer
from passages.passage_indexer import PassageIndexer
import logging
import json
from QuestionStore import QuestionManager
from utils import process_and_tokenize_string


def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


def load_json_from_file(doc_source_file):
    with open("data\\" + doc_source_file + ".json") as f:
        docs_json = json.load(f)
    return docs_json


def load_questions(question_source_file):
    qs = QuestionManager()
    qs.create("data\\" + question_source_file)
    return qs


def run():
    #SETTINGS
    #doc_source_file = "document_passages_shorten_2"
    #doc_source_file = "document_passages_shorten"
    doc_source_file = "document_passages"
    query_string = r"How did Elvis perceive the music he had to sing in his movies?"
    reindex_documents = False
    reindex_passages = True

    docs_json = load_json_from_file(doc_source_file)
    docs_indexer = Documents_Indexer(doc_source_file)
    passage_indexer = PassageIndexer(doc_source_file)

    #score_documents_retrieval(docs_json, docs_indexer, passage_indexer)
    #return

    docs = {x: ' '.join(docs_json[x].values()) for x in docs_json}
    docs_indexer.index(docs, reindex_documents)
    top_docs = docs_indexer.execute_query(query_string)
    print("Documents: ")
    print(top_docs[0])

    sliced_docs = {top_doc.doc.get_id(): docs_json[str(top_doc.doc.get_id())] for top_doc in top_docs[0:1]}
    passage_indexer.index(sliced_docs, reindex_passages)
    top_passages = passage_indexer.execute_query(query_string)
    print("Passages: ")
    print(top_passages[0:5])
    print(docs_json[str(top_docs[0].doc.get_id())][str(top_passages[0].passage.get_id())])
    print(process_and_tokenize_string(docs_json[str(top_docs[0].doc.get_id())][str(top_passages[0].passage.get_id())]))

    print(docs_json[str(top_docs[0].doc.get_id())][str(64)])
    print(process_and_tokenize_string(docs_json[str(top_docs[0].doc.get_id())][str(64)]))


def score_documents_retrieval(docs_json, document_indexer,passage_indexer):

    count = 0
    start = 5
    question_count = 1
    qs = load_questions('train.tsv')
    document_indexer.index(None, False)

    for i in range(start, start + question_count):

        query = qs.questions[i]
        top_docs = document_indexer.execute_query(query.question)
        sliced_docs = {top_doc.doc.get_id(): docs_json[str(top_doc.doc.get_id())] for top_doc in top_docs[0:1]}
        passage_indexer.index(sliced_docs, True)
        top_passages = passage_indexer.execute_query(query.question)

        print('\nExpected: document: ' + str(qs.questions[i].document_id) + " Passages: " + str(qs.questions[i].passages))
        print('Results:\n' + str(top_passages[0:10]))

        #if qs.questions[i].document_id == top_docs[0].doc.get_id():
        #    print("Success! Expected: " + str(qs.questions[i].document_id) + " Result: " + str(top_docs[0].doc.get_id()))
        #    count += 1
        #else:
        #    print("Fail! Expected: " + str(qs.questions[i].document_id) + " Result: " + str(top_docs[0].doc.get_id()))

    #print("Final tally: " + str(count) + " correct out of " + str(questions) + "(" + str(count/questions) + ")")


def print_questions(docs_json):
    qs = QuestionManager()
    qs.create("data\\train.tsv")
    for i in range(200):
        print(" ")
        print(i)
        print((qs.questions[i].question))
        print((docs_json[str(qs.questions[i].document_id)][str(qs.questions[i].passages[0])]))
        print(process_and_tokenize_string(qs.questions[i].question))
        print(process_and_tokenize_string(docs_json[str(qs.questions[i].document_id)][str(qs.questions[i].passages[0])]))


if __name__ == '__main__':
    main()
