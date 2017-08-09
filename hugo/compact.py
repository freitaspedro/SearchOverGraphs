#!/usr/bin/env python

'''
Esse modulo (1) filtra a maior componente conexa do grafo e a salva; (2) processa o grafo
atribuindo aos vertices o valor 1 (True) ou 0 (False) dependendo se autor representado pelo vertice
participou ou nao de um congresso passado como parametro; (3) conta o total de 1's no grafo;
(4) calcula as fracoes dos tipos de arestas; (5) escolhe aleatoriamente n vertices para iniciar as buscas;
(6) grava as informacoes do grafo em listas e salva em arquivos
'''


import graph_tool.all as gt
import random
import pickle
import sys
import ast

def get_random_vertices(graph, n):
    g = gt.load_graph(graph)
    print "%s vertices" % g.num_vertices()
    print "%s edges" % g.num_edges()
    rand = [1]*n
    zeros = [0]*(g.num_vertices()-n)
    rand.extend(zeros)
    random.shuffle(rand)
    u = gt.GraphView(g, vfilt=lambda v: rand[int(v)])
    print "%s vertices" % u.num_vertices()
    print "%s edges" % u.num_edges()
    name = "200k_"+graph
    u.save(name)
    print "%s saved" % name

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
    vprop = g.new_vertex_property("bool")        # boolean
    g.vp.value = vprop
    for v in g.vertices():
        if conf in g.vp.confs[v]:
            g.vp.value[v] = True
        else:
            g.vp.value[v] = False
    # name = conf+"/"+conf+"_"+graph
    name = "200k_"+conf+"/"+conf+"_"+graph
    g.save(name)
    print "%s saved" % name

def set_values2(graph, confs, group):
    g = gt.load_graph(graph)
    vprop = g.new_vertex_property("bool")        # boolean
    g.vp.value = vprop
    for v in g.vertices():
        inter = [i for i in g.vp.confs[v] if i in confs]
        if inter:
            g.vp.value[v] = True
        else:
            g.vp.value[v] = False
    # name = group+"/"+group+"_"+graph
    name = "200k_"+group+"/"+group+"_"+graph
    g.save(name)
    print "%s saved" % name

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

def get_starts(graph, n):
    g = gt.load_graph(graph)
    ids = []
    for v in g.vertices():
        ids.append(int(v))
    starts = random.sample(ids, n)  # sorteia aleatoriamento n vertices
    # print "starts", starts
    with open("200k_starts", "wb") as f:
        for item in starts:
            f.write("%s\n" % item)
    print "starts saved"

def graph_to_list(graph):
    g = gt.load_graph(graph)
    neighbours = [[1268108] for count in range(1268106)]     # todos os vertices comecam tendo um vizinho que nao existe
    for v in g.vertices():
        neighbours[int(v)] = [int(n) for n in v.out_neighbours()]
    filename = graph[:graph.find(".")]
    with open(filename, "wb") as f:
        for item in neighbours:
            f.write("%s\n" % item)
    print "%s saved" % filename

def graph_values_to_list(graph):
    g = gt.load_graph(graph)
    values = [False]*1268106      # todos os vertices comecam tendo valor 'false'
    for v in g.vertices():
        values[int(v)] = bool(g.vp.value[v])
    filename = graph[:graph.find(".")]
    with open(filename, "wb") as f:
        for item in values:
            f.write("%s\n" % item)
    print "%s saved" % filename


if __name__ == "__main__":
    # sys.argv[1] corresponde a funcao que sera executada
    #
    mtype = int(sys.argv[1])

    if mtype == 0:
        get_gcc(sys.argv[2])
        # compact.py 0 "200k_dblp_g.xml.gz"
    elif mtype == 1:
        count_positives(sys.argv[2], sys.argv[3])
        # compact.py 1 "gcc_200k_dblp_g.xml.gz" "textgraphs"
        # compact.py 1 "gcc_200k_dblp_g.xml.gz" "p2p"
        # compact.py 1 "gcc_200k_dblp_g.xml.gz" "wcnc"
    elif mtype == 2:
        count_positives2(sys.argv[2], ast.literal_eval(sys.argv[3]))
        # compact.py 2 "gcc_200k_dblp_g.xml.gz" "['icassp', 'icip', 'icmcs', 'interspeech', 'hci', 'chi', 'siggraph']"
        # compact.py 2 "gcc_200k_dblp_g.xml.gz" "['iscas', 'icra', 'iros', 'smc', 'vtc', 'eusipco']"
    elif mtype == 3:
        set_values(sys.argv[2], sys.argv[3])
        # compact.py 3 "gcc_200k_dblp_g.xml.gz" "textgraphs"
        # compact.py 3 "gcc_200k_dblp_g.xml.gz" "p2p"
        # compact.py 3 "gcc_200k_dblp_g.xml.gz" "wcnc"
        # compact.py 3 "gcc_dblp_g.xml.gz" "immerscom"
        # compact.py 3 "gcc_dblp_g.xml.gz" "socialcom"
        # compact.py 3 "gcc_dblp_g.xml.gz" "aaai"
    elif mtype == 4:
        set_values2(sys.argv[2], ast.literal_eval(sys.argv[3]), sys.argv[4])
        # compact.py 4 "gcc_200k_dblp_g.xml.gz" "['icassp', 'icip', 'icmcs', 'interspeech', 'hci', 'chi', 'siggraph']" "group1"
        # compact.py 4 "gcc_200k_dblp_g.xml.gz" "['iscas', 'icra', 'iros', 'smc', 'vtc', 'eusipco']" "group2"
    elif mtype == 5:
        calculate_edges(sys.argv[2])
        # compact.py 5 "200k_textgraphs/textgraphs_gcc_200k_dblp_g.xml.gz"
        # compact.py 5 "200k_p2p/p2p_gcc_200k_dblp_g.xml.gz"
        # compact.py 5 "200k_wcnc/wcnc_gcc_200k_dblp_g.xml.gz"
        # compact.py 5 "200k_group1/group1_gcc_200k_dblp_g.xml.gz"
        # compact.py 5 "200k_group2/group2_gcc_200k_dblp_g.xml.gz"
        # compact.py 5 "immerscom/immerscom_gcc_dblp_g.xml.gz"
        # compact.py 5 "socialcom/socialcom_gcc_dblp_g.xml.gz"
        # compact.py 5 "aaai/aaai_gcc_dblp_g.xml.gz"
    elif mtype == 6:
        get_starts(sys.argv[2], int(sys.argv[3]))
        # compact.py 6 "gcc_200k_dblp_g.xml.gz" 100
    elif mtype == 7:
        graph_to_list(sys.argv[2])
        # compact.py 7 "gcc_200k_dblp_g.xml.gz"
    elif mtype == 8:
        graph_values_to_list(sys.argv[2])
        # compact.py 8 "200k_textgraphs/textgraphs_gcc_200k_dblp_g.xml.gz"
        # compact.py 8 "200k_p2p/p2p_gcc_200k_dblp_g.xml.gz"
        # compact.py 8 "200k_wcnc/wcnc_gcc_200k_dblp_g.xml.gz"
        # compact.py 8 "200k_group1/group1_gcc_200k_dblp_g.xml.gz"
        # compact.py 8 "200k_group2/group2_gcc_200k_dblp_g.xml.gz"
        # compact.py 8 "immerscom/immerscom_gcc_dblp_g.xml.gz"
        # compact.py 8 "socialcom/socialcom_gcc_dblp_g.xml.gz"
        # compact.py 8 "aaai/aaai_gcc_dblp_g.xml.gz"
    elif mtype == 9:
        get_positive_subgraph(sys.argv[2], sys.argv[3])
        # compact.py 9 "200k_textgraphs/textgraphs_gcc_200k_dblp_g.xml.gz" "200k_textgraphs/positives_textgraphs_gcc_200k_dblp_g.xml.gz"
        # compact.py 9 "200k_p2p/p2p_gcc_200k_dblp_g.xml.gz" "200k_p2p/positives_p2p_gcc_200k_dblp_g.xml.gz"
        # compact.py 9 "200k_wcnc/wcnc_gcc_200k_dblp_g.xml.gz" "200k_wcnc/positives_wcnc_gcc_200k_dblp_g.xml.gz"
        # compact.py 9 "200k_group1/group1_gcc_200k_dblp_g.xml.gz" "200k_group1/positives_group1_gcc_200k_dblp_g.xml.gz"
        # compact.py 9 "200k_group2/group2_gcc_200k_dblp_g.xml.gz" "200k_group2/positives_group2_gcc_200k_dblp_g.xml.gz"
        # compact.py 9 "immerscom/immerscom_gcc_dblp_g.xml.gz" "immerscom/positives_immerscom_gcc_dblp_g.xml.gz"
        # compact.py 9 "socialcom/socialcom_gcc_dblp_g.xml.gz" "socialcom/positives_socialcom_gcc_dblp_g.xml.gz"
        # compact.py 9 "aaai/aaai_gcc_dblp_g.xml.gz" "aaai/positives_aaai_gcc_dblp_g.xml.gz"
    elif mtype == 10:
        get_random_vertices(sys.argv[2], int(sys.argv[3]))
        # compact.py 10 "dblp_g.xml.gz" 200000