# list all unique urls captured in the internet archive for a domain or directory
from urllib.request import urlopen

# download a url as blob of data
def download_html(urlpath):
	# print(urlpath)
	with urlopen(urlpath) as f:
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
	if query.endswith('/'):
		query = query[:-1]
	# base for archive.or searches
	search_url = 'http://web.archive.org/cdx/search/cdx'
	# construct search url
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
# ???
		# skip if http return code 3xx 4xx or 5xx
		if code != '200':
			continue
		# skip robots.txt
		if url.endswith('/robots.txt'):
			continue
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

# list of all common archive extensions
def get_archive_ext():
	# common
	archives = ['.zip', '.exe', '.rar', '.arj']
	# lesson common
	archives += ['.bz2', '.z', '.7z', '.ace']
	# mac
	archives += ['.lha', '.sit', '.hqx', '.bin', '.dmg']
	# amiga
	archives += ['.lha', 'lhz', '.lzx']
	# posix
	archives += ['.tar', '.gz', '.tgz']
	# multi-part arj
	archives += ['.a0%d' % i for i in range(0,10)]
	# multi-part rar
	archives += ['.r0%d' % i for i in range(0,10)]
	# quake stuff
	archives += ['.qc', 'progs.dat']
	return archives

# report unique urls found on a domain
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
query = 'ftp.epix.net'


# perform query
urls = get_unique_urls(query)
ext = []

# report urls with filter
# ext = get_archive_ext() + ['.txt']
#
# report all url results
if ext:
	report_urls(urls, ext)
else:
	report_urls(urls)






