# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 11:23:01 2019

@author: miklos

Main script:
	Reads NN putput matrix, reads previously saved bigram dictionary from a json format
	Calls BeamSearch algorithm without and with phoneme level bigram LM 
"""

import numpy as np
import BeamSearch
import LanguageModel
import pandas as pd
import Classes

def softmax(mat):
	"calc softmax such that labels per time-step form probability distribution"
	maxT, _ = mat.shape # dim0=t, dim1=c
	res = np.zeros(mat.shape)
	for t in range(maxT):
		y = mat[t, :]
		e = np.exp(y)
		s = np.sum(e)
		res[t, :] = e/s
	return res

def loadRNNOutput(fn):
	"load RNN output from csv file. Last entry in row terminated by semicolon."
	return np.genfromtxt(fn, delimiter=';')[:, : -1]


def testMiniExample():
	"example which shows Beam search with and without LM"
	
	# classes for the simple phoneme recognition
	#classes = ['AA', 'B', 'CH']
	#mat = np.array([[0.4, 0, 0.6, 0.2], [0.4, 0, 0.6, 0.2]])
    
	# phonemes and input matrix
	df = pd.read_csv('testminiexampledata.csv', header = None)
	classes = Classes.get_classes()
	mat = df.values   
	
	lm = LanguageModel.LanguageModel('bigram.json', classes)
	
    # decode
	gt = ['M', 'AY', ' ', 'CH', 'AE', 'T']
	print('TARGET       : {}'.format(gt))
	#resultofBeamSearch = BeamSearch.ctcBeamSearch(mat, classes, None)
	#print('BEAM SEARCH  mat: {}'.format(resultofBeamSearch))
	resultofBeamSearch = BeamSearch.ctcBeamSearch(mat, classes, None)
	print('BEAM SEARCH  expl: {}'.format(resultofBeamSearch))
	resultofBeamSearch = BeamSearch.ctcBeamSearch(mat, classes, lm)
	print('BEAM SEARCH  LM: {}'.format(resultofBeamSearch))

if __name__ == '__main__':

	# example decoding dummy matrix containing reference sequence of 'My cat'
	print('=====Mini example=====')
	testMiniExample()


    
    
    
