# search the contents of all zip files in a dir for files with a given extension

import os
import zipfile

# list contents of a zip file
def get_files_with_ext(filepath, queries):
	matches = list()
	# open zip file
	with zipfile.ZipFile(filepath) as f:
		# enumerate files in the zip
		for name in f.namelist():
			# enumerate all search queries
			for query in queries:
				# check for file with extension
				if name.lower().endswith(query):
					matches.append([query, name])
	return matches

# list of all common archive extensions
def get_archive_ext():
	# common
	# archives = ['.zip', '.exe', '.rar', '.arj']
	archives = ['.zip', '.rar', '.arj']
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
	return archives

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
		# search contents of zip for matches
		matches = get_files_with_ext(filepath, queries)
		# report
		if matches:
			print('Searching: %s' % filename)
			for query, name in matches:
				print('\t%s' % name)



# dir containing .zip files
path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/gamapog1/'
# path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/gamapog2/'

# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/reaper/'
# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/eliminator/'
# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/frogbot/'
# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/frikbot/'
# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/other/'


# search for mods
# query = ['progs.dat']

# search for archives inside the .zip files
queries = get_archive_ext()

# go
search_all_zips(path, queries)

