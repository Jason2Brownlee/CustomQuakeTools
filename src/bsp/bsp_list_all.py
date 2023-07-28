# list all maps in a quake mod directory (maps/ and .pak files)
import os
import sys
import re
from vgio.quake.bsp import Bsp
from vgio.quake.pak import PakFile
from vgio.quake.bsp.bsp29 import Bsp as Bsp29
from vgio.quake.bsp.bsp29a import Bsp as Bsp29a

# process entity definitions into dicts, assumes all entities are valid
def parse_nv_pairs(entities_raw):
    entities = list()
    # process entities
    current = None
    for line in entities_raw.splitlines():
        if line =='{':
            # start of entity def
            current = dict()
        elif line == '}':
            # end of entity def
            entities.append(current)
        else:
            # in the middle of an entity
            name, value = re.findall('"([^"]*)"', line)
            current[name] = value
    return entities

# load bsp entities from a file
def load_bsp_entities_file(filepath):
    entities = list()
    # try q1 format
    try:
        with Bsp29.open(filepath) as file:
            # parse all entity definitions
            entities = parse_nv_pairs(file.entities)
    except:
        # try q2 format
        try:
            with Bsp29a.open(filepath) as file:
                # parse all entity definitions
                entities = parse_nv_pairs(file.entities)
        except:
            print(' >unable to load %s: %s' % (filepath, sys.exc_info()[1]))
    return entities

# load bsp file from bytes
def load_bsp_entities_bytes(bsp_bytes, filepath, pakpath):
    entities = list()
    # try q1 format
    try:
        with Bsp29.open(bsp_bytes) as file:
            # parse all entity definitions
            entities = parse_nv_pairs(file.entities)
    except:
        # try q2 format
        try:
            with Bsp29a.open(bsp_bytes) as file:
                # parse all entity definitions
                entities = parse_nv_pairs(file.entities)
        except:
            print(' >unable to load %s from %s: %s' % (filepath, pakpath, sys.exc_info()[1]))
    return entities

# search through a list of bsp entities for classname: worldspawn
def get_worldspawn_entity(entities):
    # search through entities for the worldspawn entity, typically listed first
    for e in entities:
        # skip if entity does not have a class name
        if 'classname' not in e:
            continue
        # get classname and covert to lower case
        classname = e['classname'].lower()
        # check if the entity is the worldspawn entity
        if classname == "worldspawn":
            return e
    return dict()

# get the bsp description
def get_bsp_description(entities):
    # get the worldspawn entity
    worldspawn = get_worldspawn_entity(entities)
    # check for no map title
    if 'message' not in worldspawn:
        # no description
        return '?'
    # retrieve description and cover to title case
    desc = worldspawn['message'].title()
    return desc

# return map name from a bsp file path
def get_bsp_name(filename):
    # separate map name from extension
    name, _, _ = filename.rpartition('.')
    # convert to lowercase
    name = name.lower()
    return name

# get the bsp author, assumes filename is in format <jam name>_<author>
def get_bsp_author(bsp_name):
    # split map name by the first underscore
    _, _, author = bsp_name.partition('_')
    # check for no author
    if author is None or not author:
        return "?"
    # convert to title case
    author = author.title()
    return author

# return a list of map names, descriptions and authors for all .bsp files in a directory
def bsp_list(dirpath):
    bsplist = list()
    # process all files in the directory
    for filename in os.listdir(dirpath):
        # skip files with the wrong extension
        if not filename.endswith('.bsp'):
            continue
        filepath = os.path.join(dirpath, filename)
        # open bsp file and load entities
        entities = load_bsp_entities_file(filepath)
        # get the map details
        bsp_name = get_bsp_name(filename)
        bsp_desc = get_bsp_description(entities)
        bsp_author = get_bsp_author(bsp_name)
        # construct an entry
        entry = [bsp_name, bsp_desc, bsp_author]
        # store the entry
        bsplist.append(entry)
    print('.loaded %d maps from %s' % (len(bsplist), dirpath))
    return bsplist

# load all bsp files from a pak file
def load_bsps_from_pak(pakpath):
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
            # open the file
            bsp_bytes = file.read(filepath)
            entities = load_bsp_entities_bytes(bsp_bytes, filepath, pakpath)
            # get the map details
            filename = os.path.basename(filepath)
            bsp_name = get_bsp_name(filename)
            bsp_desc = get_bsp_description(entities)
            bsp_author = get_bsp_author(bsp_name)
            # construct an entry
            entry = [bsp_name, bsp_desc, bsp_author]
            # store the entry
            bsplist.append(entry)
    print('.loaded %d maps from %s' % (len(bsplist), pakpath))
    return bsplist

# load all bsps from all pak files in a mod
def load_bsps_from_paks(mod_path):
    bsplist = list()
    # process all files in the directory
    for filename in os.listdir(mod_path):
        # skip files with the wrong extension
        if not filename.lower().endswith('.pak'):
            continue
        # load all bsps in the pak
        filepath = os.path.join(mod_path, filename)
        bsplist += load_bsps_from_pak(filepath)
    return bsplist

# remove duplicate map names
def remove_duplicates(bsplist):
    # convert list to map
    bspmap = dict()
    for entry in bsplist:
        bspmap[entry[0]] = entry
    diff = len(bsplist) - len(bspmap)
    if diff > 0:
        print('.removed %d duplicate(s)' % diff)
    # return values
    return list(bspmap.values())

# filter out some maps
def filter_maps(bsplist):
    newlist = bsplist
    # remove maps that have 'test' in their filename
    newlist = [a for a in newlist if 'test' not in a[0]]
    # remove maps that start with b_, bsp models I think
    newlist = [a for a in newlist if not a[0].startswith('b_')]
    diff = len(bsplist) - len(newlist)
    if diff > 0:
        print('.filtered out %d map(s)' % diff)
    return newlist

# get a list of BSP files in a mod directory and print to screen using sep
def print_bsp_list(mod_path, sep='\t', report_author=True):
    bsplist = list()
    # load bsp files from maps/ directory
    mapspath = os.path.join(mod_path, 'maps/')
    if os.path.exists(mapspath):
        # get the list of bsp details
        bsplist += bsp_list(mapspath)
    # load bsp details from pak files
    bsplist += load_bsps_from_paks(mod_path)
    # remove duplicates
    bsplist = remove_duplicates(bsplist)
    # filter some map names
    bsplist = filter_maps(bsplist)
    # sort list by map name
    bsplist.sort(key=lambda tup: tup[0])
    # remove author if needed
    if not report_author:
        bsplist = [a[:-1] for a in bsplist]
    # report
    print('Done.\n')
    for entry in bsplist:
        print(sep.join(entry))

# protect the entry point
if __name__ == '__main__':
    # path to mod directory
    path = '...'
    # report all maps in mod directory
    print_bsp_list(path, '\t', True)
