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

	def getAdjNodeIds(self, data):
		friendImg = data.find_all("img", src="/yoweb/images/matey.png")
		if len(friendImg) == 0:
			return []
		friendDiv = friendImg[0].parent.parent.parent.find_all('a')
		#print friendDiv
		friendList = [str(x.text) for x in friendDiv]
		#print friendList
		return friendList

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

	def getAdjNodeIds(self, data):
		allLinks = data.find_all("a")
		flagLinks = [x for x in allLinks if "flagid" in x['href']]
		return [link['href'].split('&')[0].split('=')[-1] for link in flagLinks]
		 




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



