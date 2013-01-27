# coding=UTF-8
from pygraphviz import *
import codecs

f = codecs.open("base.dot","r","utf-8")

base = ""
for row in f:
    base += row

print base
'''
 
dot = """
graph graph1
{
              猫 -- ドラえもん -- 狸;
                札幌 -- 富良野;
                }
"""
 
'''
 
graph = AGraph(string=base)
graph.layout(prog='dot')
graph.draw('pgv1.png')
