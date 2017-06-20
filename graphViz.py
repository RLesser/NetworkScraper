#!/usr/bin/python

from ppScrape import ppfNetwork, pppNetwork
from hmScrape import HypeMNetwork
from tmdScrape import TMDNetwork
from collatzGraph import CollatzGraph
from ghScrape import GithubNetwork
from wordGraph import WordChange

ns = WordChange()
#ns.propegateGraph('RLesser', save_interval_and_location = [100, 'github_1000'], limit = 1000, verbose = True)
ns.propegateGraph('farce', verbose = True)
# 'hypeM_all' killed after 18114 by /danivachon/ -> /Radio/

# ns.propegateGraph(10003215, verbose = True)
# ns.saveGraph('github_1000')
# ns.loadGraph('github_1000')
# ns.colorNodes(keyProperty = "customName")
# ns.graphNetworkx(buds_visible = True, labels_visible = False, iterations = 100)
# time.sleep(5)

ns.colorNodes(keyProperty = "vowels")

ns.graphD3(buds_visible = False, filter_assym_edges = True)