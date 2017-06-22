#!/usr/bin/python

from networkScrape import NetworkScraper

class CountyGraph(NetworkScraper):
	"""docstring for CountyGraph"""
	def __init__(self):
		super(CountyGraph, self).__init__()
		
	def getCountyData(self):
		if not hasattr(self, 'countyDict'):
			with open("county_adjacency.txt", "rb") as f:
				self.countyDict = {}
				for county in f.read().split("\n\""):
					counties = county.replace("\t\t","\t").replace("\"","").split("\t")
					counties = ["|".join(item) for item in zip(counties[0::2], counties[1::2])]
					self.countyDict[counties[0].split("|")[1]] = [item.strip() for item in counties[1:]]

	def getDataSource(self, nodeId):
		self.getCountyData()
		nodeId = str(nodeId)
		data = (nodeId, self.countyDict[nodeId])
		return data

	def getNodeName(self, data):
		currentCounty = [x for x in data[1] if x.split("|")[1] == data[0]][0]
		print currentCounty.split("|")[0].strip()
		return currentCounty.split("|")[0].strip()

	def getEdgeData(self, data):
		adjCounties = [self.makeEdgeObject(x.split("|")[1]) for x in data[1] 
					 		if data[0] != x.split("|")[1]]
		print adjCounties
		return adjCounties

	def getNodeProperties(self, data):
		propertiesObj = {}
		currentCounty = [x for x in data[1] if x.split("|")[1] == data[0]][0]
		propertiesObj["countyId"] = int(currentCounty.split("|")[1])
		propertiesObj["state"] = currentCounty.split("|")[0].split(",")[-1].strip()
		return propertiesObj
