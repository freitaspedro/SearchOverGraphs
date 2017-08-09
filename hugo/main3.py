#!/usr/bin/env python

'''
Esse modulo realizada os diversos tipos de busca (bfs, dfs, busca heuristica e mod) sobre um grafo
de entrada. Cada busca e realizada 'runs' vezes com vertices iniciais aleatorios. Ao fim, e calulada a media e
desvio padrao do tempo gasto assim como dos vertices positivos encontrados (i.e, vertices com a variavel
indicadora igual a 1 (True)) para todas as buscas.
Usando valores previamente calculados para as heuristicas
'''

import pickle
import search3
import sys
import ast
import numpy as np

def load_list(filename):
    with open(filename, "rb") as f:
        mlist = [ast.literal_eval(line.rstrip("\n")) for line in f]
    return mlist

def save(steps, name, mtype, budgets, time, positives):
    time_mean = np.mean(time, axis=1)
    positives_mean = np.mean(positives, axis=1)
    positives_std = np.std(positives, axis=1)
    result = np.column_stack((budgets, time_mean, positives_mean, positives_std))
    filename = name+"_"+mtype+".search.csv"
    np.savetxt(filename, result, delimiter=",", header="budget, time, positives_mean, positives_stdev")
    print "%s saved" % filename

def store(steps, j, positives_t, time_t, positives, time):
    for k in xrange(0, steps+1):
        positives_t[k][j] = positives[k]
        time_t[k][j] = time[k]
    return positives_t, time_t

def load_dict(filename):
    mdict = {}
    with open(filename, "rb") as f:
        for row in f:
            key, value = row.split(":", 1)
            key = ast.literal_eval(key)
            value = value.rstrip("\n")
            if value == "nan":
                value = 1.0
            else:
                value = ast.literal_eval(value)
            mdict[key] = value
    return mdict

def main(starts_file, neighbours_file, values_file, ini=1, initial_budget=0, step_size=0, steps=0, runs=0):
    neighbours = load_list(neighbours_file)
    # print "neighbours", neighbours[:10]

    values = load_list(values_file)
    # print "values", values[:10]

    starts = load_list(starts_file)
    # print "starts", starts

    budgets = [initial_budget+st*step_size for st in range(steps+1)]
    # print "budgets", budgets

    preheu1 = load_dict(values_file+"_HEU1_pre")
    # print preheu1[(52, 98)]     # (52, 98):4.49640152562e-236
    preheu2 = load_dict(values_file+"_HEU2_pre")
    # print preheu2[(2, 1132)]     # (2, 1132):nan
    # print preheu2[(2, 642)] # (2, 642):0.999999998991
    preheu3 = load_dict(values_file+"_HEU3_pre")
    # print preheu3[(90, 5)]     # (90, 5):0.999999958711

    fake_preheu1 = load_dict(values_file+"_fake_HEU1_pre")
    # print fake_preheu1[(52, 98)]      # (52, 98):7.00649232162e-46
    fake_preheu2 = load_dict(values_file+"_fake_HEU2_pre")
    # print fake_preheu2[(51, 121)]     # (51, 121):0.530374882313
    fake_preheu3 = load_dict(values_file+"_fake_HEU3_pre")
    # print fake_preheu3[(90, 5)]       # (90, 5):1.0

    bfs_positives_t, bfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    bfs_positives_t, bfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dfs_positives_t, dfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    heu1_positives_t, heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    fake_heu1_positives_t, fake_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy_heu1_positives_t, dy_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    heu2_positives_t, heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    fake_heu2_positives_t, fake_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy_heu2_positives_t, dy_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    heu3_positives_t, heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    fake_heu3_positives_t, fake_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy_heu3_positives_t, dy_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    mod_positives_t, mod_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]

    j = 0
    while j < runs:
        print "round", j
        curr_start = starts[j]
        # print "curr_start", curr_start

        # breadth first search (BFS)
        bfs_positives, bfs_time = search3.breadth_first_search(neighbours, values, 1268106, curr_start, budgets)
        bfs_positives_t, bfs_time_t = store(steps, j, bfs_positives_t, bfs_time_t, bfs_positives, bfs_time)

        # depth first search (DFS)
        dfs_positives, dfs_time = search3.depth_first_search(neighbours, values, 1268106, curr_start, budgets)
        dfs_positives_t, dfs_time_t = store(steps, j, dfs_positives_t, dfs_time_t, dfs_positives, dfs_time)

        # ideia 1 - ocorrer em todas as arestas
        heu1_positives, heu1_time = search3.heu_search(neighbours, values, 1268106, curr_start, budgets, preheu1)
        heu1_positives_t, heu1_time_t = store(steps, j, heu1_positives_t, heu1_time_t, heu1_positives, heu1_time)

        # ideia 1.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        fake_heu1_positives, fake_heu1_time = search3.heu_search(neighbours, values, 1268106, curr_start, budgets, fake_preheu1)
        fake_heu1_positives_t, fake_heu1_time_t = store(steps, j, fake_heu1_positives_t, fake_heu1_time_t, \
        fake_heu1_positives, fake_heu1_time)

        # ideia 1.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        dy_heu1_positives, dy_heu1_time = search3.dy_heu_search(neighbours, values, 1268106, curr_start, budgets, ini, 1)
        dy_heu1_positives_t, dy_heu1_time_t = store(steps, j, dy_heu1_positives_t, dy_heu1_time_t, dy_heu1_positives, dy_heu1_time)

        # # ideia 2 - ocorrer na maioria das arestas
        # heu2_positives, heu2_time = search3.heu_search(neighbours, values, 1268106, curr_start, budgets, preheu2)
        # heu2_positives_t, heu2_time_t = store(steps, j, heu2_positives_t, heu2_time_t, heu2_positives, heu2_time)

        # # ideia 2.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        # fake_heu2_positives, fake_heu2_time = search3.heu_search(neighbours, values, 1268106, curr_start, budgets, fake_preheu2)
        # fake_heu2_positives_t, fake_heu2_time_t = store(steps, j, fake_heu2_positives_t, fake_heu2_time_t, \
        # fake_heu2_positives, fake_heu2_time)

        # # ideia 2.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy_heu2_positives, dy_heu2_time = search3.dy_heu_search(neighbours, values, 1268106, curr_start, budgets, ini, 2)
        # dy_heu2_positives_t, dy_heu2_time_t = store(steps, j, dy_heu2_positives_t, dy_heu2_time_t, dy_heu2_positives, dy_heu2_time)

        # ideia 3 - ocorrer em pelo menos uma aresta
        heu3_positives, heu3_time = search3.heu_search(neighbours, values, 1268106, curr_start, budgets, preheu3)
        heu3_positives_t, heu3_time_t = store(steps, j, heu3_positives_t, heu3_time_t, heu3_positives, heu3_time)

        # ideia 3.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        fake_heu3_positives, fake_heu3_time = search3.heu_search(neighbours, values, 1268106, curr_start, budgets, fake_preheu3)
        fake_heu3_positives_t, fake_heu3_time_t = store(steps, j, fake_heu3_positives_t, fake_heu3_time_t, \
        fake_heu3_positives, fake_heu3_time)

        # ideia 3.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        dy_heu3_positives, dy_heu3_time = search3.dy_heu_search(neighbours, values, 1268106, curr_start, budgets, ini, 3)
        dy_heu3_positives_t, dy_heu3_time_t = store(steps, j, dy_heu3_positives_t, dy_heu3_time_t, dy_heu3_positives, dy_heu3_time)

        # maximum observed degree (mod adaptado)
        mod_positives, mod_time = search3.mod(neighbours, values, 1268106, curr_start, budgets)
        mod_positives_t, mod_time_t = store(steps, j, mod_positives_t, mod_time_t, mod_positives, mod_time)
        j += 1

    name =  values_file[:values_file.find("_")]
    save(steps, name, "BFS", budgets, bfs_time_t, bfs_positives_t)
    save(steps, name, "DFS", budgets, dfs_time_t, dfs_positives_t)
    save(steps, name, "HEU1", budgets, heu1_time_t, heu1_positives_t)
    save(steps, name, "fakeHEU1", budgets, fake_heu1_time_t, fake_heu1_positives_t)
    save(steps, name, "dyHEU1", budgets, dy_heu1_time_t, dy_heu1_positives_t)
    # save(steps, name, "HEU2", budgets, heu2_time_t, heu2_positives_t)
    # save(steps, name, "fakeHEU2", budgets, fake_heu2_time_t, fake_heu2_positives_t)
    # save(steps, name, "dyHEU2", budgets, dy_heu2_time_t, dy_heu2_positives_t)
    save(steps, name, "HEU3", budgets, heu3_time_t, heu3_positives_t)
    save(steps, name, "fakeHEU3", budgets, fake_heu3_time_t, fake_heu3_positives_t)
    save(steps, name, "dyHEU3", budgets, dy_heu3_time_t, dy_heu3_positives_t)
    save(steps, name, "MODs", budgets, mod_time_t, mod_positives_t)


if __name__ == "__main__":
    # sys.argv[1] corresponde ao path para o arquivo de entrada contendo a estrutura do
    # grafo
    #
    # sys.argv[2] corresponde ao path para o arquivo de entrada contendo os valores (0 ou 1)
    # dos vertices
    #
    # sys.argv[3] corresponde ao valor inicial para nt, nd e nn no calculo de pt_t e pd_t dinamico
    #
    # sys.argv[4] corresponde ao orcamento inicial para as buscas
    #
    # sys.argv[5] corresponde ao incremento no orcamento
    #
    # sys.argv[6] corresponde ao numero de vezes que o orcamento e incrementado
    #
    # sys.argv[7] corresponde ao numero de rodadas da simulacao
    if len(sys.argv) != 8:
        print "err: missing params. the program need 7 params."
    else:
        main("starts", sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))

    # main3.py "gcc_dblp_g" "textgraphs/textgraphs_gcc_dblp_g" 1 10000 20000 17 50
    # main3.py "gcc_dblp_g" "p2p/p2p_gcc_dblp_g" 1 10000 20000 17 50
    # main3.py "gcc_dblp_g" "wcnc/wcnc_gcc_dblp_g" 1 10000 20000 17 50

    # main3.py "gcc_dblp_g" "group1/group1_gcc_dblp_g" 1 10000 20000 17 50
    # main3.py "gcc_dblp_g" "group2/group2_gcc_dblp_g" 1 10000 20000 17 50

    # main3.py "gcc_dblp_g" "immerscom/immerscom_gcc_dblp_g" 1 10000 20000 17 50
    # main3.py "gcc_dblp_g" "socialcom/socialcom_gcc_dblp_g" 1 10000 20000 17 50
    # main3.py "gcc_dblp_g" "aaai/aaai_gcc_dblp_g" 1 10000 20000 17 50
