# find all files listed on a website that are not in a local directory
# (or the reverse)

import os
from urllib.request import urlopen
from urllib.parse import urlparse
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

# get a list of files on a url
def get_all_files_url(urlpath):
	# download html
	content = download_url(urlpath)
	# get all urls from the content
	links = get_urls_from_html(content)
	# get all files from the
# TODO make a set to get unique files?
	all_files = list()
	for link in links:
		# retrieve the file path
		filepath = urlparse(link).path
		# get the filename from the path
		filename = os.path.basename(filepath)
		# skip urls without a filename
		if not filename:
			continue
		if len(filename) < 5:
			continue
		if not filename[-4] == '.':
			continue
# TODO filter filenames more?
		# print(filename)
		# store
		all_files.append(filename)
	return all_files

# get all filenames from a local directory
def get_all_files_dir(dirpath):
	filelist = [name for name in os.listdir(dirpath)]
	# for d in filelist:
	# 	print(d)
	return filelist

# get all filenames in list1 that are not in list2
def get_filename_diff(filelist1, filelist2):
	# convert lists to sets
	set1 = set(filelist1)
	set2 = set(filelist2)
	# entries in 1 not in 2
	result = set1.difference(set2)
	# convert to list
	result = list(result)
	return result

# list all files in one dir/url not in a second dir/url
def diff_files(path1, path2):
	# get all files at first location
	if path1.startswith('http'):
		filenames1 = get_all_files_url(path1)
	else:
		filenames1 = get_all_files_dir(path1)
	print('%d files in %s' % (len(filenames1), path1))
	# get all files at second location
	if path2.startswith('http'):
		filenames2 = get_all_files_url(path2)
	else:
		filenames2 = get_all_files_dir(path2)
	print('%d files in %s' % (len(filenames2), path2))
	# difference between the sets
	diff = get_filename_diff(filenames1, filenames2)
	# sort for readability
	diff.sort()
	# display
	print('%d files in [%s] not in [%s]:' % (len(diff), path1, path2))
	for name in diff:
		print(name)


# entry point

# path1 = 'https://www.quaddicted.com/files/idgames2/quakec/bots/'
# path2 = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/'

# path1 = 'https://www.quaddicted.com/files/idgames2/quakec/bots/reaper/'
# path2 = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/reaper/'

# path1 = 'https://www.quaddicted.com/files/idgames2/quakec/bots/eliminator/'
# path2 = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/eliminator/'

path1 = 'https://github.com/Jason2Brownlee/QuakeBotArchive/blob/main/README.md'
path2 = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/'

# do it
diff_files(path1, path2)

