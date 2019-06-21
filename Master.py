from DocumentStore import *
from QuestionStore import *
path = ""


def main():
    ds = DocumentManager()
    ds.create(path + "data\\document_passages.json")
    qs = QuestionManager()
    qs.create(path + "data\\dev.tsv")

    doc = ds.get_document_by_id(344)
    para = doc.get_paragraph_by_id(1)
    print(para.get_text())

    print(str(qs.questions[0].question))


if __name__ == '__main__':
    main()
