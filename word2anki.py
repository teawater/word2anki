#!/usr/bin/python
# -*- coding: utf-8 -*-

import pypinyin
import optparse
import urllib
import urllib2
import re
import time

parser = optparse.OptionParser()
parser.add_option("-w", "--word", dest="word",
                  help="word file")
parser.add_option("-o", "--out", action="store",
                  type="string", default="./out.txt")
parser.add_option("-d", "--debug", action="store_true", default=False)
args = parser.parse_args()[0]


def ensure_unicode(v):
    if isinstance(v, str):
        v = v.decode('utf8')
    return unicode(v)


class AndiPinyin:
    def __init__(self, word, url=None):
        self.right = ""
        self.url_pinyin = ""
        self.heteronym_pinyin = ""

        pinyin_array = pypinyin.pinyin(word, heteronym=True)

        self.pinyin_array_to_utf8(pinyin_array)
        if self.right != "":
            return
        if url == None:
            return

        if args.debug:
            print "Got heteronym and try to handle it", self.heteronym_pinyin

        time.sleep(1)
        contents = urllib2.urlopen(url).read()

        right_list = []
        url_list = []
        for url_pinyin in re.findall(r'\[(.+)\]', contents):
            # Check one [ xxx xxx ] from url
            url_pinyin = url_pinyin.strip()
            url_pinyin = url_pinyin.split(" ")
            if len(url_pinyin) != len(pinyin_array):
                continue
            got = False
            for up in url_pinyin:
                string = "~!@#$%^&*()_+-*/<>,.[]\/"
                for i in string:
                    if i in up:
                        got = True
                        break
                if got:
                    break
            if got:
                continue

            if args.debug:
                print "Got url pinyin", " ".join(url_pinyin)

            # Set ret
            is_first = True
            line = ""
            for i in range(len(url_pinyin)):
                # Check each word in [ xxx xxx ]
                new_pinyin = ""
                for pinyin_array_one in pinyin_array[i]:
                    if pinyin_array_one.encode('utf8') == url_pinyin[i]:
                        new_pinyin = url_pinyin[i]
                        break
                if new_pinyin == "":
                    line = ""
                    break
                if is_first:
                    is_first = False
                else:
                    line += " "
                line += new_pinyin

            if line != "":
                # Check if there is same line in right_list
                need_apply = True
                for right_list_one in right_list:
                    if line == right_list_one:
                        need_apply = False
                if need_apply:
                    right_list.append(line)

            # Set url_list
            upinyin = " ".join(url_pinyin)
            # Check if there is same line in url_list
            need_apply = True
            for one in url_list:
                if upinyin == one:
                    need_apply = False
            if need_apply:
                if args.debug:
                    print "Got url pinyin", upinyin
                url_list.append(upinyin)

        self.right = "或".join(right_list)
        self.url_pinyin = "或".join(url_list)

    def pinyin_array_to_utf8(self, pinyin_array):
        self.right = ""
        self.heteronym_pinyin = ""

        is_first = True
        have_heteronym = False

        for pinyin in pinyin_array:
            if len(pinyin) != 1:
                self.right = ''
                have_heteronym = True
            if is_first:
                is_first = False
            else:
                if not have_heteronym:
                    self.right += " "
                self.heteronym_pinyin += " "
            if not have_heteronym:
                self.right += pinyin[0]
            self.heteronym_pinyin += "|".join(pinyin)
        self.right = self.right.encode('utf8')
        self.heteronym_pinyin = self.heteronym_pinyin.encode('utf8')


if args.debug:
    print "呈现"
    p = AndiPinyin(ensure_unicode(
        "呈现"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("呈现") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin

    print "长大"
    p = AndiPinyin(ensure_unicode(
        "长大"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("长大") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin

    print "冰激凌"
    p = AndiPinyin(ensure_unicode(
        "冰激凌"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("冰激凌") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin

    print "扑腾"
    p = AndiPinyin(ensure_unicode(
        "扑腾"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("扑腾") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin

    print "好主意"
    p = AndiPinyin(ensure_unicode(
        "好主意"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("好主意") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin

    exit(0)

if args.word == None:
    parser.error("option --word must set")

print "从文件", args.word, "读入词语"
print "写入文件", args.out

out = open(args.out, "w")
heteronym = False
for word in open(args.word):
    word = word.strip()
    if word == "":
        continue
    url_word = urllib.quote(word)
    baidu_url = 'https://hanyu.baidu.com/s?wd=' + url_word + '&amp;from=zici'
    p = AndiPinyin(
        ensure_unicode(word), baidu_url)

    pinyin = ''
    if p.right == "":
        heteronym = True
        if p.url_pinyin != "":
            pinyin = p.url_pinyin
            print "处理", word, "拼音是", pinyin, "可能有问题，注意检查。"
        else:
            pinyin = "多音字" + p.heteronym_pinyin
            print "处理", word, pinyin, "失败，请手动处理。"
    else:
        pinyin = p.right

    line = "<h2><b>" + pinyin + "</b></h2>\t"
    line += '"' + word
    line += '<div><a href=""http://bishun.shufaji.com/?char=' + \
        url_word + '"">笔顺</a><br></div>'
    line += '<div><a href=""' + baidu_url + '"">解释</a><br></div>"'

    out.write(line)
    out.write("\n")
out.close()

if heteronym:
    print '有多音字请注意搜索多音字并替换成相应拼音'
