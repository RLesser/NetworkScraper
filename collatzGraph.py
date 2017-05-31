#!/usr/bin/python

from networkScrape import NetworkScraper

class CollatzGraph(NetworkScraper):
	"""docstring for CollatzGraph"""
	def __init__(self):
		super(CollatzGraph, self).__init__()

	def getDataSource(self, nodeId):
		data = nodeId
		return data

	def getEdgeData(self, data):
		upstreamNums = [data*2]
		if (data-1) != 0 and (data-1)%3 == 0 and ((data-1)/3)%2 == 1:
			upstreamNums.append((data-1)/3)
		upstreamEdges = [self.makeEdgeObject(x) for x in upstreamNums]
		return upstreamEdges