from math import log

class Posting:

    def __init__(self, doc_id: int, initial_pos: int, initial_html_tag: str):
        self.doc_id = doc_id
        self.count = 1
        self.positions = [initial_pos]
        self.html_tags = [initial_html_tag]
        self.term_freq = 0
        self.inverse_doc_freq = 1

    def __str__(self):
        return 'Posting(doc_id = {}, count = {}, tf = {}, idf = {})'.format(self.getDocId(), self.getCount(), self.getTermFreq(), self.getInverseDocFreq()) 

    def convertToDict(self):
        posting_json = {}
        posting_json['doc_id'] = self.getDocId()
        posting_json['count'] = self.getCount()
        posting_json['positions'] = self.getPositions()
        posting_json['term_freq'] = self.getTermFreq()
        posting_json['inverse_doc_freq'] = self.getInverseDocFreq()
        return posting_json

    def updatePosting(self, new_pos: int, new_html_tag: str):
        self.count += 1
        self.positions.append(new_pos)
        self.html_tags.append(new_html_tag)

    def setTermFreq(self, total_words):
        self.term_freq = self.count / total_words

    def setInverseDocFreq(self, appearances, total_doc = 55393):
        self.inverse_doc_freq = log(float(total_doc) / appearances)

    def getDocId(self):
        return self.doc_id

    def getCount(self):
        return self.count

    def getPositions(self):
        return self.positions

    def getHtmlTags(self):
        return self.html_tags

    def getTermFreq(self):
        return self.term_freq

    def getInverseDocFreq(self):
        return self.inverse_doc_freq
