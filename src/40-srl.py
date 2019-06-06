import os, subprocess

path = '../text/split/'

for filename in os.listdir(path):
    with open(path + filename, 'r', encoding="utf-8") as myreadfile:
        if filename.endswith(".sents"):
            incant = '/Users/au564346/senna/senna-osx -path /Users/au564346/senna/senna < ' + \
                        path + filename + ' > ' + path + filename + '.srl'
            subprocess.call(incant, shell=True)
