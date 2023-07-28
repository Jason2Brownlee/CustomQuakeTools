# crawl a website and report all unique urls (multithreaded)
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# download a url as blob of data
def download_html(urlpath):
    with urlopen(urlpath) as f:
        return f.read()

# retrieve all URLs from a downloaded blob of content (html)
def get_urls_from_html(content):
    # decode the content
    html = content.decode('ascii', 'ignore')
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
    # handle 404 errors, and bad parse errors
    try:
        # download html
        content = download_html(path)
        # get all relative urls
        rel_links = get_urls_from_html(content)
    except Exception as e:
        print(f'> error {path} -> {e}')
        return (path, list())
    # process one by one, so if there is a failure, we don't lose it all
    abs_links = set()
    for url in rel_links:
        try:
            # join the url with the path to make absolute
            abs_link = urljoin(path, url)
            # add to set
            abs_links.add(abs_link)
        except Exception as e:
            # skip invalid urls that cannot be parsed
            continue
    return (path, abs_links)

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

# report all urls in a pretty way
def report_urls(name, url_set):
    # convert to list
    url_list = list(url_set)
    # sort
    url_list.sort()
    # report name
    print(name)
    # report one per line
    for url in url_list:
        print(url)

# check if a url is in scope or not
def in_scope(hosts, url):
    # convert to lower case
    url = url.lower()
    # check if we have a single host
    if not isinstance(hosts, list):
        hosts = [hosts]
    # check each host in the list
    for host in hosts:
        # check if url starts with the
        if url.startswith(host):
            return True
    # the url is not in scope
    return False

# entry point
def main(host, start_url):
    # set of all urls found and processes
    unqiue_urls = set()
    # set of urls that need to be processed
    in_progress = set()
    # set of all skipped urls
    skipped = set()
    # add the entry point to the in progress set
    in_progress.add(start_url)
    # add the entry point to the set of all known urls on the host
    unqiue_urls.add(start_url)
    # create process pool
    with ThreadPoolExecutor(100) as exe:
        # run until there are no further urls to process
        while in_progress:
            # pop all urls
            candidates = [in_progress.pop() for _ in range(len(in_progress))]
            # download each url in parallel
            futures = [exe.submit(process_url, url) for url in candidates]
            # process results in completion order
            for future in as_completed(futures):
                # unpack into url and results
                next_url, urls = future.result()
                # mark the url as processed
                unqiue_urls.add(next_url)
                # report a message
                print(f'> {next_url} -> found {len(urls)}')
                # process all new urls
                for url in urls:
                    # check if it is offsite
                    if not in_scope(host, url):
                        # print(f'> skipping {url}')
                        skipped.add(url)
                        continue
                    # check if the url has been processed
                    if url in unqiue_urls:
                        continue
                    # check if the url is known and will be processed
                    if url in in_progress:
                        continue
                    # skip urls that don't look right
                    if not can_process_url(url):
                        # print(f'> skipping {url}')
                        # add to the set of all known urls on the host
                        unqiue_urls.add(url)
                        continue
                    # add as a url to the set we want to process
                    in_progress.add(url)
    # final message
    print('DONE')
    print(f'Found {len(unqiue_urls)} unique urls:')
    print(f'Skipped {len(skipped)} unique urls:')
    print('\n\n')
    report_urls('Crawled URLs:', unqiue_urls)

# protect the entry point
if __name__ == '__main__':
    # define the hostname used to filter urls to consider
    host = 'http://...'
    # define the starting point of the crawl
    start_url = 'http://...'
    # perform the crawl
    main(host, start_url)
