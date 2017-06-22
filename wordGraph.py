#!/usr/bin/python

from networkScrape import NetworkScraper

class WordChange(NetworkScraper):
	"""docstring for WordChange"""
	def __init__(self):
		super(WordChange, self).__init__()

	def getWordsOfLength(self, length):
		if not hasattr(self, 'wordList'):
			with open("engWordList.txt", "rb") as f:
				self.wordList = [x.strip().lower() for x in f if len(x.strip()) == length]
				print len(self.wordList)

	def getDataSource(self, nodeId):
		self.getWordsOfLength(len(nodeId))
		data = nodeId
		return data

	def getEdgeData(self, data):
		currentWord = data
		adjacentWords = []
		for word in self.wordList:
			if len([i for i, j in zip(word, currentWord) if i == j]) == len(word)-1:
				adjacentWords.append(word)
		print adjacentWords
		adjacentEdges = [self.makeEdgeObject(x) for x in adjacentWords]
		return adjacentEdges

	def getNodeProperties(self, data):
		propertiesObj = {}
		word = data
		vowels = [l for l in word if l in "aeiou"]
		propertiesObj["vowels"] = "".join(sorted(vowels))
		vowelPos = [str(idx) for idx in range(len(word)) if word[idx] in "aeiou"]
		propertiesObj["vowelPos"] = "".join(vowelPos)

		return propertiesObj




