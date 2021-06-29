import os
from posixpath import dirname
from BSBI import BSBIIndex
from postingEncoder import UncompressedPostings
from idmap import IdMap
import pickle

print('\033c')

id_map = IdMap();

p = {}
arr = []

def append_to(val):
  index = len(arr)
  arr.append(val)
  return index

id_map['test']



# print(id_map.id_to_str)
# print(id_map.str_to_id)

# print(id_map[0])

data_path = '../Dataset_IR/Test'
output_path = '../output'

    
def search(query):
    blocks = next(os.walk('../Dataset_IR/Test'), (None, [], []))[1]
    found = set()
    for block_dir_relative in blocks:
        # print(block_dir_relative)
        block_abs_path = os.path.join('../Dataset_IR/Test', block_dir_relative)
        doc_names = next(os.walk(block_abs_path), (None, None, []))[2]
        
        for doc_name in doc_names:
            doc_path = os.path.join(block_abs_path, doc_name)
                        
            with open(doc_path, 'r', encoding='utf8') as f:
                for line in f:
                    for i, term in enumerate(line.split()):
                        if term == query:
                            found.add((doc_path, i))
    
    for res in found:
        print(res)

# for x in sorted(next(os.walk(data_path))[1]):
#   print(x)

bsbi = BSBIIndex(data_path, output_path)

bsbi.index()

# print(bsbi.term_id_map.str_to_id)

# results = bsbi.retrieve('شهردار')
while True:
    query = input('query:')
    search(query)
    print('=============')
    results = bsbi.retrieve(query)

    for result in results:
        print(result)
        print('-----------------')


# posting_list = [(1, []), (2, []), (3, []), (4, []), ]
# item = [item for item in posting_list if item[0] == 1]
# print(item)

p = {'2': 1, '3': 4}
# print(list(p))