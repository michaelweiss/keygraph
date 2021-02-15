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
        
#-----------Main----------------
if __name__ == "__main__":
    test_lemmatize()
    test_strip()