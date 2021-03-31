#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import codecs
import pprint
import time

import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community.quality import modularity

from document import Document
 
# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# sys.stdin = codecs.getreader('utf_8')(sys.stdin)

class Util:
    @staticmethod
    # Pretty-print a Python object
    def pp(obj):
        pp = pprint.PrettyPrinter(indent=4, width=160)
        s = pp.pformat(obj)
        return s    
  
    @staticmethod
    # Read file name from the console
    def get_file_name():
        if (len(sys.argv) != 2):
            print("Usage: #python %s file-name" % sys.argv[0])
            sys.exit()
        return sys.argv[1]
 
class KeyGraph:
    def __init__(self, document, M=30, K=12):
        self.document = document
        self.base = self.compute_base(M)
        self.G_C = self.compute_hubs(K)

#   Compute base of frequently co-occurring words
    def compute_base(self, M):
        # Sort words by their frequency (in ascending order)
        freq_count = self.document.freq_count()
        words_freq = sorted(freq_count.items(), key=lambda x: x[1])
        
        # Compute unique words        
        self.words = [w for w, f in words_freq]
        
        # Calculate word frequency in sentences
        self.wfs = self.calculate_wfs()
        
        # Determine high frequency words
        hf = [w for w, f in words_freq[-M:]]

        # Calculate co-occurrence degree of high-frequency words
        co = self.calculate_co_occurrence(hf)

        # Keep only the tightest links
        co = [[i, j] for i, j, c in co[-M:]]

        print(Util.pp(co))

        # Compute the base of G (links between black nodes)
        return self.find_clusters(co)
    
#   Calculate word frequency in sentences
    def calculate_wfs(self):
        wfs = {}
        for w in self.words:
            for s_idx, s in enumerate(self.document.sentences):
                if w not in wfs:
                    wfs[w] = {}
                wfs[w][s_idx] = s.count(w)
        return wfs
    
#   Calculate co-occurrence degree of high-frequency words
    def calculate_co_occurrence(self, hf):
        co = {}
        for hf1 in hf:
            co[hf1] = {}
            for hf2 in hf[hf.index(hf1)+1:]:
                co[hf1][hf2] = 0
                for s in self.document.sentences:
                    # Why sum products, not min, as in Ohsawa (1998)?
                    # co[hf1][hf2] += s.count(hf1) * s.count(hf2)
                    co[hf1][hf2] += min(s.count(hf1), s.count(hf2))
        co_list = []
        for x in co.keys():
            for y in co[x].keys():
                co_list.append([x, y, co[x][y]])
        co_list.sort(key=lambda a: a[2])
        return co_list

#   Detect communities in the base and remove edges between clusters
    def find_clusters(self, base):
        G = nx.Graph()
        for i, j in base:
            G.add_edge(i, j)
        
        communities = girvan_newman(G)
        communities_by_quality = [(c, modularity(G, c)) for c in communities]
        c_best = sorted([(c, m) for c, m in communities_by_quality], key=lambda x: x[1], reverse=True)
        c_best = c_best[0][0]
        # print(Util.pp(communities_by_quality))
        print("clusters", modularity(G, c_best), c_best)
        
        # only include clusters of more than one node (for now)
        self.clusters = [c for c in c_best if len(c) > 1]

        # for cluster in c_best:
        #     print(G.subgraph(cluster).edges())
        new_base = [edge for cluster in c_best for edge in G.subgraph(cluster).edges()]
        
        return new_base
 
#   Compute hubs that connect words in the base
    def compute_hubs(self, K):
        # Extract nodes in the base
        G_base = set([x for pair in self.base for x in pair])

        # Remove high frequency words from G_base, leaving non-high frequency words
        self.words = [w for w in self.words if w not in G_base]

        # Compute key terms that connect clusters
        key = self.key(self.words)

        print(Util.pp(key))

        # Sort terms in D by keys
        high_key = sorted(key.items(), key=lambda x: x[1])
        high_key = high_key[-K:]
        
        high_key = [k for k, f in high_key]

        print(Util.pp(high_key))

        # Calculate columns
        C = self.columns(high_key, G_base)
        
        print(Util.pp(C))

        # Compute the top links between key terms (red nodes) and columns
        G_C = [[i, j] for i, j, c in C[-K:]]
                
        # Compute adjacency list
        self.base_adj = self.adjacency_list(self.base, G_C)
        
        return G_C
        
    # Compute key terms that connect clusters
    def key(self, words):
        # optimization: compute the neighbors of all clusters ahead of time
        neighbors = {}
        for g_idx, g in enumerate(self.clusters):
            neighbors[g_idx] = self.neighbors(g)
        # key is a dictionary of the form　key = {w: key value}
        key = {}
        for w in words:
            # print("keyword: {}".format(w))
            product = 1.0
            for g_idx, g in enumerate(self.clusters):
                # print("g", g_)
                # print("neighbors", neighbors)
                based = self.based(w, g)
                # print("based", based)
                product *= 1 - based/neighbors[g_idx]
            key[w] = 1.0 - product
        return key

    # Count of words in sentences including words in cluster g 
    def neighbors(self, g):
        neighbors = 0
        for s, sentence in enumerate(self.document.sentences):
            g_s = 0
            for t in g:
                g_s += self.wfs[t][s]
            # print("g_s", g_s)
            for w in sentence:
                # print(s, w)
                w_s = self.wfs[w][s]
                if w in g:
                    # print("w in g")
                    neighbors += + w_s * (g_s - w_s)
                else:
                    # print("w not in g")
                    neighbors += w_s * g_s
        return neighbors
        
    # Count how many times w appeared in D based on concept represented by cluster g
    def based(self, w, g):
        based = 0
        for s, sentence in enumerate(self.document.sentences):
            # print(s, w)
            g_s = 0
            for t in g:
                g_s += self.wfs[t][s]
            # print("g_s", g_s)
            w_s = self.wfs[w][s]
            if w in g:
                # print("w in g")
                based += w_s * (g_s - w_s)
            else:
                # print("w not in g")
                based += w_s * g_s
        return based
    
    # Calculate columns c(wi,wj)
    def columns(self, hk, base):
        c = {}
        for k in hk:
            c[k] = {}
            for b in base:
                c[k][b] = 0
                for s in self.document.sentences:
                    c[k][b] += min(s.count(k), s.count(b))
        n_clusters = self.clusters_touching(c)
        print(Util.pp(n_clusters))
        c_list = [] 
        for k in c.keys():
            for b in c[k].keys():
                if n_clusters[k] > 1 and c[k][b] > 0:
                    c_list.append([k, b, c[k][b]])
        c_list.sort(key=lambda a: a[2])
        return c_list 

    # How many clusters does each column touch
    def clusters_touching(self, c):
        n_clusters = {}
        for k in c.keys():
            # print("k", k)
            n_clusters[k] = 0
            for g in self.clusters:
                # print("g", g)
                in_cluster = 0
                for b in c[k].keys():
                    # print("b", b)
                    if c[k][b] > 0 and b in g:
                        # print("b in g")
                        in_cluster = 1
                n_clusters[k] += in_cluster
        return n_clusters
    
    # Create an adjacency list
    def adjacency_list(self, base, G_C):
        a_list = {}
        
        for i, j in base:
            if i in a_list:
                a_list[i].append([j,'base'])
            else:
                a_list[i] = [[j,'base']]
            if j in a_list:
                a_list[j].append([i,'base'])
            else:
                a_list[j] = [[i,'base']]
        
        for i, j in G_C:
            if i in a_list:
                a_list[i].append([j,'key'])
            else:
                a_list[i] = [[j,'key']]
            if j in a_list:
                a_list[j].append([i,'key'])
            else:
                a_list[j] = [[i,'key']]
        
        return a_list
    
    def save_adjacency_list(self, fname):
        fout = codecs.open("./adjacency_list/" + fname + ".txt", "w", "utf-8")
        fout.write(Util.pp(self.base_adj))
        fout.close()
    
    # Draw keygraph in dot format
    def draw(self, fname):
        fout = codecs.open("./dot/" + fname + ".dot","w","utf-8")
        fout.write('graph keygraph {\n')
        fout.write('graph [size="10,10", overlap="scale"]\n')
    
        g = []
        for i, j in self.base:
            g.append(i)
            g.append(j)
        for i in set(g):
            fout.write(self.quote(i) + ' [color="black"]\n')
        k = []
        for i, j in self.G_C:
            k.append(i)
        for i in set(k):
            fout.write(self.quote(i) + ' [color="red"]\n')
            
        for i, j in self.base:
            fout.write(self.quote(i) + '--' + self.quote(j) +'\n')
        for i, j in self.G_C:
            fout.write(self.quote(i) + '--' + self.quote(j) + ' [color="red", style="dotted"]\n')
        fout.write('}')
        fout.close()
        
    # Add optional quotes around a name
    def quote(self, name):
        if 1 in [c in name for c in ['-', '/', '.', '\'']] or name in ["graph"]:
            return "\"{}\"".format(name)
        return name
             
#-----------Main----------------
if __name__ == "__main__":
    stime = time.time() 
    
#   Create a document
    fname = Util.get_file_name()
    doc = Document(file_name = 'txt_files/' + fname + '.txt')
        
#   Create a keygraph
    kg = KeyGraph(doc, M=20, K=12) # default: M=30, K=12
    print("clusters", kg.clusters)

    kg.save_adjacency_list(fname)
    kg.draw(fname)
    
    etime = time.time()
    print("Execution time: %.4f seconds" % (etime - stime))
