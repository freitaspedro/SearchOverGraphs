#!/usr/bin/env python

'''
Esse modulo substitui caracteres especiais em html no xml, e cria uma
tabela de conversao para esses caracteres.
'''

import sys

def main(xml_in, xml_out, tabel)
    html = {}
    cnt = 0
    f = open(xml_in)
    f2 = open(xml_out, "w")
    marker = "###"
    for i in f:
        c1 = i.count("&")
        c2 = i.count(";")
        p1 = 0
        p2 = 0
        if c1 and c2:
            for j in xrange(c1):
                p1 = i.find("&", p1)
                p2 = i.find(";", p1)
                if p1 >= 0 and p2 >= 0 and p2 > p1:
                    if i[p1:p2+1] not in html:
                        html[i[p1:p2+1]] = cnt
                        cnt += 1
                    else:
                        i = i.replace(i[p1:p2+1], marker + str(html[i[p1:p2+1]]) + marker)
                p1 += 1
                p2 += 1
        f2.write(i)
    f.close()
    f2.close()
    f = open(tabel,"w")
    for i in html:
        f.write(i+"|"+str(html[i])+"\n")
    f.close()


if __name__ == "__main__":
    # sys.argv[1] corresponde ao path para o arquivo de entrada contendo o xml do dblp
    #
    # sys.argv[2] corresponde ao path para o arquivo de saida contendo o xml do dblp sem os
    # caracteres especiais html
    #
    # sys.argv[3] corresponde ao path para o arquivo de saida contendo a tabela de conversao
    # dos caracteres especiais html
    #
    if len(sys.argv) != 4:
        print "err: missing params. the program need 3 params."
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
        # removehtml.py "dblp/dblp.xml" "dblp2.xml" "tabela.txt"