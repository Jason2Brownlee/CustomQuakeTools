# search the contents of all zip files in a dir for files with a given extension

import os
import zipfile

# list contents of a zip file
def get_files_with_ext(filepath, query):
	filelist = list()
	# open zip file
	with zipfile.ZipFile(filepath) as f:
		# enumerate files in
		for name in f.namelist():
			# check for file with extension
			if name.lower().endswith(query):
				filelist.append(name)
	return filelist

# search all zip files in a directory
def search_all_zips(dirpath, query):
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
		print('Searching: %s' % filename)
		result = get_files_with_ext(filepath, query)
		# report
		if result:
			for value in result:
				print('\t%s' % value)



# dir containing .zip files
# path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/gamapog1/'
# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/reaper/'
# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/eliminator/'
# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/frogbot/'
# path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/frikbot/'
path = '/Users/jasonb/Development/Quake/QuakeBotArchive/bin/other/'


# file or extension to search for
query = 'progs.dat'


# go
search_all_zips(path, query)

