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
    def create_tokens_from(self, s):
        return [t.lower() for t in nltk.tokenize.word_tokenize(s)]
    
    # Divide into tokens
    def create_tokens(self):
        return self.create_tokens_from(self.content)

    # Divide into sentences
    def create_sentences(self):
        return [self.create_tokens_from(s) for s in nltk.tokenize.sent_tokenize(self.content)]
