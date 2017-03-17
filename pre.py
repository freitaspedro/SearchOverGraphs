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

    out_degree_dist, in_degree_dist =  props.get_degree_dist(g)
    write_dict_txt(name+".out_degrees.txt", out_degree_dist)
    write_dict_txt(name+".in_degrees.txt", in_degree_dist)

    gt.graph_draw(g, output=name+".png")
    print "%s.png saved" % name

def main(name, headers, isdirected):
    if headers == -1:       # polblogs
        props_draw_save(name, isdirected, True)
    else:           # egonets - facebook, gplus, twitter
        txt_to_csv(name+".feat", headers)
        txt_to_csv(name+".edges", 0)
        props_draw_save(name, isdirected, False)


if __name__ == "__main__":
    # main("snap/facebook/1912", 481, False)
    # main("snap/gplus/116807883656585676940", 3751, False)
    # main("uci/polblogs/polblogs.gml", -1, False)
    main("snap/twitter/256497288", 1359, False)