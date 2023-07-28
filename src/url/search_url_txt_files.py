# search the contents of .txt files for keywords on an ftp html page
# google typically does not index the contents of these files...
import os
import re
import urllib
from bs4 import BeautifulSoup

# download a url as blob of data
def download_url(urlpath):
    with urllib.request.urlopen(urlpath) as f:
        content = f.read()
        return content

# retrieve all URLs from a downloaded blob of content (html)
def get_urls_from_html(content):
    # decode the content
    html = content.decode('utf-8', errors='ignore')
    # parse the doc
    soup = BeautifulSoup(html, features="lxml")
    # find all a tags
    atags = soup.find_all('a')
    # extract links
    links = list()
    for tag in atags:
        link = tag.get('href', None)
        if link is not None:
            links.append(link)
    return links

# convert relative urls to absolute urls so we can download them
def rel_to_abs(path, urls):
    abs_urls = list()
    for url in urls:
        # check if we should skip/drop a bad url
        if url.startswith('../'):
            continue
        # check if already absolute
        if url.startswith('http'):
            abs_urls.append(url)
            continue
        # build an absolute url
        # TODO safer???
        absurl = path + url
        abs_urls.append(absurl)
    return abs_urls

# report the line of text that contains a query
def get_line_with_query(txt, query):
	lines = txt.splitlines()
	for line in lines:
		if re.search(query, line):
			return line
	return ""

# search a .txt url for instances of each query and report
def get_matches_txt_url(url, queries):
	matches = list()
	# download file
	content = download_url(url)
	# decode as txt
	txt = content.decode('utf-8', errors='ignore')
	# convert to lowercase
	txt = txt.lower()
	# check each query
	for query in queries:
		# search
		if re.search(query, txt):
			# get the line with the query
			line = get_line_with_query(txt, query)
			matches.append([query, line])
	return matches

# search the contents of .txt files on an ftp html page
def search_txt_files(urlpath, queries):
	print(urlpath)
	# download html
	content = download_url(urlpath)
	# get all relative urls
	rel_links = get_urls_from_html(content)
	print('.%d files' % (len(rel_links)))
	# filter to only the .txt files
	rel_links = [a for a in rel_links if a.endswith('.txt')]
	print('.%d txt files' % (len(rel_links)))
	# convert relative urls to absolute urls
	abs_links = rel_to_abs(urlpath, rel_links)
	# download and search each url
	for url in abs_links:
		# search contents of the url for queries
		matches = get_matches_txt_url(url, queries)
		# report
		if matches:
			print(url)
			for query, line in matches:
				print('\tContains \"%s\": %s' % (query, line))

# search across multiple pages
def search_txt_files_across_pages(pages, queries):
	for urlpath in pages:
		# perform search
		search_txt_files(urlpath, queries)
		# separate report from the next
		print('\n')
		print('----------' * 8)

# list of keywords with bot like names
def get_bot_keywords():
	queries = list()
	# classic bots
	queries += ['reaper', 'reaprb', 'robot', 'eliminator', 'bgbot', 'zeus', 'cujo']
	# less common classic bots
	queries += ['warbot', 'wisp', 'bplayer', 'bgadm', 'btskn', 'darkbt', 'cronosbot']
	# modern bots
	queries += ['frogbot', 'omicron', 'frikbot']
	# generic
	queries += ['bot[s,\.\s]']
	return queries

# protect the entry point
if __name__ == '__main__':
	# list of pages of files to consider
	pages = list()
	pages += ['https://...']
	pages += ['https://...']
	# ...
	# queries to search for
	queries = get_bot_keywords()
	# perform search
	search_txt_files_across_pages(pages, queries)

