# download all files for a website from archive.org

# notes:
# uses HTTP API
# only considers files with a 200 HTTP response code
# saves all files


from urllib.request import urlopen
from urllib.parse import urlparse
import os

# download a url as blob of data
def download_url(urlpath):
	try:
		with urlopen(urlpath) as f:
			content = f.read()
			return content
	except Exception:
		return None

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
	result_list = list()
	for line in result.splitlines():
		# split into pieces
		entry = line.split()
		# store
		result_list.append(entry)
	return result_list

# returns a list of unique urls with 200 response code and timestamp
def filter_results(url_list):
	url_map = dict()
	for entry in url_list:
		# <internal name> <timestamp> <url> <format> <return code> <hash> <number>
		_, timestamp, url, fmt, code, _, _ = entry
		# skip if http return codes like 3xx 4xx 5xx
		if code != '200':
			continue
		# remove port if present
		if ':80' in url:
			url = url.replace(':80', '')
		# assume www and non www versions are the same?
		if 'www.' in url:
			url = url.replace('www.', '')
		# check if exists
		ts = int(timestamp)
		if url in url_map:
			# replace timestamp if newer
# planetquake will return 200 for 404 because they suck!
# keep oldest instead of newest
			# if ts > url_map[url]:
			if ts < url_map[url]:
				url_map[url] = ts
		else:
			url_map[url] = ts
	return url_map

# query archive.org and return map of urls to timestamp
def get_unique_urls(query):
	# build the query
	urlpath = build_query(query)
	print('%s' % query)
	# execute the query and download results
	content = download_url(urlpath)
	# decode as text
	txt = content.decode('utf-8', errors='ignore')
	# parse text to entries
	result_list = parse_result(txt)
	print('.%d results' % len(result_list))
	# filter urls
	url_map = filter_results(result_list)
	print('.%d unique urls' % len(url_map))
	return url_map

# download an archived url
def download_archived_url(url, timestamp):
	# build the url
	base = 'https://web.archive.org/web'
	archive_url = '%s/%sfw_/%s' % (base, timestamp, url)
	# download the data
	content = download_url(archive_url)
	return content

# load urls with timestamp
def download_urls(url_map, basepath):
	print('Saving to: %s' % basepath)
	# enumerate urls
	for url, timestamp in url_map.items():
		# retrieve the file path
		filepath = urlparse(url).path
		# get the filename
		filename = os.path.basename(filepath)
		# skip files that don't have a filename extension
		if not '.' in filename:
			print(f'.skipping {filepath} as its not a file')
			continue
		# remove leading slash
		filepath = filepath[1:]
		# construct the output path
		outpath = os.path.join(basepath, filepath)
		# check if the file exists locally
		if os.path.isfile(outpath):
			print(f'.skipping {outpath} as it already exists')
			continue
		# create any directories if needed
		directory = os.path.dirname(outpath)
		os.makedirs(directory, exist_ok=True)
		# download the bytes
		data = download_archived_url(url, str(timestamp))
		if not data:
			print(f'.error {outpath} could not be downloaded')
			continue
		# save to file
		with open(outpath, 'wb') as f:
			f.write(data)
		# reporting
		print(filepath)


# entry point

# query
# query = 'www.planetquake.com/ramshackle/'
# query = 'www.planetquake.com/qca/'
query = 'redwood.gatsbyhouse.com'
outpath = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/redwood-gatsbyhouse-com'

# get map of urls to timestamps
url_map = get_unique_urls(query)
# download the unique files
download_urls(url_map, outpath)


