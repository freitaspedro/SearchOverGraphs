#!/usr/bin/env python

'''
Esse modulo contem os tipos de busca sobre grafo (bfs, dfs, busca heuristica e mod) sem o uso
do graph-tool
'''

import math
import scipy
import time

MapHeu1 = {}
MapHeu2 = {}
MapHeu3 = {}

def breadth_first_search(neighbours, values, start, budgets):
    # TODO
    # return bfs_positives, bfs_time
    return -1

def depth_first_search(neighbours, values, start, budgets):
     # TODO
    # return dfs_positives, dfs_time
    return -1

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

def heu_search(neighbours, values, num_vertices, start, budgets, pt_t, pd_t, mtype):
    # TODO
    # return heu_positives, heu_time
    return -1

def dy_heu_search(neighbours, values, num_vertices, start, budgets, pt_t, pd_t, mtype):
    # TODO
    # return heu_positives, heu_time
    return -1

def mod(neighbours, values, num_vertices, start, budgets):
    # TODO
    # return mod_positives, mod_time
    return -1