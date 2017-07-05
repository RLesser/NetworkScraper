#!/usr/bin/python

from networkScrape import NetworkScraper
import string

class ArtistNetwork(NetworkScraper):
	"""docstring for ArtistNetwork"""
	def __init__(self):
		super(ArtistNetwork, self).__init__()

	def convertToURL(self, nodeId):
		return nodeId

	def convertFromURL(self, nodeId):
		return nodeId
		
	def getDataSource(self, nodeId):
		print nodeId
		nodeId = self.convertToURL(nodeId)
		PROF_ADDR = lambda artistId: "https://www.last.fm/music/" + artistId
		soup = self.url_to_soup(PROF_ADDR(nodeId))
		return soup

	def getEdgeData(self, data):
		relatedList = data.find_all("ol", class_ = "grid-items")[-1]
		links = relatedList.find_all("a", class_ = "link-block-cover-link")
		ids = [self.convertFromURL(link["href"].replace("/music/","")) for link in links]
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




