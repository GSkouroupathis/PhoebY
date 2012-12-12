###################################
# CODE AUTHOR: GEORGE SKOUROUPATHIS
###################################

#Relaxation function
def compute_ranks(urlRelations):
	d = 0.8 # damping factor
	numloops = 10
    
	ranks = {}
	numUrls = len(urlRelations)
	for urlRelation in urlRelations.keys():
		ranks[urlRelation] = 1.0 / numUrls
    
	for i in range(numloops):
		newranks = {}
        	for urlRelation in urlRelations.keys():
			newrank = (1 - d) / numUrls
 	
			for outUrl in urlRelations[urlRelation]:
				if outUrl in urlRelations.keys(): #This is because the cralwer stops crawling at a point
								  # and outUrl might not have relations
					if urlRelation in urlRelations[outUrl]:
						newrank += d * (ranks[outUrl] / len(urlRelations[outUrl]))
				else:
					i += 1

			newranks[urlRelation] = newrank
		ranks = newranks
	return ranks
