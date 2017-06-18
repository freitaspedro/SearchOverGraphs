#!/usr/bin/env python

'''
Esse modulo plota o grafico orcamento x vertices positivos para todas as buscas menos as fakeheu e dyheu
'''

import matplotlib.pyplot as plt
import numpy as np
import sys

def main(file_bfs, file_dfs, file_heu1, file_heu2, file_heu3, file_mods, exit_file):
    budget, time, bfs_positives_mean, bfs_positives_stdev = np.loadtxt(file_bfs, delimiter=",", unpack=True)
    dfsb, dfst, dfs_positives_mean, dfs_positives_stdev = np.loadtxt(file_dfs, delimiter=",", unpack=True)
    heu1b, heu1t, heu1_positives_mean, heu1_positives_stdev = np.loadtxt(file_heu1, delimiter=",", unpack=True)
    # heu2b, heu2t, heu2_positives_mean, heu2_positives_stdev = np.loadtxt(file_heu2, delimiter=",", unpack=True)
    heu3b, heu3t, heu3_positives_mean, heu3_positives_stdev = np.loadtxt(file_heu3, delimiter=",", unpack=True)
    modb, modt, mods_positives_mean, mods_positives_stdev = np.loadtxt(file_mods, delimiter=",", unpack=True)

    budget = np.insert(budget, 0, 0)
    bfs_positives_mean = np.insert(bfs_positives_mean, 0, 0)
    bfs_positives_stdev = np.insert(bfs_positives_stdev, 0, 0)
    dfs_positives_mean = np.insert(dfs_positives_mean, 0, 0)
    dfs_positives_stdev = np.insert(dfs_positives_stdev, 0, 0)
    heu1_positives_mean = np.insert(heu1_positives_mean, 0, 0)
    heu1_positives_stdev = np.insert(heu1_positives_stdev, 0, 0)
    # heu2_positives_mean = np.insert(heu2_positives_mean, 0, 0)
    # heu2_positives_stdev = np.insert(heu2_positives_stdev, 0, 0)
    heu3_positives_mean = np.insert(heu3_positives_mean, 0, 0)
    heu3_positives_stdev = np.insert(heu3_positives_stdev, 0, 0)
    mods_positives_mean = np.insert(mods_positives_mean, 0, 0)
    mods_positives_stdev = np.insert(mods_positives_stdev, 0, 0)

    bfs_line = plt.plot(budget, bfs_positives_mean, marker="o", markersize=4, markeredgewidth=1, markeredgecolor="b",
        markerfacecolor="None", color="b", label="BFS")
    dfs_line = plt.plot(budget, dfs_positives_mean, marker="s", markersize=4, markeredgewidth=1, markeredgecolor="g",
        markerfacecolor="None", color="g", label="DFS")
    heu1_line = plt.plot(budget, heu1_positives_mean, marker="^", markersize=4, markeredgewidth=1, markeredgecolor="r",
        markerfacecolor="None", color="r", label="Heu1")
    # heu2_line = plt.plot(budget, heu2_positives_mean, marker="p", markersize=4, markeredgewidth=1, markeredgecolor="c",
    #     markerfacecolor="None", color="c", label="Heu2")
    heu3_line = plt.plot(budget, heu3_positives_mean, marker="v", markersize=4, markeredgewidth=1, markeredgecolor="m",
        markerfacecolor="None", color="m", label="Heu3")
    mods_line = plt.plot(budget, mods_positives_mean, marker="D", markersize=4, markeredgewidth=1, markeredgecolor="k",
        markerfacecolor="None", color="k", label="MOD*")

    # plt.errorbar(budget, bfs_positives_mean, yerr=bfs_positives_stdev, color="b")
    # plt.errorbar(budget, dfs_positives_mean, yerr=dfs_positives_stdev, color="g")
    # plt.errorbar(budget, heu1_positives_mean, yerr=heu1_positives_stdev, color="r")
    # plt.errorbar(budget, heu2_positives_mean, yerr=heu2_positives_stdev, color="c")
    # plt.errorbar(budget, heu3_positives_mean, yerr=heu3_positives_stdev, color="m")
    # plt.errorbar(budget, mods_positives_mean, yerr=mods_positives_stdev, color="k")

    heu2_positives_mean = [0]
    plt.xticks(np.arange(100, max(budget)+201.0, 200.0), fontsize = 9)
    plt.yticks(np.arange(0, max([max(bfs_positives_mean), max(dfs_positives_mean),  max(heu1_positives_mean), max(heu2_positives_mean),
        max(heu3_positives_mean), max(mods_positives_mean)])+0.0, 1.0), fontsize = 9)

    # plt.grid(True)

    plt.ylabel("vertices positivos", fontsize=9)
    plt.xlabel("vertices explorados", fontsize=9)

    plt.legend(loc="upper left", fontsize=11)

    plt.savefig(exit_file)
    plt.clf()
    print "%s saved" % exit_file


if __name__ == "__main__":
    #
    # sys.argv[1] - sys.argv[7] corresponde ao csv's com os resultados das buscas
    #
    if len(sys.argv) != 8:
        print "err: missing params. the program need 7 params."
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])

    # plot.py "textgraphs/textgraphs_BFS.search.csv" "textgraphs/textgraphs_DFS.search.csv" "textgraphs/textgraphs_HEU1.search.csv" "textgraphs/textgraphs_HEU2.search.csv" "textgraphs/textgraphs_HEU3.search.csv" "textgraphs/textgraphs_MODs.search.csv" "textgraphs/textgraphs.png"