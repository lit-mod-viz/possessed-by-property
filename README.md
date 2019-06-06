2019-06-06

Code and data related to "Clarissa - Possessed by Property".

Updates: 

New Clarissa text, split by letter writer.
Added script for extracting named entities better.
New reports on text split by letters.

To be done (wk ending June 10):

Match entities to associated verb.
    
      for letter in novel:
          for sentence in letter:
              - Read sentence
              - Find 'actor'
              - Look up verb in WordNet for verb.possession
                  - Isolate 'benefactor'
                  - Extract all B's of form "A verb.possession B""
              - Output csv
                  - Actor&Benefactor edgelist


~rdkm
