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


	def getNodeColor(self, data):
		return 'r'


	def getEdgeData(self, data):
		return None


	def makeEdgeObject(self, nodeId, edgeColor = 'r', edgeVisible = True):
		edge = {
			'nodeId': nodeId,
			'edgeColor': edgeColor,
			'edgeVisible': edgeVisible
		}
		return edge

	def getNodeProperties(self, data):
		return {}

	def makeBaseNode(self, nodeId):
		# print "Entering makeBaseNode"
		node = {
			'name': None,
			'nodeId': nodeId,
			'nodeColor': None,
			'edges': [],
			'properties': {}
		}
		return node


	def fillNodeData(self, node):
		# print "Entering fillNodeData"
		data = self.getDataSource(node['nodeId'])
		name = self.getNodeName(data)
		# print "node name:", node['nodeId']
		if name == None:
			name = node['nodeId']
		node['name'] = name
		node['nodeColor'] = self.getNodeColor(data)
		node['edges'] = self.getEdgeData(data)
		node['properties'] = self.getNodeProperties(data)
		#print node
		return node


	def getNewNodes(self, seedNode):
		# print "Entering getNewNodes"
		newNodes = [self.makeBaseNode(edge['nodeId']) for edge in seedNode['edges']]
		return newNodes


	def getUniqueConnections(self, connectionList):
		currNodeList = [x['nodeId'] for x in self.exploreList]
		uniqueList = [x for x in connectionList if x['nodeId'] not in currNodeList]
		return uniqueList


	def propegateGraph(self, nodeId, limit = None, verbose = False):
		self.exploreList.append(self.makeBaseNode(nodeId))
		curNodeIdx = 0
		self.nodeExplorations = None
		if limit != None:
			self.nodeExplorations = limit
		while (not limit or curNodeIdx < limit) \
			and curNodeIdx < len(self.exploreList):
			fullCurNode = self.fillNodeData(self.exploreList[curNodeIdx])
			self.exploreList[curNodeIdx] = fullCurNode
			if verbose:
				print curNodeIdx, '[', len(self.exploreList), ']',
				print self.exploreList[curNodeIdx]['name']
				print self.exploreList[curNodeIdx]['properties']
			newNodes = self.getNewNodes(self.exploreList[curNodeIdx])
			newUnusedNodes = self.getUniqueConnections(newNodes)
			self.exploreList += newUnusedNodes
			curNodeIdx += 1


	def saveGraph(self, graphName, path = "./savedData/"):
		with open(path + graphName + ".pkl", "wb") as f:
			pickle.dump([self.exploreList, self.nodeExplorations], f, pickle.HIGHEST_PROTOCOL)


	def loadGraph(self, graphName, path = "./savedData/"):
		with open(path + graphName + ".pkl", "rb") as f:
			loadedData = pickle.load(f)
			self.exploreList = loadedData[0]
			self.nodeExplorations = loadedData[1]


	def makeGraphData(self):
		# For now, nodes should just be nodeId
		# For now, construct graph using dict method
		graphDict = {}
		#setting the graph dict with keys being the nodes and vals being connections
		for nodeIdx in range(len(self.exploreList)):
			node = self.exploreList[nodeIdx]
			# if the node has edges...
			if len(node['edges']):
				# create a list of nodeIds from nodeEdges if the edge is visible
				# and not a bud (if buds_visible is False)
				budIdList = [item['nodeId'] for item in self.exploreList[self.nodeExplorations:]]
				isBud = lambda nodeId: nodeId in budIdList
				#print node['nodeId']
				# uncomment list comprehension once logic fixed
				adjNodes = [edge['nodeId'] for edge in node['edges'] \
							if edge['edgeVisible'] and \
							(not isBud(edge['nodeId']) or self.buds_visible)]

			else:
				# possible to have non-bud (aka explored) node w/o adjNodes
				adjNodes = []

			# if buds_visible is false, dont add buds to graphDict
			# could possibly end loop early but this works too
			if nodeIdx < self.nodeExplorations or self.buds_visible:
				#print "adding node:", node['nodeId']
				graphDict[node['nodeId']] = adjNodes

		#print graphDict
		nxGraph = nx.Graph(graphDict)
		for node in self.exploreList:
			if node['nodeId'] in nxGraph.node:
				print node['nodeId']
				nxGraph.node[node['nodeId']] = node['properties']
		return nxGraph

	#def color_nodes(self):



	def graph(self, buds_visible = True, labels_visible = True, iterations = 1000):
		self.buds_visible = buds_visible
		G = self.makeGraphData()
		print G.node
		if labels_visible:
			nx.draw_networkx(G, pos=nx.spring_layout(G, iterations = iterations), node_color = ['blue','red'])
		else:
			nx.draw(G, pos=nx.spring_layout(G, iterations = iterations), node_color = ['blue','red'])
		plt.show()
