#!/usr/bin/env python

'''
Esse modulo contem os tipos de busca sobre grafo (bfs e busca heuristica)
'''

import graph_tool.all as gt
import props
import math

class BFSVisitorBudget(gt.BFSVisitor):

    def __init__(self, value, budget):
        self.value = value
        self.budget = budget
        self.visited = []
        self.positive_count = 0

    def examine_vertex(self, u):
        if len(self.visited) < self.budget:         # TODO: pode ser otimizado se a bfs parar quando atingir budget
            self.visited.append(u)
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
        self.visited = []
        self.positive_count = 0

    def discover_vertex(self, u):
        if len(self.visited) < self.budget:         # TODO: pode ser otimizado se a dfs parar quando atingir budget
            self.visited.append(u)
            if int(self.value[u]) == 1:
                self.positive_count += 1

def depth_first_search(g, start, budget):
    visitor = DFSVisitorBudget(g.vp.value, budget)
    gt.dfs_search(g, start, visitor)
    return visitor.positive_count, visitor.visited

def binom(x, y):
    try:
        binom = math.factorial(x) // math.factorial(y) // math.factorial(x - y)
    except ValueError:
        binom = 0
    return binom

def p_t_k(k, kt, kn, pt_t, pd_t):
    ini = max(0, k-kn)
    end = min(kt, k)
    sum_k = 0
    for i in range(ini, end):
        # sum_k += binom(kt, i) * pt_t**i * (1-pt_t)**(kt-i) * binom(kn, k-i) * pd_t**(k-i) * (1-pd_t)**(kn-k+i)
        sum_k += pt_t**i * (1-pt_t)**(kt-i) * pd_t**(k-i) * (1-pd_t)**(kn-k+i)
    return sum_k

def heuristic(pt_t, pd_t, kt, kn, mtype):
    if mtype == 1:                  # ideia 1 - ocorrer em todas as arestas
        return pt_t**kt * pd_t**kn
    elif mtype == 2:                # ideia 2 - ocorrer na maioria das arestas
        pm = 0
        ini = int(math.ceil((kt+kn)/2.0))
        end = kt+kn
        for i in range(ini, end):
            pm += p_t_k(i, kt, kn, pt_t, pd_t)
        return pm
    elif mtype == 3:                # ideia 3 - ocorre em pelo menos uma aresta
        return 1 - (1-pt_t)**kt * (1-pd_t)**kn

def get_max_rank(g, l):
    max_n = l[0]
    for n in l:
        if g.vp.rank[max_n] < g.vp.rank[n]:
            max_n = n
    return max_n

def ot_heu_search(g, start, budget, pt_t, pd_t, mtype):
    positives = 0
    explored, discovered = [], []
    explored.append(start)
    i = 1
    while i < budget:
        if int(g.vp.value[start]) == 1:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in start.out_neighbours():
                if n not in discovered:
                    discovered.append(n)            # adiciona os vertices vizinhos ao explorado a lista de descobertos
                g.vp.kt[n] += 1
                g.vp.rank[n] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype)
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                if n not in discovered:
                    discovered.append(n)
                g.vp.kn[n] += 1
                g.vp.rank[n] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype)
        if not discovered:
            print "not discovered"
            return positives, explored
        else:
            start = get_max_rank(g, discovered)
            discovered.remove(start)
            explored.append(start)              # prox vertice a ser explorado
        i += 1
    return positives, explored

def heu_search(g, start, budget, pt_t, pd_t, mtype):
    positives = 0
    explored = []
    discovered = list(g.vertices())                 # err: 'discovered' nao devia conter todos os vertices do grafo
    explored.append(start)                           # e sim apenas os vertices descobertos
    discovered.remove(start)
    i = 1
    while i < budget:
        # print "start", g.vp.name[start]           # egonets - facebook, gplus, twitter
        # print "start", g.vp.label[start]              # polblogs, polbooks
        if int(g.vp.value[start]) == 1:
            positives += 1
            for n in start.out_neighbours():
                g.vp.kt[n] += 1
                g.vp.rank[n] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype)
        else:
            for n in start.out_neighbours():
                g.vp.kn[n] += 1
                g.vp.rank[n] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype)
        # discovered = sorted(discovered, key=lambda n: g.vp.rank[n])
        # start = discovered.pop()                # err: 'start' pode ser um vertice nao descoberto ainda
        start = get_max_rank(g, discovered)
        discovered.remove(start)
        explored.append(start)              # prox vertice a ser explorado
        i += 1
    return positives, explored

def pure_heu_search(g, start, budget, pt_t, pd_t, mtype):
    positives = 0
    explored = []
    discovered = list(g.vertices())                 # err: 'discovered' nao devia conter todos os vertices do grafo
    explored.append(start)                           # e sim apenas os vertices descobertos
    discovered.remove(start)
    i = 1
    while i < budget:
        # print "start", g.vp.name[start]           # egonets - facebook, gplus, twitter
        # print "start", g.vp.label[start]              # polblogs, polbooks
        for n in start.out_neighbours():
            if int(g.vp.value[start]) == 1:
                g.vp.kt[n] += 1
            else:
                g.vp.kn[n] += 1
            g.vp.rank[n] = heuristic(pt_t, pd_t, g.vp.kt[n], g.vp.kn[n], mtype)
        discovered = sorted(discovered, key=lambda n: g.vp.rank[n])
        # print "discovered", props.get_v_names_ranks(g, discovered)            # egonets - facebook, gplus, twitter
        # print "discovered", props.get_v_labels_ranks(g, discovered)               # polblogs, polbooks
        start = discovered.pop()                # err: 'start' pode ser um vertice nao descoberto ainda
        explored.append(start)              # prox vertice a ser explorado
        i += 1
    return positives, explored

def get_max_kt(g, l):
    max_n = l[0]
    for n in l:
        if g.vp.kt[max_n] < g.vp.kt[n]:
            max_n = n
    return max_n

def mod(g, start, budget):
    positives = 0
    explored, discovered = [], []
    explored.append(start)
    i = 1
    while i < budget:
        if int(g.vp.value[start]) == 1:          # ao explorar o vertice constata que ele tem a caracteristica
            positives += 1
            for n in start.out_neighbours():
                if n not in discovered:
                    discovered.append(n)            # adiciona os vertices vizinhos ao explorado a lista de descobertos
                g.vp.kt[n] += 1
        else:                                       # constata que ele nao tem a caracteristica
            for n in start.out_neighbours():
                if n not in discovered:
                    discovered.append(n)
        if not discovered:
            print "not discovered"
            return positives, explored
        else:
            start = get_max_kt(g, discovered)
            discovered.remove(start)
            explored.append(start)              # prox vertice a ser explorado
        i += 1
    return positives, explored