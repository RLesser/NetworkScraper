#!/usr/bin/python

import sys
import time
from ppScrape import *
from hmScrape import *
from tmdScrape import *

ns = HypeMNetwork()
# ns.propegateGraph('BobLesser', limit = 1000, verbose = True)
# 989 -> 3221

# ns.propegateGraph(10004940, verbose = True)
# ns.saveGraph('HypeM_1000')
ns.loadGraph('HypeM_10')
ns.colorNodes(keyProperty = "supporter")
# ns.graphNetworkx(buds_visible = True, labels_visible = False, iterations = 100)
# time.sleep(5)
ns.graphD3(buds_visible = False)