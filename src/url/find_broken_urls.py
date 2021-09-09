# find all broken urls on a webpage

import os
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# download a url as blob of data
def download_url(urlpath):
	with urlopen(urlpath) as f:
		content = f.read()
		return content

# retrieve all URLs from a downloaded blob of content (html)
def get_urls_from_html(content):
    # decode the content
    html = content.decode('utf-8')
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
        	# add to list
            abs_urls.append(url)
            continue
        # build an absolute url
        absurl = urljoin(path, url)
        # add to list
        abs_urls.append(absurl)
    return abs_urls

# filter urls
# XXX customize...
def filter_urls(urls):
	filtered = list()
	for url in urls:
		# expect this string to be in the path
		expected = '/Jason2Brownlee/QuakeBotArchive/blob/main/bin/'
		if expected not in url:
			continue
		# expect the url to be a file, like .txt or .zip
		if '.' not in url[-4:]:
			continue
		# store
		filtered.append(url)
	return filtered

# return a list of links that do not return HTTP 200
def find_broken_links(urls):
	broken = list()
	for url in urls:
		code = 0
		try:
			with urlopen(url) as f:
				# get the code
				code = f.getcode()
		except HTTPError as e:
			code = e.getcode()
		# report progress
		print('> %d %s' % (code, url))
		# check code
		if code != 200:
			broken.append(url)
	return broken

# find and report all broken urls on a webpage
def find_broken_urls(urlpath):
	print(urlpath)
	# download webpage
	data = download_url(urlpath)
	# find all links in the webpage
	links = get_urls_from_html(data)
	# convert any relative links into absolute links
	abs_links = rel_to_abs(urlpath, links)
	# filter urls
	filtered = filter_urls(abs_links)
	# test each link and find broken links
	broken = find_broken_links(filtered)
	# report broken
	print('\n')
	for url in broke:
		print(url)


# entry point


urlpath = 'https://github.com/Jason2Brownlee/QuakeBotArchive/blob/main/README.md'


# download all files
find_broken_urls(urlpath)


