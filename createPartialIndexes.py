# Standard Library
import os
import sys
import json
import pickle

# Other Libraries
import helpers
from bs4 import BeautifulSoup

# Data Structures
from collections import deque
from postings import Posting


def offLoadPartialIndx(folder: str, partial_indx: dict, num: int):
    file_name = "{}/partial_indx{}".format(folder, num)
    with open(file_name, "wb") as open_file:
        for token, postings in sorted(partial_indx.items()):
            pickle.dump((token, postings), open_file, protocol = pickle.HIGHEST_PROTOCOL)
        print("Created:", file_name)


def constructPartialIndexes(directory: str, partial_indx_folder: str):
    partial_indx = {}
    partial_indx_qty = 1
    
    doc_queue = helpers.queueOfDirectoryFiles(directory)
    doc_id = 1
    id_url_dict = {}

    while doc_queue:
        if len(doc_queue) % 1000 == 0: print(len(doc_queue))
        doc = doc_queue.popleft()

        with open(doc) as doc_file: data = json.load(doc_file)

        if data["encoding"] not in ['utf-8', 'ascii']: continue
        id_url_dict[doc_id] = data["url"]
        term_dict = helpers.createTermDictionary(doc_id, BeautifulSoup(data["content"], 'html.parser'))

        for word, posting in term_dict.items():
            if sys.getsizeof(partial_indx) > 1000000:
                offLoadPartialIndx(partial_indx_folder, partial_indx, partial_indx_qty)
                partial_indx = {}
                partial_indx_qty += 1
            if word not in partial_indx: partial_indx[word] = [posting]
            else: partial_indx[word].append(posting)
        doc_id += 1

    offLoadPartialIndx(partial_indx_folder, partial_indx, partial_indx_qty)

    with open('docId_url_dict/idUrl0513', 'wb') as f:
        pickle.dump(id_url_dict, f) 


constructPartialIndexes("DEV", "partial_indx_0513")