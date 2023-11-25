import os
import pandas as pd
from pathlib import Path

def extract_emails(file_path):
    with open(file_path, 'r') as file:
        email_content = file.read()
    return email_content

data_path = Path(__file__).parents[2]
raw_train_path = os.path.join(data_path, 'data', 'preprocessed', 'train')
target_summary_train_path = os.path.join(data_path, 'data', 'target_summary', 'train')

raw_file_list = os.listdir(raw_train_path)
target_summary_file_list = os.listdir(target_summary_train_path)
common_files = set(raw_file_list) & set(target_summary_file_list)
df = pd.DataFrame(columns=['raw_email', 'target_email'])

for file_name in common_files:
    raw_file_path = os.path.join(raw_train_path, file_name)
    target_summary_file_path = os.path.join(target_summary_train_path, file_name)

    raw_email = extract_emails(raw_file_path)
    target_summary_email = extract_emails(target_summary_file_path)

    # Append data to the DataFrame
    df.loc[df.shape[0]] = [raw_email, target_summary_email]

