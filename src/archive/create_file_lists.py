# List all known urls on a domain captured by the internet archive.
#
# 1. read a file containing a list of domains/urls
# 2. query each domain/url on the internet archive to get a list of captured urls
# 3. store the results for each in a unique file
#
# Stored .txt files are used in "check_files_in_lists.py"
#
from os import listdir
from os.path import join
from list_unique_urls import get_unique_urls

# load file contents into memory, return as string
def load_file(filepath):
    with open(filepath, 'rt', encoding='utf8') as file:
        return file.read()

def load_lists(path_dir):
    return set([name for name in listdir(path_dir)])

def domain_to_filename(domain):
    # convert slashes to dash
    pretty_domain = domain.replace('/', '-')
    # force lower case
    pretty_domain = pretty_domain.lower()
    # add .txt extension
    return f'{pretty_domain}.txt'

def save_results(results, domain, dir_path):
    # create filepath
    filename = domain_to_filename(domain)
    filepath = join(dir_path, filename)
    # save to file
    with open(filepath, 'wt') as f:
        # f.writelines(results)
        f.write('\n'.join(results))
    print(f'\tSaved {filename}')

def process(path_domainlist, path_dir):
    # load domain list
    domain_list = load_file(path_domainlist)
    domain_list = domain_list.splitlines()
    print(f'Loaded {len(domain_list)} domains in domain list.')
    # load a set of all existing lists, so we can skip those already loaded
    lists = load_lists(path_dir)
    print(f'Loaded {len(lists)} existing lists.')
    # process domains
    for domain in domain_list:
        # skip empty lines
        if not domain or domain[0]=='#':
            continue
        # check if the domain exists
        if domain_to_filename(domain) in lists:
            # print(f'.skipping "{domain}", already processed')
            continue
        # perform query and store results
        print(f'Downloading "{domain}"...')
        results = get_unique_urls(domain)
        # report
        print(f'\tFound "{len(results)}" files at {domain}')
        # always save results, to avoid duplicating queries
        save_results(results, domain, path_dir)

# protect the entry point
if __name__ == '__main__':
    # path to domain/url wish list
    path_domainlist = '../../dev/domains.txt'
    # dir to save file list txt files
    path_dir = '../../dev/lists/'
    # process the wishlist
    process(path_domainlist, path_dir)


