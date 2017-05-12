#!/usr/bin/env python

'''
Esse modulo (1) filtra a maior componente conexa do grafo e a salva; (2) processa o grafo
atribuindo aos vertices o valor 1 ou 0 dependendo se autor representado pelo vertice
participou ou nao de um congresso passado como parametro; (3) conta o total de 1's no grafo;
(4) calcula as fracoes dos tipos de arestas; (5) escolhe aleatoriamente n vertices para iniciar as buscas;
(6) grava as informacoes do grafo em listas e salva em arquivos
'''


import graph_tool.all as gt
import numpy as np
import pickle

def get_gcc(graph):
    g = gt.load_graph(graph)
    l = gt.label_largest_component(g)
    u = gt.GraphView(g, vfilt=l)
    print "%s vertices" % u.num_vertices()
    print "%s edges" % u.num_edges()
    # print g.vertice(1268088) # out
    name = "gcc_"+graph
    u.save(name)
    print "%s saved" % name

def get_all_confs(graph):
    g = gt.load_graph(graph)
    # g = graph
    confs = []
    for v in g.vertices():
        confs.extend(g.vp.confs[v])
    return list(set(confs))

def count_positives(graph, conf):
    g = gt.load_graph(graph)
    # g = graph
    positive_count = 0
    for v in g.vertices():
        if conf in g.vp.confs[v]:
            positive_count += 1
    out = "feat %s - %s positives (%s percent)" % (conf, positive_count, 100*(positive_count/float(g.num_vertices())))
    print out
    # with open("positives.txt", "a") as file:
    #     file.write(out+"\n")

def count_positives2(graph, confs):
    g = gt.load_graph(graph)
    # g = graph
    positive_count = 0
    for v in g.vertices():
        inter = [i for i in g.vp.confs[v] if i in confs]
        if inter:
            positive_count += 1
    out = "feat %s - %s positives (%s percent)" % (confs, positive_count, 100*(positive_count/float(g.num_vertices())))
    print out
    # with open("positives.txt", "a") as file:
    #     file.write(out+"\n")

def set_values(graph, conf):
    g = gt.load_graph(graph)
    vprop = g.new_vertex_property("int")
    g.vp.value = vprop
    for v in g.vertices():
        if conf in g.vp.confs[v]:
            g.vp.value[v] = 1
        else:
            g.vp.value[v] = 0
    name = conf+"/"+conf+"_"+graph
    g.save(name)
    print "%s saved" % name

def set_values2(graph, confs, group):
    g = gt.load_graph(graph)
    vprop = g.new_vertex_property("int")
    g.vp.value = vprop
    for v in g.vertices():
        inter = [i for i in g.vp.confs[v] if i in confs]
        if inter:
            g.vp.value[v] = 1
        else:
            g.vp.value[v] = 0
    name = group+"/"+group+"_"+graph
    g.save(name)
    print "%s saved" % name

def calculate_edges(graph):
    g = gt.load_graph(graph)
    pt = 0.0
    pd = 0.0
    pn = 0.0
    for e in g.edges():
        src = e.source()
        tgt = e.target()
        if g.vp.value[src] != g.vp.value[tgt]:
            pd = pd + 1
        elif int(g.vp.value[src]) == 0 and int(g.vp.value[tgt]) == 0:
            pn = pn + 1
        else:
            pt = pt + 1
    num_edges = g.num_edges()
    if (pt+pd+pn) != num_edges:
        print "err in calculate pt, pd and pn"
    # else:
    #     pt = pt/float(num_edges)
    #     pd = pd/float(num_edges)
    #     pn = pn/float(num_edges)
    print "pt:", pt
    print "pd:", pd
    print "pn:", pn
    pt_t = pt/float(num_edges-pd)             # prob de ser 't'-'t' dado que temos um 't'
    pd_t = pd/float(num_edges-pn)            # prob de ser 't'-'n' dado que temos um 'n'
    print "pt_t:", pt_t
    print "pd_t:", pd_t

def get_starts(graph, n):
    g = gt.load_graph(graph)
    ids = []
    for v in g.vertices():
        ids.append(int(v))
    starts = np.random.choice(ids, n)  # sorteia aleatoriamento n vertices
    # print "starts", starts
    filename = "starts.txt"
    np.savetxt(filename, starts, delimiter=" ")
    print "%s saved" % filename

def graph_to_list(graph):
    g = gt.load_graph(graph)
    neighbours = [None]*1268107
    for v in g.vertices():
        neighbours[int(v)] = [int(n) for n in v.out_neighbours()]
    with open("gcc_dblp_g", "wb") as fp:
        pickle.dump(neighbours, fp)

def graph_values_to_list(graph):
    g = gt.load_graph(graph)
    values = [-1]*1268107
    for v in g.vertices():
        values[int(v)] = int(g.vp.value[v])
    with open("group2/group2_gcc_dblp_g", "wb") as fp:
        pickle.dump(values, fp)

def main():
    # get_gcc("dblp_g.xml.gz")
    # count_positives("gcc_dblp_g.xml.gz", "sbsc")
    # set_values2("gcc_dblp_g.xml.gz", ['iscas', 'icra', 'iros', 'smc', 'vtc', 'eusipco'] , "group2")
    calculate_edges("group2/group2_gcc_dblp_g.xml.gz")
    # get_starts("gcc_dblp_g.xml.gz", 20)
    # graph_to_list("gcc_dblp_g.xml.gz")
    # graph_values_to_list("group2/group2_gcc_dblp_g.xml.gz")

if __name__ == "__main__":
    main()
