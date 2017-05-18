#!/usr/bin/python

from networkScrape import NetworkScraper
import datetime


class HypeMNetwork(NetworkScraper):
	"""docstring for HypeMNetwork"""
	def __init__(self):
		super(HypeMNetwork, self).__init__()

	def getDataSource(self, nodeId):
		# print "Entering getDataSource"
		print nodeId
		PROF_ADDR = lambda userName: "http://hypem.com/" + userName + "/list_friends"
		soup = self.url_to_soup(PROF_ADDR(nodeId))
		pageInfo = soup.find('div', class_ = "paginator infinite")
		soupList = [soup]
		if pageInfo:
			numList = [int(str(x.text.encode("utf-8"))) for x in pageInfo.find_all("a")
					   if str(x.text.encode("utf-8")).isdigit()]
			if len(numList) != 0:
				maxPages = max(numList)
				for pNum in range(2,maxPages+1):
					soupList.append(self.url_to_soup(PROF_ADDR(nodeId)+"/"+str(pNum)))
		return soupList

	def getEdgeData(self, data):
		allFriendIds = []
		for page in data:
			friendList = page.find_all("div", id = "track-list")
			friendList = friendList[0].find_all("div", class_ = "user header-box")
			friendIds = []
			for friend in friendList:
				friendData = friend.find("div", class_ = "infoslices").find_all("a")
				friendFriends = friendData[1].find("span", class_ = "big-num")
				friendFriendCount = int(friendFriends.text.replace(",",""))
				if friendFriendCount < 1000: # only real people!
					friendIds.append(friend.find_all("a")[0]['href'][1:])
			#print friendIds
			allFriendIds += friendIds
		#print allFriendIds
		friendObjs = [self.makeEdgeObject(fid) for fid in allFriendIds]
		return friendObjs

	def getNodeName(self, data):
		data = data[0]
		profileData = data.find_all("div", class_ = "header-box")[0]
		name = profileData.find("p", class_ = "username").find('a').text.strip()
		return name

	def getNodeProperties(self, data):
		data = data[0]
		DEFAULT_PHOTO_URL = "http://static.hypem.net/images/user_profile_default.png"
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

		#print propertiesObj

		#print bigNums
		for num in bigNums:
			if "Favorite" in num.parent.text:
				propertiesObj['favorites'] = int(num.text.replace(",",""))
			elif "Friend" in num.parent.text:
				propertiesObj['friends'] = int(num.text.replace(",",""))
			elif "Site" in num.parent.text:
				propertiesObj['sites'] = int(num.text.replace(",",""))
			elif "Artist" in num.parent.text:
				propertiesObj['artists'] = int(num.text.replace(",",""))
			else:
				print "ERROR IN FAVE / FRIENDS PROPERTY"
				exit()

		dateStr = str(profileData.find('p', class_ = "join-date").text)
		dateList = dateStr.replace("Joined ", "").split()
		day = dateList[1][0:-3]
		if len(day) == 1:
			day = "0" + day
		dateList[1] = day
		dateStr = " ".join(dateList)
		dateObj = datetime.datetime.strptime(dateStr, "%b %d %Y")
		propertiesObj['joinDate'] = dateObj

		nameArea = profileData.find("p", class_ = "username")
		supporter = nameArea.find('a', class_ = 'supporter-badge')
		if supporter:
			propertiesObj['supporter'] = True
		else:
			propertiesObj['supporter'] = False

		return propertiesObj
