import re
import math
import os
import sys
from pathlib import Path
import tensorflow_hub as hub
from nltk.tokenize import sent_tokenize
from reader import DataReader

grandparent_path = Path(__file__).parents[1]
data_path = Path(__file__).parents[2]

interim_train_path = os.path.join(data_path, 'data', 'interim', 'train')
interim_test_path = os.path.join(data_path, 'data', 'interim', 'test')
interim_dev_path = os.path.join(data_path, 'data', 'interim', 'dev')

preprocessed_train_path = os.path.join(data_path, 'data', 'preprocessed', 'train')
preprocessed_test_path = os.path.join(data_path, 'data', 'preprocessed', 'test')
preprocessed_dev_path = os.path.join(data_path, 'data', 'preprocessed', 'dev')

def tokenize_sentences(text):
    paragraphs = [p for p in text.split('\n') if p]
    sentences = []
    for paragraph in paragraphs:
        sentences.append(sent_tokenize(paragraph))
    return sentences

def sanitize(text):
    decorative_pattern = r'[!@#$%^&*(),.?":{}|<>~]{3,}'
    unicode_pattern = r'[^\x00-\x7F]+'
    sanitized_text = re.sub(decorative_pattern, '', text)
    sanitized_text = re.sub(unicode_pattern, '', sanitized_text)
    return sanitized_text

def remove_duplicates(interim_path, preprocessed_path):
    f = DataReader(interim_path)
    emails = f.read_file()

    for i in range(len(emails)):
        sentence_tokens = tokenize_sentences(text)
        sentence_list = []
        for sentences in sentence_tokens:
            for sentence in sentences:
                sentence_list.append(sentence)
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        embeddings = embed(sentence_list)
        flag = [0] * len(embeddings)
        summary_sentences = set()

        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                em1 = embeddings[i]
                em2 = embeddings[j]
                x = float(cosine_similarity(em1, em2))
                print(sentence_list[i])
                print(sentence_list[j])
                print(x)
                if x > 0.75:
                    if flag[i] or flag[j]:
                        flag[i] = 1
                        flag[j] = 1
                    else:
                        summary_sentences.add(sentence_list[i])
                        flag[j] = 1
                        flag[i] = 1
        print(flag)
        for i in range(len(flag)):
            print(i)
            if (flag[i] == 0):
                summary_sentences.add(sentence_list[i])
        
        email_id = "email_{id}.txt".format(id = i + 1)
        file_path = os.path.join(preprocessed_path, email_id)
        writer = open(file_path, "w")
        for sentence in summary_sentences:
            writer.write(sentence)
        writer.close()


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