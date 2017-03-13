#!/usr/bin/env python

'''
Esse modulo contem metodos que retornam propriedades do grafo
de entrada
'''

import graph_tool.all as gt
import statistics
from collections import Counter

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
    out_degree = []
    in_degree = []
    for v in g.vertices():
        out_degree.append(v.out_degree())
        in_degree.append(v.in_degree())
    return out_degree, in_degree

def get_avg_degrees(g):
    out_degree, in_degree = get_degrees(g)
    return "avg_in_degree %s (std %s)\navg_out_degree %s (std %s)\n" % (statistics.mean(in_degree),
        statistics.pstdev(in_degree), statistics.mean(out_degree), statistics.pstdev(out_degree))

def get_degree_dist(g):
    out_degree, in_degree = get_degrees(g)
    return dict(Counter(out_degree)), dict(Counter(in_degree))

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

def get_all_names(g):
    names = []
    for v in g.vertices():
        names.append(int(g.vp.name[v]))
    return names

def get_v_names_ranks(g, mlist):
    nrank = []
    for v in mlist:
        nrank.append((int(g.vp.name[v]), g.vp.rank[v]))
    return nrank

def get_v_names(g, mlist):
    names = []
    for v in mlist:
        names.append(int(g.vp.name[v]))
    return names

