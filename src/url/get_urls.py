# list all urls on an ftp file list page
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup

# download a url as blob of data
def download_html(urlpath):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urlopen(urlpath, context=ctx) as f:
        content = f.read()
        return content

# retrieve all URLs from a downloaded blob of content (html)
def get_urls_from_html(content):
    # decode the content
    html = content.decode('utf-8', errors='ignore')
    # parse the doc
    soup = BeautifulSoup(html, features="html.parser")
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
        if url.startswith('http') or url.startswith('ftp'):
            abs_urls.append(url)
            continue
        # build an absolute url
        # TODO safer?
        absurl = path + url
        abs_urls.append(absurl)
    return abs_urls

# protect the entry point
if __name__ == '__main__':
    # website to consider
    website = 'https://...'
    # download html
    content = download_html(website)
    # get all relative urls
    rel_links = get_urls_from_html(content)
    # convert relative urls to absolute urls
    abs_links = rel_to_abs(website, rel_links)
    # report results
    for a in abs_links:
        print(a)
