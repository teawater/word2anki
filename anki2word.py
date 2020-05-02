#!/usr/bin/python
# -*- coding: utf-8 -*-

import pypinyin
import optparse
import urllib
import urllib2
import re
import time
import codecs

parser = optparse.OptionParser()
parser.add_option("-a", "--anki", dest="anki",
                  help="anki txt file")
parser.add_option("-o", "--out", action="store",
                  type="string", default="./word.txt")
args = parser.parse_args()[0]

def ensure_unicode(v):
    if isinstance(v, str):
        v = v.decode('utf8')
    return unicode(v)

out = codecs.open(args.out, "w", 'utf8')
for raw_line in open(args.anki):
    raw_line = raw_line.strip()
    if raw_line == "" or raw_line[0] == '#':
        continue
    line = raw_line.split("\t")
    if len(line) < 2:
        print raw_line, "格式不对"
    line = ensure_unicode(line[1])

    searchObj = re.search(u'^\"([\u4e00-\u9fa5]+)\<div\>', line)
    if searchObj == None:
        print raw_line, "格式不对"
        continue

    out.write(searchObj.group(1))
    out.write("\n")
out.close()
