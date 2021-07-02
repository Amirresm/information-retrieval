from math import log

class Idf:

    def __init__(self, doc_len_map, inverted_index):
        self.doc_len_map = doc_len_map
        self.inverted_index = inverted_index
       
    def get_tf(self, term_id, doc_id):
       frequency = self.inverted_index[term_id].count(doc_id)
       
       return frequency

    def get_df(self, term_id):
         inverted_index_set = set(self.inverted_index[term_id])
         frequency = len(inverted_index_set)
         
         return frequency

    def get_idf(self, term_id):
        N = len(self.doc_len_map) # number of documents
        df = self.get_df(term_id)

        upper = N - df + 0.5
        below = df + 0.5
        idf = log((upper / below) + 1)
        
        return idf