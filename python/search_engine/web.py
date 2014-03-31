import cherrypy
import search

search.crawl("index.html")

form = "<html> \
		<body> \
			<h3>Search Engine</h3> \
			<form action='q' method='get'> \
				<input type='text' name='search_string'> \
				<input type='submit' value='Submit'> \
			</form> \
		</body> \
		</html>"

class HelloWorld(object):
	def index(self):
		return form

	def q(self, search_string):
		urls = search.query(search_string)
		results = "<html><body>"
		if urls != ["No results found."]:
			results += "<ul>"
			for url in urls:
				results += "<li><a href='"  + url[0] + "'>" + url[0] + "</a></li>"
			results += "</ul></body></html>"
		else:
			results += "No results found."
			results += "</body></html>"

		return results

	index.exposed = True
	q.exposed = True

cherrypy.quickstart(HelloWorld())