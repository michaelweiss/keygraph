#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 17:05:16 2021

@author: mrw
"""

import nltk

def test_lemmatize():
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for w in ["last", "las", "us", "Q1-1", "decreased"]:
        print(w, lemmatizer.lemmatize(w))
        
def test_strip():
    for s in [" a", "b ", " c ", "d\n", "e"]:
        print("<{}>".format(s), "<{}>".format(s.strip()))
        
def test_pos_tag():
    s = "the wealthy customers decreased"
    tags = nltk.pos_tag(nltk.word_tokenize(s))
    print(tags)
    print([(w, wordnet_pos(t)) for w, t in tags])
    
def test_lemmatize_pos():
    s = "the wealthy customers decreased"
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tags = nltk.pos_tag(nltk.word_tokenize(s))
    print([lemmatizer.lemmatize(w, wordnet_pos(t)) for w, t in tags])
   
# Lookup WordNet POS
# https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
def wordnet_pos(tag):
    tags = {"J": nltk.corpus.wordnet.ADJ,
            "N": nltk.corpus.wordnet.NOUN,
            "V": nltk.corpus.wordnet.VERB,
            "R": nltk.corpus.wordnet.ADV}
    # tag example: 'VBD' for verb
    return tags.get(tag[0], nltk.corpus.wordnet.NOUN)
        
#-----------Main----------------
if __name__ == "__main__":
    test_lemmatize()
    test_strip()
    test_pos_tag()
    test_lemmatize_pos()