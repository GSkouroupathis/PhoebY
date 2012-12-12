###################################
# CODE AUTHOR: GEORGE SKOUROUPATHIS
###################################
import urllib, re
from BeautifulSoup import BeautifulSoup

#Global variables
noOfUrlsCrawled = 0
urlsVisited = []

#Crawls recursively and returns index and urlRelations
def construct_crawling_tables(s, baseUrls, index, urlRelations):
	global noOfUrlsCrawled
	global urlsVisited
	urlChildrenToCrawl = []
	
	#Extract the required crawling settings
	noOfUrls = int(s.noOfUrls)
	noOfUrlChildren = int(s.noOfUrlChildren)

	for baseUrl in baseUrls:
		if baseUrl in urlsVisited: continue

		#Return at most the first 'noOfUrls' sites
		if noOfUrlsCrawled == noOfUrls:	return
		
		print "Crawling", str(baseUrl) + "..."
		#Inform about the progress of crawling
		print len(urlRelations), "URLs crawled in total"
		
		#Try to connect to the website
		try:
			page = urllib.urlopen(baseUrl).read()
		except:
			print "Failed to connect to", baseUrl
			continue
		
		#Construct index
		if baseUrl not in urlRelations.keys():
			add_page_to_index(baseUrl, page, index)
			#New URL is found
			noOfUrlsCrawled += 1
		
		urlsVisited.append(baseUrl)
		#Construct urlRelations
		try:
			urlRelations[baseUrl] = construct_urlChildren(page, baseUrl, noOfUrlChildren)
			urlChildrenToCrawl.extend(urlRelations[baseUrl])
		except:
			print "Cannot find children of", baseUrl
	
	#Continue constructing urlRelations
	print urlChildrenToCrawl
	construct_crawling_tables(s, urlChildrenToCrawl, index, urlRelations)

#Finds the url children of every page
def construct_urlChildren(page, baseUrl, noOfUrlChildren):
	print " > Crawling for children for", baseUrl + "..."
	#Construct the children URLs (at most noOfUrlChildren)
	urlChildren = []
	soup = BeautifulSoup(page)
	for urlChild in soup.findAll('a', href=True):
		#link has to be absolute and not repeated and not the same as the mother-url
		if re.match(r'(http://|https://).*[^ef]$', urlChild['href']) and urlChild['href'] not in urlChildren and urlChild['href'] != baseUrl:
			urlChildren.append(urlChild['href'])
			print "   >>  Crawled URL child:", urlChild['href']
	
	return urlChildren

#Adds a page to the index
def add_page_to_index(url, page, index):
    for keyword in re.findall(r'([a-zA-Z0-9]{3,})', page): #find all words with 4+ letters
        add_to_index(keyword, url, index)

#Adds or updates a keyword to the index
def add_to_index(keyword, url, index):
#adds the keyword to the index along with the URLs that contain it
	if keyword in index.keys():
		if url not in index[keyword]:
			index[keyword].append(url)
	else:
		index[keyword] = [url]

#writeDfFile
def writePhoebyFile(phoebyFile, dc):
	with open('app/data/%s.phoeby' %phoebyFile, 'w') as phoebyFile:
		for key in dc.keys():
			phoebyFile.write(key)
			for value in dc[key]:
				try: #fix
					phoebyFile.write("," + value)
				except:
					pass
			phoebyFile.write("\n")

#readDfFile
def readPhoebyFile(phoebyFile):
	dc = {}
	with open('app/data/%s.phoeby' %phoebyFile, 'r') as phoebyFile:
		for line in phoebyFile.readlines():
			line = line.replace("\n", "")
			listComponents = line.split(",")
			dc[listComponents[0]] = listComponents[1:]
	return dc
