# search .txt files in a zip file for keywords
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
	print('Searching: %s' % filename)
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
				print(name)
				for query, line in matches:
					print('\tContains \"%s\": %s' % (query, line))
	print('Done.')

# protect the entry point
if __name__ == '__main__':
	# tokens to search for
	queries = [	'reaper', 'warbot', 'eliminator', 'bgbot', 'frogbot', 'omicron',
				'frikbot', 'zeus', 'wisp', 'cujo', 'bot[,. ]', 'bots[,. ]']
	# path to zip file to search
	path = '...'
	# perform the search
	search_contents(path, queries)
