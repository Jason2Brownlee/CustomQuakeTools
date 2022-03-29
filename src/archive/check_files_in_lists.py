# load a wishlist of files, then check for them in other lists of files.
from os import listdir
from os.path import join
import re

# load file contents into memory, return as string
def load_file(filepath):
    with open(filepath, 'rt', encoding='utf8') as file:
        return file.read()

# report the line of text that contains a query
def get_lines_with_query(txt, query, url_set):
    lines = list()
    for line in txt:
        # skip urls already reported
        if line in url_set:
            continue
        if re.search(f'/{query.lower()}', line.lower()):
            lines.append(line)
    return lines

def report_matches(filepath, data, wish, url_set):
    # get all lines from file that have the wish
    matches = get_lines_with_query(data, wish, url_set)
    # report results
    if matches:
        # report file we are looking at
        print(filepath)
        # report all urls with wish
        print(f'\t{wish}')
        for url in matches:
            # report url
            print(f'\t{url}')
            # store url so we do not report it again
            url_set.add(url)

def doit(file_wishlist, file_lists):
    url_set = set()
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
            # skip empty lines
            if not wish:
                continue
            # skip comment lines
            if wish[0] == '#':
                continue
            # report first match in file for wish
            report_matches(filepath, data, wish, url_set)


# wishlist file path
file_wishlist = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist.txt'
# file_wishlist = '/Users/jasonb/Development/Quake/QuakeOfficialArchive/research/wishlist.txt'

# file lists dir path
file_lists = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/lists'
# do it
doit(file_wishlist, file_lists)


