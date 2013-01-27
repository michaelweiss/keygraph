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

#   候補pについてpを含む候補qの出現回数がp以上ならばpを,p以下ならばqを候補から捨てる．
#   {bcd}は{cd}を含むという	
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
 
def popin(words_freq):

    for w1,f1 in words_freq:
        print w1 
        for w2,f2 in words_freq[words_freq.index([w1,f1])+1:]:
            if(w1.count(w2)>0):
                if(f1 <= f2):
                    words_freq.remove([w1,f1])
                else:
                    words_freq.remove([w2,f2])
            if(w2.count(w1)>0):
                if(f1 <= f2):
                    words_freq.remove([w1,f1])
                else:
                    words_freq.remove([w2,f2])
    return words_freq 
                     
def test(words, fd):
    for w1 in words:
        for w2 in words[words.index(w1)+1:]:
            if(w1.count(w2)>0):
                if(fd[w1] <= fd[w2]):
                    words.remove(w1)
                    print w1
                else:
                    words.remove(w2)
                    print w2
            if(w2.count(w1)>0):
                if(fd[w1] <= fd[w2]):
                    words.remove(w1)
                    print w1 
                else:
                    words.remove(w2)
                    print w2 

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

#Cの計算 wi : HighKey中の語　wj:いずれかの土台に含まれる語
def c(high_key,base,sents):
    c = {} 
    for wi,fi in high_key:#	high key
        c[wi] = {}#初期化
        for wj,fj in base:
            c[wi][wj] = 0#初期化
#			c[wi][wj]の辞書を作るよー
            for s in range(len(sents)):
                c[wi][wj] += sents[s].count(wi) * sents[s].count(wj)		 
                
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



