#!/usr/bin/python

from networkScrape import NetworkScraper

class pppNetwork(NetworkScraper):
	"""network scraping subclass specifically for Puzzle Pirate pirates"""
	def __init__(self):
		super(pppNetwork, self).__init__()

	def getDataSource(self, nodeId):
		# print "Entering getDataSource"
		BASE_ADDR = "http://emerald.puzzlepirates.com/yoweb"
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

	def getDataSource(self, nodeId):
		BASE_ADDR = "http://emerald.puzzlepirates.com/yoweb"
		FLAG_STR = lambda nodeId: "/flag/info.wm?flagid=" + str(nodeId)
		soup = self.url_to_soup(BASE_ADDR + FLAG_STR(nodeId))
		return soup

	def getNodeName(self, data):
		flagName = data.find_all("font", size="+2")[0].text
		return flagName

	def getEdgeData(self, data):
		allLinks = data.find_all("a")
		flagLinks = [x for x in allLinks if "flagid" in x['href']]

		visibleStatus = ""
		colorStatus = ""
		visibleStatusDict = {}
		colorStatusDict = {}
		if len(flagLinks) == 0:
			return []
		for item in flagLinks[0].parent.text.split('\n'):

			if item == "At war with:":
				visibleStatus = True
				colorStatus = "r"
			elif item == "Allied with:":
				visibleStatus = True
				colorStatus = "g"
			elif item == "Declaring war against:":
				visibleStatus = False
				colorStatus = ""
			elif item == "Trying to form an alliance with:":
				visibleStatus = False
				colorStatus = ""
			elif item == "Islands controlled by this flag:":
				visibleStatus = "islands"
			elif visibleStatus != "islands":
				visibleStatusDict[item] = visibleStatus
				colorStatusDict[item] = colorStatus

		#print visibleStatusDict
		#print colorStatusDict

		idDict = {}
		for link in flagLinks:
			idDict[link['href'].split('&')[0].split('=')[-1]] = link.text

		#print idDict

		flagEdges = [self.makeEdgeObject(flagId) \
					 for flagId in idDict.keys()]

		#print flagEdges
		return flagEdges
		 




	# def getConnections(self, flagId):
	# 	allLinks = flagSoup.find_all("a")
	# 	flagLinks = [x for x in allLinks if "flagid" in x['href']]
	# 	# if len(friendImg) == 0:
	# 	# 	return []
	# 	# friendDiv = friendImg[0].parent.parent.parent.find_all('a')
	# 	# #print friendDiv
	# 	# friendList = [str(x.text) for x in friendDiv]
	# 	# #print friendList
	# 	# return friendList
		

if __name__ == '__main__':
	x = pppNetwork()
	x.propegateGraph('Sugara', limit = 20, verbose = True)
	x.graph()



