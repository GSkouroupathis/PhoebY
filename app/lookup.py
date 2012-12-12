###################################
# CODE AUTHOR: GEORGE SKOUROUPATHIS
###################################
import re

#Returns the URLs that associate with the given keyword(s), along with their weights
def lookup(index, keywordString):

	indexedUrls = [] #URLs associated
	urlWeights = {} #number os keywords each URL has
	
	#Modifies indexedUrls
	for keyword in re.findall(r'([a-zA-Z0-9]{3,})', keywordString):
		if keyword in index:
			indexedUrls = indexedUrls + index[keyword]
	
	#Modifies urlWeights
	for url in indexedUrls:
		if url in urlWeights.keys():
			urlWeights[url] += 1
		else:
			urlWeights[url] = 1
		
		#Searched whether the keyword is in the URL
		for keyword in re.findall(r'([a-zA-Z0-9]{3,})', keywordString):
			if url.find(keyword) != -1:
				urlWeights[url] += 100

	return urlWeights
