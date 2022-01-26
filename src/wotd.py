#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
## author: Tom Cai <1tomcai@gmail.com>
## date  : 2017-11-02
## pseudo code
* this code is scraping the words of the day specific to how vocabulary.com implemented.
* first get the entries for all words-of-the-day from the initial url
* process the first entry to get words and their respective definition, sample sentences, and descriptions
"""

import requests
import os
import json
import sys
from lxml import html


BASE_URL = 'https://www.vocabulary.com'
INIT_PATH = '/lists/news'
OUT_FILE = '%s/.pslive/data.yaml' % os.getenv("HOME")

def get_page_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def get_elements(tree, query):
    results = tree.xpath(query)
    return results

def get_wotd(list_path, out_file):
    # get a list of words for the current period (most recent)
    url = '{}{}'.format(BASE_URL, list_path)
    words_tree = get_page_tree(url)
    query_word_entries = '//ol[@id="wordlist"]/li[@class="entry learnable"]'
    word_entries = get_elements(words_tree, query_word_entries)
    with open(out_file, 'w') as f:
        for entry in word_entries:
            word_info = [e.text_content().replace('\n','') for e in entry.getchildren()]
            entry = '{}: {}'.format(word_info[0], json.dumps(word_info[1:]))
            print(entry)
            f.write(entry+'\n')

def get_current_path():
    url = '{}{}'.format(BASE_URL, INIT_PATH)
    page_tree = get_page_tree(url)
    query = '//section[@class="bycat hasmore"]/div[1]/h2/a[1]'
    periods = get_elements(page_tree, query)
    if len(periods)<=0:
        print("no news entries found")
        return

    # get a list of words for the current period (most recent)
    current_path = periods[0].get('href')
    return current_path


if __name__ == '__main__':
    if len(sys.argv) > 1:
        current_path = sys.argv[1]
    else:
        current_path = get_current_path()

    get_wotd(current_path, OUT_FILE)
