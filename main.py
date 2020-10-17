from process_text import Processtext

process = Processtext()
process.process('.\\data\\Alice.txt', '.\\data\\processed_text.txt', sentence_max_len=15)


