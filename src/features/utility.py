import os
from pathlib import Path
path = os.path.expanduser('~')
path += "./Natural Language Processing/Project/hybrid-summarization/data/target_summary/train"
 
data_path = Path(__file__).parents[2]
preprocessed_copy_path = os.path.join(data_path, 'data', 'preprocessed - Copy/train')
 
file_list = os.listdir(path)
for filename in file_list:
    os.remove(preprocessed_copy_path + "/" + filename)
