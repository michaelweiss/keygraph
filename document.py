#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs

class Document:
    def __init__(self, content = ""):
        self.content = content
    
    # Read content from file
    def read_from_file(self, file_name):
        f = codecs.open(file_name, 'r', 'utf-8')
        self.content = f.read()
        f.close()