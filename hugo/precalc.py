#!/usr/bin/env python

'''
Esse modulo pre-calcula os valores das heu1, heu2 e heu3 para os params de
entrada pt_t, pd_t, ini e end
'''

import math
import scipy.special as sp
import sys

def p_t_k(k, kt, kn, pt_t, pd_t):
    ini = max(0, k-kn)
    end = min(kt, k)
    sum_k = 0
    for i in xrange(ini, end):
        sum_k += sp.binom(kt, i) * math.pow(pt_t, i) * math.pow(1-pt_t, kt-i) * sp.binom(kn, k-i) * math.pow(pd_t, k-i) \
        * math.pow(1-pd_t, kn-k+i)
    return sum_k

def heu1(pt_t, pd_t, ini, end, out_file):
    MapHeu1 = {}
    for kt in range(ini, end):
        for kn in range(ini, end):
            pfor = math.pow(pt_t, kt) * math.pow(pd_t, kn)
            MapHeu1[(kt, kn)] = pfor
    write_dict(MapHeu1, out_file)

def heu2(pt_t, pd_t, ini, end, out_file):
    MapHeu2 = {}
    for kt in range(ini, end):
        for kn in range(ini, end):
            pm = 0
            inis = int(math.ceil((kt+kn)/2.0))
            ends = kt+kn
            for i in xrange(inis, ends):
                pm += p_t_k(i, kt, kn, pt_t, pd_t)
            MapHeu2[(kt, kn)] = pm
    # write_dict(MapHeu2, out_file)
    wappend_dict(MapHeu2, out_file)

def heu3(pt_t, pd_t, ini, end, out_file):
    MapHeu3 = {}
    for kt in range(ini, end):
        for kn in range(ini, end):
            pfra = 1 - math.pow(1-pt_t, kt) * math.pow(1-pd_t, kn)
            MapHeu3[(kt, kn)] = pfra
    write_dict(MapHeu3, out_file)

def write_dict(mdict, out_file):
    with open(out_file, "wb") as f:
        for key, value in mdict.items():
            f.write("%s:%s\n" % (key, value))
    print "%s saved" % out_file

def wappend_dict(mdict, out_file):
    with open(out_file, "a") as f:
        for key, value in mdict.items():
            f.write("%s:%s\n" % (key, value))
    print "%s saved" % out_file

def main(pt_t, pd_t, ini, end, out_file):
    # heu1(pt_t, pd_t, ini, end+1, out_file+"_HEU1_pre")
    heu2(pt_t, pd_t, ini, end+1, out_file+"_HEU2_pre")        # 0 - 315 / cluster
    # heu3(pt_t, pd_t, ini, end+1, out_file+"_HEU3_pre")


if __name__ == "__main__":
    # sys.argv[1] corresponde ao valor de pt_t (prob de ser 't'-'t' dado que temos um 't')
    #
    # sys.argv[2] corresponde ao valor de pd_t (prob de ser 't'-'n' dado que temos um 'n')
    #
    # sys.argv[3] corresponde ao menor valor que kt ou kn pode assumir
    #
    # sys.argv[4] corresponde ao maior valor que kt ou kn pode assumir (ideologicamente o maior grau na rede)
    #
    # sys.argv[5] corresponde ao path onde o arquivo sera salvo
    #
    if len(sys.argv) != 6:
        print "err: missing params. the program need 5 params."
    else:
        main(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
        # precalc.py 0.00003175968038 0.966625463535 0 1254 "textgraphs/textgraphs_gcc_dblp_g"
        # precalc.py 0.000653964742925 0.943121351449 0 1254 "p2p/p2p_gcc_dblp_g"
        # precalc.py 0.0158277548439 0.846422940786 0 1254 "wcnc/wcnc_gcc_dblp_g"
        # precalc.py 0.150230752852 0.673388529313 0 1254 "group1/group1_gcc_dblp_g"
        # precalc.py 0.127930776191 0.697543572635 0 1254 "group2/group2_gcc_dblp_g"
        # precalc.py 0.000370557573471 0.964109380934 0 1254 "immerscom/immerscom_gcc_dblp_g"
        # precalc.py 0.000897882738423 0.943834338661 0 1254 "socialcom/socialcom_gcc_dblp_g"
        # precalc.py 0.0149804707989 0.858407026033 0 1254 "aaai/aaai_gcc_dblp_g"

        # precalc.py 0.5 0.5 0 1254 "textgraphs/textgraphs_gcc_dblp_g_fake"
        # precalc.py 0.5 0.5 0 1254 "p2p/p2p_gcc_dblp_g_fake"
        # precalc.py 0.5 0.5 0 1254 "wcnc/wcnc_gcc_dblp_g_fake"
        # precalc.py 0.5 0.5 0 1254 "group1/group1_gcc_dblp_g_fake"
        # precalc.py 0.5 0.5 0 1254 "group2/group2_gcc_dblp_g_fake"
        # precalc.py 0.5 0.5 0 1254 "immerscom/immerscom_gcc_dblp_g_fake"
        # precalc.py 0.5 0.5 0 1254 "socialcom/socialcom_gcc_dblp_g_fake"
        # precalc.py 0.5 0.5 0 1254 "aaai/aaai_gcc_dblp_g_fake"