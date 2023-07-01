#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib
import shutil

source_dir = './old'
target_dir = './new'

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

for filename in os.listdir(source_dir):
    if filename.endswith('.gif'):
        new_filename = urllib.unquote(filename).decode('utf8')
        new_filename = new_filename[:-4] + '.gif'
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, new_filename)
        print target_path
        shutil.copy(source_path, target_path)
