# Libraries
import os
import pickle
import helpers
from nltk.corpus import stopwords
from contextlib import ExitStack

# Data Structures
from collections import deque

def offloadInvertedIndex(ii_folder: str, letter: str, inverted_indx: dict):
    file_name = "{}/inverted_indx_{}".format(ii_folder, letter)
    with open(file_name, "wb") as open_file:
        pickle.dump(inverted_indx, open_file, protocol = pickle.HIGHEST_PROTOCOL)


def mergePartialIndexes(pi_folder: str, ii_folder: str, report_file: str):
    with ExitStack() as stack:
        doc_queue = [stack.enter_context(open('{}/{}'.format(pi_folder, pi_file), 'rb')) for pi_file in os.listdir(pi_folder)]

        token_postings = []
        for pi_file in doc_queue:
            try:
                token_postings.append(pickle.load(pi_file))
            except EOFError:
                continue

        letters = deque(['b','c','d','e','f','g','h','i','j','k','l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
        letter = 'a'

        inverted_index = {}
        while token_postings:
            token, postings = min(token_postings, key = lambda x : x[0])
            min_index = token_postings.index(min(token_postings, key = lambda x : x[0]))

            if token[0] != letter:
                offloadInvertedIndex(ii_folder, letter, inverted_index)
                letter = letters.popleft()
                inverted_index = {}

            if token not in inverted_index:
                inverted_index[token] = postings
            else:
                inverted_index[token].extend(postings)

            try:
                token_postings[min_index] = pickle.load(doc_queue[min_index])
            except EOFError:
                token_postings.remove(token_postings[min_index])
                doc_queue.remove(doc_queue[min_index])
        offloadInvertedIndex(ii_folder, letter, inverted_index)


mergePartialIndexes("partial_indx_0512", "inverted_indx_0512", "reports/m1_0512")