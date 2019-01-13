import os, csv
import string
from collections import Counter
from pandas import DataFrame
from textblob import Word
from textblob import TextBlob

path = os.getcwd() + '/'
#path = '/home/denten/Documents/papers/projects-academic/workbench/lit-mod-viz/char-agent/corpus/airport/'

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
benefactor_labels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

# only grabbing the boundary-defining semantic roles related to location
factor_labels = ['AM-DIR', 'AM-EXT', 'AM-LOC']

def clean_string(w):
    return Word(w.strip().lower().translate(
        str.maketrans('','',string.punctuation))).lemmatize()

# Parse the csv in sentence blocks which in our data are separated by blank
# lines. Go through each column clause and if you find A0 grab also all the
# A1+ in the same sentence block. Write results into a list of lists. Columns
# are necessary because A0 can be in any column and we have an arbitrary
# number of columns in senteces that have many clauses.

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
srl_edge_list = []

for block in csv_blocks:
    srl_block_panda_df = DataFrame.from_records(block)
    for column in srl_block_panda_df:
        for index0, item0 in srl_block_panda_df[column].iteritems():
            if 'A0' in item0:

                nouna = clean_string(srl_block_panda_df[0][index0])
                labela = srl_block_panda_df[1][index0].strip()

                if labela in noun_labels and nouna and nouna not in blacklist:

                    actor = nouna
                    benefactors = []

                    for index1, item1 in srl_block_panda_df[column].iteritems():

                        nounb = clean_string(srl_block_panda_df[0][index1])
                        labelb = srl_block_panda_df[1][index1].strip()

                        if any(l in item1 for l in benefactor_labels) and                         labelb in noun_labels and nounb and nounb not in blacklist:
                            benefactors.append(nounb)

                    srl_edge_list.append([actor, benefactors])

final_edge_tuples = []

for cluster in srl_edge_list:
    actor = cluster[0]
    if cluster[1]:
        for benefactor in cluster[1]:
            final_edge_tuples.append([actor, benefactor])
    else: # there are no benefactors, assume self referential action
        final_edge_tuples.append([actor, actor])

with open(path + 'reports/06-actor-benefactor-edge-list.csv', 'w') as write_file:
    csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)
    for t in final_edge_tuples:
        csvwriter.writerow(t)
