#!/usr/bin/env python

'''
Esse modulo contem os tipos de busca sobre grafo (bfs, dfs, busca heuristica e mod) sem o uso
do graph-tool, sem numpy e usando valores previamente calculados para as heuristicas
'''

import math
import scipy.special as sp
import time

MapDyHeu1 = {}
MapDyHeu2 = {}
MapDyHeu3 = {}

def breadth_first_search(neighbours, values, num_vertices, start, budgets):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, time_t = [0]*max_budget, [0]*max_budget
    status = [False]*num_vertices          # status 0 - desconhecido, status 1 - explorado
    positives = 0
    queue = [start]
    i = 0
    while queue and  i < max_budget:
        start = queue.pop(0)        # retira da fila o vertice mais antigo
        if not status[start]:
            if values[start]:
                positives += 1
            for n in neighbours[start]:
                if not status[n]:
                    queue.append(n)         # poe na fila os vizinhos desconhecidos do vertice explorado
            status[start] = True
            positives_t[i] = positives
            time_t[i] = time.time() - start_time
            i += 1
    bfs_positives = [positives_t[i-1] for i in budgets]
    bfs_time = [time_t[i-1] for i in budgets]
    return bfs_positives, bfs_time

def depth_first_search(neighbours, values, num_vertices, start, budgets):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, time_t = [0]*max_budget, [0]*max_budget
    status = [False]*num_vertices          # status 0 - desconhecido, status 1 - explorado
    positives = 0
    stack = [start]
    i = 0
    while stack and  i < max_budget:
        start = stack.pop()        # retira da pilha o vertice mais recente
        if not status[start]:
            if values[start]:
                positives += 1
            for n in neighbours[start]:
                if not status[n]:
                    stack.append(n)         # poe na pilha os vizinhos desonhecidos do vertice explorado
            status[start] = True
            positives_t[i] = positives
            time_t[i] = time.time() - start_time
            i += 1
    dfs_positives = [positives_t[i-1] for i in budgets]
    dfs_time = [time_t[i-1] for i in budgets]
    return dfs_positives, dfs_time

def p_t_k(k, kt, kn, pt_t, pd_t):
    ini = max(0, k-kn)
    end = min(kt, k)
    sum_k = 0
    for i in xrange(ini, end):
        sum_k += sp.binom(kt, i) * math.pow(pt_t, i) * math.pow(1-pt_t, kt-i) * sp.binom(kn, k-i) * math.pow(pd_t, k-i) * math.pow(1-pd_t, kn-k+i)
    return sum_k

def dyheuristic(pt_t, pd_t, kt, kn, mtype):
    if mtype == 1:                  # ideia 1 - ocorrer em todas as arestas
        if (pt_t, pd_t, kt, kn) in MapDyHeu1:
            return MapDyHeu1[(pt_t, pd_t, kt, kn)]
        pfor = math.pow(pt_t, kt) * math.pow(pd_t, kn)
        MapDyHeu1[(pt_t, pd_t, kt, kn)] = pfor
        return pfor
    elif mtype == 2:                # ideia 2 - ocorrer na maioria das arestas
        if (pt_t, pd_t, kt, kn) in MapDyHeu2:
            return MapDyHeu2[(pt_t, pd_t, kt, kn)]
        pm = 0
        ini = int(math.ceil((kt+kn)/2.0))
        end = kt+kn
        for i in xrange(ini, end):
            pm += p_t_k(i, kt, kn, pt_t, pd_t)
        MapDyHeu2[(pt_t, pd_t, kt, kn)] = pm
        return pm
    elif mtype == 3:                # ideia 3 - ocorre em pelo menos uma aresta
        if (pt_t, pd_t, kt, kn) in MapDyHeu3:
            return MapDyHeu3[(pt_t, pd_t, kt, kn)]
        pfra = 1 - math.pow(1-pt_t, kt) * math.pow(1-pd_t, kn)
        MapDyHeu3[(pt_t, pd_t, kt, kn)] = pfra
        return pfra

def heu_search(neighbours, values, num_vertices, start, budgets, preheu):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, time_t =  [0]*max_budget, [0]*max_budget
    kt_values = [0]*num_vertices
    kn_values = [0]*num_vertices
    heu_values = {}
    status = [0]*num_vertices             # status 0 - desconhecido, status 1 - descoberto, status 2 - explorado
    positives = 0
    status[start] = 2
    i = 0
    while i < max_budget:
        if values[start]:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in neighbours[start]:
                if status[n] == 0:            # vertice desconhecido passa a descoberto
                    status[n] = 1
                if status[n] == 1:     # incrementa kt e calcula heuristica para descobertos
                    kt_values[n] += 1
                    heu_values[n] = preheu[(kt_values[n], kn_values[n])]
        else:                                       # constata que ele nao tem a caracteristica
            for n in neighbours[start]:
                if status[n] == 0:
                    status[n] = 1
                if status[n] == 1:
                    kn_values[n] += 1
                    heu_values[n] = preheu[(kt_values[n], kn_values[n])]
        start = max(heu_values, key=lambda i: heu_values[i])
        del heu_values[start]
        status[start] = 2
        positives_t[i] = positives
        time_t[i] = time.time() - start_time
        i += 1
    heu_positives = [positives_t[i-1] for i in budgets]
    heu_time = [time_t[i-1] for i in budgets]
    return heu_positives, heu_time

def dy_heu_search(neighbours, values, num_vertices, start, budgets, ini, mtype):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, time_t = [0]*max_budget, [0]*max_budget
    kt_values = [0]*num_vertices
    kn_values = [0]*num_vertices
    heu_values = {}
    status = [0]*num_vertices          # status 0 - desconhecido, status 1 - descoberto, status 2 - explorado
    positives = 0
    status[start] = 2
    # nt - num de arestas 't'-'t', nd - num de arestas 't'-'n', nn - num de arestas 'n'-'n'
    nt, nd, nn = ini, ini, ini
    pt_t = nt/float(nt+nd)                  # calculo dinamico de pt_t e pd_t
    pd_t = nd/float(nd+nn)
    i = 0
    while i < max_budget:
        if not i % 10:            # condicao de atualizacao de pt_t e pd_t
            pt_t = nt/float(nt+nn)                  # calculo dinamico de pt_t e pd_t
            pd_t = nd/float(nt+nd)
        value_start = values[start]
        if value_start:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in neighbours[start]:
                if status[n] == 0:            # vertice desconhecido passa a descoberto
                    status[n] = 1
                if status[n] == 1:     # incrementa kt e calcula heuristica para descobertos
                    kt_values[n] += 1
                    heu_values[n] = dyheuristic(pt_t, pd_t, kt_values[n], kn_values[n], mtype)
        else:                                       # constata que ele nao tem a caracteristica
            for n in neighbours[start]:
                if status[n] == 0:
                    status[n] = 1
                if status[n] == 1:
                    kn_values[n] += 1
                    heu_values[n] = dyheuristic(pt_t, pd_t, kt_values[n], kn_values[n], mtype)
        next_start = max(heu_values, key=lambda i: heu_values[i])
        del heu_values[next_start]
        status[next_start] = 2
        value_next_start = values[next_start]
        # dependendo do par de valores de vertice explorado e do prox vertice a ser explorado atualiza nt, nd ou nn
        if value_start != value_next_start:
            nd = nd + 1
        elif value_start and value_next_start:
            nt = nt + 1
        else:
            nn = nn + 1
        start = next_start         # prox vertice a ser explorado se torna o vertice da vez
        positives_t[i] = positives
        time_t[i] = time.time() - start_time
        i += 1
    heu_positives = [positives_t[i-1] for i in budgets]
    heu_time = [time_t[i-1] for i in budgets]
    return heu_positives, heu_time

def mod(neighbours, values, num_vertices, start, budgets):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, time_t = [0]*max_budget, [0]*max_budget

    ktv = dict.fromkeys(range(num_vertices), 1)
    kt_values = {}
    status = [0]*num_vertices           # status 0 - desconhecido, status 1 - descoberto, status 2 - explorado
    positives = 0
    status[start] = 2
    i = 0
    while i < max_budget:
        if values[start]:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in neighbours[start]:
                if status[n] == 0:
                    status[n] = 1
                    kt_values[n] = 0           # inicializa kt com 0 para os vertices descobertos
                if status[n] == 1:
                    kt_values[n] += 1
        else:                                       # constata que ele nao tem a caracteristica
            for n in neighbours[start]:
                if status[n] == 0:
                    status[n] = 1
                    kt_values[n] = 0
        start = max(kt_values, key=lambda i: kt_values[i])
        del kt_values[start]
        status[start] = 2
        positives_t[i] = positives
        time_t[i] = time.time() - start_time
        i += 1
    mod_positives = [positives_t[i-1] for i in budgets]
    mod_time = [time_t[i-1] for i in budgets]
    return mod_positives, mod_time