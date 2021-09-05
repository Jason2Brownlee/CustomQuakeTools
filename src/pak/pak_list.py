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
		print('.' + entry)

# test = '/Users/jasonb/Games/QuakeYouTube/ad/pak0.pak'
# test = '/Users/jasonb/Downloads/awesome/Pak0.pak'
test = '/Users/jasonb/Downloads/wqmodv.8/pak2.pak'


# list contents
list_pak_file(test)
