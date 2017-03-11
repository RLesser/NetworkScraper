#!/usr/bin/python

import urllib2
import bs4
import networkx as nx
import matplotlib.pyplot as plt
import pickle


class NetworkScraper(object):
	"""base class for scraping websites for network connections"""
	def __init__(self):
		super(NetworkScraper, self).__init__()
		# exploreList is a list of nodes
		self.exploreList = []
		# relationDict has the nodeId's as keys
		# self.relationDict = {}


	def url_to_soup(self, url):
	    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
	    html = urllib2.urlopen(req).read()
	    soup = bs4.BeautifulSoup(html)
	    return soup


	def getDataSource(self, nodeId):
		pass


	def getNodeName(self, data):
		return None


	def getAdjNodeIds(self, data):
		return []


	def getNodeColor(self, data):
		return 'r'


	def getEdgeColors(self, data):
		return []


	def makeBaseNode(self, nodeId):
		# print "Entering makeBaseNode"
		node = {
			'name': None,
			'nodeId': nodeId,
			'adjNodeIds': [],
			'nodeColor': None,
			'edgeColors': None
		}
		return node


	def fillNodeData(self, node):
		# print "Entering fillNodeData"
		data = self.getDataSource(node['nodeId']);
		name = self.getNodeName(data)
		# print "node name:", node['nodeId']
		if name == None:
			name = node['nodeId']
		node['name'] = name
		node['adjNodeIds'] = self.getAdjNodeIds(data)
		node['nodeColor'] = self.getNodeColor(data)
		node['edgeColors'] = self.getEdgeColors(data)
		return node


	def getNewNodes(self, seedNode):
		# print "Entering getNewNodes"
		newNodes = [self.makeBaseNode(nodeId) for nodeId in seedNode['adjNodeIds']]
		return newNodes


	def getUniqueConnections(self, connectionList):
		currNodeList = [x['nodeId'] for x in self.exploreList]
		uniqueList = [x for x in connectionList if x['nodeId'] not in currNodeList]
		return uniqueList


	def propegateGraph(self, nodeId, limit = None, verbose = False):
		self.exploreList.append(self.makeBaseNode(nodeId))
		curNodeIdx = 0
		while (not limit or curNodeIdx < limit) \
			and curNodeIdx < len(self.exploreList):
			fullCurNode = self.fillNodeData(self.exploreList[curNodeIdx])
			self.exploreList[curNodeIdx] = fullCurNode
			if verbose:
				print curNodeIdx, '[', len(self.exploreList), ']',
				print self.exploreList[curNodeIdx]['name']
			newNodes = self.getNewNodes(self.exploreList[curNodeIdx])
			newUnusedNodes = self.getUniqueConnections(newNodes)
			self.exploreList += newUnusedNodes
			curNodeIdx += 1;


	def saveGraph(self, graphName, path = "./savedData/"):
		with open(path + graphName + ".pkl", "wb") as f:
			pickle.dump(self.exploreList, f, pickle.HIGHEST_PROTOCOL)


	def loadGraph(self, graphName, path = "./savedData/"):
		with open(path + graphName + ".pkl", "rb") as f:
			self.exploreList = pickle.load(f)


	def makeGraphData(self):
		# For now, nodes should just be nodeId
		# For now, construct graph using dict method
		graphDict = {}
		for node in self.exploreList:
			graphDict[node['nodeId']] = node['adjNodeIds']
		nxGraph = nx.Graph(graphDict)
		return nxGraph


	def graph(self):
		G = self.makeGraphData()
		nx.draw(G)
		plt.show()
