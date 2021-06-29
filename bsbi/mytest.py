import os
from posixpath import dirname
from BSBI import BSBIIndex
from postingEncoder import UncompressedPostings
from idmap import IdMap
from normalizer import DocNormalizer
from pathlib import Path

print('\033c')

normalizer = DocNormalizer()

data_path = '../Dataset_IR/Test'
transformed_data_path = '../transformed-data'
output_path = '../output'

def normalize_docs(force=False):
    already_normalized = len(next(os.walk(transformed_data_path), (None, [], []))[1]) > 0
    print(len(next(os.walk(transformed_data_path), (None, [], []))[1]))
    if not already_normalized or force:
        print('normalizing docs...')
        blocks = next(os.walk(data_path), (None, [], []))[1]
        for block_dir_relative in blocks:
            block_abs_path = os.path.join(data_path, block_dir_relative)
            transformed_block_abs_path = os.path.join(transformed_data_path, block_dir_relative)
            Path(transformed_block_abs_path).mkdir(parents=True, exist_ok=True)
            doc_names = next(os.walk(block_abs_path), (None, None, []))[2]
            
            for doc_name in doc_names:
                doc_path = os.path.join(block_abs_path, doc_name)
                transformed_doc_path =  os.path.join(transformed_block_abs_path, doc_name)
    
                with open(doc_path, 'r', encoding='utf8') as f:
                    print(transformed_doc_path)
                    with open(transformed_doc_path, 'w', encoding='utf8') as tf:
                        tf.write(normalizer.normalize(f.read()))
        print('finished normalizing docs.')
    else:
        print('normalized docs exist.')
    
def search(query):
    blocks = next(os.walk(transformed_data_path), (None, [], []))[1]
    found = set()
    for block_dir_relative in blocks:
        # print(block_dir_relative)
        block_abs_path = os.path.join(transformed_data_path, block_dir_relative)
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


normalize_docs()

bsbi = BSBIIndex(transformed_data_path, output_path)

bsbi.index()

while True:
    query = input('query:')
    # print('normalizing query...')
    normalized_query = normalizer.query_tokenizer(query)
    print('normalized query:', normalized_query)
    
    # search(normalized_query[0])
    # print('=============')
    
    results = bsbi.retrieve(normalized_query)

    for result in results:
        print(result)
        print('-----------------')
