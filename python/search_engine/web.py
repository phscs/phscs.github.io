import cherrypy as cp
import search as se

se.crawl("index.html")

home = "<html>\
	<body onLoad='document.search_form.query.focus()'>\
	<form action='search' method='get' name='search_form'>\
		<input type='text' name='query' value=''/>\
		<input type='submit' value='Search'/>\
	</form>\
	</body>\
	</html>"

class SearchEngine(object):
	def index(self):
		return home

	def search(self, query=None):
		index_results = se.query(query)
		response = 	"<html>\
				<body onLoad='document.search_form.query.focus()'>\
				<form action='search' method='get' name='search_form'>\
					<input type='text' name='query' value=''/>\
					<input type='submit' value='Search'/>\
				</form>"
		response += "<p>Results for: <i>" + query + "</i></p>"
		if index_results != None:		
			response += "<ul>"
			for entry in index_results:
				response += "<li><a href='" + entry[0] + "'>" + entry[0] + "</a></li>"
			response += "</ul>"
		response += "<a href='/'>[home]</a>"
		response += "</body></html>"
		return response

	index.exposed = True
	search.exposed = True

cp.quickstart(SearchEngine())
