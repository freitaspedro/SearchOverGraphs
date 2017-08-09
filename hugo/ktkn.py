#!/usr/bin/env python

import itertools

# mlist = range(1254+1)
mlist = range(100+1)
# print mlist

kt_kn = [p for p in itertools.product(mlist, repeat=2)]
# print len(kt_kn)      # 1575025
# print len(kt_kn)      # 10201

# with open("kt_kn", "wb") as f:
with open("kt_kn_100", "wb") as f:
    for kt, kn in kt_kn:
        f.write("%s:%s\n" % (kt, kn))
# print "kt_kn saved!"
print "kt_kn_100 saved!"
