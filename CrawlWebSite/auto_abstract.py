#-*- encoding:utf-8 -*-

from textrank4zh import TextRank4Sentence

#函数原型
def abstract(text):

#功能说明：输入一段文本，自动生成其摘要并返回    
#参数text：输入的文本字符串，str类型  
#返回值：
#成功：abstract_text，生成的摘要，str类型
#错误：None
#备注：
    abstract_text=None
    try:  
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True, source = 'all_filters')
        abstract_text = tr4s.get_key_sentences(num=1)[0].sentence#摘要
        #print abstract_text
    except:
        abstract_text = None#摘要
    return abstract_text

