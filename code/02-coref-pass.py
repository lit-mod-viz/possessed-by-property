from neuralcoref import Coref
import os

path = os.getcwd() + '/chapters/'

def run_coref(text):

    coref = Coref()
    clusters = coref.one_shot_coref(utterances=text, context=None)

    return coref.get_resolved_utterances()


def write_file (filename, resolved_text):

    with open(path + filename + '.resolved', 'w') as write_file:
        for item in resolved_text:
            write_file.write("{}\n".format(item))


for filename in os.listdir(path):
    with open(path + filename, 'r') as myreadfile:
        if filename.endswith(".wrap"):
            write_file(filename, run_coref(myreadfile.read()))
