###################################
# CODE AUTHOR: GEORGE SKOUROUPATHIS
###################################
import crawler, rank, lookup, re

#Global variables
urlRelations = {}
index = {}
ranks = {}

#A class that stores the settings of the crawler
class settings():
	def __init__(self):
		settingsFile = open('app/data/settings.phoeby')
		for line in settingsFile.readlines():
			line = line.replace("\n", "")
			regex = re.match(r'\s*([a-zA-Z0-9]*)\s*=\s*(.*)', line)
			if regex:
				vars(self)[regex.group(1)] = regex.group(2)

#Starts crawling websites and saves the index and the urlRelations
def crawl():
	global urlRelations
	global index
	global ranks
	
	#Create the settings needed to crawl
	s = settings()

	#Initialise urlRelations
	urlRelations = crawler.readPhoebyFile('urlRelations')
	
	#Initialise index
	index = crawler.readPhoebyFile('index')
	
	#Start crawling from the baseUrl defined in settings
	print "Crawling" , s.noOfUrls, "URLs, starting from: ", s.baseUrl
	crawler.construct_crawling_tables(s, [s.baseUrl], index, urlRelations)
	crawler.writePhoebyFile('index', index)
	crawler.writePhoebyFile('urlRelations', urlRelations)
	
	#Compute ranks
	print "Computing ranks for", len(urlRelations), "URLs"
	ranks = rank.compute_ranks(urlRelations)

#Searches for the supplied string, after computing the ranks
#The final results are based on the urlWeights, which take
#into account in how many pages each keyword is found
def search(keywordString):
	global index
	global ranks
	
	#Initialise urlRelations
	urlRelations = crawler.readPhoebyFile('urlRelations')
	
	#Initialise index
	index = crawler.readPhoebyFile('index')
	
	#Compute ranks
	ranks = rank.compute_ranks(urlRelations)
	
	urlWeights = lookup.lookup(index, keywordString)
	for url in urlWeights.keys():
		urlWeights[url] += ranks[url]
	sortedUrlWeights = sorted(urlWeights.items(), key=lambda x: x[1], reverse=True)
	return map(lambda x: x[0], sortedUrlWeights)
	
#Other stuff

version = 1.0

__doc__ = '''
A python library which provides web crawling capabilties. Good for web search engines.
Uses breadth-first search.
---------------
function crawl() :
Crawls the web according to the settings in the data/settings.phoeby file.
Call it before anyone uses search(). Can be called by running gather.py
---------------
function search(keywordString) :
Searches index for every word of three (3) or more letters in the string (keywordString)
supplied. Returns results in order of weights.
'''







