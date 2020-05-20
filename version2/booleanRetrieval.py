import re
import os
import string
import pickle
from time import process_time 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from postings import Posting


def booleanRetrieval(query: str, mode: str, ii_dict: dict, ii_file, doc_id_file: str):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    tokens = {ps.stem(word.lower()) for word in word_tokenize(query) if word not in stop_words}
    if mode.upper() == 'AND':
        return booleanRetrievalAnd(tokens, ii_dict, ii_file, doc_id_file)


def booleanRetrievalAnd(tokens: list, ii_dict: dict, ii_file, doc_id_file: str):
    print(tokens)
    doc_ids = []

    postings_of_tokens = [grabPosting(ii_dict[token], ii_file) for token in tokens if token in ii_dict]
    for min_posting in postings_of_tokens[0]:
        min_posting_id = min_posting.getDocId()
        matches = 0
        for postings in postings_of_tokens:
            for posting in postings:
                posting_id = posting.getDocId()
                if posting_id == min_posting_id:
                    matches += 1
        if matches == len(tokens):
            doc_ids.append(min_posting_id)
    
    return grabUrls(doc_ids, doc_id_file)


def grabPosting(seek_value: int, ii_file):
    postings = []
    ii_file.seek(seek_value)
    for posting in ii_file.readline().strip().split('|'):
        posting = posting.strip().lstrip('(').rstrip(')')
        if posting != '':
            doc_id = posting[0:posting.find(',')]
            posting = posting[posting.find(',') + 1::]

            count = posting[0:posting.find(',')]
            posting = posting[posting.find(',') + 1::]

            term_freq = posting[0:posting.find(',')]
            posting = posting[posting.find(',') + 1::]

            positions = posting[0:posting.find(']') + 1]
            posting = posting[posting.find(']') + 2::]

            tags = posting.strip()

            pos_list = [int(pos) for pos in positions.strip().lstrip('[').rstrip(']').split(',')]
            tags_list = tags.strip().lstrip('[').rstrip(']').split(',')

            postings.append(Posting(int(doc_id), int(count), float(term_freq), pos_list, tags_list))
    return postings
 

def grabUrls(doc_ids: [int], doc_id_file: str):
    with open(doc_id_file, 'rb') as f:
        doc_id_dict = pickle.load(f)
        return [doc_id_dict[doc_id] for doc_id in doc_ids]


if __name__ == '__main__':  

    query = input('Search: ')
    mode =  'and' # input("Choose Mode ('and', 'or'): ")
    ii_pickle = 'version2/inverted_indexes/inverted_index0518.pickle'
    ii_txt = 'version2/inverted_indexes/inverted_index0518.txt'
    doc_id_file = 'version2/docId_url_dict/idUrl0518'

    with open(ii_pickle, 'rb') as f:
        ii_dict = pickle.load(f)

    f = open(ii_txt)
    start = process_time()
    # booleanRetrieval(query, mode, ii_dict, f, doc_id_file)
    urls = booleanRetrieval(query, mode, ii_dict, f, doc_id_file)[0:5]
    end = process_time()

    for url in urls:
        print(url)

    f.close()

    print("Elapsed time during the search in seconds:", end-start)  