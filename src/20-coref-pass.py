import spacy
import os

path = '../text/split/'

def run_coref(text):

    nlp = spacy.load('en_coref_md')
    doc = nlp(text)

    return doc._.coref_resolved

def write_file (filename, resolved_text):

    with open(path + filename + '.resolved', 'w') as write_file:
        for item in resolved_text:
            # write_file.write("{}\n".format(item))
            write_file.write(item)


for filename in os.listdir(path):
    with open(path + filename, 'r') as myreadfile:
        if filename.endswith(".wrap"):
            write_file(filename, run_coref(myreadfile.read()))
