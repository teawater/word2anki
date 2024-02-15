#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import os
import urllib
import urllib2
import re
import random
import time

parser = optparse.OptionParser()
parser.add_option("-w", "--word", dest="word",
                  help="word file")
parser.add_option("-o", "--out", action="store",
                  type="string", default="./out")
parser.add_option("-d", "--old", action="store",
                  type="string", default="./old")
parser.add_option("-c", "--cn", action="store_true", default=False)
args = parser.parse_args()[0]

if args.word == None:
    parser.error("option --word must set")
if not os.path.exists(args.out):
    os.makedirs(args.out)
if not os.path.exists(args.old):
    print args.old + " is not exist"
    args.old = ""
elif os.path.isfile(args.out):
    parser.error("option --out should set a directory")

print "从文件", args.word, "读入词语"
print "文件存入目录", args.out

def ensure_unicode(v):
    if isinstance(v, str):
        v = v.decode('utf8')
    return unicode(v)

def download_file(url, filename):
    try:
        local_filename, headers = urllib.urlretrieve(url, filename)
        if headers.gettype() != 'image/gif':
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
    utf8_word = word.encode('utf8')
    url_word = urllib.quote(utf8_word)

    try:
        if args.cn:
            contents = urllib2.urlopen("http://bishun.strokeorder.info/mandarin.php?q="+url_word).read()
        else:
            contents = urllib2.urlopen("http://www.strokeorder.info/mandarin.php?q="+url_word).read()
    except:
        return False
    if args.cn:
        searchObj = re.search(r'\<img src=\"(http:\/\/bishun\.strokeorder\.info\/characters\/\d+\.gif)\" alt\=\"' + utf8_word + r'的笔顺\"\>', contents)
    else:
        searchObj = re.search(r'\<img src=\"(http:\/\/bishun\.strokeorder\.info\/characters\/\d+\.gif)\" alt\=\"stroke order animation of ' + utf8_word + r'\"\>', contents)
    if searchObj == None:
        return False
    pic_url = searchObj.group(1)
    return download_file(pic_url, pic_dir)

def get_from_zdic(word, pic_dir):
    unicode_word = hex(ord(word))[2:].upper().rstrip('L').zfill(4)
    return download_file("https://img.zdic.net/kai/jbh/" + unicode_word + ".gif", pic_dir)

fail_words = []
for line in open(args.word):
    line = line.strip()
    if line == "" or line[0] == '#':
        continue
    line = ensure_unicode(line)
    for word in line:
        print "尝试取得", word, "的图片"
        unicode_word = hex(ord(word))[2:].upper().rstrip('L').zfill(4)
        pic_dir = os.path.join(args.out, word + ".gif")

        if os.path.exists(pic_dir):
            print word, "的文件已经存在"
            continue

        if args.old != "" and os.path.exists(os.path.join(args.old, word + ".gif")):
            print word, "的文件已经存在" + args.old
            continue

        if not get_from_strokeorder(word, pic_dir):
            if not get_from_zdic(word, pic_dir):
                fail_words.append(word)
                print word, "下载失败"
                continue

        print pic_dir
        time.sleep(random.randint(1,3))

if len(fail_words) > 0:
    print "这些字下载失败"
    for w in fail_words:
        print w
