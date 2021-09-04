# list all bsp files in all Quake pak files in a mod directory

import os
from vgio.quake.pak import PakFile

# get all bsp file entries from a pak file
def get_bsp_entries_from_pak(pakpath):
    bsplist = list()
    # open the pak file
    with PakFile(pakpath) as file:
        # enumerate all entries
        for filepath in file.namelist():
            # skip if not in maps/ directory
            if not filepath.lower().startswith('maps/'):
                continue
            # skip if not .bsp file
            if not filepath.lower().endswith('.bsp'):
                continue
            # skip if in subdirectory of maps
            if filepath.count('/') > 1 or filepath.count('\\') > 1:
                continue
            # store the entry
            bsplist.append(filepath)
    # sort list for readability
    bsplist.sort()
    return bsplist

# get a list of all pak file paths in a mod directory
def get_all_pak_files(modpath):
	paklist = list()
	for filename in os.listdir(modpath):
		# skip files with the wrong extension
		if not filename.lower().endswith('.pak'):
			continue
		# build path
		filepath = os.path.join(modpath, filename)
		# store
		paklist.append(filepath)
	# sort list for readability
	paklist.sort()
	return paklist

# process all pak files in a mod directory
def report_all_bsps_in_all_paks(modpath):
	# get all pak files
	pakfiles = get_all_pak_files(modpath)
	# process each pak file and get bsps
	for pakfile in pakfiles:
		# get all bsps in the pak
		bsps = get_bsp_entries_from_pak(pakfile)
		# report
		print(pakfile)
		for bsp in bsps:
			print('\t%s' % bsp)


path = '/Users/jasonb/Games/QuakeYouTube/ad/'
# list contents
report_all_bsps_in_all_paks(path)
