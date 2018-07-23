# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 15:18:12 2018

@author: wtb
"""

import os
import math
import random
import shutil

file_dir = "all"
train_dir = "train"
dev_dir = "dev"
test_dir = "test"

def main():
    files = os.listdir(file_dir)
    num = len(files)
    train_num = math.ceil(0.7 * num)
    dev_num = math.ceil((num - train_num) / 3)
    #test_num = num - train_num - dev_num
    train_index = random.sample(range(num), train_num)
    temp = list(set(range(num)) - set(train_index))
    dev_index = random.sample(temp, dev_num)
    test_index = list(set(temp) - set(dev_index))
    
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    if not os.path.exists(dev_dir):
        os.mkdir(dev_dir)
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
        
    for i in train_index:
        file = files[i]
        shutil.copyfile(os.path.join(file_dir, file), os.path.join(train_dir, file))
    for i in dev_index:
        file = files[i]
        shutil.copyfile(os.path.join(file_dir, file), os.path.join(dev_dir, file))
    for i in test_index:
        file = files[i]
        shutil.copyfile(os.path.join(file_dir, file), os.path.join(test_dir, file))
        
if __name__ == '__main__':
    main()