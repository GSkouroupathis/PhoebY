###################################
# CODE AUTHOR: GEORGE SKOUROUPATHIS
###################################
import tornado.ioloop, tornado.web, os
import sys
sys.path.insert(0, os.path.abspath(".."))
from app import phoeby

#Main Handler
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('templates/main.html')

#Search Handler
class SearchHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('templates/search.html')

#API Handler
class APIHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('templates/api.html')
					
#Results Handler
class ResultsHandler(tornado.web.RequestHandler):
	def get(self):
		keywords = self.get_argument("searchQuery", None)
		if keywords == None or keywords=="what are you looking for?":
			self.redirect('/')
		else:
			results = phoeby.search(keywords)
			self.render('templates/results.html', results = results)
	
settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "."),
	"cookie_secret": "VVoVTzKXQAGZYdkL5fEmGeJ3FuYh1EQnp2XdTP1o/Vo2",
	"xsrf_cookies": True,
}

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/search", SearchHandler),
	(r"/results", ResultsHandler),
	(r"/api", APIHandler),
], **settings)

if __name__ == "__main__":
	application.listen(6666)
	print "Server running!"
	tornado.ioloop.IOLoop.instance().start()
