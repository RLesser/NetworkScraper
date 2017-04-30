#!/usr/bin/python

import sys
from ppScrape import *
from hmScrape import *
from tmdScrape import *

ns = TMDNetwork()
ns.propegateGraph('arts/steve-jobs-review', limit = 3, verbose = True)

# ns.propegateGraph(10004940, verbose = True)
# ns.saveGraph('tmd_arts_100')

# ns.loadGraph('tmd_arts_100')
ns.graph()