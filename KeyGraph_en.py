# -*- coding:utf-8 -*-
import sys
import MeCab
import codecs
import re
import itertools 
import unicodedata 
from pylab import *
import time
import urllib 
import nltk
from nltk.collocations import *
 
M = 30

#ノイズの削除
def delNoise(text):
#   ノイズファイルの詠み込み
    noise_list=[]
    for line in open('./noise.txt', 'r'):
        noise_list.append(line[:-1].split("\n"))	
         
#   ノイズ削除
    for i in range(len(noise_list)-1):
        noise =  noise_list[i]
        text = text.replace(noise[0], ' ')
         
    return text

#センテンス（文）のlist作成
def creSent(text):
#	文分割:sents
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_tokenizer.tokenize(delNraw)
    return sents
     
#名詞だけを取得してリストにいれる　リストを返す
def pyMecab(s):
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(s)
    nouns = []
    while node:
#		めかぶの名詞のidが38から60なんだよね
        if node.posid >= 38 and node.posid <= 60:
            nouns.append(node.surface)
     
        node = node.next
         
    return nouns

#頻出度上位30の語を返す
def high_freq(text):
    #   ストップワード,一部の除外シンボルの定義
    stopwords = nltk.corpus.stopwords.words('english')
    symbols = ["'", '"', '`', '.', ',', '-', '!', '?', ':', ';', '(', ')', '&', '0'] 

    fd = nltk.FreqDist(w.lower() for w in text if w.lower() not in stopwords + symbols)
    return fd.keys()[:30] 

#共起度coを計算する
def calCo(hf,sents):
    co = {} 
    for hf1 in hf:
        co[hf1] = {} #初期化
        for hf2  in hf[hf.index(hf1)+1:]:
            co[hf1][hf2] = 0 
            for s in sents:
                co[hf1][hf2] += s.count(hf1) * s.count(hf2)
                 
#	listにしています	
    co_list = [] 
    for x in co.keys():
        for y in co[x].keys():
            co_list.append([x,y,co[x][y]])
    
    co_list.sort(key=lambda a: a[2])

    return co_list 
 
def calwfs(words, sents):
    wfs = {} 
    for w in words:
        for s in sents:
            if w in wfs:
                wfs[w][s] = s.count(w)
            else:
                wfs[w] = {}
                wfs[w][s] = s.count(w) 
    
    return wfs

def key(words, wfs, base, sents): 
#	keyは辞書型　key = {w:key値}	
    key = {}
    stime = time.time()
     
#   F(g)の計算 
    Fg = fg(words,wfs,base,sents)
    etime = time.time()
    print (str(etime-stime))
    print Fg
    for w in words:
        tmp = 1.0
        tmp_count = 0
        for b in base:
            tmp *= (1-(fwg(w,wfs,b,sents)*(1.0)/Fg[b])) 
        key[w] = 1.0-tmp
    return key		

#f(w,g)計算
def fwg(w,wfs,b,sents):	
    gws = 0
    fwg = 0
    for s in sents:
#		|g-w|sの計算  gs=wfs[g][s]  ws=wfs[w][s]
        if b.find(w) >= 0:# w ∈ g
#			|g|sの計算
            gws = wfs[b][s] - wfs[w][s]
        else:# w not ∈ g
            gws = wfs[b][s]
        fwg += wfs[w][s]*gws
    return fwg

#F(g)の計算
def fg(words, wfs, base, sents):
    fg = {} 
    for b in base:
        fg[b] = 0
        for s in sents:
            for w in words:
                if b.find(w) >= 0:# w ∈ g
                    fg[b] += wfs[b][s] - wfs[w][s]
                else:# w not ∈ g
                    fg[b] += wfs[b][s] 
    return fg


#cの計算
def c(hk, hf, sents):
    c = {}
    for k in hk:
        for f in hf:
            for s in sents:
                if k in c:
                    c[k][f] += s.count(k) * s.count(f)
                else:
                    c[k] = {}
                    c[k][f] = 0
                    c[k][f] += s.count(k) * s.count(f)



#-----------Main----------------
if __name__ == "__main__":

#	イベントファイル読み込み
    f = open('./oktoberfest.txt', 'r')
    raw = f.read()

#	ノイズを削除します
    delNraw = delNoise(raw)

#	センテンスに分ける
    sents = creSent(delNraw) 
    
#	tokens:文字列を単語と句読点に分割したもの
    tokens = nltk.word_tokenize(delNraw)

#   大文字小文字による文字の揺れをなくすためすべて小文字に
    tokens = [w.lower() for w in tokens]
    sents = [s.lower() for s in sents]
     
#	text:NLTKのテキスト生成
    text = nltk.Text(tokens)    

#   語の集合を作る
    words = set(tokens)

#   HighFreqの計算:hf 
    hf = high_freq(text)

#   HighFreqの共起度を計算する 返り値リスト->[wi,wj,co]
    co = calCo(hf,sents)

#   各センテンスに対して語wの出現度をwfsとして算出(word freqency in sentence)
    wfs = calwfs(words, sents) 
    
#   keyの計算   
    key = key(words, wfs, hf, sents)
     
    high_key = sorted(key.items(), key=lambda x:x[1])
    high_key = dict(high_key[-12:])
    hk = high_key.keys() 
    print hk
    print hf
     
      
'''
#	c(wi,wj)の計算
    c(hk, hf, sentences)	
'''
