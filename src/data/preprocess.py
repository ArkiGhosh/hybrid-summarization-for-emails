import re
import math
import os
import sys
from pathlib import Path
import tensorflow_hub as hub
from nltk.tokenize import sent_tokenize

grandparent_path = Path(__file__).parents[1]
data_path = Path(__file__).parents[2]

interim_train_path = os.path.join(data_path, 'data', 'interim', 'train')
interim_test_path = os.path.join(data_path, 'data', 'interim', 'test')
interim_dev_path = os.path.join(data_path, 'data', 'interim', 'dev')

preprocessed_train_path = os.path.join(data_path, 'data', 'preprocessed', 'train')
preprocessed_test_path = os.path.join(data_path, 'data', 'preprocessed', 'test')
preprocessed_dev_path = os.path.join(data_path, 'data', 'preprocessed', 'dev')

mymodule_dir = os.path.join(grandparent_path, 'utils')
sys.path.append( mymodule_dir )

from reader import DataReader
# embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def tokenize_sentences(text):
    paragraphs = [p for p in text.split('\n') if p]
    sentences = []
    for paragraph in paragraphs:
        sentences.append(sent_tokenize(paragraph))
    return sentences

def dot_product(vector1, vector2):
    x = 0
    for i in range(len(vector1)):
        x += vector1[i] * vector2[i]
    return x

def magnitude(vector1):
    x = 0
    for val in vector1:
        x += val * val
    return math.sqrt(x)

def cosine_similarity(vector1, vector2):
    return dot_product(vector1, vector2)/(magnitude(vector1) * magnitude(vector2))

# def remove_duplicates(text):
        
    sentence_tokens = tokenize_sentences(text)
    sentence_list = []

    # why?
    for sentences in sentence_tokens:
        for sentence in sentences:
            sentence_list.append(sentence)

    embeddings = embed(sentence_list)
    flag = [0] * len(embeddings)
    summary_sentences = set()

    for z in range(len(embeddings)):
        for j in range(z + 1, len(embeddings)):
            em1 = embeddings[z]
            em2 = embeddings[j]
            x = float(cosine_similarity(em1, em2))
            if x > 0.75:
                if flag[z] or flag[j]:
                    flag[z] = 1
                    flag[j] = 1
                else:
                    summary_sentences.add(sentence_list[z])
                    flag[j] = 1
                    flag[z] = 1

    for z in range(len(flag)):
        if (flag[z] == 0):
            summary_sentences.add(sentence_list[z])

    preprocessed_sentences = ""
    for sentence in summary_sentences:
        preprocessed_sentences += sentence

    return preprocessed_sentences

def sanitize(interim_path, preprocessed_path):

    decorative_pattern = r'[!@#$%^&*(),.?":{}|<>~]{3,}'
    unicode_pattern = r'[^\x00-\x7F]+'

    f = DataReader(interim_path)
    emails = f.read_file()

    for i in range(len(emails)):
        sanitized_text = re.sub(decorative_pattern, '', emails[i])
        processed_text = re.sub(unicode_pattern, '', sanitized_text)
        # processed_text = remove_duplicates(sanitized_text)

        email_id = "email_{id}.txt".format(id = i + 1)
        file_path = os.path.join(preprocessed_path, email_id)
        writer = open(file_path, "w")
        writer.write(processed_text)
        writer.close()

sanitize(interim_train_path, preprocessed_train_path)
sanitize(interim_test_path, preprocessed_test_path)
sanitize(interim_dev_path, preprocessed_dev_path)
