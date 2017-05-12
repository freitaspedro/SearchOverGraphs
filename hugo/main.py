#!/usr/bin/env python

'''
'''

import numpy as np
import pickle
import os
import statistics
import search

def load_list(filename):
    with open(filename, "rb") as fp:
        mlist = pickle.load(fp)
    return mlist

def save(steps, name, feat_column, mtype, budgets, time, positives):
    filename = name+"_f"+feat_column+"_"+mtype+".search.csv"
    if not os.path.isfile(filename):
        out_csv = csv.writer(open(filename, "wb"))
        out_csv.writerow(["budget", "time", "positives_mean", "positives_stdev"])
        for i in xrange(0, steps+1):
            out_csv.writerow([budgets[i], statistics.mean(time[i]), statistics.mean(positives[i]), statistics.stdev(positives[i])])
    else:
        out_csv = csv.writer(open(filename, "a"))
        for i in xrange(0, steps+1):
            out_csv.writerow([budgets[i], statistics.mean(time[i]), statistics.mean(positives[i]), statistics.stdev(positives[i])])
    print "%s saved" % filename

def store(steps, j, positives_t, time_t, positives, time):
    for k in xrange(0, steps+1):
        positives_t[k][j] = positives[k]
        time_t[k][j] = time[k]
    return positives_t, time_t

def main(starts_file, neighbours_file, values_file, pt_t, pd_t, initial_budget=0, step_size=0, steps=0, runs=0):
    neighbours = load_list(neighbours_file)
    values = load_list(values_file)

    starts = np.loadtxt(starts_file, delimiter=" ")

    budgets = [0]*(steps+1)
    for i in xrange(0, steps+1):
        budgets[i] = initial_budget+i*step_size
    print "budgets", budgets

    bfs_positives_t, bfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    dfs_positives_t, dfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    heu1_positives_t, heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    heu2_positives_t, heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    fake_heu2_positives_t, fake_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    dy_heu2_positives_t, dy_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    heu3_positives_t, heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]
    mod_positives_t, mod_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)], \
    [[0]*runs for count in range(steps+1)]

    j = 0
    while j < runs:
        print "round", j
        # start = g.vertex(random.choice(inn))
        start = g.vertex(starts[j])
        # print "start", g.vp.name[start]       # egonets - facebook, gplus, twitter
        # print "start", g.vp.label[start]          # polblogs, polbooks

        bfs_positives, bfs_time = search.breadth_first_search(neighbours, values, start, budgets)         # breadth first search (BFS)
        bfs_positives_t, bfs_time_t = store(steps, j, bfs_positives_t, bfs_time_t, bfs_positives, bfs_time)

        dfs_positives, dfs_time = search.depth_first_search(neighbours, values, start, budgets)           # depth first search (DFS)
        dfs_positives_t, dfs_time_t = store(steps, j, dfs_positives_t, dfs_time_t, dfs_positives, dfs_time)

        # ideia 1 - ocorrer em todas as arestas
        heu1_positives, heu1_time = search.heu_search(neighbours, values, 1268107, start, budgets, pt_t, pd_t, 1)
        heu1_positives_t, heu1_time_t = store(steps, j, heu1_positives_t, heu1_time_t,
            heu1_positives, heu1_time)

        # ideia 2 - ocorrer na maioria das arestas
        heu2_positives, heu2_time = search.heu_search(neighbours, values, 1268107, start, budgets, pt_t, pd_t, 2)
        heu2_positives_t, heu2_time_t = store(steps, j, heu2_positives_t, heu2_time_t,
            heu2_positives, heu2_time)

        # ideia 2.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        fake_heu2_positives, fake_heu2_time = search.heu_search(neighbours, values, 1268107, start, budgets, pt_t, pd_t, 2)
        fake_heu2_positives_t, fake_heu2_time_t = store(steps, j, fake_heu2_positives_t,
            fake_heu2_time_t, fake_heu2_positives, fake_heu2_time)

        # ideia 2.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        dy_heu2_positives, dy_heu2_time = search.heu_search(neighbours, values, 1268107, start, budgets, pt_t, pd_t, 2)
        dy_heu2_positives_t, dy_heu2_time_t = store(steps, j, dy_heu2_positives_t, dy_heu2_time_t,
            dy_heu2_positives, dy_heu2_time)

        # ideia 3 - ocorrer em pelo menos uma aresta
        heu3_positives, heu3_time = search.heu_search(neighbours, values, 1268107, start, budgets, pt_t, pd_t, 3)
        heu3_positives_t, heu3_time_t = store(steps, j, heu3_positives_t, heu3_time_t,
            heu3_positives, heu3_time)

        # maximum observed degree (mod adaptado)
        mod_positives, mod_time = search.mod(neighbours, values, 1268107, start, budgets)
        mod_positives_t, mod_time_t = store(steps, j, mod_positives_t, mod_time_t,
            mod_positives, mod_time)
        j += 1

    save(steps, name, feat_column, "BFS", budgets, bfs_time_t, bfs_positives_t)
    save(steps, name, feat_column, "DFS", budgets, dfs_time_t, dfs_positives_t)
    save(steps, name, feat_column, "HEU1", budgets, heu1_time_t, heu1_positives_t)
    save(steps, name, feat_column, "HEU2", budgets, heu2_time_t, heu2_positives_t)
    save(steps, name, feat_column, "HEU3", budgets, heu3_time_t, heu3_positives_t)
    save(steps, name, feat_column, "MODs", budgets, mod_time_t, mod_positives_t)


if __name__ == "__main__":
    main("starts.txt", "gcc_dblp_g", "textgraphs/textgraphs_gcc_dblp_g", 3.16763289247e-05, 0.966659806545, 1000, 2000, 14, 20)
    # main("gcc_dblp_g", "p2p/p2p_gcc_dblp_g", 1000, 2000, 13, 20)
    # main("gcc_dblp_g", "wcnc/wcnc_gcc_dblp_g", 10000, 20000, 13, 20)
    # main("gcc_dblp_g", "group1/group1_gcc_dblp_g", 10000, 20000, 13, 20)
    # main("gcc_dblp_g", "group2/group2_gcc_dblp_g", 10000, 20000, 13, 20)