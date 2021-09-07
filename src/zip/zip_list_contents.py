# list the contents of a .zip file

import zipfile

# list contents of a zip file
def list_contents(filepath):
	# open zip file
	with zipfile.ZipFile(filepath) as f:
		# list contents
		for name in f.namelist():
			print(name)



# entry
path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/gamapog1/hereweap.zip'

list_contents(path)