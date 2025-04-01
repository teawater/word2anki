#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pypinyin
import argparse
import urllib.request
import re

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--anki", dest="anki",
                    help="anki txt file", required=True)
parser.add_argument("-o", "--out", action="store",
                    type=str, default="./word.txt")
args = parser.parse_args()

fail_lines = []
with open(args.out, "w", encoding='utf-8') as out:
    with open(args.anki, encoding='utf-8') as anki_file:
        for raw_line in anki_file:
            raw_line = raw_line.strip()
            if raw_line == "" or raw_line[0] == '#':
                continue

            searchObj = re.search(r'\t\"(\W+)\<div\>', raw_line)
            if searchObj is None:
                fail_lines.append(raw_line)
                continue

            out.write(searchObj.group(1))
            out.write("\n")

if fail_lines:
    print("这些行处理失败")
    for line in fail_lines:
        print(line)
