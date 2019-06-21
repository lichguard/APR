from DocumentStore import *

path = ""


def main():
    ds = DocumentManager()

    ds.create(path + "document_passages.json")

    doc = ds.get_document_by_id(344)
    para = doc.get_paragraph_by_id(1)

    print(para.get_text())


if __name__ == '__main__':
    main()
