import os
from pathlib import Path

def normalize_docs(data_path, transformed_data_path, normalizer, force=False):
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
        
def generate_abs_path(data_path, transformed_data_path, output_path):
    abs_data_path = os.path.abspath(data_path)
    abs_transformed_data_path = os.path.abspath(transformed_data_path)
    abs_output_path = os.path.abspath(output_path)
    return (abs_data_path, abs_transformed_data_path, abs_output_path);