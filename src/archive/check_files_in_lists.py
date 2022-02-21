# load a wishlist of files, then check for them in other lists of files.
from os import listdir
from os.path import join
import re

# load file contents into memory, return as string
def load_file(filepath):
    with open(filepath, 'rt', encoding='utf8') as file:
        return file.read()

# report the line of text that contains a query
def get_line_with_query(txt, query):
    for line in txt:
        if re.search(query, line):
            return line
    return None

def doit(file_wishlist, file_lists):
    # load wishlist
    wishlist = load_file(file_wishlist)
    wishlist = wishlist.splitlines()
    print(f'Loaded {len(wishlist)} files in wish list.')
    # get a filenames in a dir
    filelist = [join(file_lists, name) for name in listdir(file_lists)]
    print(f'Discovered {len(filelist)} files lists.')
    # scan through each file list looking for each wishlist file
    for filepath in filelist:
        # load it
        data = load_file(filepath)
        data = data.splitlines()
        # check for each file in wishlist
        for wish in wishlist:
            if not wish:
                continue
            if wish[-4:] not in ['.zip', '.txt', '.rar', '.exe', '.sit', '.hqx', 'r.gz']:
                # print(wish[-4:])
                continue
            # get matching line with query
            line = get_line_with_query(data, wish)
            if line:
                # report result
                print(filepath)
                print(f'\t{wish}\n\t{line}')



# wishlist file path
file_wishlist = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist.txt'
# file lists dir path
file_lists = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/lists'
# do it
doit(file_wishlist, file_lists)