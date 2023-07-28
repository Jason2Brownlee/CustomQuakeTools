# load a local wishlist of file urls, then attempt to download each
# file url from the internet archive and report progress
from urllib.request import urlopen

# load file contents into memory, return as string
def load_file(filepath):
    with open(filepath, 'rt', encoding='utf8') as file:
        return file.read()

def get_archive_url(url, timestamp):
    return f'https://web.archive.org/web/{timestamp}fw_/{url}'

def save_to_file(data, filepath):
    # save to file
    with open(filepath, 'wb') as f:
        f.write(data)

# download a url as blob of data
def download_url(urlpath):
    try:
        with urlopen(urlpath) as response:
            return response.read()
    except Exception as e:
        # print(e)
        return None

# query archive.org
def build_query(query):
    # remove leading protocol
    if query.startswith('http://'):
        query = query.replace('http://', '')
    if query.startswith('https://'):
        query = query.replace('https://', '')
    if query.startswith('ftp://'):
        query = query.replace('ftp://', '')
    # remove trailing slash for consistency
    if query.startswith('/'):
        query = query[:-1]
    # build the url path
    urlpath = f'http://web.archive.org/cdx/search/cdx?url={query}*&output=txt'
    return urlpath

# parse result into a list of records
def parse_result(result):
    result_list = list()
    for line in result.splitlines():
        # split into pieces
        entry = line.split()
        # store
        result_list.append(entry)
    return result_list

# return dict of URL to set of timestamps
def filter_results(url_list):
    url_map = dict()
    for entry in url_list:
        # <internal name> <timestamp> <url> <format> <return code> <hash> <number>
        _, timestamp, url, fmt, code, _, _ = entry
        print(f'\t{code}, {timestamp}, {url}')
        # skip if http return codes like 3xx 4xx 5xx
        if code != '200':
            continue
        # remove port if present
        if ':80' in url:
            url = url.replace(':80', '')
        # assume www and non www versions are the same?
        if 'www.' in url:
            url = url.replace('www.', '')
        # check if exists
        ts = int(timestamp)
        if url in url_map:
            # add timestamp to set
            url_map[url].add(ts)
        else:
            # create new entry in dict
            url_map[url] = {ts}
    return url_map

# query archive.org and return map of urls to timestamp
def get_unique_urls(query):
    # build the query
    urlpath = build_query(query)
    # execute the query and download results
    content = download_url(urlpath)
    if content is None:
        return None
    # decode as text
    txt = content.decode('utf-8', errors='ignore')
    # parse text to entries
    result_list = parse_result(txt)
    # filter urls
    url_map = filter_results(result_list)
    # print('.%d unique urls' % len(url_map))
    return url_map

def download_wishlist(wishlist):
    for line in wishlist:
        # skip empty lines
        line = line.strip()
        if not line:
            continue
        # skip comments
        if line.startswith('#'):
            continue
        # skip ftp
        if line.startswith('ftp'):
            continue
        # get archive url
        url_map = get_unique_urls(line)
        print(f'{line} got {url_map}')
        # TODO download everything???

# protect the entry point
if __name__ == '__main__':
    # local path wishlist file containing one file url per line
    wishlist_path = '...'
    # load wishlist into memory
    wishlist = load_file(wishlist_path)
    wishlist = wishlist.splitlines()
    print(f'Loaded {len(wishlist)} lines from wishlist.')
    # try and download each url from the internet archive
    download_wishlist(wishlist)

