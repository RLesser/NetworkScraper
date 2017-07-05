#!/usr/bin/python

from networkScrape import NetworkScraper

class ArtistNetwork(NetworkScraper):
	"""docstring for ArtistNetwork"""
	def __init__(self):
		super(ArtistNetwork, self).__init__()
		
	def getDataSource(self, nodeId):
		nodeId = nodeId.replace("_","+")
		PROF_ADDR = lambda artistId: "https://www.last.fm/music/" + artistId
		soup = self.url_to_soup(PROF_ADDR(nodeId))
		return soup

	def getEdgeData(self, data):
		relatedList = data.find_all("ol", class_ = "grid-items")[-1]
		links = relatedList.find_all("a", class_ = "link-block-cover-link")
		ids = [link["href"].replace("/music/","").replace("+","_") for link in links]
		edgeObjs = [self.makeEdgeObject(nodeId) for nodeId in ids]
		return edgeObjs

	def getNodeName(self, data):
		title = data.find("h1", class_ = "header-title")
		return title.text.strip()

