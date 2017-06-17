#!/usr/bin/env python

'''
Esse modulo e responsavel por montar a rede de colaboracao de autores no dblp. Os autores
recebem um indicador para dizer se participaram ou nao do congresso(journal) passado como
parametro.
'''


import xml.etree.ElementTree as et
import graph_tool.all as gt
import itertools as itools
import sys

def get_tabel(name):
    html_map = {}                  #guarda o mapeamento dos caracteres html
    f = open(name)
    for i in f:
        i = i.rstrip("\n").split("|")
        html_map[i[1]] = i[0]
    f.close()
    return html_map

class AllEntities:
    def __getitem__(self, key):
        #key is your entity, you can do whatever you want with it here
        return key

def remove_dup(mlist):
    return set(tuple(sorted(k)) for k in mlist)

def main(xml_in, xml_out):
    p = et.XMLParser(html=True, encoding="latin1")
    p.parser.UseForeignDTD(True)
    p.entity = AllEntities()

    it = iter(et.iterparse(xml_in, events=("end", "end-ns", "start", "start-ns"), parser=p))
    jnk, root = next(it)

    pubs = set([u"inproceedings"])            # tipos de publicacao validas
    ways = [u"conf"]            # meios de publicacao validos
    inval = set([u"et al.", u"anonymous", None])          # nomes de autor invalidos

    author_conf = {}
    author_author = []
    cnt = 0
    print "parsing xml..."
    for ev, el in it:
        if len(el.getchildren()) and el.tag in pubs:              # verifica se o node possui filhos e se possui uma tag de publicacao valida
            att = el.get("key")
            # OBS: <article mdate="2012-05-29" key="journals/ijcaet/SinghP09">
            # meio = journals, nome = ijcaet
            if att is not None:
                w = att.split("/")[0]
                if w in ways:
                    c = att.split("/")[1]
                    authors = [j.text for j in el.findall("author") if j.text not in inval]               # pega os autores da publicacao
                    for author in authors:
                        # if author is None:
                        #     print "err 1: author is %s" % author
                        author_conf.setdefault(author, []).append(c)
                    author_author.extend([t for t in itools.combinations(authors, 2)])
        el.clear()                 # importante, limpa a memoria
        root.clear()
        cnt += 1
        if not cnt % 1000000: print cnt
        # if not cnt % 1000000: break

    author_author = remove_dup(author_author)
    # for k, v in author_conf.iteritems():
    #     if k is None:
    #         print "err 2: author is %s" % k
    # for v in author_author:
    #     if v[0] is None or v[1] is None:
    #         print "err 3: some author is None (%s or %s)" % (v[0], v[1])

    print "building graph..."
    g = gt.Graph(directed=False)
    vprop = g.new_vertex_property("string")
    vprop1 = g.new_vertex_property("vector<string>")
    g.vp.name = vprop
    g.vp.confs = vprop1

    id_name = {}            # mapeia os ids gerados pelo graph tool com os nomes dos autores
    print "len(author_conf)", len(author_conf)
    # len(author_conf) 1901632 - pubs = set([u"article", u"inproceedings", u"proceedings"]); ways = [u"conf", u"journals"]
    # len(author_conf) 1268107 - pubs = set([u"inproceedings"]); ways = [u"conf"]
    print "adding vertices..."
    for k, v in author_conf.iteritems():
        vertex = g.add_vertex()
        g.vp.name[vertex] = k
        g.vp.confs[vertex] = set(v)
        id_name[k] = int(vertex)

    print "len(author_author)", len(author_author)
    # len(author_author) 8569010 - pubs = set([u"article", u"inproceedings", u"proceedings"]); ways = [u"conf", u"journals"]
    # len(author_author) 5243768 - pubs = set([u"inproceedings"]); ways = [u"conf"]
    print "adding edges..."
    cnt = 0
    for v in author_author:
        src = g.vertex(id_name[v[0]])
        tgt = g.vertex(id_name[v[1]])
        g.add_edge(src, tgt)
        cnt += 1
        if not cnt % 1000000: print cnt

    # for v in g.vertices():
    #     print "name: %s, confs: %s" % (g.vp.name[v], g.vp.confs[v])
    # for e in g.edges():
    #     print "src: %s, tgt: %s" % (g.vp.name[e.source()], g.vp.name[e.target()])

    print "%s vertices" % g.num_vertices()
    print "%s edges" % g.num_edges()

    # gt.graph_draw(g)
    g.save(xml_out)
    print "graph saved!"


if __name__ == "__main__":
    # sys.argv[1] corresponde ao path para o arquivo de entrada contendo o xml do dblp
    #
    # sys.argv[2] corresponde ao path para o arquivo de saida contendo o xml do grafo
    # do dblp
    #
    if len(sys.argv) != 3:
        print "err: missing params. the program need 2 params."
    else:
        main(sys.argv[1], sys.argv[2])
        # parser.py "dblp2.xml" "dblp_g.xml.gz"