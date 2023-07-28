# Custom Quake Tools

A collection of custom scripts for working with Quake assets.

Used in the **Quake Buffet** project at http://QuakeBuffet.com and in the **Quake Bot Archive** project at http://QuakeBotArchive.com

## Install

Assumes Python 3.10+ is installed.

1. Download code
	`git clone git@github.com:Jason2Brownlee/CustomQuakeTools.git`
2. Install requirements
	`pip3 install -r requirements.txt`
3. Run scripts...

## Scripts

Summary of the scripts in this project.

### Internet Archive

Scripts for downloading files from the internet archive, e.g. https://archive.org

* Search for a wishlist of files in all lists of files for domains on the internet archive.
* List all files in the internet archive for a domain.
* Download all versions of a file from the internet archive.
* Download the most recent version of all files for a website on the internet archive.
* Download all versions of all files for a site on the internet archive.
* Try and download all URLs in a wishlist file from the internet archive.
* List all unique URLs for a website on the internet archive.
* List all unique URLs in website downloaded from the internet archive.

### Quake Map Files (BSPs)

* List all BSP files in a mod directory (maps/ and pak files).
* Summarize the worldspawn entity for a map file.

### Quake Pak files (PAKs)

* Extract all files from a pak file.
* List all files in a pak file.
* List all map files in all pak files in a mod directory.

### Websites / URLs

* Crawl a website and list all unique URLs found.
* List all files on a website (e.g. HTML FTP file list) not in a local directory.
* Download all files listed on a website (e.g. an HTML FTP file list).
* Find all broken URLs on a webpage.
* List all URLs on a webpage.
* Search all text files listed on an HTML FTP for given tokens.

### Zip Files

* List the contents of a zip file.
* Search all zip files in a directory for files with a given extension.
* Search all text files in all zip files in a directory for given tokens.
* Search all text files in one zip file for given tokens


## References

* [quake-cli-tools](https://github.com/joshuaskelly/quake-cli-tools/) Command line tools for creating Quake content.
* [vgio](https://github.com/joshuaskelly/vgio/) File I/O for video games.
* [Wayback CDX Server API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) Wayback machine API.
* [wget python](https://pypi.org/project/wget/) Pure python download utility.
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) Python web scraping library.
