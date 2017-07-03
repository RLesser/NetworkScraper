#!/usr/bin/python

from networkScrape import NetworkScraper


class pppNetwork(NetworkScraper):
	"""network scraping subclass specifically for Puzzle Pirate pirates"""
	def __init__(self):
		super(pppNetwork, self).__init__()
		self.ocean = "cerulean"

	def setOcean(self, ocean = "cerulean"):
		self.ocean = ocean

	def getDataSource(self, nodeId):
		# print "Entering getDataSource"
		BASE_ADDR = "http://" + self.ocean + ".puzzlepirates.com/yoweb"
		PIRATE_STR = lambda nodeId: "/pirate.wm?target=" + nodeId
		soup = self.url_to_soup(BASE_ADDR + PIRATE_STR(nodeId))
		return soup

	def getEdgeData(self, data):
		friendImg = data.find_all("img", src="/yoweb/images/matey.png")
		if len(friendImg) == 0:
			return []
		friendDiv = friendImg[0].parent.parent.parent.find_all('a')
		#print friendDiv
		friendEdges = [self.makeEdgeObject(str(x.text)) for x in friendDiv]
		#print friendList
		return friendEdges


class ppfNetwork(NetworkScraper):
	"""network scraping subclass specifically for Puzzle Pirate flags"""
	def __init__(self):
		super(ppfNetwork, self).__init__()
		self.ocean = "cerulean"

	def setOcean(self, ocean = "cerulean"):
		self.ocean = ocean

	def getDataSource(self, nodeId):
		print nodeId
		BASE_ADDR = "http://" + self.ocean + ".puzzlepirates.com/yoweb"
		FLAG_STR = lambda nodeId: "/flag/info.wm?flagid=" + str(nodeId)
		soup = self.url_to_soup(BASE_ADDR + FLAG_STR(nodeId))
		return soup

	def getNodeName(self, data):
		flagName = data.find_all("font", size="+2")[0].text
		return flagName

	def getEdgeData(self, data):
		allLinks = data.find_all("a")
		flagLinks = [x for x in allLinks if "flagid" in x['href']]

		if len(flagLinks) == 0:
			return []

		edges = {}

		currentType = ""

		for item in flagLinks[0].parent:
			if item != "\n" and item.name != "br":
				if item.text == "At war with:":
					currentType = "war"
				elif item.text == "Allied with:":
					currentType = "ally"
				elif item.text == "Declaring war against:":
					currentType = "attempt war"
				elif item.text == "Trying to form an alliance with:":
					currentType = "attempt ally"
				elif item.text.split("\n")[0] == "Islands controlled by this flag:":
					break

				else:
					nodeId = item["href"].split("&")[0].split("=")[-1]
					edges[nodeId] = {"status": currentType}

		flagEdges = [self.makeEdgeObject(flagId, edges[flagId]) for flagId in edges.keys()]

		return flagEdges

	def getNodeProperties(self, data):
		propertyObj = {}

		# islands
		islandNum = len([x for x in data.find_all("a") if "/island/" in x["href"]])
		propertyObj["islands controlled"] = islandNum

		# fame
		fame = [x.text for x in data.find_all("a") if "/ratings/" in x["href"]][0]
		propertyObj["fame"] = fame

		# reputation

		repImgs = [x for x in data.find_all("a") if "/ratings/" in x["href"]][1:]
		repText = [x.parent.parent.text.strip() for x in repImgs]
		propertyObj["conqueror rep"] = repText[0]
		propertyObj["explorer rep"] = repText[1]
		propertyObj["patron rep"] = repText[2]
		propertyObj["magnate rep"] = repText[3]

		# crew

		tableList = [x for x in data.find_all("table") \
					     if "align" in x.attrs and "center" == x.attrs["align"]]

		if len(tableList) < 3:
			totalMembers = totalCrews = totalPopulatedCrews = 0
		else:
			crewTable = tableList[-1]
			crewSizes = [x.text.strip().split("\n")[-1] for x in crewTable.find_all("tr")[1:]]
			totalMembers = int(crewSizes[-1])
			totalCrews = len(crewSizes) - 1
			totalPopulatedCrews = len([x for x in crewSizes[:-1] if int(x) > 0])

		propertyObj["total members"] = totalMembers
		propertyObj["total crews"] = totalCrews
		propertyObj["total real crews"] = totalPopulatedCrews

		return propertyObj

