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
		name = profileData.find("p", class_ = "username").text
		return name

	def getNodeProperties(self, data):
		DEFAULT_PHOTO_URL = "http://static.hypem.net/images/bg-album-art.gif"
		CUSTOM_PHOTO_BASE_URL = "http://s3.amazonaws.com/faces-s3.hypem.com"

		propertiesObj = {}
		profileData = data.find_all("div", class_ = "header-box")[0]

		if profileData.find("img")["src"] == DEFAULT_PHOTO_URL:
			propertiesObj['customPhoto'] = False
		elif CUSTOM_PHOTO_BASE_URL in profileData.find("img")["src"]:
			propertiesObj['customPhoto'] = True
		else:
			print "ERROR IN PHOTO PROPERTY"
			exit()

		nameLoc = profileData.find("p", class_ = "username").find("a")
		if nameLoc["href"][1:] == nameLoc.text:
			propertiesObj['customName'] = False
		else:
			propertiesObj['customName'] = True

		bigNums = profileData.find_all(class_ = "big-num")


		for num in bigNums:
			#print num.parent.text
			if "Favorite" in num.parent.text:
				propertiesObj['favorites'] = int(num.text.replace(",",""))
			elif "Friend" in num.parent.text:
				propertiesObj['friends'] = int(num.text.replace(",",""))
			else:
				print "ERROR IN FAVE / FRIENDS PROPERTY"
				exit()

		followData = profileData.find(class_ = "follow-information")

		for link in followData.find_all("a"):
			value = 0
			if link.text.split()[0] != "no":
				value = int(link.text.split()[0])


			if "blog" in link.text.split()[1]:
				propertiesObj["blogFollows"] = value;
			elif "artist" in link.text.split()[1]:
				propertiesObj["artistFollows"] = value;
			else:
				print "ERROR IN BLOG / ARTIST PROPERTY"
				exit()

		followData.find_all("a")[0].text.split()[0]
		#print followData.find_all("a")[1].text.split()[0]


		return propertiesObj
