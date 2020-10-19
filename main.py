from process_text import Processtext
import numpy as np
import sys
import getopt

def readfile(filename):
    with open(filename, encoding='utf-8-sig') as f:
        rows = []
        for line in f:
            rows.append(line)
        return rows

def main(argv):
    inputfile = ''
    outputfile = ''
    n = 0
    try:
        opts, args = getopt.getopt(argv,"hi:o:n:",["ifile=","ofile=","ngram="])
    except getopt.GetoptError:
        print ('main.py -i <inputfile> -o <outputfile> -n <number of ngrams>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-n", "--ngram"):
            n = get_integer(arg)
    return inputfile, outputfile, n

def get_integer(arg):
    n = 0
    try:
        n = int(arg)
    except:
        print("Error: please give positive integer number as n parameter!")
        exit()
    return n

inputfile = ''
outputfile = ''
n = 0
header_string = 'Alice was beginning to get very tired'
footer_string = 'THE END'

if __name__ == "__main__":
    (inputfile, outputfile, n) = main(sys.argv[1:])

process = Processtext()
process.process(inputfile, outputfile, header_string, footer_string, sentence_max_len=15)

processed_text = readfile(outputfile)

text_arr = processed_text[0].split(' ')

ngrams = np.asarray([' '], dtype=np.str)
sentence = []

for token in text_arr:
    sentence.append(token)
    if token == "EOS":
        ngrams = np.append(ngrams, process.get_ngrams(sentence, n))
        sentence.clear()

file_proc = open(outputfile + '_ngrams.txt', "w")
x = 0
for token in ngrams:
    if token == 'SOS':
        x = 0
    file_proc.write(token + ' ')
    x += 1
    if x >= n:
        file_proc.write('\n')
        x = 0

file_proc.close()


