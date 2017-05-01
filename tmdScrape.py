#!/usr/bin/python

from networkScrape import NetworkScraper

class TMDNetwork(NetworkScraper):
	"""docstring for TMDNetwork"""
	def __init__(self):
		super(TMDNetwork, self).__init__()

	def getDataSource(self, nodeId):
		# print "Entering getDataSource"
		PROF_ADDR = lambda articleName: "https://www.michigandaily.com/section/" + articleName
		soup = self.url_to_soup(PROF_ADDR(nodeId))
		return soup

	def getEdgeData(self, data):
		nodebox = data.find_all("div", class_ = "nodebox")[0]
		links = [x['href'] for x in nodebox.find_all("a")]
		article_IDs = [x.replace("/section/","") for x in links]
		edgeObjs = [self.makeEdgeObject(a_id) for a_id in article_IDs]
		return edgeObjs

	def getNodeName(self, data):
		titleDiv = data.find_all("div", class_ = "pane-node-title")[0]
		# profileData = data.find_all("div", class_ = "header-box")[0]
		# name = profileData.find("p", class_ = "articleName").text
		# return name
		return titleDiv.text.strip()

	def getNodeProperties(self, data):
		propertiesObj = {}

		kicker = data.find("div", class_ = "pane-node-field-kicker")
		if kicker:
			kicker = kicker.text.strip()
		else:
			kicker = ""
		propertiesObj['kicker'] = kicker

		#section = data.find_all("")

		return propertiesObj