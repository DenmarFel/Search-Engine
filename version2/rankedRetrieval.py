import pickle

from math import log, log10, sqrt
from time import process_time 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from postings import Posting
  

# Rids query of stop words and stems each token using NLTK
def formatQuery(query: str) -> [str]:
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    return [ps.stem(word.lower()) for word in word_tokenize(query) if word not in stop_words]
    

# Convers an entire line from the inverted index txt file into a Posting
def grabPostings(seek_value: int, open_ii_txt) -> [Posting]:
    postings = []
    open_ii_txt.seek(seek_value)

    # Helper method converts a string to a Posting
    def constructPosting(posting_txt: str) -> Posting:
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

    for posting in open_ii_txt.readline().strip().split('x|x'):
        posting = posting.strip().lstrip('(').rstrip(')')
        if posting != '': postings.append(constructPosting(posting))
    return postings


# Given a list containing lists of postings, return the doc_ids that are found
# in each list. This means the corresponding document contains every token.
def intersectionOfPostings(postings_of_tokens: [[Posting]]) -> {int}:
    doc_ids = {posting.getDocId() for posting in postings_of_tokens[0]}
    for i in range(1, len(postings_of_tokens)):
        doc_ids.intersection({posting.getDocId() for posting in postings_of_tokens[i]})
    return doc_ids


# def cosineScore(tokens: [str]):
def cosineRank(tokens: [str], doc_id_dict: dict, ii_dict: dict, open_ii_txt):
    nested_dict = {}
    for token in tokens:
        nested_dict[token] = {}
        for posting in grabPostings(ii_dict[token], open_ii_txt):
            nested_dict[token][posting.getDocId()] = posting

    doc_ids = set(nested_dict[tokens[0]].keys())
    for i in range(1, len(tokens)):
        doc_ids = doc_ids.intersection(set(nested_dict[tokens[i]].keys()))
    
    results = []
    ltc_vector = ltc(tokens, doc_id_dict, ii_dict, open_ii_txt)
    for doc_id in doc_ids:
        lnc_vector = lnc(tokens, nested_dict, doc_id)

        doc_score = sum([lnc_vector[i] * ltc_vector[i] for i in range(len(tokens))])
        results.append((doc_score, doc_id_dict[doc_id]))
    return sorted(results, reverse = True)

def lnc(tokens: [str], nested_dict: dict, doc_id: int) -> [float]:
    tf_vector = [log(1 + nested_dict[token][doc_id].getTermFreq()) for token in tokens]
    divisor = sqrt(sum([num ** 2 for num in tf_vector]))
    normalized_wt_vector_lnc = [num / divisor for num in tf_vector]
    return normalized_wt_vector_lnc

# ltc (logarithmic tf, idf, cosine normalization)
# Computes the ltc portion of lnc.ltc(ddd.qqq) SMART Notation 
def ltc(tokens: [str], doc_id_dict: dict, ii_dict: dict, open_ii_txt) -> [float]:
    logarithmic_tf_vector = [log(1 + (tokens.count(token) / len(tokens))) for token in tokens]
    idf_vector = [log10(len(doc_id_dict) / len(grabPostings(ii_dict[token], open_ii_txt))) if token in ii_dict else 0 for token in tokens]
    wt_vector = [logarithmic_tf_vector[i] * idf_vector[i] for i in range(len(logarithmic_tf_vector))]
    divisor = sqrt(sum([num ** 2 for num in wt_vector]))
    normalized_wt_vector = [num / divisor for num in wt_vector]
    return normalized_wt_vector


if __name__ == '__main__':  

    # Inverted Index Pickle (ii_pickle)
    # Pickle file contains Python dictionary with keys being tokens and values 
    # being the position of the corresponding Posting's list in ii_txt.
    # This enables constant access to the Posting's list of a token.
    ii_pickle = 'version2/inverted_indexes/inverted_index0523.pickle'

    # Inverted Index Text File (ii_txt)
    # Txt file contains all postings of the inverted index. 
    # Each Posting contains:
    #   document_id (int)
    #   count (int)
    #   term_frequency (float) (Number of times term t appears in a document) / (Total number of terms in the document)
    #   positions ([int])
    #   html_tags ([str])
    ii_txt = 'version2/inverted_indexes/inverted_index0523.txt'

    # Document Id File (doc_id_pickle)
    # Pickle file contains Python dictionary with keys being document_id and 
    # values being the corresponding url. This dictionary is useful for 
    # obtaining the total amount of documents for idf computation and gathering
    # urls to return given a query.
    doc_id_pickle = 'version2/docId_url_dict/idUrl0518'

    # Open files once. Then use throughout program.
    with open(ii_pickle, 'rb') as f: 
        ii_dict =  pickle.load(f)

    with open(doc_id_pickle, 'rb') as f:
        doc_id_dict = pickle.load(f)

    with open(ii_txt) as open_ii_txt:
        query = input("Search: ")
        k = 10
        formatted_query = formatQuery(query)
        print(formatted_query)

        start = process_time()
        results = cosineRank(formatted_query, doc_id_dict, ii_dict, open_ii_txt)
        end = process_time()

        print("Elapsed time during the search in seconds:", end-start)
        for item in results:
            print(item)
