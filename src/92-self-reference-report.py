import os, csv
from collections import Counter
from operator import itemgetter

path = os.getcwd() + '/'
#path = '/home/denten/Documents/papers/projects-academic/workbench/lit-mod-viz/char-agent/corpus/airport/'

# resolving compound names by hand at the moment
blacklist = ['t', 'vernon', 'bakersfeld', 'livingstone', 'freemantle',
             'captain', 'lady', 'men', 'man', 'peter']

# read in the csv edge list
self_ref = []
with open('../reports/09-edge-counts.csv', 'r') as csvfile:
    srlreader = csv.reader(csvfile, delimiter=',')

    for row in srlreader:
        self_ref.append(row)

# calculate ratio of self-referential action/total action by self
self_ref_counts = []
for rowa in self_ref:
    # mel, mel, 230
    if rowa[0] == rowa[1]:

        char_count = []
        for rowb in self_ref:
            if rowb[0] == rowa[0]:
                char_count.append(int(rowb[2]))

        solipsism = round(int(rowa[2])/sum(char_count), 2)
        self_ref_counts.append([rowa[0], rowa[1], rowa[2], sum(char_count), solipsism])

sorted_counts = sorted(self_ref_counts, key=itemgetter(4), reverse=False)
# write out actors
with open('../reports/92-solipcism.csv', 'w') as write_file:

    csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['actor', 'benefactor', 'self-act', 'total-act', 'self-ratio'])
    for c in sorted_counts:
            csvwriter.writerow(c)
