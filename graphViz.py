#!/usr/bin/python

import sys
from ppScrape import *
from hmScrape import *
from tmdScrape import *

ns = HypeMNetwork()
ns.propegateGraph('BobLesser', limit = 10, verbose = True)

# ns.propegateGraph(10004940, verbose = True)
ns.saveGraph('hypeM_10')

ns.loadGraph('hypeM_10')
# ns.colorNodes(keyProperty = "section")
# ns.graphNetworkx(buds_visible = True, labels_visible = False, iterations = 100)
ns.graphD3()