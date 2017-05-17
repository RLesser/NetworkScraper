#!/usr/bin/python

import sys
from ppScrape import *
from hmScrape import *
from tmdScrape import *

ns = TMDNetwork()
#ns.propegateGraph('no-section/michigan-daily-grade-guide-compare-class-grade-distributions-across-lsa', limit = 10, verbose = True)

# ns.propegateGraph(10004940, verbose = True)
#ns.saveGraph('tmd_arts_10')

ns.loadGraph('tmd_grades_100')
# ns.colorNodes(keyProperty = "section")
# ns.graphNetworkx(buds_visible = True, labels_visible = False, iterations = 100)
ns.graphD3()