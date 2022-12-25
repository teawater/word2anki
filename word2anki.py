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
parser.add_option("-p", "--pinyin", action="store_true", default=False)
parser.add_option("-d", "--debug", action="store_true", default=False)
parser.add_option("--heteronym", action="store_true", default=False)
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
        self.heteronym = False

        pinyin_array = pypinyin.pinyin(word, heteronym=True)

        self.pinyin_array_to_utf8(pinyin_array)
        if self.right != "":
            return
        if url == None:
            return

        if args.debug:
            print "Got heteronym and try to handle it", self.heteronym_pinyin

        time.sleep(1)
        if args.debug:
            print "Access url to get pinyin", url
        contents = urllib2.urlopen(url).read()

        right_list = []
        url_list = []

        raw_pinyin_list = []
        if len(word) > 1:
            raw_pinyin_list = re.findall(r'\[(.+)\]', contents)
        else:
            contents = contents.split('<div class="pronounce" id="pinyin">')
            if len(contents) == 2:
                contents = contents[1]
                contents = contents.split("</div>")
                if len(contents) > 1:
                    contents = contents[0]
                    pattern = re.compile(r'\<b\>(.+)\<\/b\>')
                    for p in pattern.findall(contents):
                        raw_pinyin_list.append(p)
        for url_pinyin in raw_pinyin_list:
            # Check one [ xxx xxx ] from url
            url_pinyin = url_pinyin.strip()
            url_pinyin = url_pinyin.split(" ")
            if len(url_pinyin) != len(pinyin_array):
                continue
            got = False
            for up in url_pinyin:
                string = "~!@#$%^&*()_+-*/<>,.[]\/0"
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
        if len(right_list) > 1 or len(url_list) > 1:
            self.heteronym = True

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
    print "顿"
    p = AndiPinyin(ensure_unicode(
        "顿"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("顿") + '&ptype=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print p.heteronym
    print "---"

    print "屹"
    p = AndiPinyin(ensure_unicode(
        "屹"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("屹") + '&ptype=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print "---"

    print "乾"
    p = AndiPinyin(ensure_unicode(
        "乾"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("乾") + '&ptype=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print "---"

    print "乾坤"
    p = AndiPinyin(ensure_unicode(
        "乾坤"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("乾坤") + '&ptype=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print "---"

    print "乾坤"
    p = AndiPinyin(ensure_unicode(
        "乾坤"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("乾坤") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print "---"

    print "呈现"
    p = AndiPinyin(ensure_unicode(
        "呈现"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("呈现") + '&ptype=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print "---"

    print "长大"
    p = AndiPinyin(ensure_unicode(
        "长大"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("长大") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print "---"

    print "冰激凌"
    p = AndiPinyin(ensure_unicode(
        "冰激凌"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("冰激凌") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print "---"

    print "扑腾"
    p = AndiPinyin(ensure_unicode(
        "扑腾"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("扑腾") + '&amp;from=zici')
    print p.right
    print p.url_pinyin
    print p.heteronym_pinyin
    print "---"

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
#print "写入文件", args.out

#out = open(args.out, "w")
heteronym_words = []


class AndiWord:
    def __init__(self, word):
        self.word = word
        self.heteronym = False

        self.url_word = urllib.quote(word)
        self.baidu_url = 'https://hanyu.baidu.com/s?wd=' + self.url_word
        if len(word) == 1:
            self.baidu_url += '&ptype=zici'
        else:
            self.baidu_url += '&amp;from=zici'
        p = AndiPinyin(ensure_unicode(word), self.baidu_url)

        self.pinyin = ''
        if p.right == "":
            self.heteronym = True
            if p.url_pinyin != "":
                self.pinyin = p.url_pinyin
                print "处理", self.word, "拼音是", self.pinyin, "可能有问题，注意检查。"
            else:
                self.pinyin = "多音字" + p.heteronym_pinyin
                print "处理", self.word, self.pinyin, "失败，请手动处理。"
            
        else:
            self.pinyin = p.right
            if p.heteronym:
                print word, "拼音是", self.pinyin, "是多音字注意检查。"
                self.heteronym = True

out = None
for word in open(args.word):
    word = word.strip()
    # First charactor check
    if word == "":
        continue
    if word[0] == '#':
        if out != None:
            out.close()
        out = open(word, "w")
        print "写入文件", word
        continue

    words = []
    for word in word.split(' '):
        word = word.strip()
        if word == "":
            continue

        w = AndiWord(word)

        if w.heteronym:
            heteronym_words.append(w.word)
            if args.pinyin and not args.heteronym:
                continue
        words.append(w)

    if len(words) == 0:
        continue

    line = ""
    if args.pinyin:
        line += "<h2><b>"
        is_first = True
        for w in words:
            if is_first:
                is_first = False
            else:
                line += " "
            line += w.word
        line += "</b></h2>\t"
        line += '"'
        for w in words:
            line += "<h2><b>" + w.pinyin + " " + w.word + "</b></h2><br>"
    else:
        line += "<h2><b>"
        is_first = True
        for w in words:
            if is_first:
                is_first = False
            else:
                line += " | "
            line += w.pinyin
        line += "</b></h2>\t"
        line += '"'
        for w in words:
            line += w.word
            line += '<div>'
            unicode_word = ensure_unicode(w.word)
            for single in unicode_word:
                line += '<img src=""' + \
                    urllib.quote(single.encode('utf8')) + '.gif"">'
            line += '<br></div>'
    for w in words:
        line += '<div><a href=""http://bishun.shufaji.com/?char=' + \
            w.url_word + '"">' + w.word + '笔顺</a><br></div>'
        line += '<div><a href=""' + w.baidu_url + '"">' + w.word + '解释</a><br></div>'
    line += '"'

    if out == None:
        out = open(args.out, "w")
        print "写入文件", args.out
    out.write(line)
    out.write("\n")
if out != None:
    out.close()

if len(heteronym_words) > 0:
    print '有多音字请注意搜索多音字并替换成相应拼音'
    for w in heteronym_words:
        print w
