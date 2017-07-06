#!/usr/bin/python

from networkScrape import NetworkScraper
import string

class ArtistNetwork(NetworkScraper):
	"""docstring for ArtistNetwork"""
	def __init__(self):
		super(ArtistNetwork, self).__init__()
		
	def getDataSource(self, nodeId):
		print nodeId
		artistURL = lambda artistId: "https://www.last.fm/music/" + artistId
		soup = self.url_to_soup(artistURL(nodeId))
		return soup

	def getEdgeData(self, data):
		relatedList = data.find_all("ol", class_ = "grid-items")[-1]
		if relatedList.find(itemprop = "album") != None:
			return []
		links = relatedList.find_all("a", class_ = "link-block-cover-link")
		ids = [link["href"].replace("/music/","") for link in links]
		edgeObjs = [self.makeEdgeObject(nodeId) for nodeId in ids]
		return edgeObjs

	def getNodeName(self, data):
		title = data.find("h1", class_ = "header-title")
		return title.text.strip()

	def getNodeProperties(self, data):
		propertiesObj = {}

		# rank
		rankDivs = data.find_all("button", class_ = "header-popularity-rank")
		if len(rankDivs) == 0:
			propertiesObj["top 100"] = "not top 100"
			propertiesObj["rank"] = "Unranked"
		else:
			propertiesObj["top 100"] = "top 100"
			propertiesObj["rank"] = rankDivs[0].text.strip()

		# scrobbles
		scrobblesDiv = data.find("li", class_ = "header-metadata-item--scrobbles")
		scrobbleNum = int(scrobblesDiv.find("abbr")["title"].replace(",",""))
		propertiesObj["scrobbles"] = scrobbleNum

		# listeners
		listenerDiv = data.find("li", class_ = "header-metadata-item--listeners")
		listenerNum = int(listenerDiv.find("abbr")["title"].replace(",",""))
		propertiesObj["listeners"] = listenerNum

		# top tag
		tags = data.find_all("li", class_ = "tag", itemprop = "genre")
		propertiesObj["top tag"] = tags[0].text.strip().replace("-"," ")
		propertiesObj["tag list"] = [tag.text.strip() for tag in tags]

		return propertiesObj


class TagNetwork(NetworkScraper):
	"""docstring for TagNetwork"""
	def __init__(self):
		super(TagNetwork, self).__init__()
		
	def getDataSource(self, nodeId):
		print nodeId
		tagURL = lambda tag: "https://www.last.fm/tag/" + tag
		soup = self.url_to_soup(tagURL(nodeId))
		return soup

	def getEdgeData(self, data):
		tagSection = data.find("section", class_ = "tag-section")
		if tagSection == None:
			return []
		tags = [tagDiv['href'].replace("/tag/","") for tagDiv in tagSection.find_all("a")]
		edgeObjs = [self.makeEdgeObject(nodeId) for nodeId in tags]
		return edgeObjs

	def getNodeName(self, data):
		title = data.find("h1", class_ = "header-title")
		return title.text.strip()

	def getNodeProperties(self, data):
		propertiesObj = {}
		# top 5 artist listeners
		artistsDiv = [x for x in data.find_all("div", class_ = "selectable-range")
					  if "More artists" in x.text]
		if artistsDiv == []:
			return {}
		listenerDivs= artistsDiv[0].find_all(class_ = "grid-items-item-aux-text")
		listenerNums = [int(div.text.strip().replace(",","").split(" ")[0]) for div in listenerDivs
						if div.text.strip() != ""]
		propertiesObj["top 5 listener sum"] = sum(listenerNums)
		return propertiesObj





