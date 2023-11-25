import os
import sys
from pathlib import Path
from bard import BardAPI
from flant5 import FlanT5
from extractive import TextRank

grandparent_path = Path(__file__).parents[1]
data_path = Path(__file__).parents[2]

preprocessed_train_path = os.path.join(data_path, 'data', 'preprocessed - Copy', 'train')
preprocessed_test_path = os.path.join(data_path, 'data', 'preprocessed - Copy', 'test')
preprocessed_dev_path = os.path.join(data_path, 'data', 'preprocessed - Copy', 'dev')

target_summary_train_path = os.path.join(data_path, 'data', 'target_summary', 'train')
target_summary_test_path = os.path.join(data_path, 'data', 'target_summary', 'test')
target_summary_dev_path = os.path.join(data_path, 'data', 'target_summary', 'dev')

mymodule_dir = os.path.join(grandparent_path, 'utils')
sys.path.append( mymodule_dir )

from reader import DataReader

def generate_target_summary(preprocessed_path, target_summary_path, token):

    f = DataReader(preprocessed_path)
    emails = f.read_file()

    f1 = open("error_log.txt", "w")

    for i in range(len(emails)):
        
        try:
            bard_object = BardAPI(token)
            t5_object = FlanT5()

            t5_response = t5_object.summarize(emails[i][0])
            full_response = t5_response

            try:
                bard_response = bard_object.summarize(emails[i][0])
                bard_list = bard_response.split(" ")
                if not(bard_list[0] == "Response" or bard_list[1] == "Error:"):
                    full_response += bard_response

            except Exception as e:
                f1.write(f"Error in file number: {emails[i][1]} with error {e}\n")
            
            extractive_text_object = TextRank(full_response)
            summary = extractive_text_object.generate_summary()

            file_id = emails[i][1]
            email_id = f"email_{file_id}.txt"
            file_path = os.path.join(target_summary_path, email_id)
            writer = open(file_path, "w")
            writer.write(summary)
            writer.close()

        except Exception as e:
            f1.write(f"Error in file number: {emails[i][1]} with error {e}\n")
    
    f1.close()



