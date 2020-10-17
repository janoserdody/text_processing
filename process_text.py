import re
import numpy as np

from vocabulary import Vocabulary
from contractions import Contractions

class Processtext:
    def __init__(self):
        self.PAD_token = 0   # Used for padding short sentences
        self.SOS_token = 1   # Start-of-sentence token
        self.EOS_token = 2   # End-of-sentence token
        self.text = []
        self.stop_words = self.readfile_cleaned('.\\data\\englishstopwords.txt')
        self.stem_words = self.readtodictionary('.\\data\\lemmatization-en.txt')
        self.trans_punctuation = {ord('.'): None, ord('?'): None, ord('!'): None, ord(';'): None, ord(','): None,
                                  ord('-'): None}

        self.translation = {
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
            ord('_'): None
        }

        self.word_to_number = {
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

        self.word_to_ordinal ={
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

        self.cont = Contractions()
        self.cDict = self.cont.cDict
        self.c_re = re.compile('(%s)' % '|'.join(self.cDict.keys()))

    def readfile(self, filename):
        with open(filename, encoding='utf-8-sig') as f:
            rows = []
            for line in f:
                rows.append(line)
            return rows

    def readfile_cleaned(self, filename):
        with open(filename, encoding='utf-8-sig') as f:
            rows = []
            for line in f:
                rows.append(line.replace('\n', ''))
            return rows

    def readtodictionary(self, filename):
        with open(filename, encoding='utf-8-sig') as f:
            lemmatization = dict()
            for line in f:
                splitted = line.replace("\n", "").split("\t")
                lemmatization[splitted[1]] = splitted[0]
            return lemmatization

    def convert(self, string):
        list1 = []
        list1[:0] = string
        return list1

    def expand_contractions(self, text):
        def replace(match):
            return self.cDict[match.group(0)]
        return self.c_re.sub(replace, text)

    def get_number(self, name):
        if name in self.word_to_number:
            return self.word_to_number[name]
        elif name in self.word_to_ordinal:
            return self.word_to_ordinal[name]
        return 0

    def is_number(self, name):
        if name in self.word_to_number or name in self.word_to_ordinal:
            return bool(1)
        return bool(0)

    def convert2number(self, xx, result):
        if self.is_number(self.text[xx]) or self.text[xx].find('-') > 0:
            str = self.text[xx].split('-')
            if len(str) == 1:
                result = self.get_number(self.text[xx])
                xx += 1
                result2 = self.convert2number(xx, result)
                while type(result2) is int and xx < len(self.text):
                    result += result2
                    self.text.pop(xx)
                    result2 = self.convert2number(xx, result)
            else:
                for item in str:
                    if self.is_number(item):
                        result += self.get_number(item)
                xx += 1
                result2 = self.convert2number(xx, result)
                while type(result2) is int and xx < len(self.text):
                    result *= result2
                    self.text.pop(xx)
                    result2 = self.convert2number(xx, result)
            return result
        else:
            return self.text[xx]

    def is_stopword(self, s):
        if s in self.stop_words:
            return bool(1)
        return bool(0)

    def dropheader(self, rows):
        for x in range(len(rows)):
            row = rows[0]
            if row.find('Alice was beginning to get very tired') != -1:
                return rows
            else:
                rows.remove(row)
        return rows

    def process_sentence(self, sentence):
        sent_tkns = []
        sent_idxs = []
        for token in sentence.split(' '):
            sent_tkns.append(token)
            sent_idxs.append(self.voc.to_index(token))
        return (sent_tkns, sent_idxs)

    def is_sentence_end(self, word):
        if word.find('.') != -1 \
                or word.find('?') != -1 \
                or word.find('!') != -1 \
                or word.find(';') != -1:
            return bool(1)
        return bool(0)

    def get_tokens(self, sentence, n):
        slen = len(sentence)
        i = 0
        while (i < slen - n + 1):
            for token in sentence [i:i + n]:
                print(token)
            print('\n')
            i = i + 1

    def process(self, filename_read, filename_save, sentence_max_len = 15):
        rows = self.readfile(filename_read)

        result = np.asarray([' '], dtype=np.str)

        rows = self.dropheader(rows)

        for row in rows:
            # find footer
            if row.find('THE END') != -1:
                break
            row = row.lower().translate(self.translation)
            s = np.asarray(row, dtype=np.str)
            result = np.char.add(result, s)

        self.text = np.char.split(result).tolist()[0]

        self.text = list(filter(lambda stop: (self.is_stopword(stop) == bool(0)), self.text))

        for x in range(len(self.text)):
            if x >= len(self.text):
                break
            self.text[x] = self.convert2number(x, 0)

        result = np.asarray(self.text)

        text_lem = np.asarray([' '], dtype=np.str)

        for item in result:
            try:
                y = self.stem_words[item]
            except:
                y = item
            y = np.char.split(self.expand_contractions(y))
            arr = y.tolist()
            text_lem = np.append(text_lem, arr)

        voc = Vocabulary('test')

        sentence = []

        text_out = [voc.to_token(self.SOS_token)]

        sen_length = 0

        for word in text_lem:
            if word == " ":
                continue
            sentence.append(word)
            sen_length += 1
            if self.is_sentence_end(word) \
                    or ((word == "and" or word.find(',') > -1 or word.find('-') > -1) and sen_length > sentence_max_len):
                index = sentence.index(word)
                sentence[index] = word.translate(self.trans_punctuation)
                sentence_str = ' '.join(sentence)
                voc.add_chunk(sentence_str)
                text_out.append(voc.to_token(self.EOS_token))
                text_out.append(voc.to_token(self.SOS_token))
                sentence.clear()
                sen_length = 0
            else:
                text_out.append(word)

        text_out[len(text_out) - 1] = "\n"

        voc.save_data('test')

        x = 0
        file_proc = open(filename_save, "w")
        for token in text_out:
            if token == voc.to_token(self.EOS_token):
                for i in range(voc.count_longest_sentence() - x):
                    file_proc.write(voc.to_token(self.PAD_token) + " ")
                x = 0
            file_proc.write(token + " ")
            x += 1

        file_proc.close()




