from __future__ import division
from __future__ import print_function

import sys
import numpy as np
import BeamSearch
import LanguageModel
import g2p_converter

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

def get_classes():
    classes = [' ', 'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH',
               'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 
               'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 
               'UW', 'V', 'W', 'Y', 'Z', 'ZH']
    return classes    

def loadRNNOutput(fn):
	"load RNN output from csv file. Last entry in row terminated by semicolon."
	return np.genfromtxt(fn, delimiter=';')[:, : -1]


def testMiniExample():
	"example which shows difference between taking most probable path and most probable labeling. No language model used."

	# chars and input matrix
	classes = ['AA', 'B', 'CH']
	mat = np.array([[0.4, 0, 0.6, 0.2], [0.4, 0, 0.6, 0.2]])
    
    # decode
	gt = 'CH'
	print('TARGET       :', '"' + gt + '"')
	print('BEAM SEARCH  :', '"' + BeamSearch.ctcBeamSearch(mat, classes, None) + '"')

def testLineExample():
	"example which decodes a RNN output of a text line. Taken from IAM dataset. RNN output produced by TensorFlow model."

	# chars of IAM dataset
	#classes = ' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
	classes = get_classes()
    # matrix containing TxC RNN output. C=len(classes)+1 because of blank label.
	mat = softmax(loadRNNOutput('../data/line/rnnOutput.csv'))

	# language model: used for token passing (word list) and beam search (char bigrams)
	lm = LanguageModel.LanguageModel('../data/line/corpus_arpa.txt', classes)

	# decode RNN output with different decoding algorithms
	gt = 'the fake friend of the family like the'
	gt_arpa = g2p_converter.text_to_arpa(gt)
        
	print('TARGET        :', '"' + gt_arpa + '"')
	print('BEAM SEARCH   :', '"' + BeamSearch.ctcBeamSearch(mat, classes, None) + '"')
	print('BEAM SEARCH LM:', '"' + BeamSearch.ctcBeamSearch(mat, classes, lm) + '"')

if __name__ == '__main__':

	# example decoding matrix containing 2 time-steps and 2 chars
	print('=====Mini example=====')
	testMiniExample()

	# example decoding a text-line
	print('=====Line example=====')
	testLineExample()
