#!/usr/bin/env python

'''
Esse modulo plota o grafico orcamento x vertices positivos para todas as buscas heu, fakeheu e dyheu
'''

import matplotlib.pyplot as plt
import numpy as np
import sys

def main(heu, file_heu, file_fakeheu, file_dy1heu, file_dy10heu, file_dy100heu, exit_file, bar):

    if heu == "Heu1": heu = "$H_1$"
    elif heu == "Heu2": heu = "$H_2$"
    elif heu == "Heu3": heu = "$H_3$"

    budget, time, heu_positives_mean, heu_positives_stdev = np.loadtxt(file_heu, delimiter=",", unpack=True)
    fakeheub, fakeheut, fakeheu_positives_mean, fakeheu_positives_stdev = np.loadtxt(file_fakeheu, delimiter=",", unpack=True)
    dy1heub, dy1heut, dy1heu_positives_mean, dy1heu_positives_stdev = np.loadtxt(file_dy1heu, delimiter=",", unpack=True)
    # dy10heub, dy10heut, dy10heu_positives_mean, dy10heu_positives_stdev = np.loadtxt(file_dy10heu, delimiter=",", unpack=True)
    # dy100heub, dy100heut, dy100heu_positives_mean, dy100heu_positives_stdev = np.loadtxt(file_dy100heu, delimiter=",", unpack=True)

    budget = np.insert(budget, 0, 0)
    heu_positives_mean = np.insert(heu_positives_mean, 0, 0)
    heu_positives_stdev = np.insert(heu_positives_stdev, 0, 0)
    fakeheu_positives_mean = np.insert(fakeheu_positives_mean, 0, 0)
    fakeheu_positives_stdev = np.insert(fakeheu_positives_stdev, 0, 0)
    dy1heu_positives_mean = np.insert(dy1heu_positives_mean, 0, 0)
    dy1heu_positives_stdev = np.insert(dy1heu_positives_stdev, 0, 0)
    # dy10heu_positives_mean = np.insert(dy10heu_positives_mean, 0, 0)
    # dy10heu_positives_stdev = np.insert(dy10heu_positives_stdev, 0, 0)
    # dy100heu_positives_mean = np.insert(dy100heu_positives_mean, 0, 0)
    # dy100heu_positives_stdev = np.insert(dy100heu_positives_stdev, 0, 0)

    heu_line = plt.plot(budget, heu_positives_mean, marker="D", markersize=4, markeredgewidth=1, markeredgecolor="k",
        markerfacecolor="None", color="k", label=heu)
    fakeheu_line = plt.plot(budget, fakeheu_positives_mean, marker="v", markersize=4, markeredgewidth=1, markeredgecolor="m",
        markerfacecolor="None", color="m", label="$sym$"+heu)
    dy1heu_line = plt.plot(budget, dy1heu_positives_mean, marker="p", markersize=4, markeredgewidth=1, markeredgecolor="c",
        markerfacecolor="None", color="c", label="$dy$"+heu)
    # dy10heu_line = plt.plot(budget, dy10heu_positives_mean, marker="^", markersize=4, markeredgewidth=1, markeredgecolor="r",
    #     markerfacecolor="None", color="r", label="dy10"+heu)
    # dy100heu_line = plt.plot(budget, dy100heu_positives_mean, marker="s", markersize=4, markeredgewidth=1, markeredgecolor="g",
    #     markerfacecolor="None", color="g", label="dy100"+heu)

    if bar == "yes":
        plt.errorbar(budget, heu_positives_mean, yerr=heu_positives_stdev, color="k", elinewidth=.3)
        plt.errorbar(budget, fakeheu_positives_mean, yerr=fakeheu_positives_stdev, color="m", elinewidth=.3)
        plt.errorbar(budget, dy1heu_positives_mean, yerr=dy1heu_positives_stdev, color="c", elinewidth=.3)
        # plt.errorbar(budget, dy10heu_positives_mean, yerr=dy10heu_positives_stdev, color="r", elinewidth=.3)
        # plt.errorbar(budget, dy100heu_positives_mean, yerr=dy100heu_positives_stdev, color="g", elinewidth=.3)

    plt.xticks(np.arange(100, max(budget)+1111.0, 200.0), fontsize = 9)
    # plt.yticks(np.arange(0, max([max(heu_positives_mean), max(fakeheu_positives_mean),
    #     max(dy1heu_positives_mean), max(dy10heu_positives_mean), max(dy100heu_positives_mean)])+10.0, 5.0), fontsize = 9)
    # plt.yticks(np.arange(0, max([max(heu_positives_mean), max(fakeheu_positives_mean)])+1111.0, 200.0), fontsize = 9)
    plt.yticks(np.arange(0, max([max(heu_positives_mean), max(fakeheu_positives_mean),
        max(dy1heu_positives_mean)])+1111.0, 200.0), fontsize = 9)

    # plt.grid(True)
    plt.xlim((0, 2700))
    plt.ylim((0, 2000))

    plt.ylabel("# vertices positivos", fontsize=9)
    plt.xlabel("# vertices explorados", fontsize=9)

    plt.legend(loc="upper left", fontsize=11)

    plt.title("caracteristica 0", fontsize=11)

    plt.savefig(exit_file)
    plt.clf()
    print "%s saved" % exit_file


if __name__ == "__main__":
    #
    # sys.argv[1] corresponde ao tipo da heuristica
    #
    # sys.argv[2] - sys.argv[6] corresponde ao csv's com os resultados das buscas
    #
    if len(sys.argv) != 9:
        print "err: missing params. the program need 8 params."
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])

    # plotheu.py "Heu1" "snap/facebook/1912/f240/heus100r/HEU1.search.csv" "snap/facebook/1912/f240/heus100r/fakeHEU1.search.csv" "snap/facebook/1912/f240/heus100r/dy1HEU1.search.csv" "snap/facebook/1912/f240/heus100r/dy10HEU1.search.csv" "snap/facebook/1912/f240/heus100r/dy100HEU1.search.csv" "snap/facebook/1912/f240/heus100r/s_heu1.png" no
    # plotheu.py "Heu2" "snap/facebook/1912/f240/heus100r/HEU2.search.csv" "snap/facebook/1912/f240/heus100r/fakeHEU2.search.csv" "snap/facebook/1912/f240/heus100r/dy1HEU2.search.csv" "snap/facebook/1912/f240/heus100r/dy10HEU2.search.csv" "snap/facebook/1912/f240/heus100r/dy100HEU2.search.csv" "snap/facebook/1912/f240/heus100r/s_heu2.png" no
    # plotheu.py "Heu3" "snap/facebook/1912/f240/heus100r/HEU3.search.csv" "snap/facebook/1912/f240/heus100r/fakeHEU3.search.csv" "snap/facebook/1912/f240/heus100r/dy1HEU3.search.csv" "snap/facebook/1912/f240/heus100r/dy10HEU3.search.csv" "snap/facebook/1912/f240/heus100r/dy100HEU3.search.csv" "snap/facebook/1912/f240/heus100r/s_heu3.png" no

    # plotheu.py "Heu1" "snap/gplus/116807883656585676940/f0/heus100r/HEU1.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/fakeHEU1.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy1HEU1.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy10HEU1.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy100HEU1.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/s_heu1.png" no
    # plotheu.py "Heu2" "snap/gplus/116807883656585676940/f0/heus100r/HEU2.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/fakeHEU2.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy1HEU2.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy10HEU2.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy100HEU2.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/s_heu2.png" no
    # plotheu.py "Heu3" "snap/gplus/116807883656585676940/f0/heus100r/HEU3.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/fakeHEU3.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy1HEU3.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy10HEU3.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/dy100HEU3.search.csv" "snap/gplus/116807883656585676940/f0/heus100r/s_heu3.png" no

    # plotheu.py "Heu1" "uci/polblogs/nheus100r/HEU1.search.csv" "uci/polblogs/nheus100r/fakeHEU1.search.csv" "uci/polblogs/nheus100r/dy1HEU1.search.csv" "uci/polblogs/nheus100r/dy10HEU1.search.csv" "uci/polblogs/nheus100r/dy100HEU1.search.csv" "uci/polblogs/nheus100r/s_heu1.png" no
    # plotheu.py "Heu2" "uci/polblogs/nheus100r/HEU2.search.csv" "uci/polblogs/nheus100r/fakeHEU2.search.csv" "uci/polblogs/nheus100r/dy1HEU2.search.csv" "uci/polblogs/nheus100r/dy10HEU2.search.csv" "uci/polblogs/nheus100r/dy100HEU2.search.csv" "uci/polblogs/nheus100r/s_heu2.png" no
    # plotheu.py "Heu3" "uci/polblogs/nheus100r/HEU3.search.csv" "uci/polblogs/nheus100r/fakeHEU3.search.csv" "uci/polblogs/nheus100r/dy1HEU3.search.csv" "uci/polblogs/nheus100r/dy10HEU3.search.csv" "uci/polblogs/nheus100r/dy100HEU3.search.csv" "uci/polblogs/nheus100r/s_heu3.png" no
