import re
import numpy as np
from numpy.core._multiarray_umath import ndarray

from contractions import Contractions

translation = {
    8217: None,
    8220: '"',
    8221: '"',
    8212: '-',
    8216: '"',
    249: ' ',
    10: ' ',
    ord(','): None,
    ord('.'): None,
    ord(';'): None,
    ord(':'): None,
    ord('?'): None,
    ord('('): None,
    ord('+'): None,
    ord('/'): None,
    ord('#'): None,
    ord('['): None,
    ord(']'): None,
    ord(')'): None,
    ord('*'): None,
    ord('!'): None
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


def convert2number(xx, result):
    if isnumber(text[xx]) or text[xx].find('-') > 0:
        str = text[xx].split('-')
        if len(str) == 1:
            result = getnumber(text[xx])
            xx += 1
            result2 = convert2number(xx, result)
            while type(result2) is int and xx < len(text):
                result += result2
                text.pop(xx)
                result2 = convert2number(xx, result)
        else:
            for item in str:
                if isnumber(item):
                    result += getnumber(item)
            xx += 1
            result2 = convert2number(xx, result)
            while type(result2) is int and xx < len(text):
                result *= result2
                text.pop(xx)
                result2 = convert2number(xx, result)
        return result
    else:
        return text[xx]

rows = readfile('.\\data\\Alice.txt')
stem_words = readtodictionary('.\\data\\lemmatization-en.txt')

result = np.asarray([' '], dtype=np.str)

for row in rows:
    row = row.lower().translate(translation)
    s = np.asarray(row, dtype=np.str)
    result = np.char.add(result, s)

text = np.char.split(result).tolist()[0]

for x in range(len(text)):
    if x >= len(text):
        break
    text[x] = convert2number(x, 0)

result = np.asarray(text)

text_lem = np.asarray([' '], dtype=np.str)

for item in result:
    try:
        y = stem_words[item]
    except:
        y = item
    y = np.char.split(expandContractions(y))
    arr = y.tolist()
    text_lem = np.append(text_lem, arr)

for item in text_lem:
    print(item)






















