# APR
he goal of this project is to implement a Question Answering (QA) system that answers questions.
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
The program accepts a large corpus of documents divided to passages
e.g.
{
  "12": {"0":"doc1 passage1..", "10": "doc1 passage2"},
  "15": {"1":"doc2 passge1", "23":"doc2 passage2"}
}