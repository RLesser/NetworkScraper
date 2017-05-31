#!/usr/bin/python

from ppScrape import ppfNetwork, pppNetwork
from hmScrape import HypeMNetwork
from tmdScrape import TMDNetwork
from collatzGraph import CollatzGraph

ns = CollatzGraph()
# ns.propegateGraph(1, limit = 10000, verbose = True)
# ns.propegateGraph('BobLesser', save_interval_and_location = [500, 'hypeM_all'], verbose = True)
# 'hypeM_all' killed after 18114 by /danivachon/ -> /Radio/

# ns.propegateGraph(10003215, verbose = True)
# ns.saveGraph('collatz_10000')
ns.loadGraph('collatz_1000')
# ns.colorNodes(keyProperty = "customName")
# ns.graphNetworkx(buds_visible = True, labels_visible = False, iterations = 100)
# time.sleep(5)
ns.graphD3(buds_visible = False, filter_assym_edges = False)