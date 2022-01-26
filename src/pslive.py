#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Tom Cai <1tomcai@gmail.com>'
__date__ = '2017-10-31'
__summary__ = 'A terminal based vocaburary leaning utility interative at every prompt. Tested on python3.'

class PSLive:
    '''
* two data files (data.json, wip.json) are stored in <HOME DIR>/.pslive folder. pslive.py will create this folder if not exist
* if data.json does not exist or too old (default age 3600 seconds)
  - fetch live data from internet and save the data to data.json (more work to be done here, or you can add your own code to fetch live data)
* if wip.json does not exist
  - get a random entry in data.json
  - display the key
  - save the key to wip.json
* if wip.json exists
  - read wip.json and compare to the corresponding entry in data.json
  - if they equel, then repeat steps as if wip.json file does not exist
  - if they do not equel, display the next value that is not in the wip.json and update wip.json to add the displayed value list

## Use cases
1. flashcard: data.json stores words and their definition, example sentences, descriptions, etc.
2. news flash: data.json stores headlines and short stores
3. reminder: data.json stores tasks / due dates
'''

import json
import random
import os
import time

PSLIVE_DIR = '%s/.pslive' % os.getenv("HOME")
CURRENT_FILE = 'wip.json'
DATA_FILE = 'data.json'
MAX_AGE = 900 # seconds = 15 minutes

def get_entries(infile, key=None):
    '''
    infile: input file in key:value or key:[x,y,z] format
    key   : a key to identify a specific entry
    output: if no key is supplied, all entries will be returned
            otherwise, the corresponding entry will be returned
    '''
    try:
        with open(infile) as f:
            entries = json.load(f.read())

        return {key: entries[key]} if key else entries

    except Exception as e:
        print(e)
        return

def get_live_data(source, kind):
    '''
    source: url
    kind: tbd
    output: None. side effort is the ~/.pslive/data.json will be populated
    notes: currently simulate live data feed by copying a local file
    '''
    import shutil
    shutil.copyfile('{}/words.txt'.format(os.getenv("HOME")), '{}/{}'.format(PSLIVE_DIR, DATA_FILE))

def file_obsolete(fname, max_age):
    '''
    fname: file name
    max_age: max age in seconds. if a file's age is greater than the max age, it's considered as obsolete
    output: True or False
    '''
    if not os.path.exists(fname) or time.time() - os.path.getctime(fname) > max_age:
        return True
    else:
        return False

def show_random_key(wip_file, data_entries):
    '''
    wip_file: file name containing the current working entry
    data_entries: dictionary containing full entries from ~/.pslive/data.json
    output: None. Side effort is to display a random key from data_entries and populate 'Key:' to the wip_file
    '''
    try:
        key = random.choice(list(data_entries.keys()))
        key_null = {key: None}
        with open(wip_file, 'w') as f:
            json.dump(key_null, f)
        print(key)
    except Exception as e:
        print('error:', e)
        return

def display_next(wip_file, partial_entry, data_entries):
    '''
    partial_entry: a dictionary for the current entry, may contain none or partial values
    data_entries: a dictionary for the whole data entries from ~/.pslive/data.json
    output: None. Side effort is to display the next value for the current key
    '''
    key = next(iter(partial_entry))
    partial_vals = partial_entry[key]
    full_vals = data_entries[key]
    partial_vals = partial_vals if isinstance(partial_vals, list) else [partial_vals] if partial_vals else []
    full_vals = full_vals if isinstance(full_vals, list) else [full_vals]
    if partial_vals == full_vals:
        os.remove(wip_file)

    while full_vals:
        next_val = full_vals.pop(0)
        if not next_val in partial_vals:
            if partial_vals:
                partial_entry[key].append(next_val)
            else:
                partial_entry[key] = [next_val]

            print(next_val)
            with open(wip_file, 'w') as f:
                json.dump(partial_entry, f)
            break

def main():
    if not (os.path.exists(PSLIVE_DIR) and os.path.isdir(PSLIVE_DIR)):
        os.mkdir(PSLIVE_DIR)

    try:
        data_file = "%s/%s" % (PSLIVE_DIR, DATA_FILE)
        if file_obsolete(data_file, MAX_AGE):
            get_live_data('~/words.txt', 'localfile')

        with open(data_file) as f:
            data_entries = json.load(f)

    except Exception as e:
        print(e)
        return

    try:
        wip_file = "%s/%s" % (PSLIVE_DIR, CURRENT_FILE)

        with open(wip_file) as f:
            partial_entry = json.load(f)

        display_next(wip_file, partial_entry, data_entries)


    except Exception as e:
        show_random_key(wip_file, data_entries)

if __name__ == '__main__':
    main()
