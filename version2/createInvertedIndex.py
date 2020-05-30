import os
import pickle
from contextlib import ExitStack
from postings import Posting


def formatPostings(token: str, postings: [Posting]) -> str:
    postings_txt = []
    for posting in postings:
        doc_id = posting.getDocId()
        count = posting.getCount()
        term_freq = posting.getTermFreq()
        positions = posting.getPositions()
        html_tags = posting.getHtmlTags()
        posting_txt = "({}, {}, {}, [".format(doc_id, count, term_freq)
        for i in range(len(positions)):
            if i != len(positions) - 1:
                posting_txt += str(positions[i]) + ', '
            else:
                posting_txt += str(positions[i]) + '], ['

        for i in range(len(html_tags)):
            if i != len(html_tags) - 1:
                posting_txt += html_tags[i] + ', '
            else:
                posting_txt += html_tags[i] + '])'

        postings_txt.append(posting_txt)
            
    return postings_txt


def mergePartialIndexes(pi_folder: str, ii_txt: str, ii_pickle):
    with ExitStack() as stack:
        doc_queue = [stack.enter_context(open('{}/{}'.format(pi_folder, pi_file), 'rb')) for pi_file in os.listdir(pi_folder)]
        token_postings = [pickle.load(pi_file) for pi_file in doc_queue]

        open_file = open(ii_txt, 'r+')
        inverted_index_pickle = {}
        total = 0
        while token_postings:
            token, postings = min(token_postings, key = lambda x : x[0])
            min_index = token_postings.index(min(token_postings, key = lambda x : x[0]))
            
            formatted_postings = formatPostings(token, postings)

            if token not in inverted_index_pickle:
                total += 1
                if len(inverted_index_pickle) != 0:
                    open_file.seek(0, 2)
                    open_file.write('\n\n')

                inverted_index_pickle[token] = open_file.tell()
                for i in range(len(formatted_postings)):
                    open_file.write(formatted_postings[i] + ' x|x ')
            else:
                for i in range(len(formatted_postings)):
                    open_file.write(formatted_postings[i] + ' x|x ')

            try:
                token_postings[min_index] = pickle.load(doc_queue[min_index])
            except EOFError:
                token_postings.remove(token_postings[min_index])
                doc_queue.remove(doc_queue[min_index])
        open_file.close()

    with open(ii_pickle, 'wb') as open_file:
        pickle.dump(inverted_index_pickle, open_file, protocol = pickle.HIGHEST_PROTOCOL)


mergePartialIndexes("version2/partial_indexes/partial_indexes0528", "version2/inverted_indexes/inverted_index0528.txt", "version2/inverted_indexes/inverted_index0528.pickle")
