#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:20:30 2021

@author: mrw
"""

# import sys
# import nltk
# from nltk.collocations import *

def delNoise(text):
    # Read noise file
    # Remove noise
    # We don't need to do this. What we need is some code to
    # strip html tags and punctuation from a document.         
    return text

# Read noise file
def noise_list():
    return [line[:-1] for line in open('./noise/noise.txt', 'r')]
    
#-----------Main----------------
if __name__ == "__main__":
    # Read event file
    f = open('./txt_files/actions.txt', 'r')
    raw = f.read()
        
    # Delete noise
    delNraw = delNoise(raw)
    
    print(delNraw)
