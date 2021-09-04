# list all urls on an ftp file list page

import urllib
from bs4 import BeautifulSoup

# download a url as blob of data
def download_html(urlpath):
    with urllib.request.urlopen(urlpath) as f:
        content = f.read()
        return content

# retrieve all URLs from a downloaded blob of content (html)
def get_urls_from_html(content):
    # decode the content
    html = content.decode('utf-8')
    # parse the doc
    soup = BeautifulSoup(html, features="lxml")
    # find all a tags
    atags = soup.find_all('a')
    # extract links
    links = list()
    for tag in atags:
        link = tag.get('href', None)
        if link is not None:
            links.append(link)
    return links

# convert relative urls to absolute urls so we can download them
def rel_to_abs(path, urls):
    abs_urls = list()
    for url in urls:
        # check if we should skip/drop a bad url
        if url.startswith('../'):
            continue
        # check if already absolute
        if url.startswith('http'):
            abs_urls.append(url)
            continue
        # build an absolute url
        # TODO safer?
        absurl = path + url
        abs_urls.append(absurl)
    return abs_urls

path = 'https://www.quaddicted.com/files/idgames2/quakec/compilations/'

# download html
content = download_html(path)
# get all relative urls
rel_links = get_urls_from_html(content)
# convert relative urls to absolute urls
abs_links = rel_to_abs(path, rel_links)

for a in abs_links:
    print(a)