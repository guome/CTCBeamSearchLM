# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:31:47 2019

@author: miklos
"""

from g2p_en import G2p

def text_to_arpa(text):
    g2p = G2p()
    out_list = g2p(text)
    
    for i in range(len(out_list)):
        if len(out_list[i]) > 2:
            symbol = out_list[i]
            symbol = symbol[:-1]
            out_list[i] = symbol
    return ' '.join(out_list)

def corpus_to_arpa(corpus):
    g2p = G2p()
    f = open(corpus, "r")
    text = f.read()
    out = g2p(text)
    return out

if __name__ == '__main__':
        
    stuff = "the fake friend of the family, like the"
    stuff2 = text_to_arpa(stuff)    
    
    arpa_list = corpus_to_arpa('../data/line/corpus.txt')
    
    for i in range(len(arpa_list)):
        if len(arpa_list[i]) > 2:
            symbol = arpa_list[i]
            symbol = symbol[:-1]
            arpa_list[i] = symbol
    
    arpa_text = ' '.join(arpa_list)
    
    f = open("../data/line/corpus_arpa.txt", "a")
    f.write(arpa_text)
    f.close()
