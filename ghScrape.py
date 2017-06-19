#!/usr/bin/python

from networkScrape import NetworkScraper

class GithubNetwork(NetworkScraper):
	"""docstring for GithubNetwork"""
	def __init__(self):
		super(GithubNetwork, self).__init__()

	def getDataSource(self, nodeId):
		print "\n", nodeId
		PROF_ADDR = lambda userName, page: "https://github.com/" + userName + \
											"?tab=following&page=" + str(page)
		soupList = []
		pageNum = 1
		lastPage = False

		while not lastPage:
			soupList.append(self.url_to_soup(PROF_ADDR(nodeId, pageNum)))
			lastPage = (soupList[-1].find(class_ = "paginate-container") == None or
						soupList[-1].find(class_ = "paginate-container").text.strip() == "" or
			   			soupList[-1].find(class_ = "pagination").find_all('a')[-1].text == "Previous")
			pageNum += 1
		return soupList

	def getEdgeData(self, data):
		allFollow = []
		for page in data:
			followDiv = page.find_all("div", class_ = "js-repo-filter")[0]
			followList = followDiv.find_all("span", class_ = "link-gray")
			followIds = [str(follow.text) for follow in followList]
			allFollow += followIds
		#print allFriendIds
		followObjs = [self.makeEdgeObject(fid) for fid in allFollow]
		return followObjs

	def getNodeName(self, data):
		data = data[0]
		name = data.find_all("span", class_ = "vcard-fullname")[0].text
		if name == "":
			name = None
		return name

	def getNodeProperties(self, data):
		data = data[0]

		propertiesObj = {}

		navInfo = data.find('nav', role = "navigation")
		statList = [x.span.text for x in navInfo.find_all('a')[1:]]
		statList = [int(stat.strip().replace(".","").replace("k",""))*100 
					if stat.strip()[-1] == "k" 
					else int(stat.strip()) 
					for stat in statList]

		propertiesObj['repositories'] = statList[0]
		propertiesObj['stars'] = statList[1]
		propertiesObj['followers'] = statList[2]
		propertiesObj['following'] = statList[3]

		profileBio = data.find_all('div', class_ = "user-profile-bio")
		if len(profileBio) > 0:
			propertiesObj['profileBio'] = str(profileBio[0].text.strip().encode("utf-8"))
		else:
			propertiesObj['profileBio'] = ""

		location = data.find_all('li', itemprop = "homeLocation")
		if len(location) > 0:
			propertiesObj['location'] = str(location[0].find(class_ ='p-label').text.strip().encode("utf-8"))
		else:
			propertiesObj['location'] = ""

		organization = data.find_all("li", {"aria-label" : "organization"})
		if len(organization) > 0:
			propertiesObj['organization'] = str(organization[0].text.replace("@","").strip().encode("utf-8"))
		else:
			propertiesObj['organization'] = ""

		return propertiesObj

		