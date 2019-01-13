from textblob import TextBlob
import os

path = os.getcwd() + '/chapters/'

def tokenize(text):

    blob = TextBlob(text)

    return blob.sentences

def write_file (filename, toke_text):

    with open(path + filename + '.sents', 'w') as write_file:
        for item in toke_text:
            write_file.write("{}\n".format(item.string))

for filename in os.listdir(path):
    if filename.endswith(".resolved"):
        with open(path + filename, 'r') as myreadfile:
            write_file(filename, tokenize(myreadfile.read()))
