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
            # print self.positives_t, self.explored_t, self.time_t

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
            # print self.positives_t, self.explored_t, self.time_t

def depth_first_search(g, start, budgets):
    visitor = DFSVisitorBudget(g.vp.value, budgets[-1], time.time())
    gt.dfs_search(g, start, visitor)
    dfs_positives = [visitor.positives_t[i-1] for i in budgets]
    dfs_time = [visitor.time_t[i-1] for i in budgets]
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

def ot_heu_search(g, start, budgets, pt_t, pd_t, mtype):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, eplusd_t, time_t = [0]*max_budget, [0]*max_budget, [0]*max_budget
    for v in g.vertices():
        g.vp.kt[v] = 0
        g.vp.kn[v] = 0
    num_vertices = g.num_vertices()
    hv = dict.fromkeys(range(num_vertices), 0)
    heu_values = heap.priority_dict(hv)
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
                if status[int(n)] == -1:            # vertice desconhecido passa a descoberto
                    status[int(n)] = 0
                if status[int(n)] == 0:     # incrementa kt e calcula heuristica para descobertos
                    g.vp.kt[n] += 1
                    heu_values[int(n)] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype) * -1
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                if status[int(n)] == -1:
                    status[int(n)] = 0
                if status[int(n)] == 0:
                    g.vp.kn[n] += 1
                    heu_values[int(n)] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype) * -1
        # print "heu_values", heu_values
        start = heu_values.pop_smallest()
        # print "status 1 -", status.count(1)
        # print "status 0 -", status.count(0)
        # print "status -1 -", status.count(-1)
        status[start] = 1
        start = g.vertex(start)         # prox vertice a ser explorado
        positives_t[i] = positives
        eplusd_t[i] = i+1+status.count(0)
        time_t[i] = time.time() - start_time
        # print "i", i
        i += 1
    heu_positives = [positives_t[i-1] for i in budgets]
    heu_eplusd = [eplusd_t[i-1] for i in budgets]
    heu_time = [time_t[i-1] for i in budgets]
    return heu_positives, heu_eplusd, heu_time

def mod(g, start, budgets):
    max_budget = budgets[-1]
    start_time = time.time()
    positives_t, eplusd_t, time_t = [0]*max_budget, [0]*max_budget, [0]*max_budget

    num_vertices = g.num_vertices()
    ktv = dict.fromkeys(range(num_vertices), 1)
    kt_values = heap.priority_dict(ktv)
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
                if status[int(n)] == -1:
                    status[int(n)] = 0
                    kt_values[int(n)] = 0           # inicializa kt com 0 para os vertices descobertos
                if status[int(n)] == 0:
                    kt_values[int(n)] -= 1
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                if status[int(n)] == -1:
                    status[int(n)] = 0
                    kt_values[int(n)] = 0
       # print "kt_values", kt_values
        start = kt_values.pop_smallest()
        # print "status 1 -", status.count(1)
        # print "status 0 -", status.count(0)
        # print "status -1 -", status.count(-1)
        status[start] = 1
        start = g.vertex(start)         # prox vertice a ser explorado
        positives_t[i] = positives
        eplusd_t[i] = i+1+status.count(0)
        time_t[i] = time.time() - start_time
        # print "i", i
        i += 1
    mod_positives = [positives_t[i-1] for i in budgets]
    mod_eplusd = [eplusd_t[i-1] for i in budgets]
    mod_time = [time_t[i-1] for i in budgets]
    return mod_positives, mod_eplusd, mod_time