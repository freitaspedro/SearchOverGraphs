#!/usr/bin/env python

'''
Esse modulo plota o grafico orcamento x vertices positivos para todas as buscas
'''

import pandas
import matplotlib.pyplot as plt
import numpy as np


def main(name_bfs, name_dfs, name_heu1, name_heu2, name_heu3, name_mod, exit_name):
    bfs = pandas.read_csv(name_bfs)
    budget = bfs["budget"].values.tolist()
    budget.insert(0, 0)
    bfs_positives_mean = bfs["positives_mean"].values.tolist()
    bfs_positives_stdev = bfs["positives_stdev"].values.tolist()
    bfs_positives_mean.insert(0, 0)
    bfs_positives_stdev.insert(0, 0)

    dfs = pandas.read_csv(name_dfs)
    dfs_positives_mean = dfs["positives_mean"].values.tolist()
    dfs_positives_stdev = dfs["positives_stdev"].values.tolist()
    dfs_positives_mean.insert(0, 0)
    dfs_positives_stdev.insert(0, 0)

    heu1 = pandas.read_csv(name_heu1)
    heu1_positives_mean = heu1["positives_mean"].values.tolist()
    heu1_positives_stdev = heu1["positives_stdev"].values.tolist()
    heu1_positives_mean.insert(0, 0)
    heu1_positives_stdev.insert(0, 0)

    flag = 0
    try:
        heu2 = pandas.read_csv(name_heu2)
        heu2_positives_mean = heu2["positives_mean"].values.tolist()
        heu2_positives_stdev = heu2["positives_stdev"].values.tolist()
        heu2_positives_mean.insert(0, 0)
        heu2_positives_stdev.insert(0, 0)
    except Exception, e:
        flag = 1

    heu3 = pandas.read_csv(name_heu3)
    heu3_positives_mean = heu3["positives_mean"].values.tolist()
    heu3_positives_stdev = heu3["positives_stdev"].values.tolist()
    heu3_positives_mean.insert(0, 0)
    heu3_positives_stdev.insert(0, 0)

    mod = pandas.read_csv(name_mod)
    mod_positives_mean = mod["positives_mean"].values.tolist()
    mod_positives_stdev = mod["positives_stdev"].values.tolist()
    mod_positives_mean.insert(0, 0)
    mod_positives_stdev.insert(0, 0)

    bfs_line = plt.plot(budget, bfs_positives_mean, marker="o", markersize=4, markeredgewidth=1, markeredgecolor="b",
        markerfacecolor="None", color="b", label="BFS")
    dfs_line = plt.plot(budget, dfs_positives_mean, marker="s", markersize=4, markeredgewidth=1, markeredgecolor="g",
        markerfacecolor="None", color="g", label="DFS")
    heu1_line = plt.plot(budget, heu1_positives_mean, marker="^", markersize=4, markeredgewidth=1, markeredgecolor="r",
        markerfacecolor="None", color="r", label="Heu1")
    if not flag:
        heu2_line = plt.plot(budget, heu2_positives_mean, marker="p", markersize=4, markeredgewidth=1, markeredgecolor="c",
            markerfacecolor="None", color="c", label="Heu2")
    heu3_line = plt.plot(budget, heu3_positives_mean, marker="v", markersize=4, markeredgewidth=1, markeredgecolor="m",
        markerfacecolor="None", color="m", label="Heu3")
    mod_line = plt.plot(budget, mod_positives_mean, marker="D", markersize=4, markeredgewidth=1, markeredgecolor="k",
        markerfacecolor="None", color="k", label="MOD*")

    # plt.errorbar(budget, bfs_positives_mean, yerr=bfs_positives_stdev, color="b")
    # plt.errorbar(budget, dfs_positives_mean, yerr=dfs_positives_stdev, color="g")
    # plt.errorbar(budget, heu1_positives_mean, yerr=heu1_positives_stdev, color="r")
    # if not flag:
    #     plt.errorbar(budget, heu2_positives_mean, yerr=heu2_positives_stdev, color="c")
    # plt.errorbar(budget, heu3_positives_mean, yerr=heu3_positives_stdev, color="m")
    # plt.errorbar(budget, mod_positives_mean, yerr=mod_positives_stdev, color="k")

    plt.xticks(np.arange(0, max(budget)+21, 20.0), fontsize = 9)
    plt.yticks(np.arange(0, max([max(bfs_positives_mean), max(dfs_positives_mean),  max(heu1_positives_mean), max(heu2_positives_mean),
        max(heu3_positives_mean), max(mod_positives_mean)])+11, 5.0), fontsize = 9)

    # plt.grid(True)

    plt.ylabel("# vertices positivos", fontsize=9)
    plt.xlabel("# vertices explorados", fontsize=9)

    plt.legend(loc="upper left", fontsize=11)

    plt.savefig(exit_name)
    plt.clf()
    print "%s saved" % exit_name


if __name__ == "__main__":
    dir_facebook = "out/snap/facebook/6s_20r[ok]/"

    main(dir_facebook+"1912_f119_BFS.search.csv", dir_facebook+"1912_f119_DFS.search.csv",
        dir_facebook+"1912_f119_HEU1.search.csv", dir_facebook+"1912_f119_HEU2.search.csv",
        dir_facebook+"1912_f119_HEU3.search.csv", dir_facebook+"1912_f119_MODs.search.csv",
        dir_facebook+"s1912_f119.png")

    # main(dir_facebook+"1912_f155_BFS.478rch.csv", dir_facebook+"1912_f155_DFS.search.csv",
    #     dir_facebook+"1912_f155_HEU1.search.csv", dir_facebook+"1912_f155_HEU2.search.csv",
    #     dir_facebook+"1912_f155_HEU3.search.csv", dir_facebook+"1912_f155_MODs.search.csv",
    #     dir_facebook+"1912_f155.png")

    # main(dir_facebook+"1912_f219_BFS.search.csv", dir_facebook+"1912_f219_DFS.search.csv",
    #     dir_facebook+"1912_f219_HEU1.search.csv", dir_facebook+"1912_f219_HEU2.search.csv",
    #     dir_facebook+"1912_f219_HEU3.search.csv", dir_facebook+"1912_f219_MODs.search.csv",
    #     dir_facebook+"s1912_f219.png")

    # main(dir_facebook+"1912_f220_BFS.search.csv", dir_facebook+"1912_f220_DFS.search.csv",
    #     dir_facebook+"1912_f220_HEU1.search.csv", dir_facebook+"1912_f220_HEU2.search.csv",
    #     dir_facebook+"1912_f220_HEU3.search.csv", dir_facebook+"1912_f220_MODs.search.csv",
    #     dir_facebook+"1912_f220.png")

    # main(dir_facebook+"1912_f260_BFS.search.csv", dir_facebook+"1912_f260_DFS.search.csv",
    #     dir_facebook+"1912_f260_HEU1.search.csv", dir_facebook+"1912_f260_HEU2.search.csv",
    #     dir_facebook+"1912_f260_HEU3.search.csv", dir_facebook+"1912_f260_MODs.search.csv",
    #     dir_facebook+"1912_f260.png")

    dir_gplus = "out/snap/gplus/6s_20r[ok]/"

    # main(dir_gplus+"116807883656585676940_f0_BFS.search.csv",
    #     dir_gplus+"116807883656585676940_f0_DFS.search.csv",
    #     dir_gplus+"116807883656585676940_f0_HEU1.search.csv",
    #     dir_gplus+"116807883656585676940_f0_HEU2.search.csv",
    #     dir_gplus+"116807883656585676940_f0_HEU3.search.csv",
    #     dir_gplus+"116807883656585676940_f0_MODs.search.csv", dir_gplus+"116807883656585676940_f0.png")

    # main(dir_gplus+"116807883656585676940_f1_BFS.search.csv",
    #     dir_gplus+"116807883656585676940_f1_DFS.search.csv",
    #     dir_gplus+"116807883656585676940_f1_HEU1.search.csv",
    #     dir_gplus+"116807883656585676940_f1_HEU2.search.csv",
    #     dir_gplus+"116807883656585676940_f1_HEU3.search.csv",
    #     dir_gplus+"116807883656585676940_f1_MODs.search.csv", dir_gplus+"116807883656585676940_f1.png")

    # main(dir_gplus+"116807883656585676940_f154_BFS.search.csv",
    #     dir_gplus+"116807883656585676940_f154_DFS.search.csv",
    #     dir_gplus+"116807883656585676940_f154_HEU1.search.csv",
    #     dir_gplus+"116807883656585676940_f154_HEU2.search.csv",
    #     dir_gplus+"116807883656585676940_f154_HEU3.search.csv",
    #     dir_gplus+"116807883656585676940_f154_MODs.search.csv", dir_gplus+"116807883656585676940_f154.png")

    # main(dir_gplus+"116807883656585676940_f798_BFS.search.csv",
    #     dir_gplus+"116807883656585676940_f798_DFS.search.csv",
    #     dir_gplus+"116807883656585676940_f798_HEU1.search.csv",
    #     dir_gplus+"116807883656585676940_f798_HEU2.search.csv",
    #     dir_gplus+"116807883656585676940_f798_HEU3.search.csv",
    #     dir_gplus+"116807883656585676940_f798_MODs.search.csv", dir_gplus+"116807883656585676940_f798.png")

    dir_polblogs = "out/uci/polblogs/6s_20r[ok]/"

    # main(dir_polblogs+"polblogs.gml_f-1_BFS.search.csv", dir_polblogs+"polblogs.gml_f-1_DFS.search.csv",
    #     dir_polblogs+"polblogs.gml_f-1_HEU1.search.csv", dir_polblogs+"polblogs.gml_f-1_HEU2.search.csv",
    #     dir_polblogs+"polblogs.gml_f-1_HEU3.search.csv", dir_polblogs+"polblogs.gml_f-1_MODs.search.csv",
    #     dir_polblogs+"polblogs.gml_f-1.png")

    dir_gplus = "out/snap/twitter/6s_20r[ok]/"

    # main(dir_gplus+"256497288_f369_BFS.search.csv",
    #     dir_gplus+"256497288_f369_DFS.search.csv",
        # dir_gplus+"256497288_f369_HEU1.search.csv",
    #     dir_gplus+"256497288_f369_HEU2.search.csv",
    #     dir_gplus+"256497288_f369_HEU3.search.csv",
    #     dir_gplus+"256497288_f369_MODs.search.csv", dir_gplus+"256497288_f369.png")

    dir_polblogs = "out/uci/polbooks/6s_20r[ok]/c/"

    # main(dir_polblogs+"polbooks.gml_f-1_BFS.search.csv", dir_polblogs+"polbooks.gml_f-1_DFS.search.csv",
    #     dir_polblogs+"polbooks.gml_f-1_HEU1.search.csv", dir_polblogs+"polbooks.gml_f-1_HEU2.search.csv",
    #     dir_polblogs+"polbooks.gml_f-1_HEU3.search.csv", dir_polblogs+"polbooks.gml_f-1_MODs.search.csv",
    #     dir_polblogs+"polbooks.gml_f-1.png")