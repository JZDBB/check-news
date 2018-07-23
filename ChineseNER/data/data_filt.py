# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 16:29:55 2018

@author: wtb
"""

import os

anns_dir = "test"
txt_dir = "../test_txt"

src_file = os.listdir(anns_dir)
roi_file = []
for i in src_file:
    i = i.replace(".anns", "")
    roi_file.append(i)
    
dst_file = os.listdir(txt_dir)
for file in dst_file:
    if file not in roi_file:
        os.remove(os.path.join(txt_dir, file))