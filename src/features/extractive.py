import numpy as np
import pandas as pd
import nltk
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from scipy import spatial
import networkx as nx

class TextRank:
    
    def __init__(self, text):
        self.sentences = sent_tokenize(text)
        self.sentences_clean = [re.sub(r'[^\w\s]','',sentence.lower()) for sentence in self.sentences]
        self.stop_words = stopwords.words('english')
        self.sentence_tokens = [[words for words in sentence.split(' ') if words not in self.stop_words] for sentence in self.sentences_clean]
        self.w2v = Word2Vec(self.sentence_tokens, min_count = 1, vector_size = 1, epochs = 1000)
        self.sentence_embeddings = [[self.w2v.wv[word] for word in words][0] for words in self.sentence_tokens]
        self.max_len = max([len(tokens) for tokens in self.sentence_tokens])
        self.sentence_embeddings = [np.pad(embedding, (0, self.max_len - len(embedding)), 'constant') for embedding in self.sentence_embeddings]

    def generate_summary(self):
        similarity_matrix = np.zeros([len(self.sentence_tokens), len(self.sentence_tokens)])
        for i,row_embedding in enumerate(self.sentence_embeddings):
            for j,column_embedding in enumerate(self.sentence_embeddings):
                similarity_matrix[i][j] = 1 - spatial.distance.cosine(row_embedding,column_embedding)

        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph, tol = 1.0e-3)
        top_sentence = {sentence : scores[index] for index,sentence in enumerate(self.sentences)}
        top = dict(sorted(top_sentence.items(), key = lambda x : x[1], reverse = True)[ : min(3, len(self.sentences))])

        summary = ""
        for sent in self.sentences:
            if sent in top.keys():
                summary += sent
        return summary
                
    
