#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import codecs
import pprint
import time

from document import Document
 
M = 12
K = 12

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
        self.base = self.compute_base()
        self.compute_hubs()

#   Compute base of frequently co-occurring words
    def compute_base(self):
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
        
        print(Util.pp(co))

        # Compute the base of G (links between black nodes)
        return [[i, j] for i, j, c in co[-M:]]  
    
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
 
#   Compute hubs that connect words in the base
    def compute_hubs(self):
        # Extract nodes in the base
        self.G_base = set([x for pair in self.base for x in pair])

        # Remove high frequency words from G_base, leaving non-high frequency words
        self.words = [w for w in self.words if w not in self.G_base]

        # Compute key terms that connect clusters
        self.key = self.key(self.words, self.wfs, self.G_base, self.document.sentences)

        print(Util.pp(self.key))

        # Sort terms in D by keys
        self.high_key = sorted(self.key.items(), key=lambda x: x[1])
        self.high_key = self.high_key[-K:]
        
        self.high_key = [k for k, f in self.high_key]

        # Calculate columns c(wi,wj)
        self.C = self.C(self.high_key, self.G_base, self.document.sentences)
        self.C.sort(key=lambda x: x[2])

        # Compute the top links between key terms (red nodes) and columns
        self.G_C = [[i, j] for i, j, c in self.C[-K:]]
                 
        # Prune the base by cutting non-redundant paths
        self.base_adj = self.adjacency_list(self.base, self.G_C)
        self.base = self.prune(self.base, self.base_adj)
        
    # Compute key terms that connect clusters
    def key(self, words, wfs, base, sents):
        # key is a dictionary of the form　key = {w: key value}
        key = {}
        Fg = self.fg(words, wfs, base, sents)
        for w in words:
            product = 1.0
            for g in base:
                product *= 1 - self.fwg(w, wfs, g, sents)*(1.0)/Fg[g]
            key[w] = 1.0 - product
        return key
    
    # Calculate F(g)
    # Neighbors(g) = count of terms in sentences including terms in cluster g
    # g_s = count of cluster g in sentence s
    # w_s = count of word w in sentence s (ie wfs[w][s])
    def fg(self, words, wfs, base, sents):
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
    
    # Calculate f(w,g)
    # Based(w, g) = how many times w appeared in D, based on the basic
    # concept represented by term g
    def fwg(self, w, wfs, g, sents):
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
    
    # Calculate columns c(wi,wj)
    def C(self, hk, base, sents):
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
    
    # Prune graph by removing edges that connect clusters
    # That is, if the two ends of an edge are connected only by
    # one edge, remove the edge to create two clusters
    def prune(self, base, base_adj):
        new_base = []
        for [i, j] in base:
            if self.find_path(base_adj, i, j, [i, j], []):
                print("find path:", [i, j])
                new_base.append([i, j])
            else:
                print("no path found:", [i, j])
        return new_base
         
    # Find a path between two nodes that does not include edge
    # This won't necessarily return the best path, but is enough
    # to test whether there is a path
    # https://www.python.org/doc/essays/graphs/
    def find_path(self, graph, start, end, edge, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in graph:
            return None
        for node in [g[0] for g in graph[start] if g[1] == 'base']:
            if (node not in path) and not([path[-1], node] == edge):
                new_path = self.find_path(graph, node, end, edge, path)
                if new_path:
                    return new_path
        return None
        
    # Draw keygraph in dot format
    def draw(self, base, G_C, fname):
        fout = codecs.open("./dot/" + fname + ".dot","w","utf-8")
        fout.write('graph keygraph {\n')
        fout.write('graph [size="10,10"]\n')
    
        g = []
        for i, j in base:
            g.append(i)
            g.append(j)
        for i in set(g):
            fout.write(self.quote(i) + ' [color="black"]\n')
        k = []
        for i, j in G_C:
            k.append(i)
        for i in set(k):
            fout.write(self.quote(i) + ' [color="red"]\n')
            
        for i, j in base:
            fout.write(self.quote(i) + '--' + self.quote(j) +'\n')
        for i, j in G_C:
            fout.write(self.quote(i) + '--' + self.quote(j) + ' [color="red", style="dotted"]\n')
        fout.write('}')
        fout.close()
        
    # Add optional quotes around a name
    def quote(self, name):
        if 1 in [c in name for c in ['-', '/', '.', '\'']]:
            return "\"{}\"".format(name)
        return name
        
#-----------Main----------------
if __name__ == "__main__":
    stime = time.time() 
    
#   Create a document
    fname = Util.get_file_name()
    doc = Document(file_name = 'txt_files/' + fname + '.txt')
        
#   Create a keygraph
    kg = KeyGraph(doc)
    kg.save_adjacency_list(fname)
    kg.draw(kg.base, kg.G_C, fname)

    etime = time.time()
    print("Execution time: %.4f seconds" % (etime - stime))
