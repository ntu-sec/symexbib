#!/usr/bin/env python

# remove section read/rating/date-added/date-modified/abstract/local-url/file
# bibtex -> markdown (accents)

from __future__ import print_function
import os
import sys
import bibtexparser
import re

def getValue(entry, key):
    try:
        return entry[key]
    except KeyError:
        print("no '{}' for '{}'".format(key, entry['id']))
        exit(1)

def delKey(entry, key):
    if key in entry:
        del entry[key]

if len(sys.argv) < 2:
    print("usage: {} bibtex_file".format(sys.argv[0]))
    exit(1)

filename = sys.argv[1]

with open(filename) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

PREAMBLE = '''|Title|Venue|Year|Authors|
|-----|-----|----|-------|
'''
mkd_fname = os.path.splitext(filename)[0] + '.md'
outlist = []
pat_year = r"'?[0-9]{2,4}.*$"
sort_key = lambda entry: str(getValue(entry, 'year')) + '::' + getValue(entry, 'id') 
entry_list = sorted(bib_database.get_entry_list(), key=sort_key, reverse=True)
for entry in entry_list:
    raw_title = getValue(entry, 'title')
    link =getValue(entry, 'link')
    title = '[' + raw_title + '](' + link + ')'
###
    venue = ''
    if 'booktitle' in entry:
        venue = entry['booktitle']
    if 'journal' in entry:
        venue = entry['journal']
    venue = re.sub(pat_year, '', venue)
###
    year = getValue(entry, 'year')
    author = getValue(entry, 'author')
    out = '|' + '|'.join([title, venue, year, author]) + '|'
    outlist.append(out)
entries = '\n'.join(outlist)
with open(mkd_fname, 'w') as md:
    md.write(PREAMBLE)
    md.write(entries)

for entry in bib_database.entries:
    for k in ['read', 'rating', 'date-added', 'date-modified', 'language', 'uri', 'abstract', 'local-url', 'file']:
        delKey(entry, k)
with open(filename, 'w') as newbib:
    bibtexparser.dump(bib_database, newbib)
