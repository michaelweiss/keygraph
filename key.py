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
    return nltk.tokenize.sent_tokenize(text)

# Divide into tokens
def create_tokens(text):
    return nltk.tokenize.word_tokenize(text)

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

    list_p = dic_p.items()
    list_p.sort(key=lambda a: a[1])
    list_q = dic_q.items()
    list_q.sort(key=lambda a: a[1])
     
    for kq,vq in list_q:
        for kp,vp in list_p:
#			含むかどうか確認
            if(kq.count(kp)>0):
#				print kp, di_comb_p[kp], kq, di_idiom_q[kq]
                if(dic_p.get(kp) <= dic_q.get(kq)):
                    if(dic_p.has_key(kp)):
                        #print kp, kq
                        dic_p.pop(kp)
                else:
                    if(dic_q.has_key(kq)):
                        #print kq, kp
                        dic_q.pop(kq)
            if(kp.count(kq)>0):
#				print kp, di_comb_p[kp], kq, di_idiom_q[kq]
                if(dic_p.get(kp) <= dic_q.get(kq)):
                    if(dic_p.has_key(kp)):
                        #print kp, kq
                        dic_p.pop(kp)
                else:
                    if(dic_q.has_key(kq)):
                        #print kq, kp
                        dic_q.pop(kq)
                         
                         
    list_p = dic_p.items()
    list_q = dic_q.items()
    list_idiom = list_p
    list_idiom.extend(list_q)
    list_p.sort(key=lambda a: a[1])

    return list_p


# Count word frequencies	
def freqcount(tokens):
    result = {}
    for t in tokens:
        if t in result:
            result[t] += 1
        else:
            result[t] = 1
    return result	
 
#リスト['word']['sentence　インデックス']=出現回数　を返す関数
def calwfs(words, sents):
    wfs = {} 
    for w in words:
        for s in sents:
            if w in wfs:
                wfs[w][s] = s.count(w)
            else:
                wfs[w] = {}
                wfs[w][s] = s.count(w) 

#	for w,n in words:
#		for s in range(len(sents)):
#			print wfs[w][s]	

    return wfs	
 
#共起度coを計算する
def calCo(hf,sents):
    co = {} 
    for hf1 in hf:
        co[hf1] = {} #初期化
        for hf2  in hf[hf.index(hf1)+1:]:
            co[hf1][hf2] = 0 #初期化だよ 
            for s in sents:
                co[hf1][hf2] += s.count(hf1) * s.count(hf2)
                 
#	listにしています	
    co_list = [] 
    for x in co.keys():
        for y in co[x].keys():
            co_list.append([x,y,co[x][y]])
    
    co_list.sort(key=lambda a: a[2])

    return co_list 
 
 
#linkを張る
def link(base):
    base_set = flatten(base)
    base_set = set(base_set)
         
    print(list(base_set))
    return list(base_set)
     
#リストの平坦化 
def flatten(x, isflat=lambda x:not isinstance(x, list)):
    if isflat(x):
        yield x
    else:
        for item in x:
            for i in flatten(item, isflat):
                yield i
                            
#key値の計算
def key(words, wfs, base, sents):
#	keyは辞書型　key = {w:key値}	
    key = {}
     
    Fg = fg(words, wfs, base, sents)

    for w in words:
        tmp = 1.0
        tmp_count = 0
        for g in base:
            tmp *= (1-(fwg(w,wfs,g,sents)*(1.0)/Fg[g])) 
        key[w] = 1.0-tmp 
        print(1.0-tmp, w) 
         
    return key		

#f(w,g)計算
def fwg(w,wfs,g,sents):	
    gws = 0
    fwg = 0
    for s in sents:
#		|g-w|sの計算  gs = wfs[g][s] ws = ws[w][s]
        if g.find(w) >= 0:# w ∈ g
#			|g|sの計算
            gws = wfs[g][s] - wfs[w][s]
        else:# w not ∈ g
            gws = wfs[g][s]
        fwg += wfs[w][s]*gws
    return fwg

#F(g)の計算
def fg(words, wfs, base, sents):
    fg = {}
    for g in base:
        fg[g] = 0
        for s in sents:
            for w in words:
                if s.find(w) >= 0:
                    if g.find(w) >= 0:# w ∈ g
                        fg[g] += wfs[g][s] - wfs[w][s]
                    else:# w not ∈ g
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
    
          
#	listにしています	
    c_list = [] 
    for x in c.keys():
        for y in c[x].keys():
            c_list.append([x,y,c[x][y]])
    
    c_list.sort(key=lambda a: a[2])

    return c_list 
  
def draw(base, G_C,fname):
    fout = codecs.open("./dot/" + fname + ".dot","w","utf-8")
    fout.write('graph keygraph {\n')
    fout.write('graph [size="10,10"]\n')
    for i,j in base:
       fout.write(i + '--' + j +'\n')
    for i,j in G_C:
       fout.write(i + '--' + j + '[style="dotted"]\n')
    fout.write('}')
     
    fout.close()

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
    
#	Count word frequencies	
    freq_dict = freqcount(tokens)
    
    print(pp(freq_dict))

    etime = time.time()
    print("Execution time: %.4f seconds" % (etime - stime))

