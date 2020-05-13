import os
import sys
import pickle
from contextlib import ExitStack

def generateReportM1(ii_folder: str, docId_file: str, report_file: str):
    token_count = 0
    ii_size = 0
    doc_count = 0

    with open(docId_file, 'rb') as f:
        doc_count = len(pickle.load(f)) 

    with ExitStack() as stack:
        doc_queue = [stack.enter_context(open('{}/{}'.format(ii_folder, pi_file), 'rb')) for pi_file in os.listdir(ii_folder)]

        for ii_file in doc_queue:
            ii_dict = pickle.load(ii_file)
            token_count += len(ii_dict)

    for pi_file in os.listdir(ii_folder):
        ii_size += os.path.getsize(ii_folder + '/' + pi_file) / 1000
        
    with open(report_file, 'w', encoding = "utf-8") as f:
        f.write("Inverted Index Report\n")
        f.write("Location: " + ii_folder + "\n")
        f.write("Total Amount of Documents: " + str(doc_count) + "\n")
        f.write("Total Amount of Tokens: " + str(token_count) + "\n")
        f.write("Size of inverted index (KB): " + str(ii_size) + "\n")
            

generateReportM1('inverted_indx_0513', 'docId_url_dict/idUrl0513', 'reports/m1_0513')