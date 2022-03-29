# read a wishlist of urls, search for all files on archive.org for each and save in a .txt file.
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

if __name__ == '__main__':
    # domain wish list
    path_domainlist = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/domains.txt'
    # dir to save file list txt files
    path_dir = '/Users/jasonb/Development/Quake/CustomQuakeTools/dev/lists/'
    # process the wishlist
    process(path_domainlist, path_dir)


# TODO use threads


