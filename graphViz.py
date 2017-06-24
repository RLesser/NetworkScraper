#!/usr/bin/python

from ppScrape import ppfNetwork, pppNetwork
from hmScrape import HypeMNetwork
from tmdScrape import TMDNetwork
from collatzGraph import CollatzGraph
from ghScrape import GithubNetwork
from wordGraph import WordChange
from countyGraph import CountyGraph

ns = CountyGraph()
#ns.propegateGraph('RLesser', save_interval_and_location = [100, 'github_1000'], limit = 1000, verbose = True)
# ns.propegateGraph('36119', verbose = True)
# 'hypeM_all' killed after 18114 by /danivachon/ -> /Radio/

# ns.propegateGraph(10003215, verbose = True)
# ns.saveGraph('adjwords_3')
# ns.loadGraph('github_1000')
# ns.colorNodes(keyProperty = "customName")
# ns.graphNetworkx(buds_visible = True, labels_visible = False, iterations = 100)
# time.sleep(5)

ns.loadGraph('hypeM_100')

# ns.colorNodes(keyProperty = "state")

ns.graphD3(buds_visible = False, filter_assym_edges = True)