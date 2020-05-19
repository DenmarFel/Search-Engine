class Posting:

    def __init__(self, doc_id: int, count: int, tf: int, positions: [int], html_tags: [str]):
        self.doc_id = doc_id
        self.count = count
        self.term_freq = tf
        self.positions = positions
        self.html_tags = html_tags


    def __str__(self):
        return 'Posting(doc_id = {}, count = {}, tf = {})'.format(self.getDocId(), self.getCount(), self.getTermFreq()) 
    

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
        