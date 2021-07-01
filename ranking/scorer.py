class BM25Scorer:

    def __init__(self, query_term_ids, doc_len_map, idf, k1 = 1.5, b = 0.75):
        self.query_term_ids = query_term_ids
        self.doc_len_map = doc_len_map
        self.docs_average_length = doc_len_map.get_average_length()
        self.idf = idf
        self.k1 = k1
        self.b = b

    def calculate_score(self, doc_id):
        total_score = 0
        doc_length = self.doc_len_map[doc_id]
        
        for query_term_id in self.query_term_ids:
            score = self.__calcaute_score_term(query_term_id, doc_id, doc_length)
            total_score += score

        return total_score
    
    def __calcaute_score_term(self, term_id, doc_id, doc_length):
        idf = self.idf.get_idf(term_id)
        tf = self.idf.get_tf(term_id, doc_id)

        upper = tf * (self.k1 + 1)
        below = tf + self.k1 * (1 - self.b + (self.b * doc_length / self.docs_average_length))

        score = idf * (upper / below)

        return score


