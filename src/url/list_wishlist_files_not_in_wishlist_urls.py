# list all files in "wishlist" that are not in "wishlist urls"
from os.path import basename

WISHLIST_URLS = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist_urls.txt'
WISHLIST = '/Users/jasonb/Development/Quake/QuakeBotArchive/research/wishlist.txt'

# load file contents into memory, return as string
def load_file(filepath):
    with open(filepath, 'rt', encoding='utf8') as file:
        return file.read()

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

def load_unique_files_wishlist_urls(filepath):
    # load wishlist urls
    wishlist_urls = load_wishlist_urls(filepath)
    # set of all files
    filenames = set()
    for url in wishlist_urls:
        # get filenames part of url
        filename = basename(url)
        # check for empty string
        if not filename:
            continue
        # check for "="
        if "=" in filename:
            ix = filename.rindex('=') + 1
            filename = filename[ix:]
        # covert to lowercase
        filename = filename.lower()
        # report progress
        # print(filename)
        # add to set of filenames
        filenames.add(filename)
    print(f'Loaded {len(filenames)} unique wishlist files')
    return filenames

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
        # skip txt files
        if line.endswith('.txt'):
            continue
        # make lower case
        line = line.lower()
        # add to set
        wishlist_files.add(line)
    print(f'Loaded {len(wishlist_files)} wishlist files')
    return wishlist_files

def main():
    # load unique filenames in wishlist url
    wishlist_urls_files = load_unique_files_wishlist_urls(WISHLIST_URLS)
    # load unique filenames in wishlist
    wishlist_files = load_wishlist_files(WISHLIST)
    # list files in wishlist url not in wishlist
    print()
    for name in sorted(list(wishlist_files)):
        # check if it exists in the wishlist urls
        if name not in wishlist_urls_files:
            print(name)

if __name__ == '__main__':
    main()