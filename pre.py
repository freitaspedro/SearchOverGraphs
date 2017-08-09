#!/usr/bin/env python

'''
Esse modulo converte os arquivos do tipo *.feat e *.edges para
arquivos do tipo *.feat.csv e *.edges.csv, salva um *.png
contendo a topologia da egonet, um *.txt contendo algumas propriedades
da egonet, e um *.out(in)_degrees.txt  com as distribuicoes de grau da egonet
'''

import graph_tool.all as gt
import props
import csv
import matplotlib.pylab as plt

def txt_to_csv(name, headers):
    in_txt = csv.reader(open(name, "rb"), delimiter=" ")
    out_csv = csv.writer(open(name+".csv", "wb"))
    if headers != 0:
        h = ["name"]
        h.extend(list(range(headers - 1)))
        out_csv.writerow(h)
    out_csv.writerows(in_txt)
    print "%s.csv saved" % name

def write_txt(name, data):
    with open(name, "w") as f:
         f.write("%s\n" % ''.join(data))
    print "%s saved" % name

def write_dict_txt(name, mdict):
    with open(name, "w") as f:
        for k, v in mdict.items():
            f.write("%s   %s\n" % (k, v))
    print "%s saved" % name

def write_tuples_txt(name, mlist):
    with open(name, "w") as f:
        for tup in mlist:
            f.write("%s\t\t%s\t\t%s\n" % (tup[0], tup[1], tup[2]))
    print "%s saved" % name

def plot_ccdf(degree_dist, num, exit_name):
    ccdf = dict.fromkeys(degree_dist.keys(), 0)
    count = 0
    for w in sorted(degree_dist.keys(), reverse=True):
        count += degree_dist[w]/float(num)
        ccdf[w] = count
    # print "ccdf", ccdf
    ccdf = sorted(ccdf.items())
    x, y = zip(*ccdf)

    # print "len(x)", len(x)
    plt.scatter(x, y)

    # plt.xticks(np.arange(0, max(x)+?, ?))
    # plt.yticks(np.arange(0, max(y)+?, ?))

    # plt.xscale("log")
    # plt.yscale("log")

    plt.ylabel("ccdf p[d>=k]")
    plt.xlabel("grau")

    plt.savefig(exit_name)
    plt.clf()
    print "%s saved" % exit_name

def props_draw_save(name, isdirected, isgml):
    pr = []
    pr.append(props.get_name(name))
    pr.append(props.is_directed(isdirected))
    if isgml:
        g = gt.load_graph(name)
        g.set_directed(isdirected)
    else:
        g = gt.load_graph_from_csv(name+".edges.csv", directed=isdirected)
    pr.append(props.get_num_vertices(g))
    pr.append(props.get_num_edges(g))
    pr.append(props.get_diameter(g))
    pr.append(props.get_avg_degrees(g))
    pr.append(props.get_global_clustering(g))
    pr.append(props.get_comps(g, isdirected))
    write_txt(name+".props.txt", pr)

    in_degree_dist, out_degree_dist =  props.get_degree_dist(g)
    # write_dict_txt(name+".in_degrees.txt", in_degree_dist)
    write_dict_txt(name+".out_degrees.txt", out_degree_dist)

    n = 100
    in_topn, in_lastn, out_topn, out_lastn = props.topn_lastn_degrees(g, n)
    # write_tuples_txt(name+".in_top"+n+".txt", in_topn)
    # write_tuples_txt(name+".in_last"+n+".txt", in_lastn)
    write_tuples_txt(name+".out_top"+str(n)+".txt", out_topn)
    write_tuples_txt(name+".out_last"+str(n)+".txt", out_lastn)

    # plot_ccdf(in_degree_dist, g.num_vertices(), name+".in_ccdf.png")
    plot_ccdf(out_degree_dist, g.num_vertices(), name+".out_ccdf.png")

    # gt.graph_draw(g, output=name+".png")
    # print "%s.png saved" % name

def main(name, headers, isdirected):
    if headers == -1:       # polblogs, polbooks
        props_draw_save(name, isdirected, True)
    else:           # egonets - facebook, gplus, twitter
        txt_to_csv(name+".feat", headers)
        txt_to_csv(name+".edges", 0)
        props_draw_save(name, isdirected, False)


if __name__ == "__main__":
    # main("snap/facebook/1912", 481, False)
    # main("snap/gplus/116807883656585676940", 3751, False)
    # main("uci/polblogs/polblogs.gml", -1, False)
    # main("snap/twitter/256497288", 1359, False)
    # main("uci/polbooks/polbooks.gml", -1, False)

    # main("hugo/dblp_g.xml.gz", -1, False)
    # main("hugo/gcc_dblp_g.xml.gz", -1, False)

    ################### pos wperformance ################################

    # main("hugo/textgraphs/positives_textgraphs_gcc_dblp_g.xml.gz", -1, False)
    # main("hugo/p2p/positives_p2p_gcc_dblp_g.xml.gz", -1, False)
    # main("hugo/wcnc/positives_wcnc_gcc_dblp_g.xml.gz", -1, False)
    # main("hugo/group1/positives_group1_gcc_dblp_g.xml.gz", -1, False)
    # main("hugo/group2/positives_group2_gcc_dblp_g.xml.gz", -1, False)
    # main("hugo/immerscom/positives_immerscom_gcc_dblp_g.xml.gz", -1, False)
    # main("hugo/socialcom/positives_socialcom_gcc_dblp_g.xml.gz", -1, False)
    # main("hugo/aaai/positives_aaai_gcc_dblp_g.xml.gz", -1, False)

    main("snap/facebook/1912/f240/gcc.xml.gz", -1, False)
    # main("snap/gplus/116807883656585676940/f862/gcc.xml.gz", -1, False)
    # main("uci/polblogs/polblogs.gcc.xml.gz", -1, False)

    # main("hugo/gcc_200k_dblp_g.xml.gz", -1, False)