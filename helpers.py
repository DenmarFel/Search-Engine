# Standard Library
import os
import re

# Data Structures
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import deque
from nltk.stem import PorterStemmer
from postings import Posting

def bytesToMB(byte_size: int) -> int:
    return byte_size / (1024 ** 2) 


def printFileTotal(directory: str):
    total = 0
    for folder in os.listdir(directory):
        total += len(os.listdir(directory + "/" + folder))
    print("Amount of Files:", total)


def printDirectorySize(directory: str):
    total = 0
    for folder in os.listdir(directory):
        for domain in os.listdir(directory + "/" + folder):
            total += os.path.getsize(directory + "/" + folder + "/" + domain)
    print("Bytes:", total)
    print("MegaBytes:", total / (1024 ** 2))


def queueOfDirectoryFiles(directory: str) -> deque:
    doc_queue = []
    
    for folder in os.listdir(directory):
        for domain in os.listdir(directory + "/" + folder):
            doc_queue.append(directory + "/" + folder + "/" + domain)
    
    doc_queue.sort()
    doc_queue = deque(doc_queue)
    return doc_queue

def createTermDictionary(doc_id: int, soup):
    invalid_html_tags = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'canvas']
    term_dict = {}

    pos = 0
    text = soup.find_all(text=True)
    for element in text:

        # Check if element is a non visible HTML Element
        if element.parent.name in invalid_html_tags:
            continue
        
        # Check if element is a comment
        if isinstance(element, Comment):
            continue 

        # Check if string is empty
        if len(element.string.strip()) == 0:
            continue 

        # Create dictionary (word, Posting)
        for word in element.string.split():
            if not isValid(word): 
                continue
            word = PorterStemmer().stem(word).lower()
            if word not in term_dict:
                term_dict[word] = Posting(doc_id, pos, element.parent.name)
            else:
                term_dict[word].updatePosting(pos, element.parent.name)
            pos += 1
    
    for word in term_dict:
        term_dict[word].setTermFreq(pos+1)
    
    return term_dict

def isValid(word: str):
	
	# Test if alphanumeric
	if not re.match(r'^[a-zA-Z]+$', word):
		return False

	# Test if only number
	# if re.match(r'^\d+$', word):
	# 	return False

	return True

def writeToJson(input_file: str, output_file: str):
    with open(input_file, 'rb') as a, open(output_file, 'w') as b:
        pi_posting = pickle.load(a)
        pi_json = {}
        tokens = deque(sorted(pi_posting.keys()))
        for token in tokens:
            pi_json[token] = []
            for posting_obj in pi_posting[token]:
                posting_json = posting_obj.convertToDict()
                pi_json[token].append(posting_json)
            json.dump(pi_json, b, indent = 2)    
