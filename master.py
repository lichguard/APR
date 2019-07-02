from documents.document_indexer import Indexer as Documents_Indexer
from passages.passage_indexer import PassageIndexer
import logging
import json
from utils import process_and_tokenize_string, load_json_from_file, load_questions


def main():
    logging.basicConfig(level=logging.NOTSET)
    run()


#SETTINGS
doc_source_file = "document_passages"
query_string = r"How were the Olympics games broadcasted?"
reindex_documents = False
reindex_passages = True


def run():
    docs_json = load_json_from_file(doc_source_file)
    docs_indexer = Documents_Indexer(doc_source_file)
    passage_indexer = PassageIndexer(doc_source_file)

    #score_documents_retrieval(docs_json, docs_indexer, passage_indexer)
    export_to_file(docs_json, docs_indexer, passage_indexer)
    #single_query(docs_json, docs_indexer, passage_indexer)


def score_documents_retrieval(docs_json, document_indexer,passage_indexer):

    count = 0
    start = 70
    question_count = 20
    qs = load_questions('test.tsv')
    document_indexer.index(None, False)

    for i in range(start, start + question_count):

        query = qs.questions[i]
        top_docs = document_indexer.execute_query(query.question)
        sliced_docs = {top_doc.doc.get_id(): docs_json[str(top_doc.doc.get_id())] for top_doc in top_docs[0:3]}
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


def single_query(docs_json, document_indexer, passage_indexer):
    docs = {x: ' '.join(docs_json[x].values()) for x in docs_json}
    document_indexer.index(docs, reindex_documents)
    top_docs = document_indexer.execute_query(query_string)
    print("Documents: ")
    print(top_docs[0:5])

    sliced_docs = {top_doc.doc.get_id(): docs_json[str(top_doc.doc.get_id())] for top_doc in top_docs[0:3]}
    passage_indexer.index(sliced_docs, reindex_passages)
    top_passages = passage_indexer.execute_query(query_string)
    print("Passages: ")
    print(top_passages)
    print(docs_json[str(top_docs[0].doc.get_id())][str(top_passages[0].passage.get_id())])
    print(process_and_tokenize_string(docs_json[str(top_docs[0].doc.get_id())][str(top_passages[0].passage.get_id())]))

    #print(docs_json[str(top_docs[0].doc.get_id())][str(1)])
    #print(process_and_tokenize_string(docs_json[str(top_docs[0].doc.get_id())][str(1)]))


def export_to_file(docs_json, document_indexer,passage_indexer):
    if reindex_documents:
        print('reindexing_documents is on.. refusing to export to file')
        return

    data = []  # load_json_from_file('answers')
    start = 0

    qs = load_questions('test.tsv')
    document_indexer.index(docs_json, reindex_documents)
    question_count = len(qs.questions)
    for i in range(start, start + question_count):
        query = qs.questions[i]
        answers = []
        response = dict()
        response['id'] = query.qid
        response['answers'] = answers
        try:
            print('Processing question: ' + str(query.qid) + " (" + str(i) + ")")
            top_docs = document_indexer.execute_query(query.question)
            sliced_docs = {top_doc.doc.get_id(): docs_json[str(top_doc.doc.get_id())] for top_doc in top_docs[0:2]}
            passage_indexer.index(sliced_docs, False)
            top_passages = passage_indexer.execute_query(query.question)
            for j in range(5):
                answer = {'answer': str(top_passages[j].passage.get_doc_id()) + ':' + str(top_passages[j].passage.get_id()), 'score': str(top_passages[j].get_score())}
                answers.append(answer)
            data.append(response)
        except Exception as e:
            print("error")

    with open('data\\answers.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)


def print_questions(docs_json):
    qs = load_questions('test.tsv')
    for i in range(200):
        print(" ")
        print(i)
        print(qs.questions[i].question)
        print(docs_json[str(qs.questions[i].document_id)][str(qs.questions[i].passages[0])])
        print(process_and_tokenize_string(qs.questions[i].question))
        print(process_and_tokenize_string(docs_json[str(qs.questions[i].document_id)][str(qs.questions[i].passages[0])]))


if __name__ == '__main__':
    main()
