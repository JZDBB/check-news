# -*- coding: utf-8 -*-

import os
from sklearn.externals import joblib

from CrawlWebSite.TextClassify import BagOfWords
from CrawlWebSite.TextClassify import TextClassify

data_dir = './CrawlWebSite/data/'

BOW = BagOfWords.BagOfWords('')# BOW = BagOfWords('')
dir = os.path.join(data_dir, 'dicitionary.pkl')
BOW.load_dictionary(dir)
clf = joblib.load("model.m")

def text_classify(text):
    ## TextClassify
    TextClassifier = TextClassify.TextClassify()
    try:
        # print(text)
        pred = TextClassifier.text_classify(text, BOW, clf)
        print(pred)
    except:
        result = '未知'
        return result
    if pred[0] == b'terrorism':
        result = '暴恐'
    elif pred[0] == b'Not_terrorism':
        result = '正常'
    else:
        result = '未知'
    return result

