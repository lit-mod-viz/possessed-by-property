import os, subprocess

path = os.getcwd() + '/chapters/'

for filename in os.listdir(path):
    with open(path + filename, 'r') as myreadfile:
        if filename.endswith(".sents"):
            incant = '/home/denten/bin/senna/senna -path /home/denten/bin/senna/ < ' + \
                        path + filename + ' > ' + path + filename + '.srl'
            subprocess.call(incant, shell=True)
