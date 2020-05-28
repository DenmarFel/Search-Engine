import os
import json
import re
import sys
import pickle

from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem import PorterStemmer
from math import log10

from postings import Posting


def listOfDirectoryFiles(directory: str) -> list:
    json_files = []
    for domain in os.listdir(directory):
        for site in os.listdir("{}/{}".format(directory, domain)):
            json_files.append("{}/{}/{}".format(directory, domain, site))
    return json_files


def isValidElement(element: 'bs4.element') -> bool:
    invalid_html_tags = {'[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'canvas', 'style'}
    # Skip element if it is not visible on document
    if element.parent.name in invalid_html_tags:
        return False

    # Skip element if it is an html comment
    if isinstance(element, Comment):
        return False

    # Skip element if there is no text
    if len(element.string.split()) == 0:
        return False

    return True


def isValidWord(word: str) -> bool:
    if not re.match(r'^\w+$', word): return False
    return True


def createTermDictionary(content: str):
    term_dict = {}
    soup = BeautifulSoup(content, 'html.parser')
    dom = soup.find_all(text = True)

    pos = 0
    for element in dom:
        if not isValidElement(element): continue

        for word in element.string.split():
            if not isValidWord(word): continue
            word = PorterStemmer().stem(word).lower()
            if word not in term_dict:
                term_dict[word] = ([pos], [element.parent.name])
            else:
                term_dict[word][0].append(pos)
                term_dict[word][1].append(element.parent.name)
            pos += 1

    return term_dict


def getTermCount(term_dict: dict) -> int:
    term_count = 0
    for word in term_dict:
        term_count += len(term_dict[word][0])
    return term_count


def offloadPartialIndex(partial_index: dict, output_folder: str):
    num = len(os.listdir(output_folder))
    file_name = "{}/partial_index{}".format(output_folder, num)
    with open(file_name, "wb") as open_file:
        for token, postings in sorted(partial_index.items()):
            pickle.dump((token, postings), open_file, protocol = pickle.HIGHEST_PROTOCOL)
    print("Created:", file_name)


def createPartialIndexes(directory: str, doc_id_file: str, pi_folder: str):
    json_files = listOfDirectoryFiles(directory)
    partial_index = {} # word : [Postings]
    doc_id_dict = {} # doc_id : url

    doc_id = 0
    for json_file in json_files:
        with open(json_file) as open_file:
            data = json.load(open_file)
            
            term_dict = createTermDictionary(data['content']) # term : ([pos], [parent tag])
            term_count = getTermCount(term_dict)

            print(doc_id, sys.getsizeof(partial_index))
            for word in term_dict:
                count = len(term_dict[word][0])
                term_freq = 1 + log10(count / term_count)
                positions = term_dict[word][0]
                html_tags = term_dict[word][1]
                posting = Posting(doc_id, count, term_freq, positions, html_tags)
            
                if sys.getsizeof(partial_index) > 1000000:
                    offloadPartialIndex(partial_index, pi_folder)
                    partial_index = {}
                if word not in partial_index:
                    partial_index[word] = [posting]
                else:
                    partial_index[word].append(posting)
            
            doc_id_dict[doc_id] = data['url']

        doc_id += 1
            
    offloadPartialIndex(partial_index, pi_folder)

    with open(doc_id_file, 'wb') as open_file:
        pickle.dump(doc_id_dict, open_file, protocol = pickle.HIGHEST_PROTOCOL)


createPartialIndexes("DEV", "version2/docId_url_dict/idUrl0528", "version2/partial_indexes/partial_indexes0528")