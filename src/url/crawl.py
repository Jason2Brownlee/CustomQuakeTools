# crawl a website and report all unique urls found
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# download a url as blob of data
def download_html(urlpath):
    with urlopen(urlpath) as f:
        return f.read()

# retrieve all URLs from a downloaded blob of content (html)
def get_urls_from_html(content):
    # decode the content
    html = content.decode('utf-8')
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

# process a single url and return all absolute urls found
def process_url(path):
    # download html
    try:
        content = download_html(path)
    except HTTPError as e:
        print(f'> skipping {path} -> {e}')
        return list()
    # get all relative urls
    rel_links = get_urls_from_html(content)
    # convert relative urls to absolute urls
    abs_links = {urljoin(path, url) for url in rel_links}
    return abs_links

# return true if the url can be processed, false otherwise
def can_process_url(url):
    # covert to lower case
    url = url.lower()
    # expect a webpage file
    if url.endswith('html'):
        return True
    if url.endswith('htm'):
        return True
    if url.endswith('/'):
        return True
    # I don't know what this is
    return False

# entry point
def main(host, start_url):
    # set of all urls found and processes
    unqiue_urls = set()
    # set of urls that need to be processed
    in_progress = set()
    # add the entry point to the in progress set
    in_progress.add(start_url)
    # add the entry point to the set of all known urls on the host
    unqiue_urls.add(start_url)
    # run until there are no further urls to process
    while in_progress:
        # retrieve the next url
        next_url = in_progress.pop()
        # get all links in the url
        urls = process_url(next_url)
        # mark the url as processed
        unqiue_urls.add(next_url)
        # report a message
        print(f'> {next_url} -> found {len(urls)}')
        # process all new urls
        for url in urls:
            # check if it is offsite
            if not url.lower().startswith(host):
                print(f'> skipping {url}')
                continue
            # check if the url has been processed
            if url in unqiue_urls:
                continue
            # check if the url is known and will be processed
            if url in in_progress:
                continue
            # skip urls that don't look right
            if not can_process_url(url):
                print(f'> skipping {url}')
                # add to the set of all known urls on the host
                unqiue_urls.add(url)
                continue
            # add as a url to the set we want to process
            in_progress.add(url)
    # final message
    print('DONE')
    print(f'Found {len(unqiue_urls)} unique urls:\n\n')
    all_urls = list(unqiue_urls)
    all_urls.sort()
    for url in all_urls:
        print(url)

# protect the entry point
if __name__ == '__main__':
    # define the hostname used to filter urls to consider
    host = 'http://...'
    # define the starting point of the crawl
    start_url = 'http://...'
    # perform the crawl
    main(host, start_url)
