#!/usr/bin/python

from ppScrape import ppfNetwork, pppNetwork
from hmScrape import HypeMNetwork
from tmdScrape import TMDNetwork

ns = TMDNetwork()
# ns.propegateGraph('no-section/michigan-daily-grade-guide-compare-class-grade-distributions-across-lsa', limit = 1000, verbose = True)
# 989 -> 3221

# ns.propegateGraph(10003215, verbose = True)
# ns.saveGraph('tmd_grades_1000')
ns.loadGraph('tmd_grades_1000')
ns.colorNodes(keyProperty = "section")
# ns.graphNetworkx(buds_visible = True, labels_visible = False, iterations = 100)
# time.sleep(5)
ns.graphD3(buds_visible = False, filter_assym_edges = False)