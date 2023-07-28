# download all versions of all files for a website from archive.org
# does not preserve directory structure, we just want the content
from multiprocessing.pool import ThreadPool
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import quote
import os
import os.path

# download a url as blob of data
def download_url(urlpath):
	try:
		with urlopen(urlpath) as response:
			return response.read()
	except Exception as e:
		print(e)
		return None

# download a url as blob of data
def download_text_url(urlpath):
	try:
		with urlopen(urlpath) as response:
			# get url info
			info = response.info()
			# get main data type (e.g. 'text')
			data_type = info.get_content_maintype()
			# get the body content if text
			if data_type == 'text':
				return response.read()
			# skip
			# print(f'>skipped {urlpath} -> [{data_type}]')
			return None
	except Exception as e:
		# print(f'>error {urlpath} -> [{e}]')
		# print(f'>error {urlpath}')
		return None

def is_text(urlpath):
	h = requests.head(some_link)
	header = h.headers
	content_type = header.get('content-type')

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
	# url encode the parameters
	query = quote(query, safe='')
	# build the url path
	urlpath = f'http://web.archive.org/cdx/search/cdx?url={query}*&output=txt'
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

# return dict of URL to set of timestamps
def filter_results(url_list):
	url_map = dict()
	for entry in url_list:
		# <internal name> <timestamp> <url> <format> <return code> <hash> <number>
		_, timestamp, url, fmt, code, _, _ = entry
		# skip if http return codes like 3xx 4xx 5xx
		if code != '200':
			continue
		# skip robots files
		if url.endswith('robots.txt'):
			continue
		# skip css files
		if url.endswith('.css'):
			continue
		# skip stuff too old
# HACK
		year = int(str(timestamp)[:4])
		if year > 2002:
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
			# add timestamp to set
			url_map[url].add(ts)
		else:
			# create new entry in dict
			url_map[url] = {ts}
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

def get_archive_url(url, timestamp):
	return f'https://web.archive.org/web/{timestamp}fw_/{url}'

# try and covert a url into a filename
def to_filename(urlpath):
	# remove colons
	urlpath = urlpath.replace(':', '')
	# replace slashes
	urlpath = urlpath.replace('/', '-')
	return urlpath

def save_to_file(data, filepath):
	# save to file
	with open(filepath, 'wb') as f:
		f.write(data)

def process_url(basepath, url, timestamps):
	# enumerate timestamps
	for timestamp in timestamps:
		# get the archive url
		archive_url = get_archive_url(url, timestamp)
		# create filename
		filename = to_filename(archive_url)
		# construct the output path
		outpath = os.path.join(basepath, filename)
		# check if the file exists locally
		if os.path.isfile(outpath):
			continue
		# download text data
		content = download_text_url(archive_url)
		# cancel if we cannot download one file
		if not content:
			# return
			# store a file with nothing, avoid trying again
			content = 'None'
		# save to file
		save_to_file(content, outpath)
		# report
		print(filename, flush=True)

# load urls with timestamp
def download_urls(url_map, basepath):
	print('Saving to: %s' % basepath)
	# create output directory
	os.makedirs(basepath, exist_ok=True)
	# create thread pool
	with ThreadPool(20) as pool:
		# issue all urls as tasks
		for url, timestamps in url_map.items():
			# issue to the pool
			_ = pool.apply_async(process_url, args=(basepath, url, timestamps))
		# close the pool
		pool.close()
		# wait for all tasks to complete
		pool.join()

# protect the entry point
if __name__ == '__main__':
	# url domain and path to download (no https:// prefox)
	query = '...'
	# dir where files will be saved
	outpath = '...'
	# get map of urls to timestamps
	url_map = get_unique_urls(query)
	# download the unique files
	download_urls(url_map, outpath)


