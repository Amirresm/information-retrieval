from .scorer import BM25Scorer
from .idf import Idf

class Ranker:
    def __init__(self, bsbi):
        self.bsbi = bsbi
        self.doc_len_map = bsbi.doc_len_map

    def __get_query_term_ids(self, query):
        query_term_ids = []

        for term in query:
            query_term_ids.append(self.bsbi.term_id_map.get(term))
            
        return query_term_ids

    def __calculate_docs_score(self, query_term_ids, inverted_index):
        idf = Idf(self.doc_len_map, inverted_index)
        bm25Scorer = BM25Scorer(query_term_ids, self.doc_len_map, idf)
        
        docs_score = []

        for doc_id in self.doc_len_map.table.keys():
            doc_score = bm25Scorer.calculate_score(doc_id)
            doc_path = self.bsbi.doc_id_map[doc_id]

            docs_score.append((doc_score, doc_path))
        
        return docs_score
    
    def rank(self, query):
        query_term_ids = self.__get_query_term_ids(query)
        inverted_index = self.bsbi.get_inverted_index(query_term_ids)

        docs_score = self.__calculate_docs_score(query_term_ids, inverted_index)
        sorted_docs_score = sorted(docs_score, key=lambda x:x[0], reverse=True)

        return sorted_docs_score

