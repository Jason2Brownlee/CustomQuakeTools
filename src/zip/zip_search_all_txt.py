# search .txt files for keywords in all zips files in a directory (and sub dirs)

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

# search a txt string (content of a .txt) for each query
def get_matches_txt(txt, filename, queries):
	matches = list()
	# convert to lowercase for searching
	txt = txt.lower()
	# check each query
	for query in queries:
		# check filename
		if re.search(query, filename.lower()):
			matches.append([query, filename])
		# search contents
		if re.search(query, txt):
			# get the line with the query
			line = get_line_with_query(txt, query)
			matches.append([query, line])
	return matches

# find all matches for queries in a txt file and report results
def report_matches_txt(txt, filepath, queries):
	# get filename from path
	filename = os.path.basename(filepath)
	# get all matches
	matches = get_matches_txt(txt, filename, queries)
	# check for no matches
	if not matches:
		return
	# report path of file
	print('Searching: %s' % filepath)
	# report filename inside the zip
	print(' >%s' % filename)
	# report all matches
	for query, line in matches:
		print('\tContains \"%s\": %s' % (query, line))

# search contents of txt files in a zip file for queries and report results
def search_zip_contents(filepath, queries):
	# opening the zip may fail, or accessing a file in the zip may fail
	try:
		# open zip file
		with zipfile.ZipFile(filepath) as archive:
			# enumerate contents
			for name in archive.namelist():
				# only consider .txt files
				if not name.lower().endswith('.txt'):
					continue
				# matches = get_matches_txt(archive, name, queries)
				with zfile.open(filename) as file:
					# read contents
					content = file.read()
				# decode txt
				txt = content.decode('utf-8', errors='ignore')
				# report matches
				report_matches_txt(txt, filepath, queries)
	except:
		# just ignore
		return

# search contents of a txt file for queries and report results
def search_txt_contents(filepath, queries):
	# load file as bytes
	with open(filepath, 'rb') as file:
		content = file.read()
	# decode txt
	txt = content.decode('utf-8', errors='ignore')
	# report matches
	report_matches_txt(txt, filepath, queries)

# search all zip files in a directory
def search_all_zips(dirpath, queries):
	# get a filenames in a dir
	filelist = [name for name in os.listdir(dirpath)]
	# sort for readability
	filelist.sort()
	# enumerate all files in a directory
	for filename in filelist:
		# construct the path
		filepath = os.path.join(dirpath, filename)
		# check for directory
		if os.path.isdir(filepath):
			# process recursively
			search_all_zips(filepath, queries)
		# check for zip file (attempts to open)
		if zipfile.is_zipfile(filepath) :
			# all .txt in the zip file
			search_zip_contents(filepath, queries)
		# process .txt files in the directory already
		elif filename.lower().endswith('.txt'):
			# search the .txt file directly
			search_txt_contents(filepath, queries)

# list of keywords with bot like names
def get_bot_keywords():
	queries = list()
	# classic bots
	queries += ['reaper', 'reaprb', 'eliminator', 'bgbot', 'zeus', 'cujo']
	# less common classic bots
	queries += ['warbot', 'wisp', 'bplayer', 'bgadm', 'btskn', 'darkbt', 'cronosbot']
	# modern bots
	queries += ['frogbot', 'omicron', 'frikbot']
	# generic
	queries += ['bot[s,\.\s]']
	return queries

# entry

# queries to search for
queries = get_bot_keywords()

# dir containing .zip files
# path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/gamapog1/'
# path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/gamapog2/'
# path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/PowerToolsforQuake(Europe)/'
# path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/ToolkitForQuake(QTool_0197)/'
path = '/Users/jasonb/Games/QuakeFiles'

# go
search_all_zips(path, queries)


