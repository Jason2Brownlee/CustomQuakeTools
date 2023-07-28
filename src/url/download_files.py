# download all files listed on an FTP HTML website
import os
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import wget

# download a url as blob of data
def download_url(urlpath):
	try:
		with urlopen(urlpath) as f:
			content = f.read()
			return content
	except Exception as e:
		print(e)
		return None

# download url to file directly (faster? fewer lines of code?)
def download_url_to_file(url, path):
	wget.download(url, path)

# keep the old way around in case we can optimize it...
def download_url_to_file_old(url, path):
	# download the bytes
	data = download_url(url)
	# save to file
	with open(path, 'wb') as f:
		f.write(data)

# retrieve all URLs from a downloaded blob of content (html)
def get_urls_from_html(content):
    # decode the content
    html = content.decode('utf-8')
    # parse the doc
    soup = BeautifulSoup(html)
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
        # TODO safer?
        absurl = path + url
        abs_urls.append(absurl)
    return abs_urls

# download all files listed on an ftp html website
def download_urls(urlpath, basepath):
	print('Saving to: %s' % basepath)
	# create any directories if needed
	os.makedirs(basepath, exist_ok=True)
	# download html
	content = download_url(urlpath)
	# get all relative urls
	rel_links = get_urls_from_html(content)
	# convert relative urls to absolute urls
	abs_links = rel_to_abs(urlpath, rel_links)
	# download each file in turn
	for abs_url in abs_links:
		# get the filename
		filename = os.path.basename(abs_url)
		# skip directories
		if not filename:
			continue
		# convert to lower case
		filename = filename.lower()
		# only download some file types
		# if not (filename.endswith('.zip') or filename.endswith('.txt')):
		# 	continue
		# construct the output path
		outpath = os.path.join(basepath, filename)
		# skip if the file already exists
		if os.path.isfile(outpath):
			print('.skipping %s' % filename)
			continue
		# download the url to a local file
		print('.downloading %s...' % filename)
		download_url_to_file(abs_url, outpath)

# protect the entry point
if __name__ == '__main__':
	# website page containing links to files
	urlpath = 'https://...'
	# local path where we will save the files
	basepath = '...'
	# download all files
	download_urls(urlpath, basepath)

