#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import nltk

class Document:
    def __init__(self, content = ""):
        self.content = content
    
    # Read content from file
    def read_from_file(self, file_name):
        f = codecs.open(file_name, 'r', 'utf-8')
        self.content = f.read()
        f.close()
    
    # Divide a string into tokens
    def create_tokens_from(self, s, lemmatized=True):
        tokens = [t.lower() for t in nltk.tokenize.word_tokenize(s)]
        return self.lemmatize(tokens) if lemmatized else tokens
    
    # Divide into tokens
    def create_tokens(self):
        return self.create_tokens_from(self.content)

    # Divide into sentences
    def create_sentences(self):
        return [self.create_tokens_from(s) for s in nltk.tokenize.sent_tokenize(self.content)]

    # Lemmatize words
    def lemmatize(self, tokens):
        lemmatizer = nltk.stem.WordNetLemmatizer()
        return [lemmatizer.lemmatize(w, self.wordnet_pos(t)) for w, t in nltk.pos_tag(tokens)]
    
    # Lookup WordNet POS
    # https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
    def wordnet_pos(self, tag):
        tags = {"J": nltk.corpus.wordnet.ADJ,
                "N": nltk.corpus.wordnet.NOUN,
                "V": nltk.corpus.wordnet.VERB,
                "R": nltk.corpus.wordnet.ADV}
        # tag example: 'VBD' for verb
        return tags.get(tag[0], nltk.corpus.wordnet.NOUN)
        
