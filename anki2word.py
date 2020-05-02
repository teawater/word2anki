#!/usr/bin/python
# -*- coding: utf-8 -*-

import pypinyin
import optparse
import urllib
import urllib2
import re
import time

parser = optparse.OptionParser()
parser.add_option("-a", "--anki", dest="anki",
                  help="anki txt file")
parser.add_option("-o", "--out", action="store",
                  type="string", default="./word.txt")
args = parser.parse_args()[0]

if args.anki == None:
    parser.error("option --anki must set")

def ensure_unicode(v):
    if isinstance(v, str):
        v = v.decode('utf8')
    return unicode(v)

fail_lines = []
out = open(args.out, "w")
for raw_line in open(args.anki):
    raw_line = raw_line.strip()
    if raw_line == "" or raw_line[0] == '#':
        continue

    searchObj = re.search(r'\t\"(\W+)\<div\>', raw_line)
    if searchObj == None:
        fail_lines.append(raw_line)
        continue

    out.write(searchObj.group(1))
    out.write("\n")

out.close()
if len(fail_lines) > 0:
    print "这些行处理失败"
    for line in fail_lines:
        print line

