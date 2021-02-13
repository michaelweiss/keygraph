#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:20:30 2021

@author: mrw
"""

# import sys
import nltk
# from nltk.collocations import *

from re import sub

def delete_noise(text):
    # Read noise file
    # Remove noise
    # We don't need to do this. What we need is some code to
    # strip html tags and punctuation from a document.         
    return text

# Read noise file
def noise_list():
    return [line[:-1] for line in open('./noise/noise.txt', 'r')]
    
# Create sentences
def create_sentences(text):
    return nltk.tokenize.sent_tokenize(text)

# Create words
def create_words(text):
    return nltk.tokenize.word_tokenize(text)

#-----------Main----------------
if __name__ == "__main__":
    # Read event file
    f = open('./txt_files/actions.txt', 'r')
    doc = f.read()
        
    # Delete noise
    doc = delete_noise(doc)
    
    # Divide into sentences
    sentences = create_sentences(doc) 
    
    # Divide into words and punctuation
    words = create_words(doc)
    
    # All lower-case letters
    words = [w.lower() for w in words]
    sentences = [s.lower() for s in sentences]
    
    # Generate text
    text = nltk.text.Text(words)
    
    print(text)
