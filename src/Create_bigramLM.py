# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:30:31 2019

@author: miklos

Script to read corpus and create a phoneme bigram dictionary
The bigram dictionary will be saved in a json format
"""
import json
import Classes

def initPhonemeBigrams(corpus_list, classes):
    """init of phoneme bigrams. Reads corpus list of phonemes and outputs 
	bigram dictionary    
	
	Input: corpus_list
		classes 
	Output: bigram dictionary
	"""

    bigram = {c: {d: 0 for d in classes} for c in classes}
    for i in range(0, len(corpus_list)):
        lenght = len(corpus_list[i]) - 1
        for j in range(0, lenght):
            first = corpus_list[i][j]
            second = corpus_list[i][j + 1]

            if j == 29:
                j = j
            # ignore unknown chars
            if first not in bigram or second not in bigram[first]:
                continue
            bigram[first][second] += 1
    return bigram


def get_classes():
    """init of phoneme bigrams    
	Input: NoNe 
	Output: classes of phonemes plus Space
	"""

    classes = [
        "AA",
        "AE",
        "AH",
        "AO",
        "AW",
        "AY",
        "B",
        "CH",
        "D",
        "DH",
        "EH",
        "ER",
        "EY",
        "F",
        "G",
        "HH",
        "IH",
        "IY",
        "JH",
        "K",
        "L",
        "M",
        "N",
        "NG",
        "OW",
        "OY",
        "P",
        "R",
        "S",
        "SH",
        "T",
        "TH",
        "UH",
        "UW",
        "V",
        "W",
        "Y",
        "Z",
        "ZH",
        " ",
    ]
    return classes


def ints2phonemes(inputIntList):
    """Converts a list of ints to a list of phonemes    
	Input: inputIntList
	Output: outList
	"""

    int2phone_dic = {
        0: "AA",
        1: "AE",
        2: "AH",
        3: "AO",
        4: "AW",
        5: "AY",
        6: "B",
        7: "CH",
        8: "D",
        9: "DH",
        10: "EH",
        11: "ER",
        12: "EY",
        13: "F",
        14: "G",
        15: "HH",
        16: "IH",
        17: "IY",
        18: "JH",
        19: "K",
        20: "L",
        21: "M",
        22: "N",
        23: "NG",
        24: "OW",
        25: "OY",
        26: "P",
        27: "R",
        28: "S",
        29: "SH",
        30: "T",
        31: "TH",
        32: "UH",
        33: "UW",
        34: "V",
        35: "W",
        36: "Y",
        37: "Z",
        38: "ZH",
        39: " ",
    }

    outList = []

    for i in range(0, len(inputIntList)):
        for (k, v) in int2phone_dic.items():
            if inputIntList[i] == k:
                outList.append(v)
    return outList


def read_corpus(path):
    """Reads corpus path and transforms it to list of list of phonemes 
	Input: path of corpus
	Output: corpus of phonemes
	"""

    out_list = []
    try:
        fp = open(path)
        content = fp.readlines()

        for i in range(0, len(content)):
            curr_line = content[i].split(",")
            intstr = curr_line[2:]
            int_line_list = intstr[0].split()

            # convert list elements to int
            for j in range(0, len(int_line_list)):
                int_line_list[j] = int(int_line_list[j])

            out_list.append(int_line_list)

    finally:
        fp.close()

    phone_corpus = intcorpus_to_phonemes(out_list)

    return phone_corpus


def intcorpus_to_phonemes(intcorpus):
    """Reads corpus of ints and calls function of ints2phonemes 
	Input: intcorpus
	Output: corpus of phonemes
	"""

    phoneme_corpus = []
    for i in range(0, len(intcorpus)):
        phoneme_corpus.append(ints2phonemes(intcorpus[i]))
    return phoneme_corpus


if __name__ == "__main__":

    path_to_file = "../data/text_processed_small"

    """
    # example decoding matrix containing 2 time-steps and 2 chars
	print('=====ints2phonemes example=====')
    # I USUALLY GET UP LATE ON SATURDAY
	intList = [5, 39, 36, 33, 38, 2, 35, 2, 20, 17, 39, 14, 10, 30, 39, 2, 
               26, 39, 20, 12, 30, 39, 0, 22, 39, 28, 1, 30, 11, 8, 17]
    
	out = ints2phonemes(intList)
	print(out)
    
    # ROCK CLIMBING
	intList = [27, 0, 19, 39, 19, 20, 5, 21, 16, 23]
	out = ints2phonemes(intList)
	print(out)
	"""

    print("===== read_corpus =====")
    list_of_content = read_corpus(path_to_file)
    print("Corpus read.")

    print("===== create bigram =====")
    classes = Classes.get_classes()
    bigram = initPhonemeBigrams(list_of_content, classes)

    with open("bigram.json", "w") as json_file:
        json.dump(bigram, json_file)

    with open("bigram.json") as json_file:
        loaded_bigram = json.load(json_file)
