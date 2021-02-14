#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# import MeCab
import codecs
# import re 
import pprint
# import itertools
import time
# import unicodedata
# import os 
import nltk
 
M = 30
K = 12

# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# sys.stdin = codecs.getreader('utf_8')(sys.stdin)

# Pretty-print a Python object
def pp(obj):
    pp = pprint.PrettyPrinter(indent=4, width=160)
    s = pp.pformat(obj)
#    return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1),16)),str)
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
    f = codecs.open('./txt_files/' + fname + '.txt', 'r', 'utf-8')
    doc = f.read()
    f.close()
    return doc

# Delete noise
def delNoise(text):
    return text 
 
# Divide into sentences
def creSentence(text):
    return [s.lower() for s in nltk.tokenize.sent_tokenize(text)]

# Divide into tokens
def create_tokens(text):
    return [t.lower() for t in nltk.tokenize.word_tokenize(text)]

#名詞だけを取得してリストにいれる　リストを返す 数字抜き
def pyMecab(s):
    pass
#     tagger = MeCab.Tagger('-Ochasen')
#     node = tagger.parseToNode(s.encode('utf-8'))
#     nouns = []
#     while node:
# #		    めかぶの名詞のidが38から60なんだよね　数字id=48抜き
#         if node.posid >= 38 and node.posid <= 67 and not(node.posid == 49):
#             if isValid(node.surface.decode('utf-8')) == True:
#                 nouns.append(node.surface.decode('utf-8'))
#         node = node.next
#     return nouns


def isValid(word):
#     alldigit = re.compile(ur"^[0-9]+$")
#     """wordが登録対象の単語のときTrueを返す"""
# # 	    1文字の単語は登録しない
#     if len(word) == 1:
#         return False
# # 	    数字だけの単語は登録しない
#     if alldigit.search(word) != None:
#         return False
# # 	    仮名2文字の単語は登録しない
#     if len(word) == 2 and unicodedata.name(word[0])[0:8] == "HIRAGANA" and unicodedata.name(word[1])[0:8] == "HIRAGANA":
#         return False
# #       仮名、漢字、数字、英字以外の文字を含む単語は登録しない
#     for c in word:
#         if not (unicodedata.name(c)[0:8] == "HIRAGANA" or
#                unicodedata.name(c)[0:8] == "KATAKANA" or
#                unicodedata.name(c)[0:3] == "CJK" or
#                unicodedata.name(c)[0:5] == "DIGIT" 
# #               英語を削除しています　コメントをとれば英語も入ります． 
#               ''' unicodedata.name(c)[0:5] == "LATIN"'''):
#             return False
    return True

#   popで熟語のやつを消すぜー	
def pop(dic_p, dic_q):
#     list_p = sorted(dic_p.items(), key=lambda a: a[1])   
#     list_q = sorted(dic_q.items(), key=lambda a: a[1])
   
#     for kq,vq in list_q:
#         for kp,vp in list_p:
#             print(kp, vp, kq, vq, "%s.count(%s)" % (kq, kp), kq.count(kp))
# #			Check if it is included
#             if(kq.count(kp)>0):
# #				print kp, di_comb_p[kp], kq, di_idiom_q[kq]
#                 print(dic_p.get(kp), dic_q.get(kq))
#                 if(dic_p.get(kp) <= dic_q.get(kq)):
#                     if kp in dic_p:
#                         #print kp, kq
#                         dic_p.pop(kp)
#                 else:
#                     if kq in dic_q:
#                         #print kq, kp
#                         dic_q.pop(kq)
#             print(kp, vp, kq, vq, "%s.count(%s)" % (kp, kq), kp.count(kq))
#             if(kp.count(kq)>0):
# #				print kp, di_comb_p[kp], kq, di_idiom_q[kq]
#                 print(dic_p.get(kp), dic_q.get(kq))
#                 if(dic_p.get(kp) <= dic_q.get(kq)):
#                     if(dic_p.has_key(kp)):
#                         #print kp, kq
#                         dic_p.pop(kp)
#                 else:
#                     if(dic_q.has_key(kq)):
#                         #print kq, kp
#                         dic_q.pop(kq)

#     list_p = dic_p.items()
#     list_q = dic_q.items()
#     list_idiom = list_p
#     list_idiom.extend(list_q)
    
#     return sorted(list_p, key=lambda a: a[1])
    pass

# Strip stopwords and special symbols from text
def strip_stopwords_and_symbols(text):
    stopwords = nltk.corpus.stopwords.words('english')
    symbols = ["'", '"', '`', '’', '.', ',', '-', '!', '?', ':', ';', '(', ')', '&', '0', '%']
    return [w for w in text if w not in stopwords + symbols]

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
        for s in sents:
            if w not in wfs:
                wfs[w] = {}
            wfs[w][s] = s.count(w)
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
                co[hf1][hf2] += s.count(hf1) * s.count(hf2)
    co_list = [] 
    for x in co.keys():
        for y in co[x].keys():
            co_list.append([x,y,co[x][y]])    
    co_list.sort(key=lambda a: a[2])
    return co_list 
 
#linkを張る
# Not needed: can extract base from words[-M:]
def link(base):
    base_set = flatten(base)
    base_set = set(base_set)
         
    print(list(base_set))
    return list(base_set)
     
#リストの平坦化 
# Not needed: can extract base from words[-M:]
def flatten(x, isflat=lambda x:not isinstance(x, list)):
    if isflat(x):
        yield x
    else:
        for item in x:
            for i in flatten(item, isflat):
                yield i
                            
# Compute key (terms that tie and hold clusters together) 
def key(words, wfs, base, sents):
    # key is a dictionary of the form　key = {w: key value}	
    key = {}   
    Fg = fg(words, wfs, base, sents)
    # print("Fg", Fg)
    for w in words:
        product = 1.0
        for g in base:
            product *= (1 - fwg(w, wfs, g, sents)*(1.0)/Fg[g]) 
        key[w] = 1.0 - product 
        print("key[{}]".format(w), 1.0 - product, w)        
    return key		

# Calculate f(w,g)
# Based(w, g) = how many times w appeared in D, based on the basic
# concept represented by g
def fwg(w, wfs, g, sents):	
    gws = 0
    fwg = 0
    for s in sents:
        # Calculate |g-w|_s
        # Count of cluster g in s: g_s = wfs[g][s]
        # Word in s: w_s = wfs[w][s]
        if g.find(w) >= 0: # w ∈ g
            gws = wfs[g][s] - wfs[w][s]
        else: # w not ∈ g
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
        for s in sents:
#            print("s", s)
            for w in words:
                if s.find(w) >= 0:
#                    print("w", w)
                    if g.find(w) >= 0: # w ∈ g
#                        print("|g-w|", g, wfs[g][s], w, wfs[w][s])
                        fg[g] += wfs[g][s] - wfs[w][s]
                    else: # w not ∈ g
#                        print("|g|", g, wfs[g][s])
                        fg[g] += wfs[g][s] 
    return fg

def C(hk, base, sents):
    c = {}
    for k in hk:
        c[k] = {}
        for b in base:
            c[k][b] = 0
            for s in sents:
                c[k][b] += s.count(k) * s.count(b)
    c_list = [] 
    for x in c.keys():
        for y in c[x].keys():
            c_list.append([x,y,c[x][y]])
    c_list.sort(key=lambda a: a[2])
    return c_list 
  
# Draw keygraph in dot format
def draw(base, G_C,fname):
    fout = codecs.open("./dot/" + fname + ".dot","w","utf-8")
    fout.write('graph keygraph {\n')
    fout.write('graph [size="10,10"]\n')
    for i, j in base:
       fout.write(quote(i) + '--' + quote(j) +'\n')
    for i, j in G_C:
       fout.write(quote(i) + '--' + quote(j) + '[style="dotted"]\n')
    fout.write('}')
    fout.close()
    
# Add optional quotes around a name
def quote(name):
    if "-" in name or "/" in name:
        return "\"{}\"".format(name)
    return name

#隣接リストを作ったけど微妙だね． 
def adjacency_dic(base, G_C, fname):
    a_dic = {}
     
    for i,j in base:
        if a_dic.has_key(i):
            a_dic[i].append([j,'base'])
        else:
            a_dic[i] = [[j,'base']] 
        if a_dic.has_key(j):
            a_dic[j].append([i,'base'])
        else:
            a_dic[j] = [[i,'base']] 
    
    for i,j in G_C:
        if a_dic.has_key(i):
            a_dic[i].append([j,'key'])
        else:
            a_dic[i] = [[j,'key']] 
        if a_dic.has_key(j):
            a_dic[j].append([i,'key'])
        else:
            a_dic[j] = [[i,'key']] 


    fout = codecs.open("./adjacency_list/" + fname + ".txt","w","utf-8")
    fout.write(pp(a_dic.items()))
    fout.close()

         
         
        
#-----------Main----------------
if __name__ == "__main__":
    stime = time.time() 
    
    fname = get_file_name()
    doc = read_from_file(fname)
    
#	Delete noise
    nc_text = delNoise(doc)
             
#	Divide into sentences
    sents = creSentence(nc_text)
        
#	Divide into tokens
    tokens = create_tokens(nc_text)
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

#   Extract nodes in the base
    G_base = words[-M:]
    
#   Remove high frequency words from, leaving non-high frequency words
    del words[-M:]
    
#   Compute the base of G (links between black nodes)
    base = [[i, j] for i, j, c in co[-M:]]  
    
#   Compute key (terms that tie and hold clusters together) 
    key = key(words, wfs, G_base, sents)

#   Sort terms in D by keys (produces list of terms ranked by their
#   association with the cluster)
    high_key = sorted(key.items(), key=lambda x: x[1])
    high_key = high_key[-K:]
    
    high_key = [k for k, f in high_key]
    
#	Calculate columns c(wi,wj)
    C = C(high_key, G_base, sents)	
    
    print(pp(C))
    
    draw(base, [], fname)
    
    etime = time.time()
    print("Execution time: %.4f seconds" % (etime - stime))

