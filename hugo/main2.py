#!/usr/bin/env python

'''
Esse modulo realizada os diversos tipos de busca (bfs, dfs, busca heuristica e mod) sobre um grafo
de entrada. Cada busca e realizada 'runs' vezes com vertices iniciais aleatorios. Ao fim, e calulada a media e
desvio padrao do tempo gasto assim como dos vertices positivos encontrados (i.e, vertices com a variavel
indicadora igual a 1 (True)) para todas as buscas
'''

import pickle
import search2
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

def main(starts_file, neighbours_file, values_file, pt_t, pd_t, ini=1, initial_budget=0, step_size=0, steps=0, runs=0):
    print "loading files"

    num_v = 1268106

    neighbours = load_list(neighbours_file)
    # print "neighbours", neighbours[:10]

    values = load_list(values_file)
    # print "values", values[:10]

    starts = load_list(starts_file)
    # print "starts", starts

    budgets = [initial_budget+st*step_size for st in range(steps+1)]
    # print "budgets", budgets

    bfs_positives_t, bfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    bfs_positives_t, bfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dfs_positives_t, dfs_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    heu1_positives_t, heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # fake_heu1_positives_t, fake_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy1_heu1_positives_t, dy1_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy10_heu1_positives_t, dy10_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy100_heu1_positives_t, dy100_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    heu2_positives_t, heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # fake_heu2_positives_t, fake_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy1_heu2_positives_t, dy1_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy10_heu2_positives_t, dy10_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy100_heu2_positives_t, dy100_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    heu3_positives_t, heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # fake_heu3_positives_t, fake_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy1_heu3_positives_t, dy1_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy10_heu3_positives_t, dy10_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    # dy100_heu3_positives_t, dy100_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    mod_positives_t, mod_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]

    print "starting"

    j = 0
    while j < runs:
        print "round", j
        curr_start = starts[j]
        # print "curr_start", curr_start

        # breadth first search (BFS)
        bfs_positives, bfs_time = search2.breadth_first_search(neighbours, values, 1268106, curr_start, budgets)
        bfs_positives_t, bfs_time_t = store(steps, j, bfs_positives_t, bfs_time_t, bfs_positives, bfs_time)

        # depth first search (DFS)
        dfs_positives, dfs_time = search2.depth_first_search(neighbours, values, 1268106, curr_start, budgets)
        dfs_positives_t, dfs_time_t = store(steps, j, dfs_positives_t, dfs_time_t, dfs_positives, dfs_time)

        # ideia 1 - ocorrer em todas as arestas
        heu1_positives, heu1_time = search2.heu_search(neighbours, values, 1268106, curr_start, budgets, pt_t, pd_t, 1)
        heu1_positives_t, heu1_time_t = store(steps, j, heu1_positives_t, heu1_time_t, heu1_positives, heu1_time)

        # # ideia 1.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        # fake_heu1_positives, fake_heu1_time = search2.heu_search(neighbours, values, 1268106, curr_start, budgets, 0.5, 0.5, 1)
        # fake_heu1_positives_t, fake_heu1_time_t = store(steps, j, fake_heu1_positives_t, fake_heu1_time_t, \
        # fake_heu1_positives, fake_heu1_time)

        # # ideia 1.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy1_heu1_positives, dy1_heu1_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 1, 1)
        # dy1_heu1_positives_t, dy1_heu1_time_t = store(steps, j, dy1_heu1_positives_t, dy1_heu1_time_t, dy1_heu1_positives, dy1_heu1_time)

        # # ideia 1.b.a - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy10_heu1_positives, dy10_heu1_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 10, 1)
        # dy10_heu1_positives_t, dy10_heu1_time_t = store(steps, j, dy10_heu1_positives_t, dy10_heu1_time_t, dy10_heu1_positives, dy10_heu1_time)

        # # ideia 1.b.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy100_heu1_positives, dy100_heu1_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 100, 1)
        # dy100_heu1_positives_t, dy100_heu1_time_t = store(steps, j, dy100_heu1_positives_t, dy100_heu1_time_t, dy100_heu1_positives, dy100_heu1_time)

        # ideia 2 - ocorrer na maioria das arestas
        heu2_positives, heu2_time = search2.heu_search(neighbours, values, 1268106, curr_start, budgets, pt_t, pd_t, 2)
        heu2_positives_t, heu2_time_t = store(steps, j, heu2_positives_t, heu2_time_t, heu2_positives, heu2_time)

        # # ideia 2.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        # fake_heu2_positives, fake_heu2_time = search2.heu_search(neighbours, values, 1268106, curr_start, budgets, 0.5, 0.5, 2)
        # fake_heu2_positives_t, fake_heu2_time_t = store(steps, j, fake_heu2_positives_t, fake_heu2_time_t, \
        # fake_heu2_positives, fake_heu2_time)

        # ideia 2.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy1_heu2_positives, dy1_heu2_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 1, 2)
        # dy1_heu2_positives_t, dy1_heu2_time_t = store(steps, j, dy1_heu2_positives_t, dy1_heu2_time_t, dy1_heu2_positives, dy1_heu2_time)

        # # ideia 2.b.a - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy10_heu2_positives, dy10_heu2_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 10, 2)
        # dy10_heu2_positives_t, dy10_heu2_time_t = store(steps, j, dy10_heu2_positives_t, dy10_heu2_time_t, dy10_heu2_positives, dy10_heu2_time)

        # # ideia 2.b.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy100_heu2_positives, dy100_heu2_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 100, 2)
        # dy100_heu2_positives_t, dy100_heu2_time_t = store(steps, j, dy100_heu2_positives_t, dy100_heu2_time_t, dy100_heu2_positives, dy100_heu2_time)

        # ideia 3 - ocorrer em pelo menos uma aresta
        heu3_positives, heu3_time = search2.heu_search(neighbours, values, 1268106, curr_start, budgets, pt_t, pd_t, 3)
        heu3_positives_t, heu3_time_t = store(steps, j, heu3_positives_t, heu3_time_t, heu3_positives, heu3_time)

        # # ideia 3.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        # fake_heu3_positives, fake_heu3_time = search2.heu_search(neighbours, values, 1268106, curr_start, budgets, 0.5, 0.5, 3)
        # fake_heu3_positives_t, fake_heu3_time_t = store(steps, j, fake_heu3_positives_t, fake_heu3_time_t, \
        # fake_heu3_positives, fake_heu3_time)

        # # ideia 3.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy1_heu3_positives, dy1_heu3_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 1, 3)
        # dy1_heu3_positives_t, dy1_heu3_time_t = store(steps, j, dy1_heu3_positives_t, dy1_heu3_time_t, dy1_heu3_positives, dy1_heu3_time)

        # # ideia 3.b.a - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy10_heu3_positives, dy10_heu3_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 10, 3)
        # dy10_heu3_positives_t, dy10_heu3_time_t = store(steps, j, dy10_heu3_positives_t, dy10_heu3_time_t, dy10_heu3_positives, dy10_heu3_time)

        # # ideia 3.b.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy100_heu3_positives, dy100_heu3_time = search2.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 100, 3)
        # dy100_heu3_positives_t, dy100_heu3_time_t = store(steps, j, dy100_heu3_positives_t, dy100_heu3_time_t, dy100_heu3_positives, dy100_heu3_time)

        # maximum observed degree (mod adaptado)
        mod_positives, mod_time = search2.mod(neighbours, values, 1268106, curr_start, budgets)
        mod_positives_t, mod_time_t = store(steps, j, mod_positives_t, mod_time_t, mod_positives, mod_time)
        j += 1

    # name =  values_file[:values_file.find("_")]
    name =  values_file[:values_file.find("/")]+"/200k"
    save(steps, name, "BFS", budgets, bfs_time_t, bfs_positives_t)
    save(steps, name, "DFS", budgets, dfs_time_t, dfs_positives_t)
    save(steps, name, "HEU1", budgets, heu1_time_t, heu1_positives_t)
    # save(steps, name, "fakeHEU1", budgets, fake_heu1_time_t, fake_heu1_positives_t)
    # save(steps, name, "dy1HEU1", budgets, dy1_heu1_time_t, dy1_heu1_positives_t)
    # save(steps, name, "dy10HEU1", budgets, dy10_heu1_time_t, dy10_heu1_positives_t)
    # save(steps, name, "dy100HEU1", budgets, dy100_heu1_time_t, dy100_heu1_positives_t)
    save(steps, name, "HEU2", budgets, heu2_time_t, heu2_positives_t)
    # save(steps, name, "fakeHEU2", budgets, fake_heu2_time_t, fake_heu2_positives_t)
    # save(steps, name, "dy1HEU2", budgets, dy1_heu2_time_t, dy1_heu2_positives_t)
    # save(steps, name, "dy10HEU2", budgets, dy10_heu2_time_t, dy10_heu2_positives_t)
    # save(steps, name, "dy100HEU2", budgets, dy100_heu2_time_t, dy100_heu2_positives_t)
    save(steps, name, "HEU3", budgets, heu3_time_t, heu3_positives_t)
    # save(steps, name, "fakeHEU3", budgets, fake_heu3_time_t, fake_heu3_positives_t)
    # save(steps, name, "dy1HEU3", budgets, dy1_heu3_time_t, dy1_heu3_positives_t)
    # save(steps, name, "dy10HEU3", budgets, dy10_heu3_time_t, dy10_heu3_positives_t)
    # save(steps, name, "dy100HEU3", budgets, dy100_heu3_time_t, dy100_heu3_positives_t)
    save(steps, name, "MODs", budgets, mod_time_t, mod_positives_t)


if __name__ == "__main__":
    # sys.argv[1] corresponde ao path para o arquivo de entrada contendo a estrutura do
    # grafo
    #
    # sys.argv[2] corresponde ao path para o arquivo de entrada contendo os valores (0 ou 1)
    # dos vertices
    #
    # sys.argv[3] corresponde ao valor de pt_t (prob de ser 't'-'t' dado que temos um 't')
    #
    # sys.argv[4] corresponde ao valor de pd_t (prob de ser 't'-'n' dado que temos um 'n')
    #
    # sys.argv[5] corresponde ao valor inicial para nt, nd e nn no calculo de pt_t e pd_t dinamico
    #
    # sys.argv[6] corresponde ao orcamento inicial para as buscas
    #
    # sys.argv[7] corresponde ao incremento no orcamento
    #
    # sys.argv[8] corresponde ao numero de vezes que o orcamento e incrementado
    #
    # sys.argv[9] corresponde ao numero de rodadas da simulacao
    if len(sys.argv) != 10:
        print "err: missing params. the program need 9 params."
    else:
        main("200k_starts", sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), \
            int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9]))

    # main2.py "gcc_dblp_g" "textgraphs/textgraphs_gcc_dblp_g" 0.00003175968038 0.966625463535 1 10000 20000 17 50
    # main2.py "gcc_dblp_g" "p2p/p2p_gcc_dblp_g" 0.000653964742925 0.943121351449 1 10000 20000 17 50
    # main2.py "gcc_dblp_g" "wcnc/wcnc_gcc_dblp_g" 0.0158277548439 0.846422940786 1 10000 20000 17 50

    # main2.py "gcc_dblp_g" "group1/group1_gcc_dblp_g" 0.150230752852 0.673388529313 1 10000 20000 17 50
    # main2.py "gcc_dblp_g" "group2/group2_gcc_dblp_g" 0.127930776191 0.697543572635 1 10000 20000 17 50

    # main2.py "gcc_dblp_g" "immerscom/immerscom_gcc_dblp_g" 0.000370557573471 0.964109380934 1 10000 20000 17 50
    # main2.py "gcc_dblp_g" "socialcom/socialcom_gcc_dblp_g" 0.000897882738423 0.943834338661 1 10000 20000 17 50
    # main2.py "gcc_dblp_g" "aaai/aaai_gcc_dblp_g" 0.0149804707989 0.858407026033 1 10000 20000 17 50

    ############################### 200k ########################################

    # main2.py "gcc_200k_dblp_g" "200k_wcnc/wcnc_gcc_200k_dblp_g" 0.0192334720796 0.847948717949 1 1000 2000 17 50

    # main2.py "gcc_200k_dblp_g" "200k_group1/group1_gcc_200k_dblp_g" 0.187868199732 0.673207849419 1 1000 2000 17 50
    # main2.py "gcc_200k_dblp_g" "200k_group2/group2_gcc_200k_dblp_g" 0.153841030491 0.703064740063 1 1000 2000 17 50

    # main2.py "gcc_200k_dblp_g" "200k_p2p/p2p_gcc_200k_dblp_g" 0.000810284686608 0.936874518861 1 1000 2000 17 50

    # main2.py "gcc_200k_dblp_g" "200k_textgraphs/textgraphs_gcc_200k_dblp_g" 0.0000195438466199 0.97619047619 1 1000 2000 17 50