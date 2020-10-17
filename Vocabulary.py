import re
import numpy as np
from contractions import Contractions

class Vocabulary:
    PAD_token = 0  # Used for padding short sentences
    SOS_token = 1  # Start-of-sentence token
    EOS_token = 2  # End-of-sentence token

    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {self.PAD_token: "PAD", self.SOS_token: "SOS", self.EOS_token: "EOS"}
        self.num_words = 3
        self.num_sentences = 0
        self.longest_sentence = 0

    def add_token(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1

    def add_chunk(self, sentence):
        sentence_len = 0
        for word in sentence.split(' '):
            sentence_len += 1
            self.add_token(word)
        if sentence_len > self.longest_sentence:
            self.longest_sentence = sentence_len
        self.num_sentences += 1

    def to_token(self, index):
        return self.index2word[index]

    def to_index(self, word):
        return self.word2index[word]

    def save_data(self, filename):
        tmp = [(k, v) for k, v in self.word2index.items()]
        np.save('.\\data\\' + filename + '_word2index', tmp)
        tmp = [(k, v) for k, v in self.index2word.items()]
        np.save('.\\data\\' + filename + '_index2word', tmp)

    def load_data(self, filename):
        self.word2index.clear()
        self.index2word.clear()
        tmp = np.load('.\\data\\' + filename + "_word2index.npy", allow_pickle=True)
        for (k, v) in tmp:
            self.word2index[k] = int(v)
        tmp = np.load('.\\data\\' + filename + "_index2word.npy", allow_pickle=True)
        for (k, v) in tmp:
            self.index2word[int(k)] = v












