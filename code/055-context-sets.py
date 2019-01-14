import os, csv
import string
from collections import Counter
from pandas import DataFrame
from textblob import Word
from textblob import TextBlob

path = os.getcwd() + '/'
# using this code for Airport only atm
# path = '/home/denten/Documents/papers/projects-academic/workbench/lit-mod-viz/char-agent/corpus/airport/'

# filter out what, that, this, and other junk etc.
# better do this with parts of speech NN and NNP
# need to parse the full report for this
# todo: add noun phrase chunker to differentiate betwen mr. x and mrs. x

blacklist = ['\'t', 'man', 'woman', 'mrs', 'mr', 'didn', 'isn', 'hadn',
        'd.', '\'p', 'o.', '\'d', '\'a', '\'it', '\'c', 'couldn',
        'w', 'n', '\'w', '\'n', '\'i', '\'let', 'doesn', '\'l', '\'r',
        '\'who', 'am', '\'o', '\'f', 'wa', 'r', '\'h', '\'e', '\'g',
        '\'k', 't', 'mr', 'mrs', 's', 'p', 'l', 'i', 'd', 'sir', 'k', 
        'o', 'a', 'id', 'c', 'g', 'e', 'yes', 'f']

# penn treebank noun labels
noun_labels = ['NN', 'NNS', 'NNP', 'NNPS']

# grouping "patients" and "adjuncts" in SRL lingo
char_labels = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']

# boundary-defining semantic roles
context_labels = ['AM-DIR', 'AM-EXT', 'AM-LOC', 'AM-TMP']

def clean_string(w):
    return Word(w.strip().lower().translate(
        str.maketrans('','',string.punctuation))).lemmatize()

# parse the csv in blocks
# separated by blank lines
# write into a list of lists
csv_blocks = []
for filename in os.listdir(path + 'chapters/'):
    if filename.endswith(".srl"):
        with open(path + 'chapters/' + filename, 'r') as csvfile:
            srlreader = csv.reader(csvfile, delimiter='\t')

            block = []
            for row in srlreader:
                if len(row) > 0:
                    block.append(row)
                else:
                    csv_blocks.append(block)
                    block = []

# process each black as dataframe
context_list = []

for block in csv_blocks:
    srl_block_panda_df = DataFrame.from_records(block)
    for column in srl_block_panda_df:
        for index0, item0 in srl_block_panda_df[column].iteritems():

            if any(l in item0 for l in context_labels):
                nouna = clean_string(srl_block_panda_df[0][index0])
                labela = srl_block_panda_df[1][index0].strip()

                if labela in noun_labels and nouna and nouna not in blacklist:

                    context = nouna
                    actants = []

                    for index1, item1 in srl_block_panda_df[column].iteritems():
                        nounb = clean_string(srl_block_panda_df[0][index1])
                        labelb = srl_block_panda_df[1][index1].strip()

                        if any(l in item1 for l in char_labels) and \
                        labelb in noun_labels and nounb and \
                        nounb not in blacklist:
                            actants.append(nounb)

                    context_list.append([context, actants])

# at this point we have a list that looks like this
# [plane, [mel, gwen]] representing every sentence
# we now need to consolidate around unique characters
# convert list into a dictionary with each noun as key

context_dict = {}
for item in context_list:

# the more pythonic way to initialize lists

#    if item[1]:
#        for i in item[1]:
#            context_dict.setdefault(item[0], []).append(i)
#

# this way is more verbose but the logic is clearer

    if item[1]:
        if item[0] in context_dict:
            context_dict[item[0]] = context_dict[item[0]] + item[1]
        else:
            context_dict[item[0]] = item[1]

# now let's get unique counts for members
# for item in context_dict.items():

for key, value in context_dict.items():
    context_dict[key] = Counter(value).most_common()

# and write out

with open(path + 'reports/055-context-members.txt', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in context_dict.items():
       writer.writerow([key, value])
