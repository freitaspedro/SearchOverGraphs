#!/usr/bin/env python

'''
Esse modulo constroi o grafo com cada vertice contendo uma variavel associada
indicando a presenca de uma feat passada como parametro. Apos alguns calculos
pertinentes, sao realizados os diversos tipos de busca (bfs, dfs, busca heuristica e mod). Cada
busca e realizada 'runs' vezes com vertices iniciais aleatorios. Ao fim, e calulada a media e
desvio padrao dos vertices explorados assim como dos vertices positivos encontrados
(i.e, vertices com a variavel indicadora igual a 1)
'''

import graph_tool.all as gt
import pandas
import props
import statistics
import search2
import numpy as np
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
            cont = cont + 1
        i = i + 1
    return cont

def initialize_vertices_0(g, rest):
    for name in rest:
        v = gt.find_vertex(g, g.vp.name, str(name))
        v = int(v[0])
        g.vp.value[v] = 0

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

def save(steps, name, feat_column, mtype, budgets, time, positives, eplusd):
    filename = name+"_f"+feat_column+"_"+mtype+".search.csv"
    if not os.path.isfile(filename):
        out_csv = csv.writer(open(filename, "wb"))
        out_csv.writerow(["budget", "time", "positives_mean", "positives_stdev", "eplusd_mean", "eplusd_stdev"])
        for i in xrange(0, steps+1):
            out_csv.writerow([budgets[i], statistics.mean(time[i]), statistics.mean(positives[i]), statistics.pstdev(positives[i]),
                statistics.mean(eplusd[i]), statistics.pstdev(eplusd[i])])
    else:
        out_csv = csv.writer(open(filename, "a"))
        for i in xrange(0, steps+1):
            out_csv.writerow([budgets[i], statistics.mean(time[i]), statistics.mean(positives[i]), statistics.pstdev(positives[i]),
                statistics.mean(eplusd[i]), statistics.pstdev(eplusd[i])])
    print "%s saved" % filename

def store(steps, j, positives_t, time_t, positives, time):
    for k in xrange(0, steps+1):
        positives_t[k][j] = positives[k]
        time_t[k][j] = time[k]
    return positives_t, time_t

def store2(steps, j, positives_t, eplusd_t, time_t, positives, eplusd, time):
    for k in xrange(0, steps+1):
        positives_t[k][j] = positives[k]
        eplusd_t[k][j] = eplusd[k]
        time_t[k][j] = time[k]
    return positives_t, eplusd_t, time_t

def main(name, isdirected, feat_column, initial_budget=0, step_size=0, steps=0, runs=0):
    if feat_column == "-1":             # polblogs, polbooks
        g = gt.load_graph(name)
        g.set_directed(isdirected)
        # g.list_properties()

        positive_count = 0
        for v in g.vertices():
            if g.vp.value[v] == 1:
                positive_count += 1
            if g.vp.value[v] == "c":        # polbooks - feat_values = "c", "n" ou "l"
                g.vp.value[v] = 1
                positive_count += 1
            elif g.vp.value[v] == "l" or g.vp.value[v] == "n":
                g.vp.value[v] = 0

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
        g.vp.value = vprop
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

    starts = np.random.choice(inn, 20)  # sorteia aleatoriamento 20 vertices na maior componente conexa
    # print "starts", starts
    filename = name+"_f"+feat_column+".starts.txt"
    np.savetxt(filename, starts, delimiter=" ")
    print "%s saved" % filename

    budgets = [0]*(steps+1)
    for i in xrange(0, steps+1):
        budgets[i] = initial_budget+i*step_size
    # print "budgets", budgets

    num_vertices = g.num_vertices()

    bfs_positives_t, bfs_eplusd_t, bfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    bfs2_positives_t, bfs2_eplusd_t, bfs2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    dfs_positives_t, dfs_eplusd_t, dfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    dfs2_positives_t, dfs2_eplusd_t, dfs2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    heu1_positives_t, heu1_eplusd_t, heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    heu2_positives_t, heu2_eplusd_t, heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    fake_heu2_positives_t, fake_heu2_eplusd_t, fake_heu2_time_t = [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy_heu2_positives_t, dy_heu2_eplusd_t, dy_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    heu3_positives_t, heu3_eplusd_t, heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    mod_positives_t, mod_eplusd_t, mod_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]

    j = 0
    while j < runs:
        print "round", j
        # start = g.vertex(random.choice(inn))
        start = g.vertex(starts[j])
        # print "start", g.vp.name[start]       # egonets - facebook, gplus, twitter
        # print "start", g.vp.label[start]          # polblogs, polbooks

        bfs_positives, bfs_time = search2.breadth_first_search(g, start, budgets)         # breadth first search (BFS)
        bfs_positives_t, bfs_time_t = store(steps, j, bfs_positives_t, bfs_time_t, bfs_positives, bfs_time)

        bfs2_positives, bfs2_time = search2.breadth_first_search2(g, start, budgets, num_vertices)         # breadth first search (BFS)
        bfs2_positives_t, bfs2_time_t = store(steps, j, bfs2_positives_t, bfs2_time_t, bfs2_positives, bfs2_time)

        dfs_positives, dfs_time = search2.depth_first_search(g, start, budgets)           # depth first search (DFS)
        dfs_positives_t, dfs_time_t = store(steps, j, dfs_positives_t, dfs_time_t, dfs_positives, dfs_time)

        dfs2_positives, dfs2_time = search2.depth_first_search2(g, start, budgets, num_vertices)           # depth first search (DFS)
        dfs2_positives_t, dfs2_time_t = store(steps, j, dfs2_positives_t, dfs2_time_t, dfs2_positives, dfs2_time)

        # ideia 1 - ocorrer em todas as arestas
        heu1_positives, heu1_eplusd, heu1_time = search2.ot_heu_search(g, num_vertices, start, budgets, pt_t, pd_t, 1)
        heu1_positives_t, heu1_eplusd_t, heu1_time_t = store2(steps, j, heu1_positives_t, heu1_eplusd_t, heu1_time_t,
            heu1_positives, heu1_eplusd, heu1_time)

        # ideia 2 - ocorrer na maioria das arestas
        heu2_positives, heu2_eplusd, heu2_time = search2.ot_heu_search(g, num_vertices, start, budgets, pt_t, pd_t, 2)
        heu2_positives_t, heu2_eplusd_t, heu2_time_t = store2(steps, j, heu2_positives_t, heu2_eplusd_t, heu2_time_t,
            heu2_positives, heu2_eplusd, heu2_time)

        # ideia 2.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        fake_heu2_positives, fake_heu2_eplusd, fake_heu2_time = search2.ot_heu_search(g, num_vertices, start, budgets, 0.5, 0.5, 2)
        fake_heu2_positives_t, fake_heu2_eplusd_t, fake_heu2_time_t = store2(steps, j, fake_heu2_positives_t, fake_heu2_eplusd_t,
            fake_heu2_time_t, fake_heu2_positives, fake_heu2_eplusd, fake_heu2_time)

        # ideia 2.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        dy_heu2_positives, dy_heu2_eplusd, dy_heu2_time = search2.dy_heu_search(g, num_vertices, start, budgets, 1.0, 2)
        dy_heu2_positives_t, dy_heu2_eplusd_t, dy_heu2_time_t = store2(steps, j, dy_heu2_positives_t, dy_heu2_eplusd_t, dy_heu2_time_t,
            dy_heu2_positives, dy_heu2_eplusd, dy_heu2_time)

        # ideia 3 - ocorrer em pelo menos uma aresta
        heu3_positives, heu3_eplusd, heu3_time = search2.ot_heu_search(g, num_vertices, start, budgets, pt_t, pd_t, 3)
        heu3_positives_t, heu3_eplusd_t, heu3_time_t = store2(steps, j, heu3_positives_t, heu3_eplusd_t, heu3_time_t,
            heu3_positives, heu3_eplusd, heu3_time)

        # maximum observed degree adaptado (mod*)
        mod_positives, mod_eplusd, mod_time = search2.mod(g, num_vertices, start, budgets)
        mod_positives_t, mod_eplusd_t, mod_time_t = store2(steps, j, mod_positives_t, mod_eplusd_t, mod_time_t,
            mod_positives, mod_eplusd, mod_time)
        j += 1

    save(steps, name, feat_column, "BFS", budgets, bfs_time_t, bfs_positives_t, bfs_eplusd_t)
    save(steps, name, feat_column, "BFS2", budgets, bfs2_time_t, bfs2_positives_t, bfs2_eplusd_t)
    save(steps, name, feat_column, "DFS", budgets, dfs_time_t, dfs_positives_t, dfs_eplusd_t)
    save(steps, name, feat_column, "DFS2", budgets, dfs2_time_t, dfs2_positives_t, dfs2_eplusd_t)
    save(steps, name, feat_column, "HEU1", budgets, heu1_time_t, heu1_positives_t, heu1_eplusd_t)
    save(steps, name, feat_column, "HEU2", budgets, heu2_time_t, heu2_positives_t, heu2_eplusd_t)
    save(steps, name, feat_column, "fakeHEU2", budgets, fake_heu2_time_t, fake_heu2_positives_t, fake_heu2_eplusd_t)
    save(steps, name, feat_column, "dyHEU2", budgets, dy_heu2_time_t, dy_heu2_positives_t, dy_heu2_eplusd_t)
    save(steps, name, feat_column, "HEU3", budgets, heu3_time_t, heu3_positives_t, heu3_eplusd_t)
    save(steps, name, feat_column, "MODs", budgets, mod_time_t, mod_positives_t, mod_eplusd_t)


if __name__ == "__main__":
    # 747 vertices, 60050 edges
    # A - feat 119 - 63 positives (8.34437086093 percent) - pt: 0.0465611990008 pd: 0.231007493755 pn: 0.722431307244
    # - pt_t: 0.0605483130495 pd_t: 0.832253419726
    # B - feat 155 - 108 positives (14.3046357616 percent) - pt: 0.121798501249 pd: 0.286661115737 pn: 0.591540383014
    # - pt_t: 0.170744233822 pd_t: 0.701810176125
    # C - feat 220 - 586 positives (77.6158940397 percent) - pt: 0.750308076603 pd: 0.225778517902 pn: 0.0239134054954
    # - pt_t: 0.969112965672 pd_t: 0.231309925956
    # D - feat 219 - 222 positives (29.4039735099) - pt: 0.132756036636 pd: 0.413189009159 pn: 0.454054954205
    # - pt_t: 0.226233043873 pd_t: 0.756832601269
    # budget 20 - 340 (20)
    main("snap/facebook/1912", False, "119", 20, 20, 16, 20)
    # main("snap/facebook/1912", False, "155", 20, 20, 16, 20)
    # main("snap/facebook/1912", False, "220", 20, 20, 16, 20)
    # main("snap/facebook/1912", False, "219", 20, 20, 16, 20)

    # feat 91 - 116 positives (15.3642384106 percent) - pt: 0.0334054954205 pd: 0.073039134055 pn: 0.893555370525
    # pt_t: 0.0360376544984 pd_t: 0.686170212766
    # main("snap/facebook/1912", False, "91", 20, 20, 16, 20)

    # feat 218 - 591 positives (78.2781456954 percent) - pt: 0.694920899251 pd: 0.277235636969 pn: 0.0278434637802
    # pt_t: 0.961476429658 pd_t: 0.285175922437
    # main("snap/facebook/1912", False, "218", 20, 20, 16, 20)

    # feat 240 - 140 positives (18.5430463576 percent) - pt: 0.0446960865945 pd: 0.310707743547 pn: 0.644596169858
    # pt_t: 0.0648434480093 pd_t: 0.874238590573
    # main("snap/facebook/1912", False, "240", 20, 20, 16, 20)

    # feat 259 - 369 positives (48.8741721854 percent) - pt: 0.256086594505 pd: 0.483830141549 pn: 0.260083263947
    # pt_t: 0.496128532714 pd_t: 0.653898091466
    # main("snap/facebook/1912", False, "259", 20, 20, 16, 20)

    # feat 260 - 377 positives (49.9337748344 percent) - pt: 0.246128226478 pd: 0.481199000833 pn: 0.272672772689
    # pt_t: 0.474417410284 pd_t: 0.661599047532
    # main("snap/facebook/1912", False, "260", 20, 20, 16, 20)

    # feat 271 - 231 positives
    # feat 313 - 619 positives
    # feat 31 - 67 positives
    # feat 338 - 118 positives
    # feat 387 - 62 positives
    # feat 419 - 64 positives
    # feat 451 - 58 positives

    ###########################################################################

    # 4872 vertices, 416992 edges
    # A - feat 0 - 3528 positives (72.3395530039 percent) - pt: 0.594615724043 pd: 0.341582092702 pn: 0.0638021832553
    # - pt_t: 0.903097739979 pd_t: 0.364861022524
    # B - feat 1 - 914 positives (18.7410293213 percent) - pt: 0.0348927557363 pd: 0.262163302893 pn: 0.702943941371
    # - pt_t: 0.047290621181 pd_t: 0.882538144829
    # C - feat 154 - 521 positives (10.6827968013 percent) - pt: 0.0443245913591 pd: 0.211699505026 pn: 0.743975903614
    # - pt_t: 0.0562280394871 pd_t: 0.826873360809
    # budget 100 - 2500 (200)
    # main("snap/gplus/116807883656585676940", False, "0", 100, 200, 12, 20)
    # main("snap/gplus/116807883656585676940", False, "1", 100, 200, 12, 20)
    # main("snap/gplus/116807883656585676940", False, "154", 100, 200, 12, 20)

    # feat 798 - 247 positives (5.06458888661 percent) - pt: 0.00694257923413 pd: 0.101531923874 pn: 0.891525496892
    # pt_t: 0.00772712956488 pd_t: 0.935998054518
    # main("snap/gplus/116807883656585676940", False, "798", 100, 200, 12, 20)

    # feat 563 - 426 positives
    # feat 862 - 367 positives
    # feat 492 - 167 positives
    # feat 3 - 144 positives

    ###########################################################################

    # 1490 vertices, 19090 edges
    # A - feat 0 (value 1) - 732 positives (49.1275167785 percent) - pt: 0.471136720796 pd: 0.0884232582504 pn: 0.440440020953
    # - pt_t: 0.516837145156 pd_t: 0.158022842164
    # feat 0 (value 0) - 758 positives (50.8724832215 percent) - pt: 0.440440020953 pd: 0.0884232582504 pn: 0.471136720796
    # pt_t: 0.483162854844 pd_t: 0.167194928685
    # budget 50 - 750 (50)
    # main("uci/polblogs/polblogs.gml", False, "-1", 50, 50, 14, 20)

    ###########################################################################

    # 213 vertices, 17930 edges
    # feat 369 - 27 positives (12.6168224299 percent) pt: 0.0253764640268 pd: 0.263190184049 pn: 0.711433351924
    # pt_t: 0.0344409961396 pd_t: 0.912060301508
    # budget 10 - 110 (10)
    # main("snap/twitter/256497288", False, "369", 10, 10, 10, 20)

    # feat 475 - 54 positives (25.2336448598 percent) - pt: 0.0980479643056 pd: 0.425376464027 pn: 0.476575571668
    # pt_t: 0.170629913617 pd_t: 0.812679808205
    # main("snap/twitter/256497288", False, "475", 10, 10, 10, 20)

    # feat 478 - 17 positives (7.94392523364 percent) - pt: 0.00864472950363 pd: 0.172783045176 pn: 0.818572225321
    # pt_t: 0.010450377562 pd_t: 0.952351675377
    # main("snap/twitter/256497288", False, "478", 10, 10, 10, 20)

    # feat 889 - 103 positives (48.1308411215 percent) pt: 0.359007250418 pd: 0.475906302287 pn: 0.165086447295
    # pt_t: 0.685005852932 pd_t: 0.570006680027
    # main("snap/twitter/256497288", False, "889", 10, 10, 10, 20)

    ###########################################################################

    # 105 vertices, 441 edges
    # feat 0 (value c) - 49 positives (46.6666666667 percent) - pt:  0.430839002268 pd:  0.104308390023 pn:  0.46485260771
    # - pt_t: 0.481012658228 pd_t: 0.194915254237
    # feat 0 (value n) - 13 positives (12.380952381 percent) - pt: 0.0204081632653 pd: 0.131519274376 pn: 0.848072562358
    # pt_t: 0.023498694517 pd_t: 0.865671641791
    # feat 0 (value l) - 43 positives (40.9523809524 percent) - pt: 0.390022675737 pd: 0.0816326530612 pn: 0.528344671202
    # pt_t: 0.424691358025 pd_t: 0.173076923077
    # budget 10 - 50 (5)
    # main("uci/polbooks/polbooks.gml", False, "-1", 10, 5, 8, 20)            # busca rotulo c