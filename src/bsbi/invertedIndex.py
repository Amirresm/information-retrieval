import os
import pickle

from .postingEncoder import UncompressedPostings


class InvertedIndex:
  
    def __init__(self, index_name, postings_encoding=None, directory=''):

        self.index_file_path = os.path.join(directory, index_name+'.index')
        self.metadata_file_path = os.path.join(directory, index_name+'.dict')

        self.directory = directory

        self.postings_dict = {}
        self.terms = []

    def __enter__(self):
        self.index_file = open(self.index_file_path, 'rb+')

        with open(self.metadata_file_path, 'rb') as f:
            self.postings_dict, self.terms = pickle.load(f)
            self.term_iter = self.terms.__iter__()                       

        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.index_file.close()
        
        with open(self.metadata_file_path, 'wb') as f:
            pickle.dump([self.postings_dict, self.terms], f)
            
class InvertedIndexWriter(InvertedIndex):
  
    def __enter__(self):
        self.index_file = open(self.index_file_path, 'ab+')              
        return self
      
    def append(self, term_id, postings_list):
        if not self.index_file.closed:
            encoded_postings_list = UncompressedPostings.encode(postings_list)
            # self.index_file.seek(0, 1)
            start_pos = self.index_file.tell()
            self.index_file.write(encoded_postings_list)
            self.postings_dict[term_id] = {'start_pos': start_pos,
                                            'posting_count': len(postings_list),
                                            'size_of_postings_list': len(encoded_postings_list)}
            # print({'start_pos': start_pos,
            #                                 'posting_count': len(postings_list),
            #                                 'size_of_postings_list': len(encoded_postings_list)})
      
      
      

class InvertedIndexIterator(InvertedIndex):
    
    def __enter__(self):
        
        super().__enter__()
        self._initialization_hook()
        return self

    def _initialization_hook(self):
        
        self.i = 0
        self.term_id_list = list(self.postings_dict)
        # print(self.postings_dict.keys())


    def __iter__(self): 
        return self
    
    def __next__(self):
        if self.i > len(self.term_id_list) - 1:
            raise StopIteration
        term_id = self.term_id_list[self.i]
        term_meta = self.postings_dict[term_id]
        self.index_file.seek(term_meta['start_pos'])
        encoded_postings_list = self.index_file.read(term_meta['size_of_postings_list'])
        postings_list = UncompressedPostings.decode(encoded_postings_list)
        # print(term_meta)
        # print(postings_list)
        self.i = self.i + 1
        return (term_id, postings_list)

    def delete_from_disk(self):
        self.delete_upon_exit = True

    def __exit__(self, exception_type, exception_value, traceback):
        self.index_file.close()
        if hasattr(self, 'delete_upon_exit') and self.delete_upon_exit:
            os.remove(self.index_file_path)
            os.remove(self.metadata_file_path)
        else:
            with open(self.metadata_file_path, 'wb') as f:
                pickle.dump([self.postings_dict, self.terms], f)
                
                
class InvertedIndexMapper(InvertedIndex):
    def __getitem__(self, key):
        return self._get_postings_list(key)
    
    def _get_postings_list(self, term_id):
        try:
            term_meta = self.postings_dict[term_id]
            self.index_file.seek(term_meta['start_pos'])
            encoded_postings_list = self.index_file.read(term_meta['size_of_postings_list'])
            postings_list = UncompressedPostings.decode(encoded_postings_list)
            return postings_list
        except:
            return []