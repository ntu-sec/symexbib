#!/usr/bin/env python

# remove section read/rating/date-added/date-modified/abstract/local-url/file
# remove accents

from __future__ import print_function
import os
import sys
import bibtexparser
import re

class BibType:
    PROC = 1
    JOURNAL  = 2

def getValue(entry, key):
    try:
        return entry[key]
    except KeyError:
        print("no '{}' for '{}'".format(key, entry['id']))
        exit(1)

def delKey(entry, key):
    if key in entry:
        del entry[key]

def Englishize(s):
    return re.sub(r'(\\[\w\"\'\`\^]|\{|\})', '', s)

def refine_title(entry):
    title = getValue(entry, 'title')
    if title[-1] == '.':
        entry['title'] = title[:-1]

venue_suffix = re.compile(r'\'[0-9]{2,4}$')
def refine_venue(entry):
# TODO should recognize type !
    if 'booktitle' in entry:
        venue = entry['booktitle'] 
        if not re.search(venue_suffix, venue):
            new_venue = venue + ' \'' + str(getValue(entry, 'year')[-2:]) 
            print('{:80} {:}'.format(venue, new_venue))
            entry['booktitle'] = new_venue

if len(sys.argv) < 2:
    print("usage: {} bibtex_file".format(sys.argv[0]))
    exit(1)

filename = sys.argv[1]

with open(filename, 'r') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

PREAMBLE = '''|Title|Year|Venue|Authors|
|-----|-----|----|-------|
'''
mkd_fname = os.path.splitext(filename)[0] + '.md'
outlist = []
entry_list = bib_database.get_entry_list()
for entry in entry_list:
    year = getValue(entry, 'year')
    venue = ''
    if 'booktitle' in entry:
        venue = entry['booktitle']
    if 'journal' in entry:
        venue = entry['journal']
    title = getValue(entry, 'title')
    link = getValue(entry, 'link')
    author = getValue(entry, 'author')
    author = Englishize(author)
    if '\\' in author:
        print(repr(author))
    outlist.append((year, venue, title, link, author))
outlist.sort(key=lambda tup: str(tup[0]) + tup[1], reverse=True)

with open(mkd_fname, 'w') as md:
    md.write(PREAMBLE)
    for tup in outlist:
        title = '[' + tup[2] + '](' + tup[3] + ')'
        out = '|' + ' |'.join([title, tup[0], tup[1], tup[4]]) + '|\n'
        md.write(out)

for entry in entry_list:
    for k in ['read', 'rating', 'date-added', 'date-modified', 'language', 'uri', 'abstract', 'local-url', 'file']:
        delKey(entry, k)
    refine_title(entry)
    # refine_venue(entry)

with open(filename, 'w') as newbib:
    bibtexparser.dump(bib_database, newbib)
