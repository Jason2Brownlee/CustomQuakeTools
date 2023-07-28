# download all versions of a file from the internet archive
# customized to download all forum posts from botboard.telefragged.com
# skips failures, so re-run to get anything missed
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import quote
import os
import os.path

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
	# url encode the parameters
	query = quote(query, safe='')
	# build query
	urlpath = f'{search_url}?url={query}&output=txt'
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
	# print('%s' % query)
	# build the query
	urlpath = build_query(query)
	# print('%s' % urlpath)
	# execute the query and download results
	content = download_url(urlpath)
	# decode as text
	txt = content.decode('utf-8', errors='ignore')
	# parse text to entries
	result_list = parse_result(txt)
	# filter urls
	url_list = filter_results(result_list)
	# print('Found %d downloadable version(s)' % len(url_list))
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
	# could fail, don't let this stop us
	try:
		url_list = get_all_versions(query)
	except:
		print(f'Error geting all versions for {query}')
		return False
	# enumerate urls
	for url, timestamp in url_list:
		# make a useful filename
		filename = url.replace('/', '_')
		filename = filename.replace(':', '_')
		filename = f'{timestamp}_{filename}.html'
		# construct the output path
		outpath = os.path.join(basepath, filename)
		# check if the file exists
		if os.path.exists(outpath):
			print(f'>skipping {outpath}')
			continue
		# download the bytes from archive.org
		# could fail, don't let this stop us
		try:
			content = download_archived_url(url, timestamp)
		except:
			print(f'Error downloading {url}')
			return False
		# save to file
		save_file(content, outpath)
		# report
		print('Saved: %s' % filename)
	# all good
	return True

# load file contents into memory, return as string
def load_file(filepath):
    with open(filepath, 'rt', encoding='utf8') as file:
        return file.read()

# load all urls that we want to download
def load_selected_urls():
	# load the list of known unique urls for the domain
	filename = 'botboard.telefragged.com.txt'
	filepath = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/lists/' + filename
	# load from disk
	data = load_file(filepath)
	# split into lines
	lines = data.splitlines()
	print(f'Loaded {len(lines)} lines from {filename}')
	filtered = list()
	# filter lines
	for line in lines:
		line = line.strip()
		if line is None:
			continue
		if 'newreply.pl' in line:
			continue
		if 'sendprivate.pl' in line:
			continue
		if 'newpost.pl' in line:
			continue
		if 'showprofile.pl' in line:
			continue
		if not 'quake1' in line:
			continue
		filtered.append(line)
	print(f'Filtered {len(filtered)} lines about quake1')
	return filtered

def update_done_file(outpath, url):
	filepath = f'{outpath}/done.txt'
	with open(filepath, 'a') as file:
		file.write(f'{url}\n')

def read_done_file(outpath):
	filepath = f'{outpath}/done.txt'
	with open(filepath, 'r') as file:
		return file.readlines()

# entry point
if __name__ == '__main__':
	# load selected urls
	urls = load_selected_urls()
	# output path
	outpath = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/botboard.telefragged.com-files'
	# read all done urls
	all_done = read_done_file(outpath)
	print(f'Read {len(all_done)} lines from done file')
	# do them all
	for query in urls:
		# check if this url is already done
		if any(query in x for x in all_done):
			print(f'>skipping {query}')
			continue
		# download all versions of a file from archive.org
		if download_all_versions(query, outpath):
			# save in done file so we don't do it again
			update_done_file(outpath, query)
