#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:20:30 2021

@author: mrw
"""

import nltk
import time

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
# Returns a list of strings
def create_sentences(text):
    return nltk.tokenize.sent_tokenize(text)

# Create words
# Returns a list of strings
def create_words(text):
    return nltk.tokenize.word_tokenize(text)

# Calulate high-frequency words
def high_frequency(text):
    fd = nltk.probability.FreqDist(strip_stopwords_and_symbols(text))
    return list(fd.keys())[:30] 

# Strip stopwords and special symbols from text
def strip_stopwords_and_symbols(text):
    stopwords = nltk.corpus.stopwords.words('english')
    symbols = ["'", '"', '`', '.', ',', '-', '!', '?', ':', ';', '(', ')', '&', '0']
    return [w for w in text if w not in stopwords + symbols]

# Calculate co-occurrence of frequent words
def calculate_co_occurrence(hf, sentences):
    co = {} 
    for hf1 in hf:
        co[hf1] = {}
        for hf2 in hf[hf.index(hf1) + 1:]:
            co[hf1][hf2] = 0 
            for s in sentences:
                # Why sum products, not min, as in Ohsawa (1998)?
                co[hf1][hf2] += s.count(hf1) * s.count(hf2)
    co_list = [] 
    for x in co.keys():
        for y in co[x].keys():
            co_list.append([x, y, co[x][y]])
    co_list.sort(key = lambda a: a[2])
    return co_list

# Calculate word frequency in sentences
def calculate_wfs(words, sentences):
    wfs = {} 
    for w in words:
        for s in sentences:
            if w not in wfs:
                wfs[w] = {}
            wfs[w][s] = s.count(w)
    return wfs
    
# Compute key (terms that tie and hold clusters together) 
def key(words, wfs, base, sentences):
    # key is a dictionary of the form　key = {w: key value}	
    key = {}
    stime = time.time()
    
    # Compute F(g)
    Fg = fg(words, wfs, base, sentences)
    etime = time.time()
    print(str(etime - stime))
    print(Fg)
    for w in words:
        product = 1.0
        for b in base:
            product *= (1 - fwg(w, wfs, b, sentences) * (1.0) / Fg[b]) 
        key[w] = 1.0 - product
    return key

def fwg(w, wfs, b, sentences):
    gws = 0
    fwg = 0
    for s in sentences:
        # Calculate |g-w|_s  
        # Count of cluster g in s: g_s = wfs[g][s]
        # Word in s: w_s = wfs[w][s]
        if b.find(w) >= 0: # w ∈ g
            # |g|_s
            gws = wfs[b][s] - wfs[w][s]
        else: # w not ∈ g
            gws = wfs[b][s]
        fwg += wfs[w][s] * gws
    return fwg
    
def fg(words, wfs, base, sentences):
    fg = {} 
    for b in base:
        fg[b] = 0
        for s in sentences:
            for w in words:
                if b.find(w) >= 0: # w ∈ g
                    fg[b] += wfs[b][s] - wfs[w][s]
                else: # w not ∈ g
                    fg[b] += wfs[b][s] 
    return fg

def c(hk, hf, sentences):
    c = {}
    for k in hk:
        c[k] = {}
        for f in hf:
            c[k][f] = 0
            for s in sentences:
                c[k][f] += s.count(k) * s.count(f)
    return c
                
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
    
    # Create a set of words
    words = set(words)
    
    # Calculate high-frequency words
    hf = high_frequency(text)
    
    # Calculate degree of co-occurrence
    co = calculate_co_occurrence(hf, sentences)
        
    # Calculate word frequency in sentences
    wfs = calculate_wfs(words, sentences)
    
    sys.exit()
    
    # Compute key
    key = key(words, wfs, hf, sentences)
    
    # Sort document by key
    high_key = sorted(key.items(), key=lambda x: x[1])
    
    print(high_key)
    
    # Top keys are the high keys (roofs?)
    # High keys are highly ranked by the touching columns
    high_key = dict(high_key[-12:])
    hk = list(high_key.keys())
    
    print(hk)
    print(hf)
    
    c = c(hk, hf, sentences)
    print(c)	