#!/usr/bin/env python

'''
Esse modulo contem metodos que retornam propriedades do grafo
de entrada
'''

import graph_tool.all as gt
import statistics
from collections import Counter

IdInDegree = []
IdOutDegree = []
InDegree = []
OutDegree = []

def get_name(name):
    return "graph '%s'\n" % name

def is_directed(directed):
    return "is directed? %s\n" % directed

def get_num_vertices(g):
    return "%s vertices\n" % g.num_vertices()

def get_num_edges(g):
    return "%s edges\n" % g.num_edges()

def get_diameter(g):
    dist, ends = gt.pseudo_diameter(g)
    return "pseudo_diameter %s (source %s, target %s)\n" % (dist, ends[0], ends[1])

def get_degrees(g):
    for v in g.vertices():
        IdInDegree.append((int(v), g.vp.name[v], v.in_degree()))
        # IdInDegree.append((int(v), g.vp.label[v], v.in_degree()))       # polblogs
        IdOutDegree.append((int(v), g.vp.name[v], v.out_degree()))
        # IdOutDegree.append((int(v), g.vp.label[v], v.out_degree()))     # polblogs
        InDegree.append(v.in_degree())
        OutDegree.append(v.out_degree())

def get_avg_degrees(g):
    get_degrees(g)
    return "max_in_degree %s\nmin_in_degree %s\navg_in_degree %s (std %s)\n" \
                "max_out_degree %s\nmin_out_degree %s\navg_out_degree %s (std %s)\n" \
                % (max(InDegree), min(InDegree), statistics.mean(InDegree), statistics.pstdev(InDegree),
                    max(OutDegree), min(OutDegree), statistics.mean(OutDegree), statistics.pstdev(OutDegree))

def get_degree_dist(g):
    return dict(Counter(InDegree)), dict(Counter(OutDegree))

def get_global_clustering(g):
    return "global_clustering %s (std %s)\n" % (gt.global_clustering(g))

def get_comps(g, directed):
    comp, hist = gt.label_components(g, directed=directed)
    d = dict(Counter(comp.a))
    resp = []
    for k, v in d.items():
        relative_size = v/float(g.num_vertices())
        resp.append("comp %s size %s (%s percent)\n" % (k, v, 100*relative_size))
    return "".join(resp)

def topn_lastn_degrees(g, n):
    sorted_IdInDegree = sorted(IdInDegree, key=lambda tup: tup[2], reverse=True)
    sorted_IdOutDegree = sorted(IdOutDegree, key=lambda tup: tup[2], reverse=True)
    return sorted_IdInDegree[:n], sorted_IdInDegree[-n:], sorted_IdOutDegree[:n], sorted_IdOutDegree[-n:]

def get_all_names(g):
    names = []
    for v in g.vertices():
        names.append(g.vp.name[v])
    return names

def get_v_names(g, mlist):
    names = []
    for v in mlist:
        names.append(g.vp.names[v])
    return names

def get_all_labels(g):
    labels = []
    for v in g.vertices():
        labels.append(g.vp.label[v])
    return labels

def get_v_labels(g, mlist):
    labels = []
    for v in mlist:
        labels.append(g.vp.label[v])
    return labels