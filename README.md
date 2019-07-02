# APR
the goal of this project is to implement a Question Answering (QA) system that answers questions.
We use Wikipedia as a knowledge base, extracting answers to user questions from the articles.

## Required Libraries
scipy 1.1.0

nltk 3.3

gensim 3.6.0

marisa_trie 0.7.5

numpy 1.16.0

PyStemmer 1.3.0

scikit_learn 0.21.2

# Startup
The main function resides in master.py.

inside run function you choose the function you want to run by commenting the other function

There are 4 settings to consider
doc_source_file - The document filename 
if you want to run a custom query  - query_string
if you wish to index again the documents or load previous indexed (must run at least once)- reindex_documents
(ignore, setting is not active) - reindex_passages

The program accepts a collection  of documents divided into passages as a json file
e.g.
{
  "12": {"0":"doc1 passage1..", "10": "doc1 passage2"},
  "15": {"1":"doc2 passge1", "23":"doc2 passage2"}
}

for the question file input it must be a tsv
e.g.
QID	Question	DocumentID	DocumentName	RelevantPassages
3086	What is the role of conversionism in Evangelicalism?	672	Evangelicalism.html	4


IMPORTANT: all files should be inside the project directory inside a folder named "data"
