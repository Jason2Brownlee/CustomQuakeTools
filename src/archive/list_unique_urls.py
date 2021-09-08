# list all unique urls captured in the internet archive for a domain or directory
import urllib.request

# download a url as blob of data
def download_html(urlpath):
	# print(urlpath)
	with urllib.request.urlopen(urlpath) as f:
		content = f.read()
		return content

# query archive.org
def build_query(query):
	# remove leading protocol
	if query.startswith('http://'):
		query = query.replace('http://', '')
	if query.startswith('https://'):
		query = query.replace('https://', '')
	if query.startswith('ftp://'):
		query = query.replace('ftp://', '')
	# remove trailing slash for consistency
	if query.startswith('/'):
		query = query[:-1]
	# TODO safely?
	search_url = 'http://web.archive.org/cdx/search/cdx'
	# assumes url ends with a '/'
	urlpath = "%s?url=%s/*&output=txt" % (search_url, query)
	return urlpath

# parse result into a list of records
def parse_result(result):
	url_list = list()
	for line in result.splitlines():
		# split into pieces
		entry = line.split()
		# TODO do any filtering here?
		url_list.append(entry)
	return url_list

def filter_results(url_list):
	url_set = set()
	for entry in url_list:
		# <internal name> <hash> <url> <format> <return code> <hash> <number>
		_, _, url, fmt, code, _, _ = entry
		# skip if http return code 3xx 4xx or 5xx
		if code.startswith('3') or code.startswith('4') or code.startswith('5'):
			continue
		# skip formats like: application/octet-stream, image/jpeg, image/gif, ...
		# if fmt != 'text/html':
		# 	continue
		# remove port if present
		if ':80' in url:
			url = url.replace(':80', '')
		# store url
		url_set.add(url)
	# convert to list
	ulist = list(url_set)
	return ulist

# query archive.org and return all unique urls for a domain or path
def get_unique_urls(query):
	# build the query
	urlpath = build_query(query)
	# execute the query and download results
	content = download_html(urlpath)
	# decode as text
	txt = content.decode('utf-8', errors='ignore')
	# parse text to entries
	url_list = parse_result(txt)
	# filter urls
	urls_filtered = filter_results(url_list)
	# sort result for readability
	urls_filtered.sort()
	return urls_filtered

# report unique urls found on a domain
EXT_ZIPS = ['.zip', '.exe', '.rar', '.arj', '.lha', '.sit', '.hqx', '.bin',
	'.tar', '.gz', '.tgz', '.txt']
def report_urls(urls, ext_filters=[]):
	for url in urls:
		if ext_filters:
			for f in ext_filters:
				if url.lower().endswith(f):
					print(url)
		else:
			print(url)

# entry point

# query
# query = 'www.planetquake.com/ramshackle/'
# query = 'http://www.bluesnews.com'
# query = 'http://www.parboil.quakeworld.ru'
# query = 'http://www.parboil.mailru.com'
# query = 'quakemecca.simplenet.com'
# query = 'http://sunsite.org.uk/packages/idgames2/planetquake/'
# query = 'http://trinca.no.sapo.pt/'
# query = 'http://www.angelfire.com/co2/kooliobot'
# query = 'http://www.botepidemic.com/fmods/'
# query = 'http://www.planetquake.com/requiem'
# query = 'https://www.bluesnews.com/files/patches/bots/'
# query = 'http://sunsite.org.uk/packages/idgames2/planetquake/'
# query = 'http://geocities.com/TimesSquare/Battlefield/2313/'
query = 'http://members.tripod.com/~pluck'

# perform query
urls = get_unique_urls(query)

# report results
report_urls(urls)

# report_urls(urls, EXT_ZIPS)






