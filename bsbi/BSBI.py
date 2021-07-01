import os
from pathlib import Path
import pickle
import contextlib
from idmap import IdMap
from documentLengthMap import DocumentLengthMap
from invertedIndex import InvertedIndexWriter, InvertedIndexIterator, InvertedIndexMapper
import heapq

class BSBIIndex:
    
    def __init__(self, data_dir, output_dir, index_name = "BSBI", 
                 postings_encoding = None):
        self.term_id_map = IdMap()
        self.doc_id_map = IdMap()
        self.doc_len_map = DocumentLengthMap()
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.index_name = index_name
        self.postings_encoding = postings_encoding

        self.intermediate_indices = []
        
    def save(self):
        
        with open(os.path.join(self.output_dir, 'terms.dict'), 'wb') as f:
            pickle.dump(self.term_id_map, f)
        with open(os.path.join(self.output_dir, 'docs.dict'), 'wb') as f:
            pickle.dump(self.doc_id_map, f)
    
    def load(self):
        
        with open(os.path.join(self.output_dir, 'terms.dict'), 'rb') as f:
            self.term_id_map = pickle.load(f)
        with open(os.path.join(self.output_dir, 'docs.dict'), 'rb') as f:
            self.doc_id_map = pickle.load(f)
            
    def index(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        for block_dir_relative in sorted(next(os.walk(self.data_dir))[1]):
            
            print('indexing block:', block_dir_relative)
            
            td_pairs = self.parse_block(block_dir_relative)
            index_id = 'index_'+block_dir_relative
            self.intermediate_indices.append(index_id)
            with InvertedIndexWriter(index_id, directory=self.output_dir, 
                                     postings_encoding=
                                     self.postings_encoding) as index:
                self.invert_write(td_pairs, index)
                td_pairs = None
        self.save()

        print('merging indexed blocks...')

        with InvertedIndexWriter(self.index_name, directory=self.output_dir, 
                                 postings_encoding=
                                 self.postings_encoding) as merged_index:
            with contextlib.ExitStack() as stack:
                indices = [stack.enter_context(
                    InvertedIndexIterator(index_id, 
                                          directory=self.output_dir, 
                                          postings_encoding=
                                          self.postings_encoding)) 
                 for index_id in self.intermediate_indices]
                self.merge(indices, merged_index)
        print('finished indexing.')
                            
    def parse_block(self, block_dir_relative):
        block_abs_path = os.path.join(self.data_dir, block_dir_relative)
        doc_names = next(os.walk(block_abs_path), (None, None, []))[2]
        
        term_doc_list = []
        
        for doc_name in doc_names:
            doc_path = os.path.join(block_abs_path, doc_name)
            
            doc_id = self.doc_id_map[doc_path]
            
            with open(doc_path, 'r', encoding='utf8') as f:
                for line in f:
                    splited_line = line.split()
                    self.doc_len_map.add(doc_id, len(splited_line))

                    for term in splited_line:
                        term_id = self.term_id_map[term]
                        term_doc_list.append((term_id, doc_id))
                                
        return term_doc_list
        
    def invert_write(self, td_pairs, index):
        sorted_pairs = sorted(td_pairs, key= lambda x: x[0])
        postings_dict = {}
        
        for td_pair in sorted_pairs:
            term_id = td_pair[0]
            doc_id = td_pair[1]
            if postings_dict.get(term_id) != None:
                postings_dict[term_id].append(doc_id)
            else:
                postings_dict[term_id] = [doc_id]
                
        for term, postings in postings_dict.items():
            index.append(term, postings)
        
    def merge(self, indices, merged_index):
        all_td_pairs = []
        for x in indices:
            all_td_pairs.append(list(x))
            
        for term_id_i in range(0, len(self.term_id_map.id_to_str)):
            all_postings = []
            for t_posting_pair in all_td_pairs:
                for term_id, posting_list in t_posting_pair:
                    if term_id_i == term_id: all_postings.append(posting_list)
            merged_postings_list = heapq.merge(*all_postings)
            merged_index.append(term_id_i, list(merged_postings_list))
            
        
        
    def retrieve(self, query):
        if len(self.term_id_map) == 0 or len(self.doc_id_map) == 0:
            self.load()

        term_ids = [] 
        for term in query:
            term_ids.append(self.term_id_map.get(term))
            
        print('term_ids=', term_ids)
        with InvertedIndexMapper(self.index_name, self.postings_encoding, self.output_dir) as index:
            postings = index[term_ids[0]]
            for term_id in term_ids:
                postings = self.intersect(postings, index[term_id])
            results = []
            for doc_id in postings:
                results.append(self.doc_id_map[doc_id])
            return set(results)

    def get_inverted_index(self, term_ids):
        postings = {}

        with InvertedIndexMapper(self.index_name, self.postings_encoding, self.output_dir) as index:
            for term_id in term_ids:
                postings[term_id] = index[term_id]
    
        return postings

    def intersect(self, a, b):
        return [x for x in a if x in b]