import cherrypy
import search
import thread

thread.start_new_thread(search.crawl, ("http://premiergranbury.com/",))

form = "<html> \
	<body> \
		<h3>Search Engine</h3> \
		<form action='q' method='get'> \
			<input type='text' name='search_string'> \
			<input type='submit' value='Submit'> \
		</form> \
	</body> \
	</html>"

class SE(object):
	def index(self):
		return form

	def q(self, search_string):
		urls = search.query(search_string)
		results = "<html><body>"
		if urls != ["No results found."]:
			results += "<ul>"
			for url in urls:
				results += "<li>[" + str(url[1]) + "] <a href='"  + url[0] + "'>" + url[0] + "</a></li>"
			results += "</ul></body></html>"
		else:
			results += "No results found."
			results += "</body></html>"

		return results

	index.exposed = True
	q.exposed = True

cherrypy.quickstart(SE())
