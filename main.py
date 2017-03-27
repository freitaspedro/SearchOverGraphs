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
import random
random.seed(42)
import csv
import os
import time

def initialize_vertices(g, names, f_values, names_in):
    i = 0
    cont = 0
    for curr_name in names:                 # atualiza os vertices com os valores da feat
        if curr_name in names_in:                   # se o vertice tiver em feat.csv e edges.csv
            v = gt.find_vertex(g, g.vp.name, curr_name)
            v = int(v[0])
            g.vp.value[v] = f_values[i]
            g.vp.kt[v] = 0
            g.vp.kn[v] = 0
            cont = cont + 1
        i = i + 1
    # v1= gt.find_vertex(g,  g.vp.name, "1917")
    # print "id 1917 - feat_value %s" % g.vp.value[int(v1[0])]      # id 1917 - feat_value 1
    # v2= gt.find_vertex(g,  g.vp.name, "2428")
    # print "id 2428 - feat_value  %s" % g.vp.value[int(v2[0])]     # id 2428 - feat_value 0
    return cont

def initialize_vertices_0(g, rest):
    for name in rest:
        v = gt.find_vertex(g, g.vp.name, str(name))
        v = int(v[0])
        g.vp.value[v] = 0
        g.vp.kt[v] = 0
        g.vp.kn[v] = 0

def calculate_edges(g):
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
    else:
        pt = pt/float(num_edges)
        pd = pd/float(num_edges)
        pn = pn/float(num_edges)
    return pt, pd, pn

def display_save(name, feat_column, mtype, budget, sum_time, time, positives_mean, positives_stdev, explored_mean,
    explored_stdev, eplusd_mean, eplusd_stdev):
    print "---------------------------%s---------------------------" % mtype
    print "budget", budget
    print "total time %ss (%ss per run)" % (sum_time, time)
    print "mean positives %s     stdev positives %s" % (positives_mean, positives_stdev)
    print "mean explored %s     stdev explored %s" % (explored_mean, explored_stdev)
    print "mean explored+discovered %s     stdev explored+discovered %s" % (eplusd_mean, eplusd_stdev)
    '''
    filename = name+"_f"+feat_column+"_"+mtype+".search.csv"
    if not os.path.isfile(filename):
        out_csv = csv.writer(open(filename, "wb"))
        out_csv.writerow(["budget", "time", "positives_mean", "positives_stdev", "explored_mean", "explored_stdev",
            "eplusd_mean", "eplusd_stdev"])
        out_csv.writerow([budget, time, positives_mean, positives_stdev, explored_mean, explored_stdev, eplusd_mean, eplusd_stdev])
    else:
        out_csv = csv.writer(open(filename, "a"))
        out_csv.writerow([budget, time, positives_mean, positives_stdev, explored_mean, explored_stdev, eplusd_mean, eplusd_stdev])
    print "%s saved" % filename
    '''

def main(name, isdirected, feat_column, initial_budget=0, step_size=0, steps=0, runs=0):
    if feat_column == "-1":             # polblogs, polbooks
        g = gt.load_graph(name)
        g.set_directed(isdirected)

        vprop1 = g.new_vertex_property("int")
        vprop2 = g.new_vertex_property("int")
        g.vp.kt = vprop1
        g.vp.kn = vprop2
        # g.list_properties()

        positive_count = 0
        for v in g.vertices():
            if g.vp.value[v] == 1:
                positive_count += 1
            if g.vp.value[v] == "l":        # polbooks - feat_values = "c", "n" ou "l"
                g.vp.value[v] = 1
                positive_count += 1
            elif g.vp.value[v] == "n" or g.vp.value[v] == "c":
                g.vp.value[v] = 0
            g.vp.kt[v] = 0
            g.vp.kn[v] = 0

        print "feat 0 - %s positives (%s percent)" % (positive_count,
            100*(positive_count/float(g.num_vertices())))

    else:               # egonets - facebook, gplus, twitter
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
        vprop1 = g.new_vertex_property("int")
        vprop2 = g.new_vertex_property("int")
        g.vp.value = vprop
        g.vp.kt = vprop1
        g.vp.kn = vprop2
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

    pt_t = pt/float(1-pd)             # prob de ser 't'-'t' dado que temos um 't'
    pd_t = pd/float(1-pn)            # prob de ser 't'-'n' dado que temos um 'n'
    print "pt_t:", pt_t
    print "pd_t:", pd_t

    l = gt.label_largest_component(g)
    mlist = list(l.a)
    out = [i for i, x in enumerate(mlist) if x==0]      # vertices fora da maior componente conexa
    # print "out", out
    glist = list(range(0, g.num_vertices()))
    inn = list(set(glist) - set(out))
    # print "inn", inn

    for i in xrange(0, steps+1):
        budget = initial_budget+i*step_size
        j = 0
        bfs_positives_t, bfs_explored_t, bfs_time = [], [], []
        dfs_positives_t, dfs_explored_t, dfs_time = [], [], []
        heu1_positives_t, heu1_explored_t, heu1_eplusd_t, heu1_time = [], [], [], []
        heu2_positives_t, heu2_explored_t, heu2_eplusd_t, heu2_time = [], [], [], []
        heu3_positives_t, heu3_explored_t, heu3_eplusd_t, heu3_time = [], [], [], []
        mod_positives_t, mod_explored_t, mod_eplusd_t, mod_time = [], [], [], []
        while j < runs:
            # print "round", i
            start = g.vertex(random.choice(inn))              # sorteia aleatoriamento um vertice na maior componente conexa
            # print "start", g.vp.name[start]       # egonets - facebook, gplus, twitter
            # print "start", g.vp.label[start]          # polblogs, polbooks

            start_time = time.time()
            bfs_positives, bfs_explored = search.breadth_first_search(g, start, budget)         # breadth first search (BFS)
            bfs_time.append(time.time() - start_time)
            bfs_positives_t.append(bfs_positives)
            bfs_explored_t.append(bfs_explored)

            start_time = time.time()
            dfs_positives, dfs_explored = search.depth_first_search(g, start, budget)           # depth first search (DFS)
            dfs_time.append(time.time() - start_time)
            dfs_positives_t.append(dfs_positives)
            dfs_explored_t.append(dfs_explored)

            start_time = time.time()
            # ideia 1 - ocorrer em todas as arestas
            heu1_positives, heu1_explored, heu1_eplusd = search.ot_heu_search(g, start, budget, pt_t, pd_t, 1)
            heu1_time.append(time.time() - start_time)
            heu1_positives_t.append(heu1_positives)
            heu1_explored_t.append(heu1_explored)
            heu1_eplusd_t.append(heu1_eplusd)

            start_time = time.time()
            # ideia 2 - ocorrer na maioria das arestas
            heu2_positives, heu2_explored, heu2_eplusd = search.ot_heu_search(g, start, budget, pt_t, pd_t, 2)
            # print "time", time.time() - start_time
            heu2_time.append(time.time() - start_time)
            heu2_positives_t.append(heu2_positives)
            heu2_explored_t.append(heu2_explored)
            heu2_eplusd_t.append(heu2_eplusd)

            start_time = time.time()
            # ideia 3 - ocorrer em pelo menos uma aresta
            heu3_positives, heu3_explored, heu3_eplusd = search.ot_heu_search(g, start, budget, pt_t, pd_t, 3)
            heu3_time.append(time.time() - start_time)
            heu3_positives_t.append(heu3_positives)
            heu3_explored_t.append(heu3_explored)
            heu3_eplusd_t.append(heu3_eplusd)

            start_time = time.time()
            mod_positives, mod_explored, mod_eplusd = search.mod(g, start, budget)        # maximum observed degree (mod)
            mod_time.append(time.time() - start_time)
            mod_positives_t.append(mod_positives)
            mod_explored_t.append(mod_explored)
            mod_eplusd_t.append(mod_eplusd)

            j = j + 1

        display_save(name, feat_column, "BFS", budget, sum(bfs_time), statistics.mean(bfs_time), statistics.mean(bfs_positives_t),
            statistics.pstdev(bfs_positives_t), statistics.mean(bfs_explored_t), statistics.pstdev(bfs_explored_t),
            0.0, 0.0)

        display_save(name, feat_column, "DFS", budget, sum(dfs_time), statistics.mean(dfs_time), statistics.mean(dfs_positives_t),
            statistics.pstdev(dfs_positives_t), statistics.mean(dfs_explored_t), statistics.pstdev(dfs_explored_t),
            0.0, 0.0)

        display_save(name, feat_column, "HEU1", budget, sum(heu1_time), statistics.mean(heu1_time), statistics.mean(heu1_positives_t),
            statistics.pstdev(heu1_positives_t), statistics.mean(heu1_explored_t), statistics.pstdev(heu1_explored_t),
            statistics.mean(heu1_eplusd_t), statistics.pstdev(heu1_eplusd_t))

        display_save(name, feat_column, "HEU2", budget, sum(heu2_time), statistics.mean(heu2_time), statistics.mean(heu2_positives_t),
            statistics.pstdev(heu2_positives_t), statistics.mean(heu2_explored_t), statistics.pstdev(heu2_explored_t),
            statistics.mean(heu2_eplusd_t), statistics.pstdev(heu2_eplusd_t))

        display_save(name, feat_column, "HEU3", budget, sum(heu3_time), statistics.mean(heu3_time), statistics.mean(heu3_positives_t),
            statistics.pstdev(heu3_positives_t), statistics.mean(heu3_explored_t), statistics.pstdev(heu3_explored_t),
            statistics.mean(heu3_eplusd_t), statistics.pstdev(heu3_eplusd_t))

        display_save(name, feat_column, "MOD", budget, sum(mod_time), statistics.mean(mod_time), statistics.mean(mod_positives_t),
            statistics.pstdev(mod_positives_t), statistics.mean(mod_explored_t), statistics.pstdev(mod_explored_t),
            statistics.mean(mod_eplusd_t), statistics.pstdev(mod_eplusd_t))


if __name__ == "__main__":
    # 747 vertices, 60050 edges
    # A - feat 119 - 63 positives (8.34437086093 percent) - pt=0.0465611990008 pd=0.231007493755 pn=0.722431307244
    # - pt_t=0.0605483130495 pd_t=0.832253419726
    # B - feat 155 - 108 positives (14.3046357616 percent) - pt=0.121798501249 pd=0.286661115737 pn=0.591540383014
    # - pt_t=0.170744233822 pd_t=0.701810176125
    # C - feat 220 - 586 positives (77.6158940397 percent) - pt=0.750308076603 pd=0.225778517902 pn=0.0239134054954
    # - pt_t=0.969112965672 pd_t=0.231309925956
    # D - feat 219 - 222 positives (29.4039735099) - pt=0.132756036636 pd=0.413189009159 pn=0.454054954205
    # - pt_t=0.226233043873 pd_t=0.756832601269
    # budget 20 - 340 (20)
    main("snap/facebook/1912", False, "119", 20, 20, 16, 20)
    # main("snap/facebook/1912", False, "155", 20, 20, 16, 20)
    # main("snap/facebook/1912", False, "220", 20, 20, 16, 20)
    # main("snap/facebook/1912", False, "219", 20, 20, 16, 20)

    # 4872 vertices, 416992 edges
    # A - feat 0 - 3528 positives (72.3395530039 percent) - pt=0.594615724043 pd=0.341582092702 pn=0.0638021832553
    # - pt_t=0.903097739979 pd_t=0.364861022524
    # B - feat 1 - 914 positives (18.7410293213 percent) - pt=0.0348927557363 pd=0.262163302893 pn=0.702943941371
    # - pt_t=0.047290621181 pd_t=0.882538144829
    # C - feat 154 - 521 positives (10.6827968013 percent) - pt=0.0443245913591 pd=0.211699505026 pn=0.743975903614
    # - pt_t=0.0562280394871 pd_t=0.826873360809
    # budget 100 - 2500 (200)
    # main("snap/gplus/116807883656585676940", False, "0", 100, 200, 12, 20)
    # main("snap/gplus/116807883656585676940", False, "1", 100, 200, 12, 20)
    # main("snap/gplus/116807883656585676940", False, "154", 100, 200, 12, 20)

    # 1490 vertices, 19090 edges
    # A - feat 0 (value 1) - 732 positives (49.1275167785 percent) - pt=0.471136720796 pd=0.0884232582504 pn=0.440440020953
    # - pt_t=0.516837145156 pd_t=0.158022842164
    # budget 50 - 750 (50)
    # main("uci/polblogs/polblogs.gml", False, "-1", 50, 50, 14, 20)

    # 213 vertices, 17930 edges
    # feat 369 - 27 positives (12.6168224299 percent) - pt=0.0253764640268 pd=0.263190184049  pn=0.711433351924
    # - pt_t=0.0344409961396 pd_t=0.912060301508
    # feat 475 - 54 positives (25.2336448598 percent) - pt=0.0980479643056 pd=0.425376464027 pn=0.476575571668
    # - pt_t= 0.170629913617 pd_t=0.812679808205
    # feat 478 - 17 positives (7.94392523364 percent) - pt=0.00864472950363 pd=0.172783045176 pn=0.818572225321
    # - pt_t=0.010450377562 pd_t=0.952351675377
    # feat 889 - 103 positives (48.1308411215 percent) - pt=0.359007250418 pd=0.475906302287 pn=0.165086447295
    # - pt_t=0.685005852932 pd_t=0.570006680027
    # budget 10 - 110 (10)
    # main("snap/twitter/256497288", False, "369", 10, 10, 10, 20)
    # main("snap/twitter/256497288", False, "475", 10, 10, 10, 20)
    # main("snap/twitter/256497288", False, "478", 10, 10, 10, 20)
    # main("snap/twitter/256497288", False, "889", 10, 10, 10, 20)

    # 105 vertices, 441 edges
    # feat 0 (value c) - 49 positives (46.6666666667 percent) - pt = 0.430839002268 pd = 0.104308390023 pn = 0.46485260771
    # - pt_t=0.481012658228 pd_t=0.194915254237
    # feat 1 (value n) - 13 positives (12.380952381 percent) - pt = 0.0204081632653 pd = 0.131519274376 pn = 0.848072562358
    # - pt_t=0.023498694517 pd_t=0.865671641791
    # feat 2 (value l) -  43 positives (46.6666666667 percent) - pt = 0.390022675737 pd = 0.0816326530612 pn = 0.528344671202
    # - pt_t=0.424691358025 pd_t=0.173076923077
    # budget 10 - 50 (5)
    # main("uci/polbooks/polbooks.gml", False, "-1", 10, 5, 8, 20)            # busca rotulo l