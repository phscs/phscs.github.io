import cherrypy
import search

search.crawl("index.html")

form = "<html> \
		<body> \
			<form action='q' method='post'> \
				<input type='text' name='search_string'> \
				<input type='submit' value='Submit'> \
			</form> \
		</body> \
		</html>"

class HelloWorld(object):
	def index(self):
		return form
	index.exposed = True

	def q(self, search_string):
		return "<html><body>" + str(search.query(search_string)) + "</body></html>"
	q.exposed = True

cherrypy.quickstart(HelloWorld())