#!/usr/bin/env python

# dump to markdown
# remove section read/rating/date-added/date-modified/abstract/local-url/file

from __future__ import print_function
import os
import sys
import bibtexparser

with open('SE.bib') as bibtex_file:
    bibtex_str = bibtex_file.read()

def getValue(entry, key):
    try:
        return entry[key]
    except KeyError:
        print("no '{}' for '{}'".format(key, entry['id']))
        exit(1)

PREAMBLE = '''|Title|Venue|Year|Authors|
|-----|-----|----|-------|
'''

outlist = []
bib_database = bibtexparser.loads(bibtex_str)
for entry in bib_database.entries:
    print(str(entry) + '\n')
    raw_title = getValue(entry, 'title')
    link =getValue(entry, 'link')
    title = '[' + raw_title + '](' + link + ')'
    venue = ''
    year = getValue(entry, 'year')
    author = getValue(entry, 'author')
    out = '|' + '|'.join([title, venue, year, author]) + '|'
    outlist.append(out)
entries = '\n'.join(outlist)

with open('SE.md', 'w') as md:
    md.write(PREAMBLE)
    md.write(entries)
