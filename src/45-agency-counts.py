import os, csv
import string
from collections import Counter
from pandas import DataFrame
from textblob import Word
from textblob import TextBlob

def clean_string(w):
    return Word(w.strip().translate(
        str.maketrans('','',string.punctuation)))

blacklist = ['\'t', 'man', 'woman', 'didn', 'don' 'isn', 'hadn',
        'd.', '\'p', 'o.', '\'d', '\'a', '\'it', '\'c', 'couldn',
        'w', 'n', '\'w', '\'n', '\'let', 'doesn', '\'l', '\'r',
        '\'who', 'am', '\'o', '\'f', 'wa', 'r', '\'h', '\'e', '\'g',
        '\'k', 't', 's', 'p', 'l', 'd', 'sir', 'k',
        'o', 'a', 'id', 'c', 'g', 'e', 'yes', 'f']

# penn treebank noun labels
noun_labels = ['NN', 'NNS', 'NNP', 'NNPS']

# grouping "patients" and "adjuncts" in SRL lingo
benefactor_labels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

# honorific titles
titles = ["Dr", "Doctor", "Professor", "Mr", "Mrs", "Lady", "Sir", "Miss", "Ms", "Madame", "Count", "St"]


# set path
path = '../text/split/'

# process csv blocks
# REMEMBER TO SET FOR SUB-FOLDERS - VOLUMES, ETC.
csv_blocks = []
for filename in os.listdir(path):
    if filename.endswith(".srl"):
        with open(path + filename, 'r') as csvfile:
            srlreader = csv.reader(csvfile, delimiter="\t")

            block = []
            for row in srlreader:
                if len(row) > 0:
                    block.append(row)
                else:
                    csv_blocks.append(block)
                    block = []

############################################
"""
Extract A0 agents
"""
############################################

# process each black as dataframe
agent_list = []

for block in csv_blocks:
    srl_block_panda_df = DataFrame.from_records(block)
    for column in srl_block_panda_df:
        for index, item in srl_block_panda_df[column].iteritems():
            if 'A0' in item:
                nouna = clean_string(srl_block_panda_df[0][index])
                labela = srl_block_panda_df[1][index].strip()
                if labela in noun_labels and nouna and nouna not in blacklist:
                    agent = nouna
                    agent_list.append(agent)


# join up names with titles - eg Mr + Rochdale
joined_up = []
all_indices = []
for idx, agent in enumerate(agent_list):
    if any(title in agent for title in titles):
        indices = idx, idx+1
        all_indices.append(indices)
        name = (agent_list[idx], agent_list[idx+1])
        joined_up.append(' '.join(name))

# delete the unconnected entities and extend joined_up list
for i in sorted([item for t in all_indices for item in t], reverse=True):
    del agent_list[i]

joined_up.extend(agent_list)

# count number of occurrences per character
counts = Counter(joined_up).most_common()

# write to csv
with open("../out/agents_A0.csv", 'a') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['name','num'])
    for entry in counts:
        csv_out.writerow(entry)

##############################################
"""
Extract A1-A5 benefactors
"""
##############################################

# process each black as dataframe
benefactor_list = []

for block in csv_blocks:
    srl_block_panda_df = DataFrame.from_records(block)
    for column in srl_block_panda_df:
        for index, item in srl_block_panda_df[column].iteritems():
            if any(label in item for label in benefactor_labels):
                nouna = clean_string(srl_block_panda_df[0][index])
                labela = srl_block_panda_df[1][index].strip()
                if labela in noun_labels and nouna and nouna not in blacklist:
                    benefactor = nouna
                    benefactor_list.append(benefactor)


# join up names with titles - eg Mr + Rochdale
joined_up = []
all_indices = []
for idx, benefactor in enumerate(benefactor_list):
    if any(title in benefactor for title in titles):
        indices = idx, idx+1
        all_indices.append(indices)
        name = (benefactor_list[idx], benefactor_list[idx+1])
        joined_up.append(' '.join(name))

# delete the unconnected entities and extend joined_up list
for i in sorted([item for t in all_indices for item in t], reverse=True):
    del benefactor_list[i]

joined_up.extend(benefactor_list)

# count number of occurrences per character
counts = Counter(joined_up).most_common()

# write to csv
with open("../out/benefactors_A1-A5.csv", 'a') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['name','num'])
    for entry in counts:
        csv_out.writerow(entry)



