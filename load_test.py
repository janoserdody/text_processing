from vocabulary import Vocabulary

voc = Vocabulary('test')

sentence = []

voc.load_data('test')

for i in range(voc.count_words()):
    print(voc.to_token(i))
