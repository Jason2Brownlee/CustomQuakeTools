# list all unique urls from a website that has been downloaded to disk
# website was probably downloaded from archive.org
import os
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import re

# load file into memory as binary blob
def load_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

# retrieve all URLs from a downloaded blob of content (html)
def get_urls_from_html(content):
    # decode the content
    html = content.decode('utf-8', errors='ignore')
    # parse the doc
    soup = BeautifulSoup(html, features='html.parser')
    # find all a tags
    atags = soup.find_all('a')
    # extract links
    links = list()
    for tag in atags:
        link = tag.get('href', None)
        if link is not None:
            links.append(link)
    return links

# check all tokens for urls
def get_urls_from_txt(content):
    # decode the content
    txt = content.decode('utf-8', errors='ignore')
    # split into tokens
    tokens = txt.split()
    # check each token to see if it is a url
    links = list()
    for token in tokens:
        t = token.lower()
        # check for urls
        if t.startswith('http'):
            links.append(token)
        if t.startswith('ftp'):
            links.append(token)
        if t.startswith('www'):
            links.append(token)
        # check for files
        if t.endswith('.zip'):
            links.append(token)
        if t.endswith('.exe'):
            links.append(token)
        if t.endswith('.tgz'):
            links.append(token)
        if t.endswith('.tar.gz'):
            links.append(token)
    return links

def load_and_get_all_urls(filepath):
    # load content into memory
    data = load_file(filepath)
    # get all links
    links = get_urls_from_html(data)
    # convert to a set
    result_set = set()
    for url in links:
        # skip empty links
        if not url or not url.strip():
            continue
        # skip relative links
        if url.startswith('#'):
            continue
        if url.startswith('/web/'):
            url = re.sub('^/web/[0-9]+/', '', url)
        if url.startswith('https://web.archive.org/web/'):
            url = re.sub('^https://web.archive.org/web/[0-9]+/', '', url)
        # store url
        result_set.add(url)
    # extract urls not encoded in html
    links = get_urls_from_txt(data)
    # add links to the set
    result_set.update(links)
    return result_set

# report all urls in a pretty way
def report_urls(url_set):
    # convert to list
    url_list = list(url_set)
    # sort
    url_list.sort()
    # report one per line
    for url in url_list:
        print(url)

def main(basepath):
    all_urls = set()

    # make a list of all paths to process
    paths = [os.path.join(basepath, name) for name in os.listdir(basepath)]
    # create thread pool
    with ThreadPool(100) as pool:
        for result_set in pool.map(load_and_get_all_urls, paths):
            # add to the master set
            all_urls.update(result_set)
    # statistics
    print(f'.processed {len(paths)} files')
    print(f'.found {len(all_urls)} unique urls')
    # report all urls
    report_urls(all_urls)

# protect the entry point
if __name__ == '__main__':
    # path to website
    path = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/fuhquake.net-forum'
    # report all unique urls
    main(path)

