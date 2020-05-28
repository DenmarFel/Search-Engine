import re
import os
import string
import pickle
from time import process_time 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from postings import Posting


def booleanRetrieval(query: str, mode: str, ii_dict: dict, ii_file, doc_id_dict: dict):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    tokens = {ps.stem(word.lower()) for word in word_tokenize(query) if word not in stop_words}
    if mode.upper() == 'AND':
        return booleanRetrievalAnd(tokens, ii_dict, ii_file, doc_id_dict)


def booleanRetrievalAnd(tokens: list, ii_dict: dict, ii_file, doc_id_dict: dict):
    print(tokens)
    postings_of_tokens = [grabPosting(ii_dict[token], ii_file) for token in tokens if token in ii_dict]

    if len(tokens) == 0: return []
    
    doc_ids = {posting.getDocId() for posting in postings_of_tokens[0]}
    for i in range(1, len(postings_of_tokens)):
        doc_ids.intersection({posting.getDocId() for posting in postings_of_tokens[i]})
    
    return sorted(grabUrls(doc_ids, doc_id_dict))


def constructPosting(posting_txt: str):
    doc_id = posting_txt[0:posting_txt.find(',')]
    posting_txt = posting_txt[posting_txt.find(',') + 1::]

    count = posting_txt[0:posting_txt.find(',')]
    posting_txt = posting_txt[posting_txt.find(',') + 1::]

    term_freq = posting_txt[0:posting_txt.find(',')]
    posting_txt = posting_txt[posting_txt.find(',') + 1::]

    positions = posting_txt[0:posting_txt.find(']') + 1]
    posting_txt = posting_txt[posting_txt.find(']') + 2::]

    pos_list = [int(pos) for pos in positions.strip().lstrip('[').rstrip(']').split(',')]
    tag_list = posting_txt.strip().lstrip('[').rstrip(']').split(',')

    return Posting(int(doc_id), int(count), float(term_freq), pos_list, tag_list)


def grabPosting(seek_value: int, ii_file):
    postings = []
    ii_file.seek(seek_value)

    for posting in ii_file.readline().strip().split('x|x'):
        posting = posting.strip().lstrip('(').rstrip(')')
        if posting != '':
            postings.append(constructPosting(posting))

    return postings
 

def grabUrls(doc_ids: [int], doc_id_dict: dict):
    return [doc_id_dict[doc_id] for doc_id in doc_ids]


if __name__ == '__main__':  

    query = input('Search: ')
    mode =  'and' # input("Choose Mode ('and', 'or'): ")
    ii_pickle = 'version2/inverted_indexes/inverted_index0528.pickle'
    ii_txt = 'version2/inverted_indexes/inverted_index0528.txt'
    doc_id_file = 'version2/docId_url_dict/idUrl0528'

    with open(ii_pickle, 'rb') as f:
        ii_dict = pickle.load(f)

    with open(doc_id_file, 'rb') as f:
        doc_id_dict = pickle.load(f)

    with open(ii_txt) as f:
        
        start = process_time()
        urls = booleanRetrieval(query, mode, ii_dict, f, doc_id_dict)[0:5]
        end = process_time()

        for url in urls:
            print(url)

    print("Elapsed time during the search in seconds:", end-start)