import re
import os
import string
import pickle
from time import process_time 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


def booleanRetrieval(query: str, mode: str, ii_folder: str, doc_id_file: str):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    tokens = {ps.stem(word.lower()) for word in word_tokenize(query) if re.match(r'^[a-zA-Z]+$', ps.stem(word)) and word not in stop_words}
    if mode.upper() == 'AND':
        return booleanRetrievalAnd(tokens, ii_folder, doc_id_file)


def booleanRetrievalAnd(tokens: list, ii_folder: str, doc_id_file: str):
    print(tokens)
    doc_ids = []
    postings_of_tokens = [grabPosting(token, ii_folder) for token in tokens]

    for min_posting in postings_of_tokens[0]:
        min_posting_id = min_posting.getDocId()
        matches = 0
        for postings in postings_of_tokens:
            if min_posting_id > postings[-1].getDocId(): continue
            for posting in postings:
                posting_id = posting.getDocId()
                if posting_id == min_posting_id:
                    matches += 1
        if matches == len(tokens):
            doc_ids.append(min_posting_id)
    
    return grabUrls(doc_ids, doc_id_file)


def grabPosting(token: str, ii_folder: str):
    ii_folder = ['{}/{}'.format(ii_folder, ii_file) for ii_file in os.listdir(ii_folder)]
    ii_file = ii_folder[string.ascii_lowercase.index(token[0])]
    with open(ii_file, 'rb') as f:
        ii_dict = pickle.load(f)
        return ii_dict[token] if token in ii_dict else []


def grabUrls(doc_ids: [int], doc_id_file: str):
    with open(doc_id_file, 'rb') as f:
        doc_id_dict = pickle.load(f)
        return [doc_id_dict[doc_id] for doc_id in doc_ids]


if __name__ == '__main__':  
    query = input('Search: ')
    mode =  'and' # input("Choose Mode ('and', 'or'): ")
    ii_folder = 'inverted_indx_0513'
    doc_id_file = 'docId_url_dict/idUrl0513'

    start = process_time()

    for url in booleanRetrieval(query, mode, ii_folder, doc_id_file)[0:5]:
        print(url)

    end = process_time()
    print("Elapsed time during the search in seconds:", end-start)  