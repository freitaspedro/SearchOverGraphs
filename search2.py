#!/usr/bin/env python

'''
Esse modulo contem os tipos de busca sobre grafo (bfs, dfs, busca heuristica e mod)
'''

import graph_tool.all as gt
import props
import math
import scipy
import time
import heap

MapHeu1 = {}
MapHeu2 = {}
MapHeu3 = {}

class BFSVisitorBudget(gt.BFSVisitor):

    def __init__(self, value, max_budget, start_time):
        self.value = value
        self.max_budget = max_budget
        self.start_time = start_time
        self.explored = 0
        self.positives = 0

        self.positives_t = [0]*max_budget
        self.time_t = [0]*max_budget

    def examine_vertex(self, u):
        if self.explored < self.max_budget:
            if int(self.value[u]) == 1:
                self.positives += 1
            self.positives_t[self.explored] = self.positives
            self.time_t[self.explored] = time.time() - self.start_time
            self.explored += 1
            # print self.positives_t, self.time_t

def breadth_first_search(g, start, budgets):
    visitor = BFSVisitorBudget(g.vp.value, budgets[-1], time.time())
    gt.bfs_search(g, start, visitor)
    bfs_positives = [visitor.positives_t[i-1] for i in budgets]
    bfs_time = [visitor.time_t[i-1] for i in budgets]
    return bfs_positives, bfs_time

class DFSVisitorBudget(gt.DFSVisitor):

    def __init__(self, value, max_budget, start_time):
        self.value = value
        self.max_budget = max_budget
        self.start_time = start_time
        self.explored = 0
        self.positives = 0

        self.positives_t = [0]*max_budget
        self.time_t = [0]*max_budget

    def discover_vertex(self, u):
        if self.explored < self.max_budget:
            if int(self.value[u]) == 1:
                self.positives += 1
            self.positives_t[self.explored] = self.positives
            self.time_t[self.explored] = time.time() - self.start_time
            self.explored += 1
            # print self.positives_t, self.time_t

def depth_first_search(g, start, budgets):
    visitor = DFSVisitorBudget(g.vp.value, budgets[-1], time.time())
    gt.dfs_search(g, start, visitor)
    dfs_positives = [visitor.positives_t[i-1] for i in budgets]
    dfs_time = [visitor.time_t[i-1] for i in budgets]
    return dfs_positives, dfs_time

def breadth_first_search2(g, start, budgets, num_vertices):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, time_t = [0]*max_budget, [0]*max_budget
    status = [0]*num_vertices          # status 0 - desconhecido, status 1 - explorado
    positives = 0
    queue = [start]
    i = 0
    while queue and  i < max_budget:
        start = queue.pop(0)        # retira da fila o vertice mais antigo
        if status[int(start)] == 0:
            if int(g.vp.value[start]) == 1:
                positives += 1
            for n in start.out_neighbours():
                if status[int(n)] == 0:
                    queue.append(n)      # poe na fila os vizinhos desconhecidos do vertice explorado
            status[int(start)] = 1
            positives_t[i] = positives
            time_t[i] = time.time() - start_time
            # print "i", i
            i += 1
    bfs_positives = [positives_t[i-1] for i in budgets]
    bfs_time = [time_t[i-1] for i in budgets]
    return bfs_positives, bfs_time

def depth_first_search2(g, start, budgets, num_vertices):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, time_t = [0]*max_budget, [0]*max_budget
    status = [0]*num_vertices          # status 0 - desconhecido, status 1 - explorado
    positives = 0
    stack = [start]
    i = 0
    while stack and  i < max_budget:
        start = stack.pop()        # retira da pilha o vertice mais recente
        if status[int(start)] == 0:
            if int(g.vp.value[start]) == 1:
                positives += 1
            for n in start.out_neighbours():
                if status[int(n)] == 0:
                    stack.append(n)      # poe na fila os vizinhos desconhecidos do vertice explorado
            status[int(start)] = 1
            positives_t[i] = positives
            time_t[i] = time.time() - start_time
            # print "i", i
            i += 1
    dfs_positives = [positives_t[i-1] for i in budgets]
    dfs_time = [time_t[i-1] for i in budgets]
    return dfs_positives, dfs_time

def p_t_k(k, kt, kn, pt_t, pd_t):
    ini = max(0, k-kn)
    end = min(kt, k)
    sum_k = 0
    for i in xrange(ini, end):
        sum_k += scipy.special.binom(kt, i) * math.pow(pt_t, i) * math.pow(1-pt_t, kt-i) * scipy.special.binom(kn, k-i) * math.pow(pd_t, k-i) \
        * math.pow(1-pd_t, kn-k+i)
    return sum_k

def heuristic(pt_t, pd_t, kt, kn, mtype):
    if mtype == 1:                  # ideia 1 - ocorrer em todas as arestas
        if (pt_t, pd_t, kt, kn) in MapHeu1:
            return MapHeu1[(pt_t, pd_t, kt, kn)]
        pfor = math.pow(pt_t, kt) * math.pow(pd_t, kn)
        MapHeu1[(pt_t, pd_t, kt, kn)] = pfor
        return pfor
    elif mtype == 2:                # ideia 2 - ocorrer na maioria das arestas
        if (pt_t, pd_t, kt, kn) in MapHeu2:
            return MapHeu2[(pt_t, pd_t, kt, kn)]
        pm = 0
        ini = int(math.ceil((kt+kn)/2.0))
        end = kt+kn
        for i in xrange(ini, end):
            pm += p_t_k(i, kt, kn, pt_t, pd_t)
        MapHeu2[(pt_t, pd_t, kt, kn)] = pm
        return pm
    elif mtype == 3:                # ideia 3 - ocorre em pelo menos uma aresta
        if (pt_t, pd_t, kt, kn) in MapHeu3:
            return MapHeu3[(pt_t, pd_t, kt, kn)]
        pfra = 1 - math.pow(1-pt_t, kt) * math.pow(1-pd_t, kn)
        MapHeu3[(pt_t, pd_t, kt, kn)] = pfra
        return pfra

def ot_heu_search(g, num_vertices, start, budgets, pt_t, pd_t, mtype):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, eplusd_t, time_t = [0]*max_budget, [0]*max_budget, [0]*max_budget
    kt_values = [0]*num_vertices
    kn_values = [0]*num_vertices
    heu_values = {}
    status = [-1]*num_vertices          # status -1 - desconhecido, status 0 - descoberto, status +1 - explorado
    positives = 0
    status[int(start)] = 1
    i = 0
    # print "max_budget", max_budget
    while i < max_budget:
        # print "start", start
        # neighbours = [int(n) for n in start.out_neighbours()]
        # print "neighbours", neighbours
        if int(g.vp.value[start]) == 1:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in start.out_neighbours():
                index = int(n)
                if status[index] == -1:            # vertice desconhecido passa a descoberto
                    status[index] = 0
                if status[index] == 0:     # incrementa kt e calcula heuristica para descobertos
                    kt_values[index] += 1
                    heu_values[index] = heuristic(pt_t, pd_t, kt_values[index], kn_values[index], mtype)
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                index = int(n)
                if status[index] == -1:
                    status[index] = 0
                if status[index] == 0:
                    kn_values[index] += 1
                    heu_values[index] = heuristic(pt_t, pd_t, kt_values[index], kn_values[index], mtype)
        # print "heu_values", heu_values
        start = max(heu_values, key=lambda i: heu_values[i])
        del heu_values[start]
        # print "status 1 -", status.count(1)
        # print "status 0 -", status.count(0)
        # print "status -1 -", status.count(-1)
        status[start] = 1
        start = g.vertex(start)         # prox vertice a ser explorado
        positives_t[i] = positives
        # eplusd_t[i] = i+1+status.count(0)
        eplusd_t[i] = i+1
        time_t[i] = time.time() - start_time
        # print "i", i
        i += 1
    heu_positives = [positives_t[i-1] for i in budgets]
    heu_eplusd = [eplusd_t[i-1] for i in budgets]
    heu_time = [time_t[i-1] for i in budgets]
    return heu_positives, heu_eplusd, heu_time

def dy_heu_search(g, num_vertices, start, budgets, ini, mtype):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, eplusd_t, time_t = [0]*max_budget, [0]*max_budget, [0]*max_budget
    kt_values = [0]*num_vertices
    kn_values = [0]*num_vertices
    heu_values = {}
    status = [-1]*num_vertices          # status -1 - desconhecido, status 0 - descoberto, status +1 - explorado
    positives = 0
    status[int(start)] = 1
    nt, nd, nn = ini, ini, ini                      # nt - num de arestas 't'-'t', nd - num de arestas 't'-'n', nn - num de arestas 'n'-'n'
    i = 0
    # print "max_budget", max_budget
    while i < max_budget:
        if not i % 100:            # condicao de atualizacao de pt_t e pd_t
            pt_t = nt/float(nt+nd)                  # calculo dinamico de pt_t e pd_t
            pd_t = nd/float(nd+nn)
        # print "pt_t", pt_t
        # print "pd_t", pd_t
        # print "start", start
        # neighbours = [int(n) for n in start.out_neighbours()]
        # print "neighbours", neighbours
        value_start = int(g.vp.value[start])
        if value_start == 1:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in start.out_neighbours():
                index = int(n)
                if status[index] == -1:            # vertice desconhecido passa a descoberto
                    status[index] = 0
                if status[index] == 0:     # incrementa kt e calcula heuristica para descobertos
                    kt_values[index] += 1
                    heu_values[index] = heuristic(pt_t, pd_t, kt_values[index], kn_values[index], mtype)
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                index = int(n)
                if status[index] == -1:
                    status[index] = 0
                if status[index] == 0:
                    kn_values[index] += 1
                    heu_values[index] = heuristic(pt_t, pd_t, kt_values[index], kn_values[index], mtype)
        # print "heu_values", heu_values
        next_start = max(heu_values, key=lambda i: heu_values[i])
        del heu_values[next_start]
        # print "status 1 -", status.count(1)
        # print "status 0 -", status.count(0)
        # print "status -1 -", status.count(-1)
        status[next_start] = 1
        next_start = g.vertex(next_start)         # prox vertice a ser explorado
        value_next_start = int(g.vp.value[next_start])
        # dependendo do par de valores de vertice explorado e do prox vertice a ser explorado atualiza nt, nd ou nn
        # print "value_start", value_start
        # print "value_next_start", value_next_start
        if value_start != value_next_start:
            nd = nd + 1
        elif value_start == 0 and value_next_start == 0:
            nn = nn + 1
        else:
            nt = nt + 1
        # print "nt", nt
        # print "nd", nd
        # print "nn", nn
        start = next_start         # prox vertice a ser explorado se torna o vertice da vez
        positives_t[i] = positives
        # eplusd_t[i] = i+1+status.count(0)
        eplusd_t[i] = i+1
        time_t[i] = time.time() - start_time
        # print "i", i
        i += 1
    heu_positives = [positives_t[i-1] for i in budgets]
    heu_eplusd = [eplusd_t[i-1] for i in budgets]
    heu_time = [time_t[i-1] for i in budgets]
    return heu_positives, heu_eplusd, heu_time

def mod(g, num_vertices, start, budgets):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, eplusd_t, time_t = [0]*max_budget, [0]*max_budget, [0]*max_budget

    ktv = dict.fromkeys(range(num_vertices), 1)
    kt_values = {}
    status = [-1]*num_vertices          # status -1 - desconhecido, status 0 - descoberto, status +1 - explorado
    positives = 0
    status[int(start)] = 1
    i = 0
    while i < max_budget:
        # print "start", start
        # neighbours = [int(n) for n in start.out_neighbours()]
        # print "neighbours", len(neighbours)
        if int(g.vp.value[start]) == 1:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in start.out_neighbours():
                index = int(n)
                if status[index] == -1:
                    status[index] = 0
                    kt_values[index] = 0           # inicializa kt com 0 para os vertices descobertos
                if status[index] == 0:
                    kt_values[index] += 1
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                index = int(n)
                if status[index] == -1:
                    status[index] = 0
                    kt_values[index] = 0
        # print "kt_values", kt_values
        start = max(kt_values, key=lambda i: kt_values[i])
        del kt_values[start]
        # print "status 1 -", status.count(1)
        # print "status 0 -", status.count(0)
        # print "status -1 -", status.count(-1)
        status[start] = 1
        start = g.vertex(start)         # prox vertice a ser explorado
        positives_t[i] = positives
        # eplusd_t[i] = i+1+status.count(0)
        eplusd_t[i] = i+1
        time_t[i] = time.time() - start_time
        # print "i", i
        i += 1
    mod_positives = [positives_t[i-1] for i in budgets]
    mod_eplusd = [eplusd_t[i-1] for i in budgets]
    mod_time = [time_t[i-1] for i in budgets]
    return mod_positives, mod_eplusd, mod_time