#!/usr/bin/env python

import graph_tool.all as gt
import pandas
import props
import random

def initialize_vertices(g, names, f_values, names_in):
    i = 0
    cont = 0
    for curr_name in names:                 # atualiza os vertices com os valores da feat
        if curr_name in names_in:                   # se o vertice tiver em feat.csv e edges.csv
            v = gt.find_vertex(g, g.vp.name, curr_name)
            v = int(v[0])
            g.vp.value[v] = f_values[i]
            cont = cont + 1
        i = i + 1
    return cont

def initialize_vertices_0(g, rest):
    for name in rest:
        v = gt.find_vertex(g, g.vp.name, str(name))
        v = int(v[0])
        g.vp.value[v] = 0

def generate_graph(graph, feat_column):
    feats = pandas.read_csv(graph+".feat.csv")
    names = feats["name"].values.tolist()
    names = [str(n) for n in names]
    # print "names", names, len(names)
    f_values = feats[feat_column].values.tolist()
    # print "feat values", f_values
    g = gt.load_graph_from_csv(graph+".edges.csv", directed=False)
    vprop = g.new_vertex_property("int")
    g.vp.value = vprop
    # g.list_properties()
    names_in = props.get_all_names(g)
    # print "names_in", names_in, len(names_in)
    out_feat_in_edges = list(set(names_in) - set(names))
    # print "edges.csv ids - feat.csv ids =", out_feat_in_edges, len(out_feat_in_edges)
    cont = initialize_vertices(g, names, f_values, names_in)
    if cont != len(names_in):       # verifica se existem vertices no edges.csv que nao estejam em feat.csv
        initialize_vertices_0(g, out_feat_in_edges)     # inicializa esses vertices com 0s
    print "%s vertices" % g.num_vertices()
    print "%s edges" % g.num_edges()
    name = graph+"/f"+feat_column+"/g.xml.gz"
    g.save(name)
    print "%s saved" % name

def get_gcc(graph):
    g = gt.load_graph(graph)
    g.set_directed(False)
    print "%s vertices" % g.num_vertices()      # polblogs
    print "%s edges" % g.num_edges()        # polblogs
    l = gt.label_largest_component(g)
    u = gt.GraphView(g, vfilt=l)
    print "%s vertices" % u.num_vertices()
    print "%s edges" % u.num_edges()
    # gcc = graph.replace("g.xml.gz", "gcc.xml.gz")
    gcc = graph.replace("gml", "gcc.xml.gz")       # polblogs
    u.save(gcc)
    print "%s saved" % gcc

def count_positives(graph, feat):
    g = gt.load_graph(graph)
    # g = graph
    positive_count = 0
    for v in g.vertices():
        if g.vp.value[v] == 1:
            positive_count += 1
    out = "feat %s - %s positives (%s percent)" % (feat, positive_count, 100*(positive_count/float(g.num_vertices())))
    print out

def calculate_edges(graph):
    g = gt.load_graph(graph)
    pt, pd, pn = 0.0, 0.0, 0.0
    for e in g.edges():
        src = e.source()
        tgt = e.target()
        if g.vp.value[src] != g.vp.value[tgt]:
            pd = pd + 1
        elif g.vp.value[src] and g.vp.value[tgt]:
            pt = pt + 1
        else:
            pn = pn + 1
    num_edges = g.num_edges()
    if (pt+pd+pn) != num_edges:
        print "err in calculate pt, pd and pn"
    else:
        pt = pt/float(num_edges)
        pd = pd/float(num_edges)
        pn = pn/float(num_edges)
    print "pt:", pt
    print "pd:", pd
    print "pn:", pn
    pt_t = pt/float(1-pd)             # prob de ser 't'-'t' dado que temos um 't'
    pd_t = pd/float(1-pn)            # prob de ser 't'-'n' dado que temos um 'n'
    print "pt_t:", pt_t
    print "pd_t:", pd_t

def get_positive_subgraph(graph, exit):
    g = gt.load_graph(graph)
    u = gt.GraphView(g, vfilt=lambda v: g.vp.value[v] == 1)
    print "%s vertices" % u.num_vertices()
    print "%s edges" % u.num_edges()
    u.save(exit)
    print "%s saved" % exit

def get_starts(graph, n, tag):
    g = gt.load_graph(graph)
    ids = []
    for v in g.vertices():
        ids.append(int(v))
    starts = random.sample(ids, n)  # sorteia aleatoriamento n vertices
    # print "starts", starts
    with open("starts_"+tag, "wb") as f:
        for item in starts:
            f.write("%s\n" % item)
    print "starts_%s saved" % (tag)

def graph_to_list(graph, num_v, filename):
    g = gt.load_graph(graph)
    neighbours = [[num_v+2] for count in range(num_v)]     # todos os vertices comecam tendo um vizinho que nao existe
    for v in g.vertices():
        neighbours[int(v)] = [int(n) for n in v.out_neighbours()]
    with open(filename, "wb") as f:
        for item in neighbours:
            f.write("%s\n" % item)
    print "%s saved" % filename

def graph_values_to_list(graph, num_v, filename):
    g = gt.load_graph(graph)
    values = [False]*num_v      # todos os vertices comecam tendo valor 'false'
    for v in g.vertices():
        values[int(v)] = bool(g.vp.value[v])
    with open(filename, "wb") as f:
        for item in values:
            f.write("%s\n" % item)
    print "%s saved" % filename


if __name__ == "__main__":
    generate_graph("snap/facebook/1912", "240")
    # get_gcc("snap/facebook/1912/f240/g.xml.gz")
    # count_positives("snap/facebook/1912/f240/gcc.xml.gz", "240")
    # calculate_edges("snap/facebook/1912/f240/gcc.xml.gz")
    # get_starts("snap/facebook/1912/f119/gcc.xml.gz", 100, "fb")         # executa uma vez por egonet
    # # graph_to_list("snap/facebook/1912/f119/gcc.xml.gz", 747, "snap/facebook/1912/neighbours")            # executa uma vez por egonet
    # graph_values_to_list("snap/facebook/1912/f240/gcc.xml.gz", 747, "snap/facebook/1912/f240/values")
    # get_positive_subgraph("snap/facebook/1912/f240/gcc.xml.gz", "snap/facebook/1912/f240/positives_gcc.xml.gz")

    # generate_graph("snap/gplus/116807883656585676940", "862")
    # get_gcc("snap/gplus/116807883656585676940/f862/g.xml.gz")
    # count_positives("snap/gplus/116807883656585676940/f862/gcc.xml.gz", "862")
    # calculate_edges("snap/gplus/116807883656585676940/f862/gcc.xml.gz")
    # get_starts("snap/gplus/116807883656585676940/f0/gcc.xml.gz", 100, "gplus")      # executa uma vez por egonet
    # # graph_to_list("snap/gplus/116807883656585676940/f0/gcc.xml.gz", 4872, "snap/gplus/116807883656585676940/neighbours")            # executa uma vez por egonet
    # graph_values_to_list("snap/gplus/116807883656585676940/f862/gcc.xml.gz", 4872, "snap/gplus/116807883656585676940/f862/values")
    # get_positive_subgraph("snap/gplus/116807883656585676940/f862/gcc.xml.gz", "snap/gplus/116807883656585676940/f862/positives_gcc.xml.gz")

    # get_gcc("uci/polblogs/polblogs.gml")
    # count_positives("uci/polblogs/polblogs.gcc.xml.gz", "-1")
    # calculate_edges("uci/polblogs/polblogs.gcc.xml.gz")
    # get_starts("uci/polblogs/polblogs.gcc.xml.gz", 100, "polblogs")
    # graph_to_list("uci/polblogs/polblogs.gcc.xml.gz", 1490, "uci/polblogs/neighbours")
    # graph_values_to_list("uci/polblogs/polblogs.gcc.xml.gz", 1490, "uci/polblogs/values")
    # get_positive_subgraph("uci/polblogs/polblogs.gcc.xml.gz", "uci/polblogs/positives_gcc.xml.gz")