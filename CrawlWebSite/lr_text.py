# -*- coding: utf-8 -*-

import os
from sklearn.externals import joblib

from CrawlWebSite.TextClassify import BagOfWords
from CrawlWebSite.TextClassify import TextClassify

data_dir = 'data'

BOW = BagOfWords.BagOfWords('')# BOW = BagOfWords('')
BOW.load_dictionary(os.path.join(data_dir, 'dicitionary.pkl'))
clf = joblib.load("model.m")

def text_classify(text):
    ## TextClassify
    TextClassifier = TextClassify.TextClassify()
    pred = TextClassifier.text_classify(text, BOW, clf)
    if pred[0] == 'terrorism':
        result = '暴恐'
    elif pred[0] == 'Not_terrorism':
        result = '正常'
    else:
        result = '未知'
    return result

