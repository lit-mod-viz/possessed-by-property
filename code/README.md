1. Noun

    A. - char-possession sets (3 days)
	  - Who owns what in the novel?
		  - Requirements: Characters
	  
	  for chapter in novel:
		  for sentence in chapter:
			  - Read sentence
			  - Find 'actor'
			  - Look up verb in WordNet for verb.possession
				  - Isolate 'benefactor'
				  - Extract all B's of form "A verb.possession B""
			  - Output csv
				  - Actor&Benefactor edgelist
		  
    B. - letter-based sets (2 days)
	  - Chunk into letters
		  - Use output from A to produce report
	
    C. - gender based sets (2 days)
	  - Label characters by gender
		  - See B

2. Verbs

    A. - co-occurrence of verb class
	  - Take output from 1A (2 days)
		  - Extract all "A verb.[any] B"
		  - Characterise resulting verb classes
		  
    B. - tense (2 days)
	  - Analyse tenses of all verb classes
		  - De-lemmatize! 
		  
    C. - indirect chain of possession "I own my grandfather's estate" (5 days)
	  - Look for grammatical forms. E.g:
		  - NSubj + verb.possession + (PRPN + NP)
	  
 
3.  Change in the over text time

	- Make sure to extract all words with their index
	
4.  EDA over all of the above

5.  Iterate
