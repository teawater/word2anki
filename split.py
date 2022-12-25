#!/usr/bin/python
# -*- coding: utf-8 -*-

def ensure_unicode(v):
    if isinstance(v, str):
        v = v.decode('utf8')
    return unicode(v)

a=ensure_unicode("测试")
for w in a:
    print w

