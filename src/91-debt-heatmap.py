import os, csv, ast
import numpy as np
import pandas as pd
from pandas import Series
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

path = os.getcwd() + '/'
#path = '/home/denten/Documents/papers/projects-academic/workbench/lit-mod-viz/char-agent/corpus/airport/'

# not resolving enteties here
# safe to just include the common character references
blacklist = ['t', 'vernon', 'bakersfeld', 'livingstone', 'freemantle',
             'captain', 'lady', 'men', 'man', 'peter', 'case']

# read in the csv edge list
edge_tuples = []
with open('../reports/06-actor-benefactor-edge-list.csv', 'r') as csvfile:
    srlreader = csv.reader(csvfile, delimiter=',')

    for row in srlreader:
        edge_tuples.append(row)

edge_counts = []
with open('../reports/09-edge-counts.csv', 'r') as csvfile:
    srlreader = csv.reader(csvfile, delimiter=',')

    for row in srlreader:
        edge_counts.append(row)

total_edge_count = []
for i in edge_counts:
    total_edge_count.append(int(i[2]))

# parse out actors and benefactors
# we want to draw most common actors > most common benefactors
actors = []
benefactors = []

actors = [a[0] for a in edge_tuples]
benefactors = [b[1] for b in edge_tuples]

common_actors = Counter(actors).most_common()
common_benefactors = Counter(benefactors).most_common()

# create pandas data frame and fill in with individual
# debt ratios
actorsc = [a[0] for a in common_actors[0:25] if a[0] not in blacklist]
benefactorsc = [b[0] for b in common_benefactors[0:22] if b[0] not in blacklist]

# create a data frame for seaborn heatmap
df = pd.DataFrame(index=benefactorsc, columns=actorsc)

# give each axis a name
df.axes[0].rename('benefactors', inplace=True)
df.axes[1].rename('actors', inplace=True)

for x in actorsc:
    for y in benefactorsc:
        xy_value = 0
        yx_value = 0

        for e in edge_counts:

            # data looks like this: mel,mel,256
            # look for a > b match
            # assume zero at the outset

            if x == e[0] and y == e[1]:
                xy_value = int(e[2])

            if y == e[0] and x == e[1]:
                yx_value = int(e[2])

        value = (xy_value - yx_value)/sum(total_edge_count)*100
        df.at[y,x] = value

# fill in any NaN values with 0
df.fillna(0, inplace=True)

fsize = 10

# draw heatmap
ax = sns.heatmap(df)
ax.xaxis.set_tick_params(labeltop=True, labelbottom=False, rotation=70,
        labelsize=fsize)
ax.yaxis.set_tick_params(rotation=0, labelsize=fsize)
ax.get_figure

# save data frame and graphic to disk
df.to_html('../reports/91-dataframe.html')

fig = ax.get_figure()
fig.tight_layout()
fig.savefig("../reports/graphs91-output.png", dpi=600)

