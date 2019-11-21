"""
Created on Tue Nov 20 12:43:26 2019

@author: miklos

LanguageModel script:
	Reads bigram dictionary from a json format
"""

import json
import Create_bigramLM


class LanguageModel:
	"simple language model: word list for token passing, char bigrams for beam search"
	def __init__(self, fn, classes):
		"read json to generate language model"
		self.initPhonemeBigrams(fn, classes)

	def initPhonemeBigrams(self, fn, classes):
		"internal init of character bigrams"
		
		with open(fn) as json_file:
			loaded_bigram = json.load(json_file)

		# init bigrams with 0 values
		self.bigram = loaded_bigram

	def getPhonemeBigram(self, first, second):
		"probability of seeing phoneme 'first' next to 'second'"
		first = first if first else ' ' # map start to word beginning
		second = second if second else ' ' # map end to word end

		# number of bigrams starting with given phoneme
		numBigrams = sum(self.bigram[first].values())
		if numBigrams == 0:
			return 0
		
		return self.bigram[first][second] / numBigrams


if __name__ == '__main__':
	
	classes2 = Create_bigramLM.get_classes()
	lm = LanguageModel('bigram.json', classes2)
	c1 = ' '
	c2 = 'AA'
	lmFactor = 0.01 # influence of language model
	bigramProb = lm.getPhonemeBigram(c1, c2) 	
	bigramProb = bigramProb ** lmFactor
	
	expected = 0.013159808858996246
	actual = lm.getPhonemeBigram(c1, c2)
	print("Expected: {}".format(expected))
	print("Actual: {}".format(actual))
	print('OK' if expected == actual else 'ERROR')
