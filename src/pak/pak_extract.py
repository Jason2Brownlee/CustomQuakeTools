# extract files from a quake pak file
from vgio.quake.pak import PakFile

# extract them all
def extract_pak(pakpath, target):
	with PakFile(pakpath, mode='r') as file:
		file.extractall(path=target)

# protect the entry point
if __name__ == '__main__':
	# path to pak file
	pakfile = '...'
	# path to unzip files
	target = '...'
	# extract contents
	extract_pak(pakfile, target)
