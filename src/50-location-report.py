import os, csv
import string
from collections import Counter
from pandas import DataFrame
from textblob import Word
from textblob import TextBlob

#path = '../split'

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

# boundary-defining semantic roles
context_labels = ['AM-DIR', 'AM-EXT', 'AM-LOC', 'AM-TMP']

def clean_string(w):
    return Word(w.strip().lower().translate(
        str.maketrans('','',string.punctuation))).lemmatize()

# parse the csv in blocks
# separated by blank lines
# write into a list of lists
csv_blocks = []
for filename in os.listdir('../text/split/'):
    if filename.endswith(".srl"):
        with open('../text/split/' + filename, 'r') as csvfile:
            srlreader = csv.reader(csvfile, delimiter='\t')

            block = []
            for row in srlreader:
                if len(row) > 0:
                    block.append(row)
                else:
                    csv_blocks.append(block)
                    block = []

# process each block as dataframe
context_list = []

for block in csv_blocks:
    srl_block_panda_df = DataFrame.from_records(block)
    for column in srl_block_panda_df:
        for index0, item0 in srl_block_panda_df[column].iteritems():
            if any(l in item0 for l in context_labels):
                noun = clean_string(srl_block_panda_df[0][index0])
                label = srl_block_panda_df[1][index0].strip()

                if label in noun_labels and noun not in blacklist:
                    context_list.append(noun)

common_contexts = Counter(context_list).most_common()

with open('../reports/05-location-report.txt', 'w') as f:
    for line in common_contexts:
        f.write(str(line) + "\n")
