import logging
import time
import marisa_trie
from collections import defaultdict


class PostingList:
    logger = logging.getLogger('PostingList')

    def __init__(self, docs_by_tokens, dictionary):
        start = time.time()
        self.logger.info("Creating posting list (inverse index)...")

        self.token_trie_tree = marisa_trie.Trie(dictionary.token2id.keys())
        self.token2docs = [defaultdict(list) for _ in range(len(dictionary.token2id.keys()))]

        for doc_index, doc in enumerate(docs_by_tokens):
            for position, token in enumerate(doc):
                trie_token_index = self.token_trie_tree[token]
                self.token2docs[trie_token_index][doc_index].append(position)

        end = time.time()
        self.logger.info("create_inverse_index. elapsed time: " + str(end - start) + " secs")

        # pr = cProfile.Profile()
        # pr.enable()
        # pr.disable()
        # after your program ends
         # pr.print_stats(sort="calls")

    # returns a set of unique ids e.g. (1,5,2,5)
    def get_relevant_docs_ids(self, query_tokens):
        relevant_docs = set()
        for token in query_tokens:
            if token in self.token_trie_tree:
                relevant_docs.update(self.token2docs[self.token_trie_tree[token]].keys())
        return relevant_docs

    def get_tokens_intersection_count(self, query_tokens, source_doc):
        count = 0
        for token in query_tokens:
            if token in self.token_trie_tree:
                if source_doc.get_id() in self.token2docs[self.token_trie_tree[token]].keys():
                    count += 1

        return count / len(query_tokens)

    def get_proximity_score(self, query_tokens, source_doc, window_size=10):
        positions = []
        query_tokens = set(query_tokens)
        # find all relevant positions
        for token in query_tokens:
            if token in self.token_trie_tree:
                if source_doc.get_id() in self.token2docs[self.token_trie_tree[token]].keys():
                    positions += self.token2docs[self.token_trie_tree[token]][source_doc.get_id()]

        doc_tokens = source_doc.get_tokens()
        max_count = 0
        for position in positions:
            count = 0
            used_tokens = set()
            for position_index in range(position-window_size, position+window_size, 1):
                if position_index < 0 or position_index >= len(doc_tokens):
                    continue
                else:
                    token = doc_tokens[position_index]
                    if token in query_tokens and token not in used_tokens:
                        count += 1
                        used_tokens.add(token)
            if count > max_count:
                max_count = count
        return max_count / len(query_tokens)

    def get_passage_proximity_score(self, query_tokens, passage, window_size=10):
        doc_tokens = passage.get_tokens()
        max_count = 0
        for position in range(0, len(passage.get_tokens()), window_size):
            count = 0
            used_tokens = set()
            for position_index in range(position-window_size, position+window_size, 1):
                if position_index < 0 or position_index >= len(doc_tokens):
                    continue
                else:
                    token = doc_tokens[position_index]
                    if token in query_tokens and token not in used_tokens:
                        count += 1
                        used_tokens.add(token)
            if count > max_count:
                max_count = count
        return max_count / len(query_tokens)