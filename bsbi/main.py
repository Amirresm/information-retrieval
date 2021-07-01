import os
from helper import normalize_docs
from BSBI import BSBIIndex
from normalizer import DocNormalizer

print('\033c')

normalizer = DocNormalizer()

data_path = 'Dataset_IR/Test'
transformed_data_path = 'transformed-data'
output_path = 'output'

abs_data_path = os.path.abspath(data_path)
abs_transformed_data_path = os.path.abspath(transformed_data_path)
abs_output_path = os.path.abspath(output_path)

normalize_docs(abs_data_path, abs_transformed_data_path, normalizer)

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
