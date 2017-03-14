#!/usr/bin/env python

'''
Esse modulo constroi o grafo com cada vertice contendo uma variavel associada
indicando a presenca de uma feat passada como parametro. Apos alguns calculos
pertinentes, sao realizados os diversos tipos de busca (bfs e busca heuristica). Cada
busca e realizada 'runs' vezes com vertices iniciais aleatorios. Ao fim, e calulada a media e
desvio padrao dos vertices explorados assim como dos vertices positivos encontrados
(i.e, vertices com a variavel indicadora igual a 1)
'''

import graph_tool.all as gt
import pandas
import props
import statistics
import search
from numpy.random import *
seed(42)
import csv
import os

def initialize_vertices(g, names, f_values, names_in):
    i = 0
    cont = 0
    for curr_name in names:                 # atualiza os vertices com os valores da feat
        if curr_name in names_in:                   # se o vertice tiver em feat.csv e edges.csv
            v = gt.find_vertex(g, g.vp.name, curr_name)
            v = int(v[0])
            g.vp.value[v] = f_values[i]
            g.vp.rank[v] = 0.0
            g.vp.numt[v] = 0
            g.vp.numn[v] = 0
            cont = cont + 1
        i = i + 1
    # v1= gt.find_vertex(g,  g.vp.name, "1917")
    # print "id 1917 - feat_value %s" % g.vp.feat[int(v1[0])]      # id 1917 - feat_value 1
    # v2= gt.find_vertex(g,  g.vp.name, "2428")
    # print "id 2428 - feat_value  %s" % g.vp.feat[int(v2[0])]     # id 2428 - feat_value 0
    return cont

def initialize_vertices_0(g, rest):
    for name in rest:
        v = gt.find_vertex(g, g.vp.name, str(name))
        v = int(v[0])
        g.vp.value[v] = 0
        g.vp.rank[v] = 0.0
        g.vp.numt[v] = 0
        g.vp.numn[v] = 0

def calculate_edges(g):
    pt = 0.0
    pd = 0.0
    pn = 0.0
    for e in g.edges():
        src = e.source()
        tgt = e.target()
        if g.vp.value[src] != g.vp.value[tgt]:
            pd = pd + 1
        elif g.vp.value[src] == 0 and g.vp.value[tgt] == 0:
            pn = pn + 1
        else:
            pt = pt + 1
    num_edges = g.num_edges()
    if (pt + pd + pn) != num_edges:
        print "err in calculate pt, pd and pn"
    else:
        pt = pt / float(num_edges)
        pd = pd / float(num_edges)
        pn = pn / float(num_edges)
    return pt, pd, pn

def display_save(name, feat_column, mtype, budget, positives_mean, positives_stdev, explored_mean, explored_stdev):
    print "---------------------------%s---------------------------" % mtype
    print "budget", budget
    print "mean positives %s     stdev positives %s" % (positives_mean, positives_stdev)
    print "mean explored %s     stdev explored %s" % (explored_mean, explored_stdev)

    filename = name+"_f"+feat_column+"_"+mtype+".search.csv"
    if not os.path.isfile(filename):
        out_csv = csv.writer(open(filename, "wb"))
        out_csv.writerow(["budget", "positives_mean", "positives_stdev", "explored_mean", "explored_stdev"])
        out_csv.writerow([budget, positives_mean, positives_stdev, explored_mean, explored_stdev])
    else:
        out_csv = csv.writer(open(filename, "a"))
        out_csv.writerow([budget, positives_mean, positives_stdev, explored_mean, explored_stdev])
    print "%s saved" % filename

def main(name, isdirected, feat_column, budget=0, runs=0):
    if feat_column == "-1":             # gml
        g = gt.load_graph(name)
        g.set_directed(isdirected)

        vprop1 = g.new_vertex_property("double")
        vprop2 = g.new_vertex_property("int")
        vprop3 = g.new_vertex_property("int")
        g.vp.rank = vprop1
        g.vp.numt = vprop2
        g.vp.numn = vprop3
        # g.list_properties()

        positive_count = 0
        for v in g.vertices():
            if g.vp.value[v] == 1:
                positive_count += 1
            g.vp.rank[v] = 0.0
            g.vp.numt[v] = 0
            g.vp.numn[v] = 0

        print "feat 0 - %s positives (%s percent)" % (positive_count,
            100*(positive_count/float(g.num_vertices())))

    else:               # csv
        feats = pandas.read_csv(name+".feat.csv")
        names = feats["name"].values.tolist()
        names = [str(n) for n in names]
        # print "names", names, len(names)
        f_values = feats[feat_column].values.tolist()
        # print "feat values", f_values
        print "feat %s - %s positives (%s percent)" % (feat_column, f_values.count(1),
            100*(f_values.count(1)/float(len(f_values))))

        g = gt.load_graph_from_csv(name+".edges.csv", directed=isdirected)
        vprop = g.new_vertex_property("int")
        vprop1 = g.new_vertex_property("double")
        vprop2 = g.new_vertex_property("int")
        vprop3 = g.new_vertex_property("int")
        g.vp.value = vprop
        g.vp.rank = vprop1
        g.vp.numt = vprop2
        g.vp.numn = vprop3
        # g.list_properties()
        names_in = props.get_all_names(g)
        # print "names_in", names_in, len(names_in)
        out_feat_in_edges = list(set(names_in) - set(names))
        # print "edges.csv ids - feat.csv ids =", out_feat_in_edges, len(out_feat_in_edges)
        cont = initialize_vertices(g, names, f_values, names_in)
        if cont != len(names_in):       # verifica se existem vertices no edges.csv que nao estejam em feat.csv
            initialize_vertices_0(g, out_feat_in_edges)     # inicializa esses vertices com 0s

    pt, pd, pn = calculate_edges(g)
    print "pt:", pt
    print "pd:", pd
    print "pn:", pn

    i = 0
    bfs_positives_60 = []
    bfs_explored_60 = []
    dfs_positives_60 = []
    dfs_explored_60 = []
    heu_positives_60 = []
    heu_explored_60 = []
    while i < runs:
        print "round", i
        start = g.vertex(randint(0, g.num_vertices()))              # sorteia aleatoriamento um vertice
        # print "start", g.vp.name[start]       # csv
        # print "start", g.vp.label[start]          # gml

        bfs_positives, bfs_explored = search.breadth_first_search(g, start, budget)
        # print "bfs_positives %s/%s" % (bfs_positives, len(bfs_explored))
        # print "bfs_explored %s" % props.get_v_names(g, bfs_explored)          # csv
        # print "bfs_explored %s" % props.get_v_labels(g, bfs_explored)             # gml
        bfs_positives_60.append(bfs_positives)
        bfs_explored_60.append(len(bfs_explored))

        dfs_positives, dfs_explored = search.depth_first_search(g, start, budget)
        # print "dfs_positives %s/%s" % (dfs_positives, len(dfs_explored))
        # print "dfs_explored %s" % props.get_v_names(g, dfs_explored)          # csv
        # print "dfs_explored %s" % props.get_v_labels(g, dfs_explored)             # gml
        dfs_positives_60.append(dfs_positives)
        dfs_explored_60.append(len(dfs_explored))

        heu_positives, heu_explored = search.heu_search(g, start, budget, pt, pd, pn)
        # print "heu_positives %s/%s" % (heu_positives, len(heu_explored))
        # print "heu_explored %s" % props.get_v_names(g, heu_explored)          # csv
        # print "heu_explored %s" % props.get_v_labels(g, heu_explored)             # gml
        heu_positives_60.append(heu_positives)
        heu_explored_60.append(len(heu_explored))
        i = i + 1

    display_save(name, feat_column, "BFS", budget, statistics.mean(bfs_positives_60), statistics.pstdev(bfs_positives_60),
        statistics.mean(bfs_explored_60), statistics.pstdev(bfs_explored_60))
    display_save(name, feat_column, "DFS", budget, statistics.mean(dfs_positives_60), statistics.pstdev(dfs_positives_60),
        statistics.mean(dfs_explored_60), statistics.pstdev(dfs_explored_60))
    display_save(name, feat_column, "HEU", budget, statistics.mean(heu_positives_60), statistics.pstdev(heu_positives_60),
        statistics.mean(heu_explored_60), statistics.pstdev(heu_explored_60))


if __name__ == "__main__":
    # feat 119 - 63 positives, feat 155 - 108 positives, feat 220 - 586 positives, feat 219 - 222 positives
    main("snap/facebook/1912", False, "119", 20, 60)

    # feat 0 - 3528 positives, feat 1 - 914 positives, feat 154 - 521 positives
    # main("snap/gplus/116807883656585676940", False, "0", 100, 60)

    # main("uci/polblogs/polblogs.gml", False, "-1", 50, 60)

