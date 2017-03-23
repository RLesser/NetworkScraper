#!/usr/bin/python

import sys
from ppScrape import *
from hmScrape import *

ns = HypeMNetwork()
ns.propegateGraph('BobLesser', limit = 2, verbose = True)

# ns.propegateGraph(10004940, verbose = True)
#ns.saveGraph('hypeM_1000')

#ns.loadGraph('hypeM_1000')
ns.graph()