import urllib
import string
import pickledb
import urlparse
import time
import sys

index = pickledb.load("index.db", False)
popularity_index = pickledb.load("popularity_index.db", False)

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

	keywords = set(keywords)

	#for word in keywords:
	#	if word in keywords[keywords.index(word)+1:]:
	#		keywords.remove(word)

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
	referrers = {}

	while len(urls_to_crawl) > 0 and crawls < 50:
		try:
			url = urls_to_crawl[0]

			parsed_uri = urlparse.urlparse(url)
			url_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)			

			print "crawling " + url

			source = urllib.urlopen(url).read()

			keywords = get_keywords(source, url)
			add_to_index(url, keywords)

			uprank_relevance(keywords, source, url)

			links = get_links(source)
			for link in links:
				print "parsing link " + link

				parsed_uri = urlparse.urlparse(link)
				link_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

				print "link domain: " + link_domain

				if link[0:2] == '//':
					link = "http:" + link
				elif link_domain[0:3] == '://':
					link = url_domain + link[1:]

				uprank_popularity(link)

				if link != url and link not in urls_already_crawled and link not in urls_to_crawl:
					urls_to_crawl.append(link)

			popularity_index.dump()

		except e:
			print "could not crawl " + url
			print e

		urls_to_crawl.remove(url)
		urls_already_crawled.append(url)
		crawls += 1
		
		# wait
		time.sleep(5)

	print "finished crawling."

def uprank_popularity(url):
	print "upranking popularity of " + url
	popularity = popularity_index.get(url)

	if popularity == None:
		popularity = 0
	else:
		popularity += 1

	popularity_index.set(url, popularity)

def uprank_relevance(keywords, source, url):
	keywords = set(keywords)
	source = source.lower()

	for keyword in keywords:
		urls = index.get(keyword)
		if urls != None:
			for entry in urls:
				if entry[0] == url:
					print "upranking relevance of " + url + " for '" + keyword + "'"
					entry[1] = source.count(keyword)
		index.set(keyword, urls)
	index.dump()

def query(search_string, relevance_weight, popularity_weight):
	sanitized_search_string = ""

	for character in search_string:
		if character not in string.punctuation:
			sanitized_search_string += character.lower()

	keywords = sanitized_search_string.split(" ")

	print "querying for " + str(keywords)

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
		sorted_urls = sort(urls, relevance_weight, popularity_weight)

		return sorted_urls

	elif len(results) == 0:
		return ["No results found."]

	else:
		urls = []
		for entry in results:
			for url in entry:
				if url not in urls:
					urls.append(url)

		sorted_urls = sort(urls, relevance_weight, popularity_weight)
		return sorted_urls
			

def sort(urls, relevance_weight, popularity_weight):
	print "sorting urls..."

	scored_urls = []

	for url in urls:
		score = 0

		try:
			score = relevance_weight * url[1] + popularity_weight * popularity_index.get(url[0])
		except:
			pass

		scored_urls.append([url[0], score])

	sorted_urls = [scored_urls[0]]

	for url in scored_urls:
		for i in range(0, len(sorted_urls)):
			sorted_url = sorted_urls[i]
			if url[1] > sorted_url[1] and url not in sorted_urls:
				sorted_urls.insert(i, url)

		if url not in sorted_urls:
			sorted_urls.append(url)

	return sorted_urls
