#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import codecs
import pprint
import time
import nltk

from document import Document
 
M = 12
K = 12

# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# sys.stdin = codecs.getreader('utf_8')(sys.stdin)

# Pretty-print a Python object
def pp(obj):
    pp = pprint.PrettyPrinter(indent=4, width=160)
    s = pp.pformat(obj)
    return s
  
# Read file name from the console
def get_file_name():
    if (len(sys.argv) != 2):
        print("Usage: #python %s file-name" % sys.argv[0])
        sys.exit()
    print(pp(sys.argv))
    return sys.argv[1]

# Read document from file
def read_from_file(file_name):
    f = codecs.open('./txt_files/' + file_name + '.txt', 'r', 'utf-8')
    doc = f.read()
    f.close()
    return doc

# Delete noise
def delNoise(text):
    return text 
 
# Divide into sentences
def creSentence(text):
    return [s.lower() for s in nltk.tokenize.sent_tokenize(text)]

# Divide into sentences and tokenize each sentence
def create_sentences(text):
    return [create_tokens(s) for s in creSentence(text)]

# Divide into tokens
def create_tokens(text):
    return [t.lower() for t in nltk.tokenize.word_tokenize(text)]

# Read user-defined stopwords
def read_user_defined_stopwords():
    stopwords = []
    for line in codecs.open('./noise/stopwords.txt', 'r', 'utf-8'):
        stopwords.append(line.strip())
    return stopwords

user_defined_stopwords = read_user_defined_stopwords()

# Strip stopwords and special symbols from list of words
def strip_stopwords_and_symbols(tokens):
    stopwords = nltk.corpus.stopwords.words('english')
    symbols = ["'", '"', '“', '”', '`', '’', '.', ',', '-', '!', '?', ':', ';', '(', ')', '[', ']', '&', '0', '%', '...', '--']
    return [w for w in tokens 
            if w not in stopwords + user_defined_stopwords + symbols and len(w) > 1]

# Lemmatize words
def lemmatize(tokens):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return [lemmatizer.lemmatize(w, wordnet_pos(t)) for w, t in nltk.pos_tag(tokens)]

# Lookup WordNet POS
# https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
def wordnet_pos(tag):
    tags = {"J": nltk.corpus.wordnet.ADJ,
            "N": nltk.corpus.wordnet.NOUN,
            "V": nltk.corpus.wordnet.VERB,
            "R": nltk.corpus.wordnet.ADV}
    # tag example: 'VBD' for verb
    return tags.get(tag[0], nltk.corpus.wordnet.NOUN)
    
# Count word frequencies
def freqcount(tokens):
    result = {}
    for t in tokens:
        if t in result:
            result[t] += 1
        else:
            result[t] = 1
    return result	
 
#	Calculate word frequency in sentences
def calwfs(words, sents):
    wfs = {} 
    for w in words:
        for s_idx, s in enumerate(sents):
            if w not in wfs:
                wfs[w] = {}
            wfs[w][s_idx] = s.count(w)
    return wfs	
 
#   Calculate co-occurrence degree of high-frequency words
def calCo(hf, sents):
    co = {} 
    for hf1 in hf:
        co[hf1] = {}
        for hf2 in hf[hf.index(hf1)+1:]:
            co[hf1][hf2] = 0 
            for s in sents:
                # Why sum products, not min, as in Ohsawa (1998)?
                # co[hf1][hf2] += s.count(hf1) * s.count(hf2)
                co[hf1][hf2] += min(s.count(hf1), s.count(hf2))
    co_list = [] 
    for x in co.keys():
        for y in co[x].keys():
            co_list.append([x, y, co[x][y]])    
    co_list.sort(key=lambda a: a[2])
    return co_list 
 
# Compute key (terms that tie and hold clusters together) 
def key(words, wfs, base, sents):
    # key is a dictionary of the form　key = {w: key value}	
    key = {}   
    Fg = fg(words, wfs, base, sents)
    for w in words:
        product = 1.0
        for g in base:
            product *= 1 - fwg(w, wfs, g, sents)*(1.0)/Fg[g]
#        print("product", product)
        key[w] = 1.0 - product 
        print("key[{}]".format(w), 1.0 - product, w)        
    return key		

# Calculate f(w,g)
# Based(w, g) = how many times w appeared in D, based on the basic
# concept represented by term g
def fwg(w, wfs, g, sents):	
    gws = 0
    fwg = 0
#    print("w", w, "g", g)
    for s, sentence in enumerate(sents):
#        print("sentence", sentence)
        # Calculate |g-w|_s
        # Count of cluster term g in s: g_s = wfs[g][s]
        # Word in s: w_s = wfs[w][s]
        if w == g: # w ∈ g
#            print("|g-w|", g, wfs[g][s], w, wfs[w][s])
            gws = wfs[g][s] - wfs[w][s]
        else: # w not ∈ g
#            print("|g|", g, wfs[g][s])
            gws = wfs[g][s]
        fwg += wfs[w][s] * gws
    return fwg

# Calculate F(g)
# Neighbors(g) = count of terms in sentences including terms in cluster g
# g_s = count of cluster g in sentence s
# w_s = count of word w in sentence s (ie wfs[w][s])
def fg(words, wfs, base, sents):
    fg = {}
    for g in base:
        fg[g] = 0
        for s, sentence in enumerate(sents):
            for w in sentence:
                if w == g: # w ∈ g
#                    print("|g-w|", g, wfs[g][s], w, wfs[w][s])
                    fg[g] += wfs[g][s] - wfs[w][s]
                else: # w not ∈ g
#                    print("|g|", g, wfs[g][s])
                    fg[g] += wfs[g][s] 
    return fg

def C(hk, base, sents):
    c = {}
    for k in hk:
        c[k] = {}
        for b in base:
            c[k][b] = 0
            for s in sents:
                c[k][b] += min(s.count(k), s.count(b))
    c_list = [] 
    for x in c.keys():
        for y in c[x].keys():
            c_list.append([x, y, c[x][y]])
    c_list.sort(key=lambda a: a[2])
    return c_list 
  
# Prune graph by removing edges that connect clusters
# That is, if the two ends of an edge are connected only by
# one edge, remove the edge to create two clusters
def prune(base, base_adj):
    new_base = []
    for [i, j] in base:
        if find_path(base_adj, i, j, [i, j], []):
            print("find path:", [i, j])
            new_base.append([i, j])
        else:
            print("no path found:", [i, j])
    return new_base
     
# Find a path between two nodes that does not include edge
# This won't necessarily return the best path, but is enough
# to test whether there is a path
# https://www.python.org/doc/essays/graphs/
def find_path(graph, start, end, edge, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    for node in [g[0] for g in graph[start] if g[1] == 'base']:
        if (node not in path) and not([path[-1], node] == edge):
            new_path = find_path(graph, node, end, edge, path)
            if new_path:
                return new_path
    return None
        
# Draw keygraph in dot format
def draw(base, G_C, fname):
    fout = codecs.open("./dot/" + fname + ".dot","w","utf-8")
    fout.write('graph keygraph {\n')
    fout.write('graph [size="10,10"]\n')

    g = []
    for i, j in base:
        g.append(i)
        g.append(j)
    for i in set(g):
        fout.write(quote(i) + ' [color="black"]\n')
    k = []
    for i, j in G_C:
        k.append(i)
    for i in set(k):
        fout.write(quote(i) + ' [color="red"]\n')
        
    for i, j in base:
        fout.write(quote(i) + '--' + quote(j) +'\n')
    for i, j in G_C:
        fout.write(quote(i) + '--' + quote(j) + ' [color="red", style="dotted"]\n')
    fout.write('}')
    fout.close()
    
# Add optional quotes around a name
def quote(name):
    if 1 in [c in name for c in ['-', '/', '.', '\'']]:
        return "\"{}\"".format(name)
    return name

# Create an adjacency list 
def adjacency_dic(base, G_C, fname):
    a_dic = {}
     
    for i,j in base:
        if i in a_dic:
            a_dic[i].append([j,'base'])
        else:
            a_dic[i] = [[j,'base']] 
        if j in a_dic:
            a_dic[j].append([i,'base'])
        else:
            a_dic[j] = [[i,'base']] 
    
    for i, j in G_C:
        if i in a_dic:
            a_dic[i].append([j,'key'])
        else:
            a_dic[i] = [[j,'key']] 
        if j in a_dic:
            a_dic[j].append([i,'key'])
        else:
            a_dic[j] = [[i,'key']] 

    fout = codecs.open("./adjacency_list/" + fname + ".txt","w","utf-8")
    fout.write(pp(a_dic))
    fout.close()
    
    return a_dic
        
#-----------Main----------------
if __name__ == "__main__":
    stime = time.time() 
    
    fname = get_file_name()
    
    doc = Document()
    doc.read_from_file('txt_files/' + fname + '.txt')
    
#	Delete noise
    nc_text = delNoise(doc.content)
             
#	Divide into sentences
    sents = create_sentences(nc_text)
    
    sents = [lemmatize(s) for s in sents]
    sents = [strip_stopwords_and_symbols(s) for s in sents]

#    sents = creSentence(nc_text)
#    sents = lemmatize_tokens_in_sentences(sents)
            
#	Divide into tokens
    tokens = create_tokens(nc_text)
    tokens = lemmatize(tokens)
    tokens = strip_stopwords_and_symbols(tokens)
    
#	Count word frequencies	
    freq_dict = freqcount(tokens)
    
#   Sort words by their frequency (in ascending order)
    words_freq = sorted(freq_dict.items(), key=lambda x: x[1])

#   Compute unique words
    words = [w for w, z in words_freq]
          
#	Calculate word frequency in sentences
    wfs = calwfs(words, sents)
            
#	Determine high frequency words
    hf = [w for w, f in words_freq[-M:]]
               
#   Calculate co-occurrence degree of high-frequency words
    co = calCo(hf, sents)
        
#   Compute the base of G (links between black nodes)
    base = [[i, j] for i, j, c in co[-M:]]  
    
#   Extract nodes in the base
    G_base = set([x for pair in base for x in pair])
    
#   Remove high frequency words from, leaving non-high frequency words
    words = [w for w in words if w not in G_base]
    
    print(pp(co))
    print(pp(G_base))
    print(pp(words))
   
#   Compute key (terms that tie and hold clusters together) 
    key = key(words, wfs, G_base, sents)

#   Sort terms in D by keys (produces list of terms ranked by their
#   association with the cluster)
    high_key = sorted(key.items(), key=lambda x: x[1])
    high_key = high_key[-K:]
    
    high_key = [k for k, f in high_key]
    
#	Calculate columns c(wi,wj)
    C = C(high_key, G_base, sents)
    C.sort(key=lambda x: x[2])
     
#   Compute the top links between key terms (red nodes) and clusters
    G_C = [[i, j] for i, j, c in C[-K:]]  
    
    # for i, j in base:
    #     print(i, j)
    # for x, y in G_C:
    #     print(x, y)

    base_adj = adjacency_dic(base, G_C, fname)
    
    pruned_base = prune(base, base_adj)
    
    draw(pruned_base, G_C, fname)

    etime = time.time()
    print("Execution time: %.4f seconds" % (etime - stime))

