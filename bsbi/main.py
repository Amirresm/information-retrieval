import os
from helper import normalize_docs
from BSBI import BSBIIndex
from normalizer import DocNormalizer

print('\033c')

normalizer = DocNormalizer()

data_path = '../Dataset_IR/Test'
transformed_data_path = '../transformed-data'
output_path = '../output'

normalize_docs(data_path, transformed_data_path, normalizer)

bsbi = BSBIIndex(transformed_data_path, output_path)

bsbi.index()

while True:
    query = input('query: ')
    
    normalized_query = normalizer.query_tokenizer(query)
    print('normalized query:', normalized_query)
    
    results = bsbi.retrieve(normalized_query)

    for result in results:
        print(result)
        print('-----------------')
