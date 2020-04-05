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


def pinyin_array_to_utf8(pinyin_array):
    ret = ''
    is_first = True
    for pinyin in pinyin_array:
        if len(pinyin) != 1:
            ret = ''
            break
        if is_first:
            is_first = False
        else:
            ret += " "
        ret += pinyin[0]
    return ret.encode('utf8')


def yinjie(word, url=None):
    pinyin_array = pypinyin.pinyin(word, heteronym=True)

    ret = pinyin_array_to_utf8(pinyin_array)
    if ret != "":
        return ret, False, ""
    if url == None:
        return ret, True, ""

    if args.debug:
        for pinyin_array_one in pinyin_array:
            print "|".join(pinyin_array_one)
        print "Got heteronym and try to handle it"

    time.sleep(1)
    contents = urllib2.urlopen(url).read()

    ret_list = []
    maybe_wrong_list = []
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

        if line == "":
            if len(ret_list) == 0:
                # Set maybe_wrong_list
                maybe_wrong = " ".join(url_pinyin)
                # Check if there is same line in maybe_wrong_list
                need_apply = True
                for one in maybe_wrong_list:
                    if maybe_wrong == one:
                        need_apply = False
                if need_apply:
                    if args.debug:
                        print "Got maybe wrong pinyin", maybe_wrong
                    maybe_wrong_list.append(maybe_wrong)
        else:
            # Check if there is same line in ret_list
            need_apply = True
            for ret_list_one in ret_list:
                if line == ret_list_one:
                    need_apply = False
            if need_apply:
                ret_list.append(line)

    return "或".join(ret_list), len(ret_list) == 0, "或".join(maybe_wrong_list)

if args.debug:
    pinyin, got_heteronym, maybe_wrong = yinjie(ensure_unicode(
        "呈现"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("呈现") + '&amp;from=zici')
    print pinyin
    print got_heteronym
    print maybe_wrong

    pinyin, got_heteronym, maybe_wrong = yinjie(ensure_unicode(
        "长大"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("长大") + '&amp;from=zici')
    print pinyin
    print got_heteronym
    print maybe_wrong

    pinyin, got_heteronym, maybe_wrong = yinjie(ensure_unicode(
        "冰激凌"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("冰激凌") + '&amp;from=zici')
    print pinyin
    print got_heteronym
    print maybe_wrong

    pinyin, got_heteronym, maybe_wrong = yinjie(ensure_unicode(
        "扑腾"), 'https://hanyu.baidu.com/s?wd=' + urllib.quote("扑腾") + '&amp;from=zici')
    print pinyin
    print got_heteronym
    print maybe_wrong

    exit(0)

if args.word == None:
    parser.error("option --word must set")

print "从文件", args.word, "读入词语"
print "写入文件", args.out

out = open(args.out, "w")
heteronym = False
for word in open(args.word):
    word = word.strip()
    url_word = urllib.quote(word)
    baidu_url = 'https://hanyu.baidu.com/s?wd=' + url_word + '&amp;from=zici'
    pinyin, got_heteronym, maybe_wrong = yinjie(ensure_unicode(word), baidu_url)

    if got_heteronym:
        heteronym = True
        if maybe_wrong != "":
            pinyin = maybe_wrong
        else:
            pinyin = "多音字"
        print "处理", word, "拼音是", pinyin, "可能有问题，注意检查。"

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
