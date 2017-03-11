#!/usr/bin/python

import sys
from ppScrape import *

ns = ppfNetwork()

# ns.propegateGraph(10004940, verbose = True)
# ns.saveGraph('emerald_all_flags')

ns.loadGraph('emerald_all_flags')
ns.graph()