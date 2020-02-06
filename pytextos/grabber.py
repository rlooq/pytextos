"""
Module to download title <h1> and body <p> text from a given set of URLs
"""

__author__ = "rlooq"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from bs4 import BeautifulSoup as soup
import requests
from requests.exceptions import HTTPError
from datetime import datetime
import sys

def manual_urls(number_of_urls):
    """ Takes number of URLs, which are entered manually, and returns list"""
    urls=[]
    for i in range(number_of_urls):
        url_entry=input('Enter URL: ')
        urls.append(url_entry)
    return urls

def urls_from_file(filename):
    """ Takes a text file with a list of URLs and returns Python list"""
    with open(filename, 'r', encoding='utf=8') as f:
        urls=f.read().splitlines() # to get rid of trailing \n
    return urls

def scrape(url_list):
    """ Takes a list of URLs and scrapes title, body text and source URL, all saved as txt file"""
    user_agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
    headers={'User-Agent': user_agent}
    n=1
    for url in url_list:
        try:
            response=requests.get(url, headers=headers)
            response.raise_for_status()
            # If the response is successful, no exception will be raised
            page=soup(response.text, 'html.parser')
            today=datetime.now().strftime('%Y%m%d')
            filename='{}_text_{}.txt'.format(today, n)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("{}\n".format(page.title.string))
                for i in page.findAll('p'):
                    f.write((i.text + '\n'))
                f.write(response.url)
        except HTTPError as http_err:
            print("HTTP error occurred: {}".format(http_err))
        except Exception as err:
            print("Other errors occurred: {}".format(err))
        else:
            print('Success! File {} saved.'.format(filename))
        n+=1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extracts title and body text from a given set of URLs and saves it to a text file')
    # Required positional argument
    parser.add_argument("--manual", help="Takes a number of URLs to be entered manually (default 1)", default=1, type=int)
    parser.add_argument("--file", help="Takes URLs from a given text tile")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    if args.file:
        scrape(urls_from_file(args.file))
    elif args.manual:
        scrape(manual_urls(args.manual))
    input('Press ENTER to exit')
