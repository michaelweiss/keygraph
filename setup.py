#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 19:35:52 2021

@author: mrw
"""

import nltk

def setup():
    # Obtain NLTK resources
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

#-----------Main----------------
if __name__ == "__main__":
    setup()