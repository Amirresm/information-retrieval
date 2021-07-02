import os
from helper import normalize_docs, generate_abs_path
from BSBI import BSBIIndex
from normalizer import DocNormalizer

print('\033c')

normalizer = DocNormalizer()

data_path = 'Dataset_IR/Train'
transformed_data_path = 'transformed-data'
output_path = 'output'

abs_data_path, abs_transformed_data_path, abs_output_path = generate_abs_path(data_path, transformed_data_path, output_path)

normalize_docs(abs_data_path, abs_transformed_data_path, normalizer, True)

bsbi = BSBIIndex(abs_transformed_data_path, abs_output_path)

bsbi.index()

while True:
    query = input('query: ')
    
    normalized_query = normalizer.query_tokenizer(query)
    print('normalized query:', normalized_query)
    
    results = bsbi.retrieve(normalized_query)

    for result in results:
        print(result)
        print('-----------------')
