# list the contents of a Quake pak file.
from vgio.quake.pak import PakFile

# open pak file and return list of pak file contents
def get_pak_contents(pakpath):
	contents = list()
	# open the pak file
	with PakFile(pakpath) as file:
		contents = [c for c in file.namelist()]
	return contents

# list the contents of a pak file
def list_pak_file(pakpath):
	# get the contents of the pak file
	contents = get_pak_contents(pakpath)
	# sort contents
	contents.sort()
	# display
	print(pakpath)
	for entry in contents:
		# print('.' + entry)
		print(entry)

# protect the entry point
if __name__ == '__main__':
	# path to pak file
	path = '...'
	# list contents of pak file
	list_pak_file(path)
