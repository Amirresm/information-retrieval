import os

from bsbi.helper import normalize_docs
from bsbi.BSBI import BSBIIndex
from bsbi.normalizer import DocNormalizer
from ranking.ranker import Ranker

print('\033c')

normalizer = DocNormalizer()

data_path = 'data/data-set/Train'
transformed_data_path = 'data/transformed-data'
output_path = 'data/output'

abs_data_path = os.path.abspath(data_path)
abs_transformed_data_path = os.path.abspath(transformed_data_path)
abs_output_path = os.path.abspath(output_path)

normalize_docs(abs_data_path, abs_transformed_data_path, normalizer)

bsbi = BSBIIndex(abs_transformed_data_path, abs_output_path)

bsbi.index()

ranker = Ranker(bsbi)

while True:
    query = input('Query: ')
    
    normalized_query = normalizer.query_tokenizer(query)

    print("Select mode:")

    print('Enter 0 --> BSBI')
    print("Enter 1 --> Ranking")

    mode = input("mode: ") 
    results = {}
    
    if mode == "0":
        results = bsbi.retrieve(normalized_query)
    else: 
        results = ranker.rank(normalized_query)

    for result in results:
        print(result)
        print('-----------------')

