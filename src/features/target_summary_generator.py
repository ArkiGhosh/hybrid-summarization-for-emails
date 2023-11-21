import os
import sys
from pathlib import Path
from bard import BardAPI
from flant5 import FlanT5
from extractive import TextRank

grandparent_path = Path(__file__).parents[1]
data_path = Path(__file__).parents[2]

preprocessed_train_path = os.path.join(data_path, 'data', 'preprocessed', 'train')
preprocessed_test_path = os.path.join(data_path, 'data', 'preprocessed', 'test')
preprocessed_dev_path = os.path.join(data_path, 'data', 'preprocessed', 'dev')

target_summary_train_path = os.path.join(data_path, 'data', 'target_summary', 'train')
target_summary_test_path = os.path.join(data_path, 'data', 'target_summary', 'test')
target_summary_dev_path = os.path.join(data_path, 'data', 'target_summary', 'dev')

mymodule_dir = os.path.join(grandparent_path, 'utils')
sys.path.append( mymodule_dir )

from reader import DataReader

def generate_target_summary(preprocessed_path, target_summary_path, token):

    f = DataReader(preprocessed_path)
    emails = f.read_file()

    for i in range(len(emails)):
        bard_object = BardAPI(token)
        t5_object = FlanT5()

        bard_response = bard_object.summarize(emails[i][0])
        t5_response = t5_object.summarize(emails[i][0])
        full_response = bard_response + t5_response
        extractive_text_object = TextRank(full_response)
        summary = extractive_text_object.generate_summary()

        file_id = emails[i][1]
        email_id = f"email_{file_id}.txt"
        file_path = os.path.join(target_summary_path, email_id)
        writer = open(file_path, "w")
        writer.write(summary)
        writer.close()

generate_target_summary(preprocessed_train_path, target_summary_train_path, "dQhkQc_KZlZgutYX69f2F5Z6NN0PeYER-sy7boNpd3Q-kGytWAqOQp5Q-P0sWsBMM4XSNw.")
generate_target_summary(preprocessed_test_path, target_summary_test_path, "dQhkQc_KZlZgutYX69f2F5Z6NN0PeYER-sy7boNpd3Q-kGytWAqOQp5Q-P0sWsBMM4XSNw.")
generate_target_summary(preprocessed_dev_path, target_summary_dev_path, "dQhkQc_KZlZgutYX69f2F5Z6NN0PeYER-sy7boNpd3Q-kGytWAqOQp5Q-P0sWsBMM4XSNw.")


