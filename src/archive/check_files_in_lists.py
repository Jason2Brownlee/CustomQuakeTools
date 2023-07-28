# Find lost files on the internet archive.
#
# 1.  load a wishlist of file names and a wishlist of known urls for those files
# 2.  search a dir of text files that contain known urls for domains on internet archive
# 3.  report all occurrences of wishlist file names in known internet archive urls
# 3a. ignore urls in a separate wishlist of known urls for those files
#
# use create_file_lists.py to create the lists of .txt files to search.
#
from os import listdir
from os.path import join
import re
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Lock
from multiprocessing import set_start_method

# load file contents into memory, return as string
def load_file(filepath):
    with open(filepath, 'rt', encoding='utf8') as file:
        return file.read()

def load_wishlist_files(filepath):
    # load wishlist
    content = load_file(filepath)
    # split into lines
    lines = content.splitlines()
    # create set of files
    wishlist_files = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        # make lower case
        line = line.lower()
        # add to set
        wishlist_files.add(line)
    print(f'Loaded {len(wishlist_files)} wishlist files')
    return wishlist_files

def load_wishlist_urls(filepath):
    # load content
    content = load_file(filepath)
    # split into lines
    lines = content.splitlines()
    # create set of urls
    wishlist_urls = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        # add to set
        wishlist_urls.add(line)
    print(f'Loaded {len(wishlist_urls)} wishlist URLs')
    return wishlist_urls

# report the line of text that contains a query
def get_lines_with_query(txt, query, url_set):
    lines = list()
    for line in txt:
        # skip urls already reported
        if line in url_set:
            continue
        if re.search(f'/{query}', line.lower()):
            lines.append(line)
    return lines

def report_matches(filepath, data, wish, url_set):
    global mutex
    # get all lines from file that have the wish
    matches = get_lines_with_query(data, wish, url_set)
    # report results
    if matches:
        with mutex:
            # report file we are looking at
            print(filepath, flush=True)
            # report all urls with wish
            print(f'\t{wish}', flush=True)
            for url in matches:
                # report url
                print(f'\t{url}', flush=True)
                # store url so we do not report it again
                url_set.add(url)

def do_file(filepath, wishlist_files, url_set):
    # load it
    data = load_file(filepath)
    data = data.splitlines()
    # check for each file in wishlist
    for wish in wishlist_files:
        # report first match in file for wish
        report_matches(filepath, data, wish, url_set)

def doit(file_wishlist, url_wishlist, file_lists):
    # load wishlist
    wishlist_files = load_wishlist_files(file_wishlist)
    # load wishlist urls, so we don't report URLs we already know
    wishlist_urls = load_wishlist_urls(url_wishlist)
    # get a filenames in a dir
    filelist = [join(file_lists, name) for name in listdir(file_lists)]
    print(f'Discovered {len(filelist)} files lists.')
    # create shared lock
    global mutex
    mutex = Lock()
    # prepare thread pool
    with ProcessPoolExecutor(8) as exe:
        # issue one task per file to check
        for filepath in filelist:
            exe.submit(do_file, filepath, wishlist_files, wishlist_urls)

# protect the entry point
if __name__ == '__main__':
    # use the fork start method when starting new processes
    set_start_method('fork')
    # file path to a wishlist of file names (one per line)
    file_wishlist = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist.txt'
    # file path to a wishlist of urls (one per file)
    url_wishlist = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist_urls.txt'
    # dir path where .txt files exist, each contains all known files from a domain on internet archive
    file_lists = '../../data/lists'
    # perform search
    doit(file_wishlist, url_wishlist, file_lists)
