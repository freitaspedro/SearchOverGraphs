#!/usr/bin/env python

'''
Esse modulo plota o grafico orcamento x vertices positivos para todas as buscas heu, fakeheu e dyheu
'''

import matplotlib.pyplot as plt
import numpy as np

def main(file_heu1, file_heu2, file_heu3, file_fakeheu1, file_fakeheu2, file_fakeheu3,
    file_dyheu1, file_dyheu2, file_dyheu3, exit_file):

    budget, time, heu1_positives_mean, heu1_positives_stdev = np.loadtxt(file_heu1, delimiter=",", unpack=True)
    heu2b, heu2t, heu2_positives_mean, heu2_positives_stdev = np.loadtxt(file_heu2, delimiter=",", unpack=True)
    heu3b, heu3t, heu3_positives_mean, heu3_positives_stdev = np.loadtxt(file_heu3, delimiter=",", unpack=True)
    fakeheu1b, fakeheu1t, fakeheu1_positives_mean, fakeheu1_positives_stdev = np.loadtxt(file_fakeheu1, delimiter=",", unpack=True)
    fakeheu2b, fakeheu2t, fakeheu2_positives_mean, fakeheu2_positives_stdev = np.loadtxt(file_fakeheu2, delimiter=",", unpack=True)
    fakeheu3b, fakeheu3t, fakeheu3_positives_mean, fakeheu3_positives_stdev = np.loadtxt(file_fakeheu3, delimiter=",", unpack=True)
    dyheu1b, dyheu1t, dyheu1_positives_mean, dyheu1_positives_stdev = np.loadtxt(file_dyheu1, delimiter=",", unpack=True)
    dyheu2b, dyheu2t, dyheu2_positives_mean, dyheu2_positives_stdev = np.loadtxt(file_dyheu2, delimiter=",", unpack=True)
    dyheu3b, dyheu3t, dyheu3_positives_mean, dyheu3_positives_stdev = np.loadtxt(file_dyheu3, delimiter=",", unpack=True)

    budget.insert(0, 0)
    heu1_positives_mean = np.insert(heu1_positives_mean, 0, 0)
    heu1_positives_stdev = np.insert(heu1_positives_stdev, 0, 0)
    heu2_positives_mean = np.insert(heu2_positives_mean, 0, 0)
    heu2_positives_stdev = np.insert(heu2_positives_stdev, 0, 0)
    heu3_positives_mean = np.insert(heu3_positives_mean, 0, 0)
    heu3_positives_stdev = np.insert(heu3_positives_stdev, 0, 0)
    fakeheu1_positives_mean = np.insert(fakeheu1_positives_mean, 0, 0)
    fakeheu1_positives_stdev = np.insert(fakeheu1_positives_stdev, 0, 0)
    fakeheu2_positives_mean = np.insert(fakeheu2_positives_mean, 0, 0)
    fakeheu2_positives_stdev = np.insert(fakeheu2_positives_stdev, 0, 0)
    fakeheu3_positives_mean = np.insert(fakeheu3_positives_mean, 0, 0)
    fakeheu3_positives_stdev = np.insert(fakeheu3_positives_stdev, 0, 0)
    dyheu1_positives_mean = np.insert(dyheu1_positives_mean, 0, 0)
    dyheu1_positives_stdev = np.insert(dyheu1_positives_stdev, 0, 0)
    dyheu2_positives_mean = np.insert(dyheu2_positives_mean, 0, 0)
    dyheu2_positives_stdev = np.insert(dyheu2_positives_stdev, 0, 0)
    dyheu3_positives_mean= np.insert(dyheu3_positives_mean, 0, 0)
    dyheu3_positives_stdev = np.insert(dyheu3_positives_stdev, 0, 0)

    heu1_line = plt.plot(budget, heu1_positives_mean, color="#ff0000", label="Heu1")
    heu2_line = plt.plot(budget, heu2_positives_mean, color="#00ffff", label="Heu2")
    heu3_line = plt.plot(budget, heu3_positives_mean, color="#bf00ff", label="Heu3")
    fakeheu1_line = plt.plot(budget, fakeheu1_positives_mean, color="#ff8000", label="fakeHeu1")
    fakeheu2_line = plt.plot(budget, fakeheu2_positives_mean, color="#0080ff", label="fakeHeu2")
    fakeheu3_line = plt.plot(budget, fakeheu3_positives_mean, color="#ff0080", label="fakeHeu3")
    dyheu1_line = plt.plot(budget, dyheu1_positives_mean, color="#ffff00", label="dyHeu1")
    dyheu2_line = plt.plot(budget, dyheu2_positives_mean, color="#0000ff", label="dyHeu2")
    dyheu3_line = plt.plot(budget, dyheu3_positives_mean, color="#ff0040", label="dyHeu3")

    # plt.errorbar(budget, heu1_positives_mean, yerr=heu1_positives_stdev, color="#ff0000")
    # plt.errorbar(budget, heu2_positives_mean, yerr=heu2_positives_stdev, color="#00ffff")
    # plt.errorbar(budget, heu3_positives_mean, yerr=heu3_positives_stdev, color="#bf00ff")
    # plt.errorbar(budget, fakeheu1_positives_mean, yerr=fakeheu1_positives_stdev, color="#ff8000")
    # plt.errorbar(budget, fakeheu2_positives_mean, yerr=fakeheu2_positives_stdev, color="#0080ff")
    # plt.errorbar(budget, fakeheu3_positives_mean, yerr=fakeheu3_positives_stdev, color="#ff0080")
    # plt.errorbar(budget, dyheu1_positives_mean, yerr=dyheu1_positives_stdev, color="#ffff00")
    # plt.errorbar(budget, dyheu2_positives_mean, yerr=dyheu2_positives_stdev, color="#0000ff")
    # plt.errorbar(budget, dyheu3_positives_mean, yerr=dyheu3_positives_stdev, color="#ff0040")

    plt.xticks(np.arange(0, max(budget)+21, 20.0), fontsize = 9)
    plt.yticks(np.arange(0, max([max(heu1_positives_mean), max(heu2_positives_mean),
        max(heu3_positives_mean), max(fakeheu1_positives_mean), max(fakeheu2_positives_mean),
        max(fakeheu3_positives_mean), max(dyheu1_positives_mean), max(dyheu2_positives_mean),
        max(dyheu3_positives_mean)])+11, 5.0), fontsize = 9)

    # plt.grid(True)

    plt.ylabel("vertices positivos", fontsize=9)
    plt.xlabel("vertices explorados", fontsize=9)

    plt.legend(loc="upper left", fontsize=11)

    plt.savefig(exit_file)
    plt.clf()
    print "%s saved" % exit_file


if __name__ == "__main__":
    #
    # sys.argv[1] - sys.argv[10] corresponde ao csv's com os resultados das buscas
    #
    if len(sys.argv) != 11:
        print "err: missing params. the program need 10 params."
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8],
            sys.argv[9], sys.argv[10])

    # plotheu.py "textgraphs/textgraphs_HEU1.search.csv" "textgraphs/textgraphs_HEU2.search.csv" "textgraphs/textgraphs_HEU3.search.csv" "textgraphs/textgraphs_fakeHEU1.search.csv" "textgraphs/textgraphs_fakeHEU2.search.csv" "textgraphs/textgraphs_fakeHEU3.search.csv" "textgraphs/textgraphs_dyHEU1.search.csv" "textgraphs/textgraphs_dyHEU2.search.csv" "textgraphs/textgraphs_dyHEU3.search.csv" "textgraphs/HEUtextgraphs.png"