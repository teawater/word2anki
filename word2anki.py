#!/usr/bin/python
# -*- coding: utf-8 -*-

import pypinyin
import optparse
import urllib

parser = optparse.OptionParser()
parser.add_option("-w", "--word", dest="word",
                  help="word file")
parser.add_option("-o", "--out", action="store",
                  type="string", default="./out.txt")
args = parser.parse_args()[0]
if args.word == None:
    parser.error("option --word must set")
print "从文件",args.word,"读入词语"
print "写入文件",args.out

def ensure_unicode(v):
    if isinstance(v, str):
        v = v.decode('utf8')
    return unicode(v)

def yinjie(word):
    s = ''
    got_heteronym = False
    is_first = True
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, heteronym=True):
        if len(i) != 1:
            got_heteronym = True
        if is_first:
            is_first = False
        else:
            s = s + " "
        s = s + '|'.join(i)
    return s.encode('utf8'), got_heteronym

out = open(args.out, "w")
heteronym = False
for word in open(args.word):
    word = word.strip()
    pinyin, got_heteronym = yinjie(ensure_unicode(word))
    url_word = urllib.quote(word)

    if got_heteronym:
        heteronym = True
        pinyin = "多音字"

    line = "<h2><b>" + pinyin + "</b></h2>\t"
    line += '"' + word
    line += '<div><a href=""http://bishun.shufaji.com/?char=' + url_word + '"">笔顺</a><br></div>'
    line += '<div><a href=""https://hanyu.baidu.com/s?wd=' + url_word + '&amp;from=zici"">解释</a><br></div>"'

    out.write(line)
    out.write("\n")
out.close()

if heteronym:
    print '有多音字请注意搜索多音字并替换成相应拼音'