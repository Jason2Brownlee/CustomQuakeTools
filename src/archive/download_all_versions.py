# download all versions of a file from the internet archive
from urllib.request import urlopen
from urllib.parse import urlparse
import os

# download a url as blob of data
def download_url(urlpath):
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
	if query.startswith('/'):
		query = query[:-1]
	# TODO safely?
	search_url = 'http://web.archive.org/cdx/search/cdx'
	# build query
	urlpath = "%s?url=%s&output=txt" % (search_url, query)
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

# returns all valid (response 200) versions of the file in the archive
def filter_results(url_list):
	results = list()
	for entry in url_list:
		# <internal name> <timestamp> <url> <format> <return code> <hash> <number>
		_, timestamp, url, fmt, code, _, _ = entry
		# skip if http return codes like 3xx 4xx 5xx
		if code != '200':
			continue
		# store
		results.append([url, timestamp])
	return results

# query archive.org and return a list of [timestamp, url]
def get_all_versions(query):
	print('%s' % query)
	# build the query
	urlpath = build_query(query)
	print('%s' % urlpath)
	# execute the query and download results
	content = download_url(urlpath)
	# decode as text
	txt = content.decode('utf-8', errors='ignore')
	# parse text to entries
	result_list = parse_result(txt)
	print('Found %d version(s)' % len(result_list))
	# filter urls
	url_list = filter_results(result_list)
	print('Found %d downloadable version(s)' % len(url_list))
	return url_list

# download an archived url
def download_archived_url(url, timestamp):
	# build the url
	base = 'https://web.archive.org/web'
	archive_url = '%s/%sfw_/%s' % (base, timestamp, url)
	# download the data
	content = download_url(archive_url)
	return content

# save content to file, create dirs if needed
def save_file(content, filepath):
	# get the dir from the filepath
	directory = os.path.dirname(filepath)
	# create any directories if needed
	os.makedirs(directory, exist_ok=True)
	# save to file
	with open(filepath, 'wb') as f:
		f.write(content)

# load urls with timestamp
def download_all_versions(query, basepath):
	# get all versions of a url
	url_list = get_all_versions(query)
	# enumerate urls
	for url, timestamp in url_list:
		# retrieve the file path
		filepath = urlparse(url).path
		# get the filename
		filename = os.path.basename(filepath)
		# prefix filename with timestamp
		filename = '%s_%s' % (timestamp, filename)
		# remove leading slash from path
		filepath = filepath[1:]
		# download the bytes from archive.org
		content = download_archived_url(url, timestamp)
		# construct the output path
		outpath = os.path.join(basepath, filename)
		# save to file
		save_file(content, outpath)
		# report
		print('Saved: %s' % filename)



# entry point

# query
query = 'http://www.cdrom.com/pub/quake/00alltxt.tar.gz'
# query = 'http://www.cdrom.com/pub/idgames2/00alltxt.tar.gz'

outpath = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/archive_file'

# download all versions of a file from archive.org
download_all_versions(query, outpath)


