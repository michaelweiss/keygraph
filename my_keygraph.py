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
    noise_list=[]
    for line in open('./noise/noise.txt', 'r'):
        noise_list.append(line[:-1])	
    return noise_list
    
#-----------Main----------------
if __name__ == "__main__":
    # Read event file
    f = open('./txt_files/actions.txt', 'r')
    raw = f.read()
    
    # Delete noise
    delNraw = delNoise(raw)
    
    print(delNraw)
