#!/usr/bin/env python

'''
Esse modulo contem os tipos de busca sobre grafo (bfs e busca heuristica)
'''

import graph_tool.all as gt
import props

class VisitorBudget(gt.BFSVisitor):

    def __init__(self, name, feat, budget):
        self.name = name
        self.feat = feat
        self.budget = budget
        self.visited = []
        self.positive_count = 0

    # def discover_vertex(self, u):
        # print "-->", self.name[u], "has been discovered!"

    def examine_vertex(self, u):
        if len(self.visited) < self.budget:         # TODO: pode ser otimizado se a bfs parar quando atingir orcamento
            self.visited.append(u)
            if self.feat[u] == 1:
                self.positive_count += 1
        # print self.name[u], "has been examined..."

def breadth_first_search(g, start, budget):
    visitor = VisitorBudget(g.vp.name, g.vp.feat, budget)
    gt.bfs_search(g, start, visitor)
    return visitor.positive_count, visitor.visited

def heuristic(g, v, pt, pd, pn):
    nt = g.vp.numt[v]
    nn = g.vp.numn[v]
    return 1 - (1-pt)**nt * (1-pd)**nn

def heu_search(g, start, budget, pt, pd, pn):
    positives = 0
    explored = []
    discovered = list(g.vertices())                 # err: 'discovered' nao devia conter todos os vertices do grafo
    explored.append(start)                           # e sim apenas os vertices descobertos
    discovered.remove(start)
    i = 1
    while i < budget:
        # print "start", g.vp.name[start]
        if g.vp.feat[start] == 1:
            positives = positives + 1
            for n in start.out_neighbours():
                g.vp.numt[n] = g.vp.numt[n] + 1
                g.vp.rank[n] = heuristic(g, n, pt, pd, pn)
        else:
            for n in start.out_neighbours():
                g.vp.numn[n] = g.vp.numn[n] + 1
                g.vp.rank[n] = heuristic(g, n, pt, pd, pn)
        discovered = sorted(discovered, key=lambda n: g.vp.rank[n])
        # print "discovered", props.get_v_names_ranks(g, discovered)
        start = discovered.pop()                # err: 'start' pode ser um vertice nao descoberto ainda
        explored.append(start)
        i = i + 1
    return positives, explored
