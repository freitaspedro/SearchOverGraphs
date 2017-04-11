#!/usr/bin/env python

'''
Esse modulo contem os tipos de busca sobre grafo (bfs, dfs, busca heuristica e mod)
'''

import graph_tool.all as gt
import props
import math
import scipy
import time

MapHeu1 ={}
MapHeu2 ={}
MapHeu3 = {}

class BFSVisitorBudget(gt.BFSVisitor):

    def __init__(self, value, budget):
        self.value = value
        self.budget = budget
        self.visited = 0
        self.positive_count = 0

    def examine_vertex(self, u):
        if self.visited < self.budget:
            self.visited += 1
            if int(self.value[u]) == 1:
                self.positive_count += 1

def breadth_first_search(g, start, budgets):
    bfs_positives = [0]*len(budgets)
    bfs_explored = [0]*len(budgets)
    bfs_time = [0]*len(budgets)
    for i in range(0, len(budgets)):
        start_time = time.time()
        visitor = BFSVisitorBudget(g.vp.value, budgets[i])
        gt.bfs_search(g, start, visitor)
        bfs_positives[i] = visitor.positive_count
        bfs_explored[i] = visitor.visited
        bfs_time[i] = time.time() - start_time
    return bfs_positives, bfs_explored, bfs_time

class DFSVisitorBudget(gt.DFSVisitor):

    def __init__(self, value, budget):
        self.value = value
        self.budget = budget
        self.visited = 0
        self.positive_count = 0

    def discover_vertex(self, u):
        if self.visited < self.budget:
            self.visited += 1
            if int(self.value[u]) == 1:
                self.positive_count += 1

def depth_first_search(g, start, budgets):
    dfs_positives = [0]*len(budgets)
    dfs_explored = [0]*len(budgets)
    dfs_time = [0]*len(budgets)
    for i in range(0, len(budgets)):
        start_time = time.time()
        visitor = DFSVisitorBudget(g.vp.value, budgets[i])
        gt.dfs_search(g, start, visitor)
        dfs_positives[i] = visitor.positive_count
        dfs_explored[i] = visitor.visited
        dfs_time[i] = time.time() - start_time
    return dfs_positives, dfs_explored, dfs_time

def p_t_k(k, kt, kn, pt_t, pd_t):
    ini = max(0, k-kn)
    end = min(kt, k)
    sum_k = 0
    for i in xrange(ini, end):
        sum_k += scipy.special.binom(kt, i) * math.pow(pt_t, i) * math.pow(1-pt_t, kt-i) * scipy.special.binom(kn, k-i) * math.pow(pd_t, k-i) * math.pow(1-pd_t, kn-k+i)
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

def ot_heu_search(g, start, budgets, pt_t, pd_t, mtype):
    start_time = time.time()
    heu_positives = [0]*len(budgets)
    heu_explored = [0]*len(budgets)
    heu_eplusd = [0]*len(budgets)
    heu_time = [0]*len(budgets)
    for v in g.vertices():
        g.vp.kt[v] = 0
        g.vp.kn[v] = 0
    num_vertices = g.num_vertices()
    heu_values = [-1]*num_vertices
    status = [-1]*num_vertices          # status -1 - desconhecido, status 0 - descoberto, status +1 - explorado
    positives = 0
    status[int(start)] = 1
    i = 1
    count = 0
    # print "max_budget", budgets[-1]
    while i <= budgets[-1]:
        # print "start", start
        # neighbours = [int(n) for n in start.out_neighbours()]
        # print "neighbours", len(neighbours)
        if int(g.vp.value[start]) == 1:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in start.out_neighbours():
                if status[int(n)] == -1:            # vertice desconhecido passa a descoberto
                    status[int(n)] = 0
                if status[int(n)] == 0:     # incrementa kt e calcula heuristica para descobertos
                    g.vp.kt[n] += 1
                    heu_values[int(n)] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype)
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                if status[int(n)] == -1:
                    status[int(n)] = 0
                if status[int(n)] == 0:
                    g.vp.kn[n] += 1
                    heu_values[int(n)] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype)
        # print "heu_values", heu_values
        max_heu = max(heu_values)
        start = heu_values.index(max_heu)
        # print "max %s (index %s)" % (heu_values[start], start)
        # print "status 1 -", status.count(1)
        # print "status 0 -", status.count(0)
        # print "status -1 -", status.count(-1)
        if max_heu < 0:                     # heuristica escolhida nunca pode ser negativa
            print "err: max_heu negative"
            return heu_positives, heu_explored, heu_eplusd, heu_time
        status[start] = 1
        heu_values[start] = -10             # heuristica para vertice explorado recebe -10 para nunca mais ser escolhido
        start = g.vertex(start)
        if i == budgets[count]:
            heu_positives[count] = positives
            heu_explored[count] = i
            heu_eplusd[count] = i+status.count(0)
            heu_time[count] = time.time() - start_time
            count += 1
            # print "i", i
        i += 1
    return heu_positives, heu_explored, heu_eplusd, heu_time

def mod(g, start, budgets):
    start_time = time.time()
    mod_positives = [0]*len(budgets)
    mod_explored = [0]*len(budgets)
    mod_eplusd = [0]*len(budgets)
    mod_time = [0]*len(budgets)
    num_vertices = g.num_vertices()
    status = [-1]*num_vertices          # status -1 - desconhecido, status 0 - descoberto, status +1 - explorado
    kt_values = [-1]*num_vertices
    positives = 0
    status[int(start)] = 1
    i = 1
    count = 0
    while i <= budgets[-1]:
        # print "start", start
        # neighbours = [int(n) for n in start.out_neighbours()]
        # print "neighbours", len(neighbours)
        if int(g.vp.value[start]) == 1:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in start.out_neighbours():
                if status[int(n)] == -1:
                    status[int(n)] = 0
                    kt_values[int(n)] = 0           # inicializa kt com 0 para os vertices descobertos
                if status[int(n)] == 0:
                    kt_values[int(n)] += 1
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                if status[int(n)] == -1:
                    status[int(n)] = 0
                    kt_values[int(n)] = 0
       # print "kt_values", kt_values
        max_kt = max(kt_values)
        start = kt_values.index(max_kt)
        # print "max %s (index %s)" % (kt_values[start], start)
        # print "status 1 -", status.count(1)
        # print "status 0 -", status.count(0)
        # print "status -1 -", status.count(-1)
        if max_kt < 0:
            print "err: max_kt negative"
            return mod_positives, mod_explored, mod_eplusd, mod_time
        status[start] = 1
        kt_values[start] = -10
        start = g.vertex(start)         # prox vertice a ser explorado
        if i == budgets[count]:
            mod_positives[count] = positives
            mod_explored[count] = i
            mod_eplusd[count] = i+status.count(0)
            mod_time[count] = time.time() - start_time
            count += 1
            # print "i", i
        i += 1
    return mod_positives, mod_explored, mod_eplusd, mod_time