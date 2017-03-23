#!/usr/bin/python

from networkScrape import NetworkScraper

class HypeMNetwork(NetworkScraper):
	"""docstring for HypeMNetwork"""
	def __init__(self):
		super(HypeMNetwork, self).__init__()

	def getDataSource(self, nodeId):
		# print "Entering getDataSource"
		PROF_ADDR = lambda userName: "http://hypem.com/" + userName + "/list_friends"
		soup = self.url_to_soup(PROF_ADDR(nodeId))
		return soup

	def getEdgeData(self, data):
		friendList = data.find_all("div", id = "track-list")
		friendList = friendList[0].find_all("div", class_ = "user header-box small")
		friendIds = [friend.find_all("a")[0]['href'][1:] for friend in friendList]
		friendObjs = [self.makeEdgeObject(fid) for fid in friendIds]
		return friendObjs

	def getNodeName(self, data):
		profileData = data.find_all("div", class_ = "header-box")[0]
		name = profileData.find_all("p", class_ = "username")[0].text
		return name
