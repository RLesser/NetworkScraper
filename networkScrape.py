#!/usr/bin/python

import urllib2
import bs4
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import webbrowser
import os
import json
import SimpleHTTPServer
import datetime

class UndefinedFunctionError(Exception):
	pass

class NetworkScraper(object):
	"""base class for scraping websites for network connections"""
	def __init__(self):
		super(NetworkScraper, self).__init__()
		# exploreList is a list of nodes
		self.exploreList = []
		# relationDict has the nodeId's as keys
		# self.relationDict = {}




	### GENERAL UTILITY FUNCTIONS ###
	def url_to_soup(self, url):
	    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
	    html = urllib2.urlopen(req).read()
	    soup = bs4.BeautifulSoup(html)
	    return soup


	def saveGraph(self, graphName, path = "./savedData/"):
		with open(path + graphName + ".pkl", "wb") as f:
			pickle.dump([self.exploreList, self.nodeExplorations], f, pickle.HIGHEST_PROTOCOL)


	def loadGraph(self, graphName, path = "./savedData/"):
		with open(path + graphName + ".pkl", "rb") as f:
			loadedData = pickle.load(f)
			self.exploreList = loadedData[0]
			self.nodeExplorations = loadedData[1]


	def basicWebServer(self):
		import SimpleHTTPServer
		import SocketServer

		PORT = 8000

		Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

		while (True):
			try:
				print "Trying to open on port", PORT
				httpd = SocketServer.TCPServer(("", PORT), Handler)
			except Exception as e:
				print "port", PORT, "did not work, checking next port"
				PORT += 1
			else:
				break

		print "serving at port", PORT
		webbrowser.open("http://localhost:"+str(PORT)+"/forceD3/force.html")
		httpd.serve_forever()



	### FUNCTIONS TO BE DEFINED IN SUBCLASSES ###
	def getDataSource(self, nodeId):
		raise UndefinedFunctionError("getDataSource must be defined in a subclass. "
									 "View the docstring for more info on implimentation")


	def getNodeName(self, data):

		return None


	def getEdgeData(self, data):
		raise UndefinedFunctionError("getEdgeData must be defined in a subclass. "
									 "View the docstring for more info on implimentation")


	def makeEdgeObject(self, nodeId, edgeVisible = True):
		edge = {
			'nodeId': nodeId,
			'edgeVisible': edgeVisible
		}
		return edge


	def getNodeProperties(self, data):
		emptyDict = {}
		return emptyDict



	### GRAPH PROPEGATION AND ASSOCIATED FUNCTIONS ###
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



	### GRAPH COMPILATION AND ASSOCIATED FUNCTIONS ###
	def createGraphDict(self):
		graphDict = {}
		#setting the graph dict with keys being the nodes and vals being connections
		for nodeIdx in range(len(self.exploreList)):
			#print self.exploreList
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
			if self.nodeExplorations == None:
				self.nodeExplorations = len(self.exploreList)
			if nodeIdx < self.nodeExplorations or self.buds_visible:
				#print "adding node:", node['nodeId']
				graphDict[node['nodeId']] = adjNodes
		return graphDict


	def filterUnreciprocatedEdges(self, graphDict):
		# print graphDict
		for node in graphDict:
			print node, graphDict[node]
			symEdges = [edge for edge in graphDict[node]
						if (node in graphDict[edge])]
			graphDict[node] = symEdges
		return graphDict


	def removeOrphanNodes(self, graphDict):
		newGraph = { k:v for k,v in graphDict.items() if v != []}
		return newGraph


	def makeGraphData(self, mode = 'networkx'):
		# For now, nodes should just be nodeId
		# For now, construct graph using dict method
		graphDict = self.createGraphDict()

		# Three bools: 
		# removeBuds, filterEdges, removeOrphans -> Non-syms, bud-edges, bud-nodes, bud-like-edges, bud-like-nodes
		# F,F,F -> T,T,T,T,T - All possible nodes and edges
		# T,F,F -> T,F,F,T,T - All non-bud nodes and non-bud edges
		# F,T,F -> F,F,T,F,T - All sym edges, all buds and bud-like are orphan graphs
		# T,T,F -> F,F,F,F,T - All sym edges, only bud-like are orphan graphs
		# F,F,T -> ERROR
		# T,F,T -> ERROR
		# F,T,T -> F,F,F,F,F - All sym edges, all buds removed
		# T,T,T -> F,F,F,F,F - All sym edges, all buds removed

		# Decision:
		# Only allow removeBuds and filterEdges, have removeOphans as part of filterEdges

		if self.filter_assym_edges:
			graphDict = self.filterUnreciprocatedEdges(graphDict)
			graphDict = self.removeOrphanNodes(graphDict)

		#print graphDict
		if mode == 'networkx':
			nxGraph = nx.Graph(graphDict)
			for node in self.exploreList:
				if node['nodeId'] in nxGraph.node:
					#print node['nodeId']
					nxGraph.node[node['nodeId']] = node['properties']
			return nxGraph


		elif mode == 'd3':
			nodeList = []
			linkList = []
			for item in graphDict:
				infoGen = (node for node in self.exploreList if node['nodeId'] == item)
				#print item
				nodeInfo = infoGen.next()
				nodeObj = {}
				nodeObj['id'] = item
				nodeObj['name'] = nodeInfo['name']
				nodeObj['properties'] = nodeInfo['properties']
				# datetimes need to be edited for the json
				for prop in nodeObj['properties']:
					if isinstance(nodeObj['properties'][prop], datetime.datetime):
						nodeObj['properties'][prop] = str(nodeObj['properties'][prop])
				nodeList.append(nodeObj)
				for link in graphDict[item]:
					linkObj = {}
					linkObj['source'] = item
					linkObj['target'] = link
					linkObj['value'] = 1
					linkList.append(linkObj)
			graphObj = {
				"nodes" : nodeList,
				"links" : linkList
			}
			return graphObj
			#print graphDict



	### GRAPH USER INTERACTION AND ASSOCIATED FUNCTIONS ###
	def colorNodes(self, colorType = "cat", keyProperty = None, colorList = None, colorDict = None):
		if not colorList:
			colorList = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
						 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', 
						 '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', 
						 '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']
		self.nodeColorInfo = {}
		self.nodeColorInfo['type'] = colorType
		self.nodeColorInfo['keyProperty'] = keyProperty
		self.nodeColorInfo['colorList'] = colorList


	def useColorData(self, G, mode):
		nodeColors = []
		termToColorIdx = {}
		currentColorIdx = 0
		colorType = self.nodeColorInfo['type']
		key = self.nodeColorInfo['keyProperty']
		colorList = self.nodeColorInfo['colorList']
		if mode == "networkx":
			if colorType == "cat":
				for node in G.node:
					if key not in G.node[node]:
						nodeColors.append('#FFFFFF')
					else:
						if G.node[node][key] not in termToColorIdx:
							termToColorIdx[G.node[node][key]] = currentColorIdx
							currentColorIdx += 1
						colorIdx = termToColorIdx[G.node[node][key]]
						color = colorList[colorIdx]
						nodeColors.append(color)
			elif colorType == "scale":
				print "not yet implimented"
				exit(1)
			return nodeColors
		elif mode == "d3":
			if colorType == "cat":
				for nodeIdx in range(len(G['nodes'])):
					node = G['nodes'][nodeIdx]
					if key not in node['properties']:
						node['color'] = '#FFFFFF'
					else:
						if node['properties'][key] not in termToColorIdx:
							termToColorIdx[node['properties'][key]] = currentColorIdx
							currentColorIdx += 1
							currentColorIdx %= len(colorList)
						colorIdx = termToColorIdx[node['properties'][key]]
						color = colorList[colorIdx]
						node['color'] = color
					G['nodes'][nodeIdx] = node
			elif colorType == "scale":
				print "not yet implimented"
				exit(1)
			return G


	def graphNetworkx(self, buds_visible = False, filter_assym_edges = False, labels_visible = True, iterations = 1000):
		self.buds_visible = buds_visible
		self.filter_assym_edges = filter_assym_edges
		G = self.makeGraphData()
		if hasattr(self, 'nodeColorInfo'):
			nodeColors = self.useColorData(G, 'networkx')
		#print G.node
		if labels_visible:
			nx.draw_networkx(G, pos=nx.spring_layout(G, iterations = iterations), node_color = nodeColors, linewidths = 1)
		else:
			nx.draw(G, pos=nx.spring_layout(G, iterations = iterations), node_color = nodeColors, linewidths = 1)
		plt.show()


	def graphD3(self, buds_visible = False, filter_assym_edges = False):
		# possibly combine with above?
		self.buds_visible = buds_visible
		self.filter_assym_edges = filter_assym_edges
		G = self.makeGraphData(mode = "d3")
		print G
		if hasattr(self, 'nodeColorInfo'):
			G = self.useColorData(G, "d3")
		# for item in adjList:
		# 	print item
		#nodeColors = self.useColorData(G)
		#for item in nx.readwrite.__dict__:
			#print item
		# nodeLinkData = nx.readwrite.d3_js(G)
		#print G
		json.dump(G, open('forceD3/force.json','w'))
		self.basicWebServer()
