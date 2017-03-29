#!/usr/bin/env python

'''
Esse modulo contem os tipos de busca sobre grafo (bfs, dfs, busca heuristica e mod)
'''

import graph_tool.all as gt
import props
import math
import scipy

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

def breadth_first_search(g, start, budget):
    visitor = BFSVisitorBudget(g.vp.value, budget)
    gt.bfs_search(g, start, visitor)
    return visitor.positive_count, visitor.visited

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

def depth_first_search(g, start, budget):
    visitor = DFSVisitorBudget(g.vp.value, budget)
    gt.dfs_search(g, start, visitor)
    return visitor.positive_count, visitor.visited

def p_t_k(k, kt, kn, pt_t, pd_t):
    ini = max(0, k-kn)
    end = min(kt, k)
    sum_k = 0
    for i in xrange(ini, end):
        sum_k += scipy.special.binom(kt, i) * math.pow(pt_t, i) * math.pow(1-pt_t, kt-i) * scipy.special.binom(kn, k-i) * math.pow(pd_t, k-i) * math.pow(1-pd_t, kn-k+i)
        # sum_k += math.pow(pt_t, i) * math.pow(1-pt_t, kt-i) * math.pow(pd_t, k-i) * math.pow(1-pd_t, kn-k+i)
    return sum_k

def heuristic(pt_t, pd_t, kt, kn, mtype):
    if mtype == 1:                  # ideia 1 - ocorrer em todas as arestas
        if (kt, kn) in MapHeu1:
            return MapHeu1[(kt, kn)]
        pfor = math.pow(pt_t, kt) * math.pow(pd_t, kn)
        MapHeu1[(kt,kn)] = pfor
        return pfor
    elif mtype == 2:                # ideia 2 - ocorrer na maioria das arestas
        if (kt, kn) in MapHeu2:
            return MapHeu2[(kt, kn)]
        pm = 0
        ini = int(math.ceil((kt+kn)/2.0))
        end = kt+kn
        for i in xrange(ini, end):
            pm += p_t_k(i, kt, kn, pt_t, pd_t)
        MapHeu2[(kt, kn)] = pm
        return pm
    elif mtype == 3:                # ideia 3 - ocorre em pelo menos uma aresta
        if (kt, kn) in MapHeu3:
            return MapHeu3[(kt, kn)]
        pfra = 1 - math.pow(1-pt_t, kt) * math.pow(1-pd_t, kn)
        MapHeu3[(kt,kn)] = pfra
        return pfra

def ot_heu_search(g, start, budget, pt_t, pd_t, mtype):
    for v in g.vertices():
        g.vp.kt[v] = 0
        g.vp.kn[v] = 0
    num_vertices = g.num_vertices()
    heu_values = [-1]*num_vertices
    status = [-1]*num_vertices          # status -1 - desconhecido, status 0 - descoberto, status +1 - explorado
    positives = 0
    status[int(start)] = 1
    i = 1
    while i < budget:
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
            return positives, i, i+status.count(0)
        status[start] = 1
        heu_values[start] = -10             # heuristica para vertice explorado recebe -10 para nunca mais ser escolhido
        start = g.vertex(start)
        i += 1
    return positives, i, i+status.count(0)

def mod(g, start, budget):
    num_vertices = g.num_vertices()
    status = [-1]*num_vertices          # status -1 - desconhecido, status 0 - descoberto, status +1 - explorado
    kt_values = [-1]*num_vertices
    positives = 0
    status[int(start)] = 1
    i = 1
    while i < budget:
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
            return positives, i, i+status.count(0)
        status[start] = 1
        kt_values[start] = -10
        start = g.vertex(start)         # prox vertice a ser explorado
        i += 1
    return positives, i, i+status.count(0)