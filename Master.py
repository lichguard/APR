from DocumentStore import *
from QuestionStore import *
path = ""


def main():
    ds = DocumentManager()
    qs = QuestionManager()

    ds.create(path + "document_passages.json")

    doc = ds.get_document_by_id(344)
    para = doc.get_paragraph_by_id(1)
    print(para.get_text())

    qs.create(path + "dev.tsv")
    print(str(qs.questions[0].question))


if __name__ == '__main__':
    main()
