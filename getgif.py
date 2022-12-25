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

fail_words = []
for line in open(args.word):
    line = line.strip()
    if line == "" or line[0] == '#':
        continue
    line = ensure_unicode(line)
    for word in line:
        print "取得", word, "的图片"
        utf8_word = word.encode('utf8')
        url_word = urllib.quote(utf8_word)
        pic_dir = os.path.join(args.out, url_word + ".gif")

        if os.path.exists(pic_dir):
            print word, "的文件已经存在"
            continue

        if args.old != "" and os.path.exists(os.path.join(args.old, url_word + ".gif")):
            print word, "的文件已经存在" + args.old
            continue

        try:
            if args.cn:
                contents = urllib2.urlopen("http://bishun.strokeorder.info/mandarin.php?q="+url_word).read()
            else:
                contents = urllib2.urlopen("http://www.strokeorder.info/mandarin.php?q="+url_word).read()
        except:
            fail_words.append((word, url_word))
            print word, "下载失败"
            continue
        if args.cn:
            searchObj = re.search(r'\<img src=\"(http:\/\/bishun\.strokeorder\.info\/characters\/\d+\.gif)\" alt\=\"' + utf8_word + r'的笔顺\"\>', contents)
        else:
            searchObj = re.search(r'\<img src=\"(http:\/\/bishun\.strokeorder\.info\/characters\/\d+\.gif)\" alt\=\"stroke order animation of ' + utf8_word + r'\"\>', contents)
        if searchObj == None:
            fail_words.append((word, url_word))
            print "没有找到", word, "的图片"
            continue
        pic_url = searchObj.group(1)
        urllib.urlretrieve(pic_url, pic_dir)
        print pic_dir
        time.sleep(random.randint(1,3))

if len(fail_words) > 0:
    print "这些字下载失败"
    for w in fail_words:
        print w[0], w[1]
