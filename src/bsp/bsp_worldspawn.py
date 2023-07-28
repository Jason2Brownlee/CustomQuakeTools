# report the worldspawn entity in a bsp file
import re
from vgio.quake.bsp import Bsp

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

# parse bsp file entities and return the worldspawn entity
def load_bsp_worldspawn(filepath):
	# open the bsp
	with Bsp.open(path) as file:
		# parse all entities
		entities = parse_nv_pairs(file.entities)
		# get the worldspawn
		worldspawn = get_worldspawn_entity(entities)
		return worldspawn

# protect the entry point
if __name__ == '__main__':
	# path to quake bsp file
	path = '...'
	# load worldspawn entity
	ws = load_bsp_worldspawn(path)
	# print somewhat nicely
	for name, value in ws.items():
		print('%s:\t\t%s' % (name, value))
