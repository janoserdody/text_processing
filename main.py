from typing import Iterator

import numpy as np
from numpy.core._multiarray_umath import ndarray

char_dict = {
    8217 : '"',
    8220 : '"',
    8221 : '"',
    8212 : '-',
    8216 : '"',
    249: ' ',
    10: ' '
}

def readfile(filename):
    with open(filename, encoding='utf-8-sig') as f:
        rows = []
        for line in f:
            rows.append(line)
        return rows

def readtodictionary(filename):
    with open(filename, encoding='utf-8-sig') as f:
        lemmatization = dict()
        for line in f:
            splitted = line.replace("\n", "").split("\t")
            lemmatization[splitted[1]] = splitted[0]
        return lemmatization

def filter_char(x):
    if (ord(x) > 127) or (ord(x) < 32):
        return char_dict[ord(x)]
    return x

def convert(string):
    list1 = []
    list1[:0] = string
    return list1

rows = readfile('.\\data\\Alice.txt')
stem_words = readtodictionary('.\\data\\lemmatization-en.txt')

result = np.asarray([' '], dtype=np.str)

for row in rows:
    row = row.lower()
    string_list = convert(row)
    cleaned_text = map(filter_char, string_list)
    s = np.asarray(''.join(cleaned_text), dtype=np.str)
    result = np.char.add(result, s)

result = np.char.split(result)

text_lem = np.asarray([' '], dtype=np.str)

for item in result[0]:
    try:
        y = stem_words[item]
    except:
        y = item
    yres = np.asarray([y], dtype=np.str)
    text_lem = np.append(text_lem, yres)

for item in text_lem:
    print(item)


















