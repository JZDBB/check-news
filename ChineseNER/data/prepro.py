# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:16:55 2018

@author: wtb
"""

import os

data_dir = "all"
files = os.listdir(data_dir)

for filename in files:
    with open(os.path.join(data_dir, filename), 'r', encoding="utf8") as f:
        get = f.read()
        result = get.splitlines()
        result_new = []
        for line in result:
            if not len(line) <= 2:
                if not line[0] in [" ","	", ""]:
                    result_new.append(line)
    with open(os.path.join(data_dir, filename), "w", encoding="utf8") as f:
        for line in result_new:
            f.write(line+'\n')
        f.write('\n')

#    with open(os.path.join(data_dir, filename), 'a+') as f:
#        f.write('\n')
