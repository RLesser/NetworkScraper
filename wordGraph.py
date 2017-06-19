#!/usr/bin/python

from networkScrape import NetworkScraper

class wordChange(NetworkScraper):
	"""docstring for wordChange"""
	def __init__(self):
		super(wordChange, self).__init__()

	def getWordsOfLength(self, length):
		if hasattr(self, wordList):
			return self.wordList
		else:
			with open("/usr/share/dict/web2", "rb") as f:
				self.wordList = [x for x in f if len(x) == length]

	def getDataSource(self, nodeId):
		data = nodeId
		return data

	def getEdgeData(self, data):
		currentWord = data
		adjacentWords = []
		for word in wordList:
			if len([i for i, j in zip(word, currentWord) if i == j]) == len(word)-1:
				adjacentWords.append(word)
		adjacentEdges = [self.makeEdgeObject(x) for x in adjacentWords]
		return adjacentEdges