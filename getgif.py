#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import urllib.request
import urllib.parse
import re
import random
import time

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--word", dest="word",
                    help="word file", required=True)
parser.add_argument("-o", "--out", action="store",
                    type=str, default="./out")
parser.add_argument("-d", "--old", action="store",
                    type=str, default="./old")
parser.add_argument("-c", "--cn", action="store_true", default=False)
args = parser.parse_args()

if not os.path.exists(args.out):
    os.makedirs(args.out)
if not os.path.exists(args.old):
    print(args.old + " is not exist")
    args.old = ""
elif os.path.isfile(args.out):
    parser.error("option --out should set a directory")

print("从文件", args.word, "读入词语")
print("文件存入目录", args.out)


def download_file(url, filename):
    try:
        local_filename, headers = urllib.request.urlretrieve(url, filename)
        if headers.get_content_type() != 'image/gif':
            return False

        content_length = headers.get('Content-Length')
        if content_length:
            local_size = os.path.getsize(local_filename)
            if int(content_length) != local_size:
                return False
        return True
    except Exception as e:
        print("Error occurred while downloading the file: {}".format(e))
        return False


def get_from_strokeorder(word, pic_dir):
    url_word = urllib.parse.quote(word)

    try:
        if args.cn:
            contents = urllib.request.urlopen("http://bishun.strokeorder.info/mandarin.php?q=" + url_word).read().decode('utf-8')
        else:
            contents = urllib.request.urlopen("http://www.strokeorder.info/mandarin.php?q=" + url_word).read().decode('utf-8')
    except Exception as e:
        print("Error occurred while fetching stroke order: {}".format(e))
        return False

    if args.cn:
        searchObj = re.search(r'<img src="(http://bishun.strokeorder.info/characters/\d+\.gif)" alt="' + word + r'的笔顺">', contents)
    else:
        searchObj = re.search(r'<img src="(http://bishun.strokeorder.info/characters/\d+\.gif)" alt="stroke order animation of ' + word + r'">', contents)
    if searchObj is None:
        return False
    pic_url = searchObj.group(1)
    return download_file(pic_url, pic_dir)


def get_from_zdic(word, pic_dir):
    unicode_word = hex(ord(word))[2:].upper().rstrip('L').zfill(4)
    return download_file("https://img.zdic.net/kai/jbh/" + unicode_word + ".gif", pic_dir)


fail_words = []
with open(args.word, encoding='utf-8') as word_file:
    for line in word_file:
        line = line.strip()
        if line == "" or line[0] == '#':
            continue
        for word in line:
            print("尝试取得", word, "的图片")
            pic_dir = os.path.join(args.out, word + ".gif")

            if os.path.exists(pic_dir):
                print(word, "的文件已经存在")
                continue

            if args.old != "" and os.path.exists(os.path.join(args.old, word + ".gif")):
                print(word, "的文件已经存在", args.old)
                continue

            if not get_from_strokeorder(word, pic_dir):
                if not get_from_zdic(word, pic_dir):
                    fail_words.append(word)
                    print(word, "下载失败")
                    continue

            print(pic_dir)
            time.sleep(random.randint(1, 3))

if len(fail_words) > 0:
    print("这些字下载失败")
    for w in fail_words:
        print(w)
