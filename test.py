#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 17:05:16 2021

@author: mrw
"""

import nltk

def test():
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for w in ["last", "las"]:
        print(w, lemmatizer.lemmatize(w))
        
#-----------Main----------------
if __name__ == "__main__":
    test()