#! /Document/python/testMecab.py
# -*- coding:utf-8 -*-
import sys
import MeCab
import codecs
import re
import itertools
import time
import unicodedata
 
  
M = 30

print 'start'
#ノイズの削除
def delNoise(text):
#   ノイズファイルの詠み込み
    noise_list=[]
    for line in codecs.open('./noise/noise.txt', 'r', 'utf-8'):
        noise_list.append(line[:-1].split("\n"))	

#ノイズ削除
    for i in range(len(noise_list)-1):
        noise =  noise_list[i]
        text = text.replace(noise[0], u'')
    return text

#センテンス（文）のlist作成
def creSentence(text):
    s_cha = u'。'
#	    cat = re.split(ur"", text)
    sentences = []
    sentences = text.strip(s_cha).split(s_cha)
    return sentences

#名詞だけを取得してリストにいれる　リストを返す 数字抜き
def pyMecab(s):
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(s.encode('utf-8'))
    nouns = []
    while node:
#		    めかぶの名詞のidが38から60なんだよね　数字id=48抜き
        if node.posid >= 38 and node.posid <= 67 and not(node.posid == 49):
            if isValid(node.surface.decode('utf-8')) == True:
                nouns.append(node.surface.decode('utf-8'))
        node = node.next
    return nouns


def isValid(word):
    alldigit = re.compile(ur"^[0-9]+$")
    """wordが登録対象の単語のときTrueを返す"""
# 	    1文字の単語は登録しない
    if len(word) == 1:
        return False
# 	    数字だけの単語は登録しない
    if alldigit.search(word) != None:
        return False
# 	    仮名2文字の単語は登録しない
    if len(word) == 2 and unicodedata.name(word[0])[0:8] == "HIRAGANA" and unicodedata.name(word[1])[0:8] == "HIRAGANA":
        return False
#       仮名、漢字、数字、英字以外の文字を含む単語は登録しない
    for c in word:
        if not (unicodedata.name(c)[0:8] == "HIRAGANA" or
               unicodedata.name(c)[0:8] == "KATAKANA" or
               unicodedata.name(c)[0:3] == "CJK" or
               unicodedata.name(c)[0:5] == "DIGIT" or
               unicodedata.name(c)[0:5] == "LATIN"):
            return False
    return True
     
#熟語の作成
def creIdiom(words, text):
    p = []
    q = []
    di_comb_p = {}
    di_comb_q = {}
#       2つ続きの単語と3続きの単語で熟語の候補を作る
    for i in range(len(words)-2):
        p.append(words[i] + words[i+1])
        q.append(words[i] + words[i+1] + words[i+2])

    for i in p:
        if di_comb_p.has_key(i):
            di_comb_p[i] += 1
        else:
            di_comb_p[i] = 1

    for i in q:
        if di_comb_q.has_key(i):
            di_comb_q[i] += 1
        else:
            di_comb_q[i] = 1

    di_idiom_p = di_comb_p
    di_idiom_q = di_comb_q

    list_comb_p = di_comb_p.items()
    list_comb_p.sort(key=lambda a: a[1])
    list_comb_q = di_comb_q.items()
    list_comb_q.sort(key=lambda a: a[1])

#	    候補pについてpを含む候補qの出現回数がp以上ならばpを,p以下ならばqを候補から捨てる．
#	    {bcd}は{cd}を含むという	
    for kq,vq in list_comb_q:
        for kp,vp in list_comb_p:
#			含むかどうか確認		 
            if(kq.count(kp)>0):
#				    print kp, di_comb_p[kp], kq, di_idiom_q[kq]
                if(di_comb_p.get(kp) <= di_comb_q.get(kq)):
                    if(di_idiom_p.has_key(kp)):
                        di_idiom_p.pop(kp)
                else:
                    if(di_idiom_q.has_key(kq)):
                        di_idiom_q.pop(kq)

    list_idiom_p = di_idiom_p.items()
    list_idiom_q = di_idiom_q.items()
    list_idiom = list_idiom_p
    list_idiom.extend(list_idiom_q)
    list_idiom.sort(key=lambda a: a[1])

    return list_idiom
 

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
                        print kp, kq
                        dic_p.pop(kp)
                else:
                    if(dic_q.has_key(kq)):
                        print kq, kp
                        dic_q.pop(kq)
                         
                         
    list_p = dic_p.items()
    list_q = dic_q.items()
    list_idiom = list_p
    list_idiom.extend(list_q)
    list_p.sort(key=lambda a: a[1])

    return list_p
                     
#単語出現度でリストをソートする為に辞書にする
def listToDict(list):
    result={}
#   単語の出現でカウント(list内のカウント）
    for i in list:
        if result.has_key(i):
            result[i] += 1
        else:
            result[i] = 1
#   出現回数でソート	
    s_result = sorted(result.items(), key=lambda x:x[1])
    return s_result	

#   dicをソートして単語:出現回数のリストで返す関数
def dic2list(dic):
    s_result = sorted(dic.items(), key=lambda x:x[1])
    return s_result	

#一つのリストから組み合わせの辞書を作成する
def list2combDec(list):
    comb = {}
#	組み合わせの辞書を作る
    for c in itertools.combinations(list,2):
        if c[0][0] in comb:
            comb[c[0][0]][c[1][0]] = 0 
        else:
            comb[c[0][0]] = {}
    return comb

#リスト['word']['sentence　インデックス']=出現回数　を返す関数
def occur(words, sentences):
    wfs = {} 
    for w,n in words:
        for s in range(len(sentences)):
            if w in wfs:
                wfs[w][s] = sentences[s].count(w)
            else:
                wfs[w] = {}
                wfs[w][s] = sentences[s].count(w) 

#	for w,n in words:
#		for s in range(len(sentences)):
#			print wfs[w][s]	

    return wfs	
     
#共起度coを計算する
def calCo(base_comb_dec, sentences):
    co = base_comb_dec 
#	同じ文書内で語が共起していたらカウントアップ
    for x in co.keys():
        for y in co[x].keys():
            for s in sentences:
                co[x][y] += s.count(x) * s.count(y)
                    
    co_list = []
#	listにしています	
    for x in co.keys():
        for y in co[x].keys():
            co_list.append([x,y,co[x][y]])

    co_list.sort(key=lambda a: a[2])

    return co_list[len(co_list)-M:len(co_list)]	

#リンクを張る
def link(base_comb_dec, base_co, high_freq):
    base_graph_link =  base_comb_dec 	
    node = high_freq	 
     
    for x in base_graph_link.keys():
        for y in base_graph_link[x].keys():
            base_graph_link[x][y] = 0

    base = []
#	coの値がM-1番目の語対にリンクを張る（隣接行列）		 
    for x,y,z in base_co[1:M]:
        base_graph_link[x][y] = 1
        
    con_graph_list = []
#con_graph_list.append(set([base_co[1][0], base_co[1][1]]))
    for x,y,z in base_co[1:M]:
        flag = False
        for l in con_graph_list:
            if (x in l) == True:
                flag = True
                l.add(y)
            if (y in l) == True:
                flag = True
                l.add(x)
        if flag == False:
            con_graph_list.append(set([x,y]))

    '''
#	グラフの連結をset（集合）型で表現する
    for x in base_graph_link.keys():
        for y in base_graph_link[x].keys():
            if base_graph_link[x][y] == 1:
                for l in con_graph_list:
                    if x in l:	
                        l.add(y)
                    elif y in l:
                        l.add(x)
                    else:
                        adjacent = [x,y]
                        adjacent = set(adjacent)
                        con_graph_list.append(adjacent)
                         
#	隣接リストをつくる　
    adjacent = []
     
    for x in base_graph_link.keys():
        for y in base_graph_link[x].keys():
            print x, y
             
             
    for x in base_graph_link.keys():
        for y in base_graph_link[x].keys():
            if base_graph_link[x][y] >= 1:				
                print x,y



    '''
                            
#key値の計算
def key(words, wfs, base, sentences):
#	keyは辞書型　key = {w:key値}	
    key = {}
    for g,y in base:
        Fg = fg(words, wfs, base, sentences)

    for w,x in words:
        tmp = 1.0
        tmp_count = 0
        for g,y in base:
#			stime = time.time()
#  			fwg(w,g,sentences)
#			entime = time.time()
#			print(str(entime-stime))		
            tmp *= (1-(fwg(w,wfs,g,sentences)*(1.0)/Fg[g])) 
        key[w] = 1.0-tmp 
        print 1.0-tmp, w 
         
    return key		

#f(w,g)計算
def fwg(w,wfs,g,sentences):	
    gws = 0
    fwg = 0
    for s in range(len(sentences)):
#		|g-w|sの計算  gs = wfs[g][s] ws = ws[w][s]
        if g.find(w) >= 0:# w ∈ g
#			|g|sの計算
            gws = wfs[g][s] - wfs[w][s]
        else:# w not ∈ g
            gws = wfs[g][s]
        fwg += wfs[w][s]*gws
    return fwg


#F(g)の計算
def fg(words, wfs, base, sentences):
    fg = {}
    for g,y in base:
        fg[g] = 0
        for s in range(len(sentences)):
            for w,f in words:
                if sentences[s].find(w) >= 0:
                    if g.find(w) >= 0:# w ∈ g
                        fg[g] += wfs[g][s] - wfs[w][s]
                    else:# w not ∈ g
                        fg[g] += wfs[g][s] 
    return fg

#Cの計算 wi : HighKey中の語　wj:いずれかの土台に含まれる語
def c(high_key,base,sentences):
    c = {} 
    for wi,fi in high_key:#	high key
        c[wi] = {}#初期化
        for wj,fj in base:
            c[wi][wj] = 0#初期化
#			c[wi][wj]の辞書を作るよー
            for s in range(len(sentences)):
                c[wi][wj] += sentences[s].count(wi) * sentences[s].count(wj)		 
                
#			print wi,wj,c[wi][wj]

    c_sum = {}
    for wi,fi in high_key:
        c_sum[wi] = 0
        for wj,fj in base:
            c_sum[wi] += c[wi][wj]

    for wj,fj in base:
        c_sum[wj] = 0
        for wi,fi in high_key:
            c_sum[wj] += c[wi][wj]

    for k, v in sorted(c_sum.items(), key=lambda x:x[1]):
        print k, v
         
         
         
#-----------Main----------------
if __name__ == "__main__":
    stime = time.time() 
#   イベントファイル読み込み
    f = codecs.open('./fes/sapporoWinFes.txt', 'r', 'utf-8')
    text = f.read()
    f.close()

#	ノイズの削除
    nc_text = delNoise(text)
     
#	センテンスリストの作成
    sentences = creSentence(nc_text)

#	形態素解析
    terms = pyMecab(nc_text) 
       
#	単語-出現度のリストの作成	
    words = listToDict(terms)

#	熟語-出現度のリストの作成
#   idioms = creIdiom(terms, nc_text)

    words = pop(dict(words), dict(words)) 

    words.sort(key=lambda a: a[1])
#	for w,f in words:
#  		print w,f

#	熟語と単語を合体
#	words.extend(idioms)

#	ソート
    words.sort(key=lambda a: a[1])
     
###################################################
#	リスト[words][センテンス番号] = 出現回数のリストwfs
    wfs = occur(words, sentences)

#	HighFreqを決める
    high_freq = words[-30:]

    del words[-30:]

    for w,f in high_freq:
        print w, f

#	highFreqの組み合わせの辞書
    base_comb_dec = list2combDec(high_freq)

#	high_freqの共起度を計算　上位Mを返す
    base = calCo(base_comb_dec, sentences)
     
#	土台graph作る high_freq中の語の共起度の順にM-1本のリンクを張る
    link = link(base_comb_dec, base, high_freq)

#	keyの計算 ＊＊＊＊＊＊＊＊high_freqの所は要相談＊＊＊＊＊＊＊＊＊＊
    key = key(words, wfs, high_freq, sentences)

#	high_keyの計算
    high_key = sorted(key.items(), key=lambda x:x[1])
    high_key = high_key[-12:]
    print high_key
     

#	c(wi,wj)の計算
    c(high_key, high_freq, sentences)	

    etime = time.time()

    print etime - stime	
     
    '''	
    for (k,v) in high_freq:
        print k,v
    '''		 
         
#print len(result)
