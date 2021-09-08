# search .txt files for keywords in all zips files in a directory

import os
import re
import zipfile

# report the line of text that contains a query
def get_line_with_query(txt, query):
	lines = txt.splitlines()
	for line in lines:
		if re.search(query, line):
			return line
	return ""

# open a .txt file and search contents for keywords
def get_matches_txt(zfile, filename, queries):
	matches = list()
	# open the file within the archive
	with zfile.open(filename) as file:
		# read contents
		content = file.read()
	# decode
	txt = content.decode('utf-8', errors='ignore')
	# convert to lowercase for searching
	txt = txt.lower()
	# check each query
	for query in queries:
		# search
		if re.search(query, txt):
			# get the line with the query
			line = get_line_with_query(txt, query)
			matches.append([query, line])
	return matches

# search contents of a zip file
def search_contents(filepath, queries):
	filename = os.path.basename(filepath)
	# open zip file
	with zipfile.ZipFile(filepath) as archive:
		# enumerate contents
		for name in archive.namelist():
			# only consider .txt files
			if not name.lower().endswith('.txt'):
				continue
			# search contents
			matches = get_matches_txt(archive, name, queries)
			# report matches
			if matches:
				print(' >%s' % name)
				for query, line in matches:
					print('\tContains \"%s\": %s' % (query, line))

# search all zip files in a directory
def search_all_zips(dirpath, queries):
	# get a filenames in a dir
	filelist = [name for name in os.listdir(dirpath)]
	# sort for readability
	filelist.sort()
	# enumerate all files in a directory
	for filename in filelist:
		# only consider .zip files
		if not filename.lower().endswith('.zip'):
			continue
		# construct the path
		filepath = os.path.join(dirpath, filename)
		# search all text
		print('Searching: %s' % filename)
		search_contents(filepath, queries)


# entry

# queries to search for
queries = [	'reaper', 'warbot', 'eliminator', 'bgbot', 'frogbot', 'omicron',
			'frikbot', 'zeus', 'wisp', 'cujo', 'bot[s,\.\s]']

# dir containing .zip files
path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/gamapog1/'
# go
search_all_zips(path, queries)


