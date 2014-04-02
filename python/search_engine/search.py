import urllib
import string
import pickledb
import urlparse

index = pickledb.load("index.db", False)
popularity_index = pickledb.load("popularity_index.db", False)

index.deldb()
popularity_index.deldb()

def get_links(source):
	print "getting links..."
	links = []
	link_temp = ""
	collecting_characters = False

	for i in range(0, len(source)):
		if source[i-6 : i] == 'href="' or source[i-6 : i] == "href='":
			collecting_characters = True

		if collecting_characters:
			if source[i] == '"' or source[i] == "'":
				collecting_characters = False
				links.append(link_temp)
				link_temp = ""
			else:
				link_temp = link_temp + source[i]

	return links

def get_keywords(source, url):
	print "getting keywords..."
	collecting_characters = False
	collected_characters = ""

	for i in range(0, len(source)):
		character = source[i]

		if character == "<":
			collecting_characters = False
		elif character == ">":
			collecting_characters = True
		elif collecting_characters:
			if character in string.punctuation or character in ["\t","\n","\r"]:
				collected_characters += " "
			else:
				collected_characters += character.lower()

	keywords = collected_characters.split(" ")

	while "" in keywords:
		keywords.remove("")

	for word in keywords:
		if word in keywords[keywords.index(word)+1:]:
			keywords.remove(word)

	return keywords

def add_to_index(url, keywords):
	for keyword in keywords:
		print "adding '" + keyword + "', " + url + " to index"
		urls = index.get(keyword)

		if urls == None:
			index.set(keyword, [[url, 0]])
		else:
			urls.append([url, 0])
			index.set(keyword, urls)

	index.dump()

def crawl(seed_page_url):
	urls_to_crawl = [seed_page_url]
	urls_already_crawled = []
	crawls = 0

	parsed_uri = urlparse.urlparse(seed_page_url)
	last_domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

	while len(urls_to_crawl) > 0 and crawls < 50:
		try:
			url = urls_to_crawl[0]				

			print "crawling " + url
			source = urllib.urlopen(url).read()

			keywords = get_keywords(source, url)
			add_to_index(url, keywords)

			uprank_relevance(keywords, source, url)

			links = get_links(source)

			for link in links:
				if link != url and link not in urls_already_crawled and link not in urls_to_crawl:

					parsed_uri = urlparse.urlparse(link)
					current_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

					if link[0:2] == "//":
						link = "http:" + link
					elif current_domain[0:4] != "http":
						link = last_domain[:len(last_domain)] + link
					elif current_domain != last_domain:
						last_domain = current_domain

					uprank_popularity(link)
					urls_to_crawl.append(link)

			popularity_index.dump()

		except:
			pass

		urls_to_crawl.remove(url)
		urls_already_crawled.append(url)
		crawls += 1

def uprank_popularity(url):
	print "upranking popularity of " + url
	popularity = popularity_index.get(url)

	if popularity == None:
		popularity = 0
	else:
		popularity += 1

	popularity_index.set(url, popularity)

def uprank_relevance(keywords, source, url):
	for keyword in keywords:
		urls = index.get(keyword)
		if urls != None:
			for entry in urls:
				if entry[0] == url:
					print "upranking relevance of " + entry[0] + " for " + keyword
					entry[1] = source.count(keyword)
		index.set(keyword, urls)

	index.dump()

def query(search_string):
	print "querying for '" + search_string + "'"
	sanitized_search_string = ""

	for character in search_string:
		if character not in string.punctuation:
			sanitized_search_string += character.lower()

	keywords = sanitized_search_string.split(" ")

	results = []

	for keyword in keywords:
		urls = index.get(keyword)
		if urls != None:
			results.append(urls)

	urls = []

	for i in range(0, len(results)):
		entry = results[i]
		for url in entry:
			in_other_entries = True
			for other_entry in (results[:i] + results[i+1:]):
				if url not in other_entry:
					in_other_entries = False
			if in_other_entries and url not in urls:
				urls.append(url)

	if len(urls) != 0:
		sorted_urls = sort(urls)

		return sorted_urls

	else:
		return ["No results found."]

def sort(urls):
	print "sorting urls..."
	relevance_weight = 1
	popularity_weight = 1

	scored_urls = []

	for url in urls:
		score = 0

		try:
			score = url[1] + popularity_index.get(url[0])
		except:
			pass

		scored_urls.append([url[0], score])

	sorted_urls = [scored_urls[0]]

	for url in scored_urls:
		for i in range(0, len(scored_urls)):
			scored_url = scored_urls[i]
			if url[1] > scored_url[1] and url not in sorted_urls:
				sorted_urls.insert(i, url)

		if url not in sorted_urls:
			sorted_urls.append(url)

	return sorted_urls
