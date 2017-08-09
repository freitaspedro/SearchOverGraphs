#!/usr/bin/env python

'''
Esse modulo realizada os diversos tipos de busca (bfs, dfs, busca heuristica e mod) sobre um grafo
de entrada. Cada busca e realizada 'runs' vezes com vertices iniciais aleatorios. Ao fim, e calulada a media e
desvio padrao do tempo gasto assim como dos vertices positivos encontrados (i.e, vertices com a variavel
indicadora igual a 1 (True)) para todas as buscas
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
    filename = name+mtype+".search.csv"
    np.savetxt(filename, result, delimiter=",", header="budget, time, positives_mean, positives_stdev")
    print "%s saved" % filename

def store(steps, j, positives_t, time_t, positives, time):
    for k in xrange(0, steps+1):
        positives_t[k][j] = positives[k]
        time_t[k][j] = time[k]
    return positives_t, time_t

def main(starts_file, neighbours_file, values_file, pt_t, pd_t, num_v, initial_budget=0, step_size=0, steps=0, runs=0):
    print "loading files"
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
    fake_heu1_positives_t, fake_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy1_heu1_positives_t, dy1_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy10_heu1_positives_t, dy10_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy100_heu1_positives_t, dy100_heu1_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    heu2_positives_t, heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    fake_heu2_positives_t, fake_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy1_heu2_positives_t, dy1_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy10_heu2_positives_t, dy10_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy100_heu2_positives_t, dy100_heu2_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    heu3_positives_t, heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    fake_heu3_positives_t, fake_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy1_heu3_positives_t, dy1_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy10_heu3_positives_t, dy10_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    dy100_heu3_positives_t, dy100_heu3_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]
    mod_positives_t, mod_time_t = [[0]*runs for count in range(steps+1)], [[0]*runs for count in range(steps+1)]

    print "starting"

    j = 0
    while j < runs:
        print "round", j
        curr_start = starts[j]
        # print "curr_start", curr_start

        # breadth first search (BFS)
        bfs_positives, bfs_time = search3.breadth_first_search(neighbours, values, num_v, curr_start, budgets)
        bfs_positives_t, bfs_time_t = store(steps, j, bfs_positives_t, bfs_time_t, bfs_positives, bfs_time)

        # depth first search (DFS)
        dfs_positives, dfs_time = search3.depth_first_search(neighbours, values, num_v, curr_start, budgets)
        dfs_positives_t, dfs_time_t = store(steps, j, dfs_positives_t, dfs_time_t, dfs_positives, dfs_time)

        # ideia 1 - ocorrer em todas as arestas
        heu1_positives, heu1_time = search3.heu_search(neighbours, values, num_v, curr_start, budgets, pt_t, pd_t, 1)
        heu1_positives_t, heu1_time_t = store(steps, j, heu1_positives_t, heu1_time_t, heu1_positives, heu1_time)

        # # ideia 1.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        # fake_heu1_positives, fake_heu1_time = search3.heu_search(neighbours, values, num_v, curr_start, budgets, 0.5, 0.5, 1)
        # fake_heu1_positives_t, fake_heu1_time_t = store(steps, j, fake_heu1_positives_t, fake_heu1_time_t, \
        # fake_heu1_positives, fake_heu1_time)

        # # ideia 1.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy1_heu1_positives, dy1_heu1_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 1, 1)
        # dy1_heu1_positives_t, dy1_heu1_time_t = store(steps, j, dy1_heu1_positives_t, dy1_heu1_time_t, dy1_heu1_positives, dy1_heu1_time)

        # # ideia 1.b.a - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy10_heu1_positives, dy10_heu1_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 10, 1)
        # dy10_heu1_positives_t, dy10_heu1_time_t = store(steps, j, dy10_heu1_positives_t, dy10_heu1_time_t, dy10_heu1_positives, dy10_heu1_time)

        # # ideia 1.b.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy100_heu1_positives, dy100_heu1_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 100, 1)
        # dy100_heu1_positives_t, dy100_heu1_time_t = store(steps, j, dy100_heu1_positives_t, dy100_heu1_time_t, dy100_heu1_positives, dy100_heu1_time)

        # ideia 2 - ocorrer na maioria das arestas
        heu2_positives, heu2_time = search3.heu_search(neighbours, values, num_v, curr_start, budgets, pt_t, pd_t, 2)
        heu2_positives_t, heu2_time_t = store(steps, j, heu2_positives_t, heu2_time_t, heu2_positives, heu2_time)

        # # ideia 2.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        # fake_heu2_positives, fake_heu2_time = search3.heu_search(neighbours, values, num_v, curr_start, budgets, 0.5, 0.5, 2)
        # fake_heu2_positives_t, fake_heu2_time_t = store(steps, j, fake_heu2_positives_t, fake_heu2_time_t, \
        # fake_heu2_positives, fake_heu2_time)

        # # ideia 2.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy1_heu2_positives, dy1_heu2_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 1, 2)
        # dy1_heu2_positives_t, dy1_heu2_time_t = store(steps, j, dy1_heu2_positives_t, dy1_heu2_time_t, dy1_heu2_positives, dy1_heu2_time)

        # # ideia 2.b.a - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy10_heu2_positives, dy10_heu2_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 10, 2)
        # dy10_heu2_positives_t, dy10_heu2_time_t = store(steps, j, dy10_heu2_positives_t, dy10_heu2_time_t, dy10_heu2_positives, dy10_heu2_time)

        # # ideia 2.b.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy100_heu2_positives, dy100_heu2_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 100, 2)
        # dy100_heu2_positives_t, dy100_heu2_time_t = store(steps, j, dy100_heu2_positives_t, dy100_heu2_time_t, dy100_heu2_positives, dy100_heu2_time)

        # ideia 3 - ocorrer em pelo menos uma aresta
        heu3_positives, heu3_time = search3.heu_search(neighbours, values, num_v, curr_start, budgets, pt_t, pd_t, 3)
        heu3_positives_t, heu3_time_t = store(steps, j, heu3_positives_t, heu3_time_t, heu3_positives, heu3_time)

        # # ideia 3.a - ocorrer na maioria das arestas com pt_t e pd_t obtido a partir do valor fictico 1/3 para pt, pd e pn
        # fake_heu3_positives, fake_heu3_time = search3.heu_search(neighbours, values, num_v, curr_start, budgets, 0.5, 0.5, 3)
        # fake_heu3_positives_t, fake_heu3_time_t = store(steps, j, fake_heu3_positives_t, fake_heu3_time_t, \
        # fake_heu3_positives, fake_heu3_time)

        # # ideia 3.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy1_heu3_positives, dy1_heu3_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 1, 3)
        # dy1_heu3_positives_t, dy1_heu3_time_t = store(steps, j, dy1_heu3_positives_t, dy1_heu3_time_t, dy1_heu3_positives, dy1_heu3_time)

        # # ideia 3.b.a - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy10_heu3_positives, dy10_heu3_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 10, 3)
        # dy10_heu3_positives_t, dy10_heu3_time_t = store(steps, j, dy10_heu3_positives_t, dy10_heu3_time_t, dy10_heu3_positives, dy10_heu3_time)

        # # ideia 3.b.b - ocorrer na maioria das arestas com pt_t e pd_t dinamicos
        # dy100_heu3_positives, dy100_heu3_time = search3.dy_heu_search(neighbours, values, num_v, curr_start, budgets, 100, 3)
        # dy100_heu3_positives_t, dy100_heu3_time_t = store(steps, j, dy100_heu3_positives_t, dy100_heu3_time_t, dy100_heu3_positives, dy100_heu3_time)

        # maximum observed degree (mod adaptado)
        mod_positives, mod_time = search3.mod(neighbours, values, num_v, curr_start, budgets)
        mod_positives_t, mod_time_t = store(steps, j, mod_positives_t, mod_time_t, mod_positives, mod_time)
        j += 1

    name =  values_file.replace("values", "")
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
    # sys.argv[2] corresponde ao path para o arquivo de entrada contendo a estrutura do
    # grafo
    #
    # sys.argv[3] corresponde ao path para o arquivo de entrada contendo os valores (0 ou 1)
    # dos vertices
    #
    # sys.argv[4] corresponde ao valor de pt_t (prob de ser 't'-'t' dado que temos um 't')
    #
    # sys.argv[5] corresponde ao valor de pd_t (prob de ser 't'-'n' dado que temos um 'n')
    #
    # sys.argv[6] corresponde ao total de vertices no grafo original
    #
    # sys.argv[7] corresponde ao orcamento inicial para as buscas
    #
    # sys.argv[8] corresponde ao incremento no orcamento
    #
    # sys.argv[9] corresponde ao numero de vezes que o orcamento e incrementado
    #
    # sys.argv[10] corresponde ao numero de rodadas da simulacao
    if len(sys.argv) != 11:
        print "err: missing params. the program need 10 params."
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9]), int(sys.argv[10]))

    # 747 vertices    60050 edges
    # 744 vertices    60046 edges
    # A - feat 119 - 63 positives (8.46774193548 percent) - pt: 0.0465643007028 pd: 0.231022882457 pn: 0.72241281684
    # - pt_t: 0.0605535582796 pd_t: 0.832253419726
    # B - feat 155 - 108 positives (14.5161290323 percent) - pt: 0.121806614929 pd: 0.286680211838 pn: 0.591513173234
    # - pt_t: 0.170760179305 pd_t: 0.701810176125
    # C - feat 220 - 582 positives (78.2258064516 percent) - pt: 0.750358058822 pd: 0.225726942677 pn: 0.0239149985011
    # - pt_t: 0.969112965672 pd_t: 0.231257464596
    # D - feat 219 - 216 positives (29.0322580645 percent) - pt: 0.132698264664 pd: 0.413216533991 pn: 0.454085201346
    # - pt_t: 0.226145200658 pd_t: 0.75692495424
    # budget 20 - 340 (20)
    # (wperf) main4.py "starts_fb" "snap/facebook/1912/neighbours" "snap/facebook/1912/f119/values" 0.0605535582796 0.832253419726 747 20 20 16 20
    # main4.py "starts_fb" "snap/facebook/1912/neighbours" "snap/facebook/1912/f155/values" 0.170760179305 0.701810176125 747 20 20 16 20
    # main4.py "starts_fb" "snap/facebook/1912/neighbours" "snap/facebook/1912/f220/values" 0.969112965672 0.231257464596 747 20 20 16 20
    # (wperf) main4.py "starts_fb" "snap/facebook/1912/neighbours" "snap/facebook/1912/f219/values" 0.226145200658 0.75692495424 747 20 20 16 20

    # feat 91 - 115 positives (15.4569892473 percent) - pt: 0.0334077207474 pd: 0.0730439996003 pn: 0.893548279652
    # - pt_t: 0.0360402443406 pd_t: 0.686170212766
    # main4.py "starts_fb" "snap/facebook/1912/neighbours" "snap/facebook/1912/f91/values" 0.0360402443406 0.686170212766 747 20 20 16 20

    # feat 240 - 139 positives (18.6827956989 percent) - pt: 0.0446990640509 pd: 0.310728441528 pn: 0.644572494421
    # - pt_t: 0.0648497148932 pd_t: 0.874238590573
    # main4.py "starts_fb" "snap/facebook/1912/neighbours" "snap/facebook/1912/f240/values" 0.0648497148932 0.874238590573 747 20 20 16 20

    ###########################################################################

    # 4872 vertices    416992 edges
    # 4867 vertices    416988 edges
    # A - feat 0 - 3522 positives (72.3649065133 percent) - pt: 0.594614233503 pd: 0.341585369363 pn: 0.0638003971337
    # - pt_t: 0.903099970497 pd_t: 0.364863826386
    # B - feat 1 - 910 positives (18.6973494966 percent) - pt: 0.0348906922981 pd: 0.262165817721 pn: 0.702943489981
    # - pt_t: 0.0472879857509 pd_t: 0.882545269599
    # C - feat 154 - 521 positives (10.7047462503 percent) - pt: 0.0443250165472 pd: 0.211701535776 pn: 0.743973447677
    # - pt_t: 0.0562287237117 pd_t: 0.826873360809
    # budget 100 - 2500 (200)
    # (wperf) main4.py "starts_gplus" "snap/gplus/116807883656585676940/neighbours" "snap/gplus/116807883656585676940/f0/values" 0.903099970497 0.364863826386 4872 100 200 12 20
    # main4.py "starts_gplus" "snap/gplus/116807883656585676940/neighbours" "snap/gplus/116807883656585676940/f1/values" 0.0472879857509 0.882545269599 4872 100 200 12 20
    # main4.py "starts_gplus" "snap/gplus/116807883656585676940/neighbours" "snap/gplus/116807883656585676940/f154/values" 0.0562287237117 0.826873360809 4872 100 200 12 20

    # feat 798 - 247 positives (5.07499486337 percent) - pt: 0.00694264583153 pd: 0.101532897829 pn: 0.891524456339
    # - pt_t: 0.00772721206459 pd_t: 0.935998054518
    # main4.py "starts_gplus" "snap/gplus/116807883656585676940/neighbours" "snap/gplus/116807883656585676940/f798/values" 0.00772721206459 0.935998054518 4872 100 200 12 20

    # feat 862 - 367 positives (7.54057941237 percent) - pt: 0.00680355309985 pd: 0.127528849751 pn: 0.865667597149
    # - pt_t: 0.00779802644237 pd_t: 0.949352851915
    # main4.py "starts_gplus" "snap/gplus/116807883656585676940/neighbours" "snap/gplus/116807883656585676940/f862/values" 0.00779802644237 0.949352851915 4872 100 200 12 20

    ###########################################################################
    # 1490 vertices     19090 edges
    # 1222 vertices     19089 edges
    # feat -1 - 636 positives (52.0458265139 percent) - pt: 0.471161401854 pd: 0.0884278904081 pn: 0.440410707737
    # - pt_t: 0.516866846733 pd_t: 0.158022842164
    # budget 50 - 750 (50)
    # main4.py "starts_polblogs" "uci/polblogs/neighbours" "uci/polblogs/values" 0.516866846733 0.158022842164 1490 50 50 14 20


