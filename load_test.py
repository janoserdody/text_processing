import re
import numpy as np

from Vocabulary import Vocabulary
from contractions import Contractions

PAD_token = 0   # Used for padding short sentences
SOS_token = 1   # Start-of-sentence token
EOS_token = 2   # End-of-sentence token

trans_punctuation = {ord('.'): None, ord('?'): None, ord('!'): None}

# TODO számok feldolgozása külön osztályba
translation = {
    8217: None,
    8220: None,
    8221: None,
    8212: ' ',
    8216: None,
    249: ' ',
    10: ' ',
    ord(':'): None,
    ord('('): None,
    ord('+'): None,
    ord('/'): None,
    ord('#'): None,
    ord('['): None,
    ord('"'): None,
    ord(']'): None,
    ord(')'): None,
    ord('*'): None,
}

word_to_number = {
    'zero': 0,
    'null': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninty': 90,
    'hundred': 100,
    'thousand': 1000,
    'million': '1000000',
    'billion': '1000000000'
}

word_to_ordinal ={
    'first': 1,
    'second': 2,
    'third': 3,
    'fourth': 4,
    'fifth': 5,
    'sixth': 6,
    'seventh': 7,
    'eighth': 8,
    'ninth': 9,
    'tenth': 10,
    'eleventh': 11,
    'twelfth': 12,
    'thirteenth': 13,
    'fourteenth': 14,
    'fifteenth': 15,
    'sixteenth': 16,
    'seventeenth': 17,
    'eighteenth': 18,
    'nineteenth': 19,
    'twentieth': 20,
    'thirtieth': 30,
    'fortieth': 40,
    'fiftieth': 50,
    'sixtieth': 60,
    'seventieth': 70,
    'eightieth': 80,
    'ninetieth': 90,
    'hundredth': 100,
    'thousandth': 1000,
    'millionth': '1000000',
    'billionth': '1000000000'
}

cont = Contractions()
cDict = cont.cDict
c_re = re.compile('(%s)' % '|'.join(cDict.keys()))

def readfile(filename):
    with open(filename, encoding='utf-8-sig') as f:
        rows = []
        for line in f:
            rows.append(line)
        return rows

def readfile_cleaned(filename):
    with open(filename, encoding='utf-8-sig') as f:
        rows = []
        for line in f:
            rows.append(line.replace('\n',''))
        return rows

def readtodictionary(filename):
    with open(filename, encoding='utf-8-sig') as f:
        lemmatization = dict()
        for line in f:
            splitted = line.replace("\n", "").split("\t")
            lemmatization[splitted[1]] = splitted[0]
        return lemmatization

def convert(string):
    list1 = []
    list1[:0] = string
    return list1

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cDict[match.group(0)]
    return c_re.sub(replace, text)

def getnumber(name):
    if name in word_to_number:
        return word_to_number[name]
    elif name in word_to_ordinal:
        return word_to_ordinal[name]
    return 0

def isnumber(name):
    if name in word_to_number or name in word_to_ordinal:
        return bool(1)
    return bool(0)

def is_stopword(s):
    if s in stop_words:
        return bool(1)
    return bool(0)

def dropheader(rows):
    for x in range(len(rows)):
        row = rows[0]
        if row.find('Alice was beginning to get very tired') != -1:
            return rows
        else:
            rows.remove(row)
    return rows

def process_sentence(sentence):
    sent_tkns = []
    sent_idxs = []
    for token in sentence.split(' '):
        sent_tkns.append(token)
        sent_idxs.append(voc.to_index(token))
    return (sent_tkns, sent_idxs)

def is_sentence_end(word):
    if word.find('.') != -1 or word.find('?') != -1 or word.find('!') != -1:
        return bool(1)
    return bool(0)

def getTokens(sentence, N):
    slen = len(sentence)
    i = 0
    while (i < slen - N + 1 ):
        for token in sentence [i:i+N]:
            print(token)
        print('\n')
        i = i + 1

stem_words = readtodictionary('.\\data\\lemmatization-en.txt')
stop_words = readfile_cleaned('.\\data\\englishstopwords.txt')

voc = Vocabulary('test')

sentence = []

voc.load_data('test')

for i in range(0, 100):
    print(voc.to_token(i))









