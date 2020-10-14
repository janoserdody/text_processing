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

def add_word(self, word):
  if word not in self.word2index:
    # First entry of word into vocabulary
    self.word2index[word] = self.num_words
    self.word2count[word] = 1
    self.index2word[self.num_words] = word
    self.num_words += 1
  else:
    # Word exists; increase word count
    self.word2count[word] += 1

