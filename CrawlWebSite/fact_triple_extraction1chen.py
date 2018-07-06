#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
"""
文本中事实三元组抽取
python *.py input.txt output.txt begin_line end_line
"""

__author__ = "tianwen jiang"

# Set your own model path
#MODELDIR=r"F:\ltp_data_v3.4.0"
#MODELDIR=r"D:\ltp_data_v3.4.0"

import sys
import os
import re 
import time

from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer


class EventInfoExtract():
    def __init__(self,modulePath,outfile):
        self.MODELDIR = modulePath
        self.adict = {
        '·' :'',
        '的':'',
        '了':'',
        '“':'',
        '”':'',
        '一次':''
        }
        self.segmentor=None
        self.postagger=None
        self.parser=None
        self.recognizer=None
        self.out_file=outfile
        
        
    def multiple_replace(self,text):  
         rx = re.compile('|'.join(map(re.escape, self.adict)))  
         def one_xlat(match):  
               return self.adict[match.group(0)]  
         return rx.sub(one_xlat, text) 


    def InitModule(self):
        #print "正在加载LTP模型... ..."
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(self.MODELDIR, "cws.model"))   #分词模型，单文件
        
        self.postagger = Postagger()
        self.postagger.load(os.path.join(self.MODELDIR, "pos.model")) #词性标注模型，单文件
        
        self.parser = Parser()
        self.parser.load(os.path.join(self.MODELDIR, "parser.model"))  #依存句法分析模型，单文件
        
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(self.MODELDIR, "ner.model")) #命名实体识别模型，单文件
        #print self.recognizer

    def release_module(self):
        '''
        release the model
        '''
        if self.segmentor!=None:
            self.segmentor.release()
        if self.postagger!=None:
            self.postagger.release()
        if self.parser!=None:
            self.parser.release()
        if self.recognizer!=None:
            self.recognizer.release()
        

    def Txtextraction_start(self,txt,out_file):
        """
        事实三元组的控制程序
        Args:
            txt:带抽取的内容
        """
        txt = txt.strip()
        out_file = open(self.out_file, 'a')
        #try:
        #print "Execute here====-===="
        self.fact_triple_extract(txt,out_file)
        out_file.flush()
        out_file.close()
    
    def addresssTime_extract(self,inputtxt):
        #这个地方先做实体抽取，提取出人物、组织和相关的时间，首先分词，得到分词结果
        sentences = inputtxt.split('。')
        DataAndTime=[]
        for sentence in sentences:
            if len(sentence)<=1:
                continue
            words = self.segmentor.segment(sentence)
            postags = self.postagger.postag(words)
            netags = self.recognizer.recognize(words, postags)
            arcs = self.parser.parse(words, postags)
            Dt={'date':'','address':''}
            if (("发生" in sentence or "遭" in sentence) and ("爆炸" in sentence or "事件" in sentence or "袭击" in sentence )) or (("恐怖" in sentence) or ("袭击" in sentence)):
                Flag=False
                Addressbackups=[]
                Address =''
                for i in range(len(postags)-1):
                    if Flag==True:
                        if postags[i]=='ns'or postags[i]=='nd' or postags[i]=='n': # ns 地理名 nd方向名词 n一般名词
                            head = arcs[i].head
                            Address=Address+words[i]
                            if postags[head-1]=="n":
                                Address+=words[head-1]
                                head = arcs[head-1].head
                            if(words[head-1]=="在" or words[head-1]=="发生" or  words[head-1]=="袭击"  or words[head-1]=="遭" or words[head-1]=="遭遇" or words[head-1]=="将"):
                                Dt['address']=Address
                                break
                        else:
                            Addressbackups.append(Address)
                            Address=''
                            Flag=False
                        continue
                    if postags[i]=='ns' and Flag == False:
                        head = arcs[i].head
                        Address = Address+words[i]
                        if (words[head-1]=="在" or words[head-1]=="发生" or  words[head-1]=="遭" or words[head-1]=="遭遇"  or words[head-1]=="将"):
                            Dt['address']=Address
                            break
                        Flag = True 
            if ("月" in sentence or '日' in sentence) and ("发生" in sentence or "袭击" in sentence):
                Flag = False
                Date=''
                Datebackup=[]
                for i in range(len(postags)-1):
                    if Flag==True:
                        if postags[i]=='nt':
                            head = arcs[i].head
                            Date=Date+words[i]
                            if words[head-1]=="发生" or words[head-1]=="袭击":
                                Dt['date']=Date
                                break
                        else:
                            Datebackup.append(Date)
                            Date=''
                            Flag=False
                        continue
                    
                    if postags[i]=='nt' and Flag == False:
                        Date = Date+words[i]
                        #获取一下head
                        head = arcs[i].head
                        if words[head-1]=="发生" or words[head-1]=="袭击":
                            Dt['date']=Date
                            break
                        if postags[i+1]!='nt':
                            Datebackup.append(Date)
                        #index=i
                        Flag = True 
                if Dt['date']=='' and len(Datebackup):
                    Dt['date']=Datebackup[-1]
            if Dt['date']!='' or Dt['address']!='':
                DataAndTime.append(Dt)
                
        if len(DataAndTime)>1:
            for i in DataAndTime:
                if i['date']=="当天":
                    DataAndTime.remove(i)
        if len(DataAndTime)==0:
            Dt['date']=''
            Dt['address']=''
            DataAndTime.append(Dt)
        
        return DataAndTime
    def extraction_start(self, input_txt,out_file_name):
        """
        事实三元组抽取的总控程序
        Args:
            in_file_name: 输入文件的名称
            #out_file_name: 输出文件的名称
            begin_line: 读文件的起始行
            end_line: 读文件的结束行
        """
        out_file = open(out_file_name, 'a')
        
        line_index = 1
        sentence_number = 0
        text_line = input_txt
        while text_line:
            if line_index < begin_line:
                text_line = in_file.readline()
                line_index += 1
                continue
            if end_line != 0 and line_index > end_line:
                break
            sentence = text_line.strip()
            if sentence == "" or len(sentence) > 1000:
                text_line = in_file.readline()
                line_index += 1
                continue
            try:
              sentence_one = sentence.split(" ")#"。"
              for num in range(len(sentence_one)-1):
                  self.fact_triple_extract(sentence, out_file)
                  out_file.flush()
            except:
                pass
            sentence_number += 1
            if sentence_number % 50 == 0:
                pass
            text_line = in_file.readline()
            line_index += 1
        in_file.close()
        out_file.close()

    def attribute_define0(self,text,keywords):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)#词性标注
        if keywords in text:
            for index in range(len(words)):
                if(words[index]==keywords):               
                    for i in range(index):
                        if(postags[index-i-2][0]=='n'):
                            continue
                        else:
                            break

    def attribute_define1(self,text,keywords):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)#词性标注
        if keywords in text:
            for index in range(len(words)):
                if(words[index]==keywords):               
                    for i in range(index):
                        if(postags[index-i-2][0]=='n'):
                            continue
                        else:
                            if(i != 0):
                                pass
                                #print "事件属性：","".join(words[index-i-1:index+1])
                            break

    def num_define(self,text):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)#词性标注
        for index in range(len(words)):
            if(postags[index]=='m'):  
                return words[index]
                        
    def attribute_define2(self,text,keywords):
        words = self.segmentor.segment(text)
        #postags = postagger.postag(words)#词性标注
        if keywords in text:
            for index in range(len(words)):
                if(words[index]==keywords):               
                    for i in range(index):
                        if(words[index-i-1]!=('发生' or '是')):#|(words[index-i-1]!='遭遇'):
                            continue
                        else:
                            if(i != 0):
                                attribute = "".join(words[index-i:index+1])
                                #attribute = multiple_replace(attribute)
                                #print '==========='
                                if attribute in '恐怖袭击事件':
                                    return
                                return attribute
                            else:
                                return


    def organization_define(self,text,keywords):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)#词性标注
        
        if keywords in text:
            for index in range(len(words)):
                if(words[index]==keywords):               
                    for i in range(index):
                        if(postags[index-i-1][0]=='n')&(index-i-1 != 0):
                            continue
                        else:
                            if(words[index-1]=='组织')&(postags[index-2][0]!='n'):      
                                continue
                            if(i != 0):
                                print("组织：","".join(words[index-i:index]))
                                return "".join(words[index-i:index])
    def organization_define1(self,text,keywords):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)#词性标注
        if keywords in text:
            for index in range(len(words)):
                if(words[index]==keywords):               
                    for i in range(index):
                        if(postags[index-i-1][0]=='n')&(index-i-1 != 0):
                            continue
                        else:
                            if(words[index-1]=='组织')&(postags[index-2][0]!='n'):      
                                continue
                            if(i != 0):
                                #print "组织：","".join(words[index-i:index])
                                return "".join(words[index-i:index])

    def fact_attribute_from_text(self,text):
        """
        """
        text = text.replace('，','。')
        sentence_one = text.split("。")
        
        fact_attribute = []
        for num in range(len(sentence_one)-1):
            if('袭击' in sentence_one[num]):
                #attribute_define0(sentence_one[num],'事件')
                    #print sentence_one[num]
                sentence_temp = self.multiple_replace(sentence_one[num])
                if('发生' in sentence_temp)|('遭遇' in sentence_temp):
                    #print '---------------',sentence_temp
                    temp_atrribut1 = self.attribute_define2(sentence_temp,'事件')
                    #print temp_atrribut1
                    if((temp_atrribut1)==None):
                        temp_atrribut2 = self.attribute_define2(sentence_temp,'袭击')
                        #print temp_atrribut2
                        if temp_atrribut2==None:
                            return
                        fact_attribute.append(str(temp_atrribut2))
                    else:
                        fact_attribute.append(str(temp_atrribut1))
        #print '------------------'
        if(len(fact_attribute)==0):
            #print '事件属性：unkown!'
            return 'None'
        else:
            #print '事件属性1:', len(fact_attribute),''.join(fact_attribute)
            #print '事件属性:',max(fact_attribute, key=len)
            return max(fact_attribute, key=len)

    def organization_from_text(self,text):
        """
        事实三元组抽取的总控程序
        Args:
            in_file_name: 输入文件的名称
            #out_file_name: 输出文件的名称
            begin_line: 读文件的起始行
            end_line: 读文件的结束行
        """
        sentence_one = text.split("。")
        #print '---------------------------',sentence_one[0]   
        ogniz = []
        for num in range(len(sentence_one)-1):
            if('负责' in sentence_one[num]):
                if('宣称' in sentence_one[num]):
                    #print sentence_one[num]
                    sentence_temp = sentence_one[num].replace('“','')
                    sentence_temp = sentence_temp.replace('”','')
                    temp_org = self.organization_define(sentence_temp,'宣称')
                    if(temp_org != None):
                        ogniz.append(temp_org)
            if(len(ogniz)==0):
                if('宣称' in sentence_one[num]):
                    #print sentence_one[num]
                    sentence_temp = sentence_one[num].replace('“','')
                    sentence_temp = sentence_temp.replace('”','')
                    temp_org = self.organization_define1(sentence_temp,'宣称')
                    if(temp_org != None):
                        ogniz.append(temp_org)
        if(len(ogniz)==0):
            #print '组织：unkown!'
            return 'unknown'
        else:
            #print '组织:',max(ogniz, key=len)
            #print ogniz
            return max(ogniz, key=len)

    def death_num_from_text(self,text):
        """
        事实三元组抽取的总控程序
        Args:
            in_file_name: 输入文件的名称
            #out_file_name: 输出文件的名称
            begin_line: 读文件的起始行
            end_line: 读文件的结束行
        """
        text = text.replace('，','。')
        text = text.replace('、','。')
        sentence_one = text.split("。")
        death_num = None
        hurt_num = None
        total_num = None
        #print '---------------------------',sentence_one[0]   
 
        for num in range(len(sentence_one)-1):
            if('死亡' in sentence_one[num])|('丧生' in sentence_one[num]):
                #print sentence_one[num]
                if(death_num == None):
                    death_num = self.num_define(sentence_one[num])
                    #print '死亡人数：',death_num
            if('受伤' in sentence_one[num]):
                #print sentence_one[num]        
                if(hurt_num == None):
                    hurt_num = self.num_define(sentence_one[num])
                    #print '受伤人数：',hurt_num
            if('伤亡' in sentence_one[num]):
                #print sentence_one[num]
                if(total_num == None):
                    total_num = self.num_define(sentence_one[num])
            #print type(death_num),type(hurt_num),type(total_num)
        return death_num,hurt_num,total_num
        


    def fact_triple_extract(self,sentence, out_file):
        #print sentence
        """
        对于给定的句子进行事实三元组抽取
        Args:
            sentence: 要处理的语句
        """
        words = self.segmentor.segment(sentence)
        postags = self.postagger.postag(words)
        netags = self.recognizer.recognize(words, postags)
        arcs = self.parser.parse(words, postags)
        child_dict_list = self.build_parse_child_dict(words, postags, arcs)
        
        Entity_Address=[]
        Entity_Name = []
        
        for index in range(len(postags)):
            e1 = ''
            if netags[index][0] == 'S' or netags[index][0] == 'B':
                if 'Ns' in netags[index]:
                    ni = index
                    if netags[ni][0] == 'B':
                        while netags[ni][0] != 'E':
                            ni += 1
                        e1 = ''.join(words[index:ni+1])
                    else:
                        e1 = words[ni]
                    Entity_Address.append(e1)
                if "Nh" in netags[index]:
                    ni = index
                    if netags[ni][0]=='B':
                        while netags[ni][0]!='E':
                            ni+=1
                        e1= ''.join(words[index:ni+1])
                    else:
                        e1=words[ni]
                        Entity_Name .append(e1)
        Entity_Address = list(set(Entity_Address))
        Entity_Name = list(set(Entity_Name))
        #for i in Entity_Name:
        #    print i
        AddressTp =[]
        LocateAddress = []
        for index in range(len(postags)):
            # 抽取以谓词为中心的事实三元组
            if postags[index] == 'v':
                child_dict = child_dict_list[index]
                # 主谓宾
                Flag = False
                if child_dict.has_key('SBV') and child_dict.has_key('VOB'):
                    e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                    r = words[index]
                    e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                    out_file.write("主语谓语宾语关系\t(%s, %s, %s)\n" % (e1, r, e2))
                    for address in Entity_Address:
                        if address in e1 and ( ("袭击" in e1 or "袭击" in e2) or ("事件" in e2 or "事件" in e1)):
                            for name in Entity_Name:
                                if name in e1:
                                    Flag == False
                                    break
                            else:
                                Flag = True
                            if Flag == True:
                                for i in Entity_Address:
                                    if i in e1 or i in e2:
                                        AddressTp.append(i)    
                    out_file.flush()
    
                # 定语后置，动宾关系
                if arcs[index].relation == 'ATT':
                    if child_dict.has_key('VOB'):
                        e1 = self.complete_e(words, postags, child_dict_list, arcs[index].head - 1)
                        r = words[index]
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        temp_string = r+e2
                        if temp_string == e1[:len(temp_string)]:
                            e1 = e1[len(temp_string):]
                        if temp_string not in e1:
                            #print "定语后置动宾关系\t(%s, %s, %s)\n" % (e1, r, e2)
                            out_file.write("定语后置动宾关系\t(%s, %s, %s)\n" % (e1, r, e2))
                            out_file.flush()
                # 含有介宾关系的主谓动补关系
                if child_dict.has_key('SBV') and child_dict.has_key('CMP'):
                    #e1 = words[child_dict['SBV'][0]]
                    e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                    cmp_index = child_dict['CMP'][0]
                    r = words[index] + words[cmp_index]
                    if child_dict_list[cmp_index].has_key('POB'):
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                        #print "介宾关系主谓动补\t(%s, %s, %s)\n" % (e1, r, e2)
                        out_file.write("介宾关系主谓动补\t(%s, %s, %s)\n" % (e1, r, e2))
                        out_file.flush()
    
            # 尝试抽取命名实体有关的三元组
            if netags[index][0] == 'S' or netags[index][0] == 'B':
                ni = index
                if netags[ni][0] == 'B':
                    while netags[ni][0] != 'E':
                        ni += 1
                    e1 = ''.join(words[index:ni+1])
                else:
                    e1 = words[ni]
                if arcs[ni].relation == 'ATT' and postags[arcs[ni].head-1] == 'n' and netags[arcs[ni].head-1] == 'O':
                    r = self.complete_e(words, postags, child_dict_list, arcs[ni].head-1)
                    if e1 in r:
                        r = r[(r.index(e1)+len(e1)):]
                    if arcs[arcs[ni].head-1].relation == 'ATT' and netags[arcs[arcs[ni].head-1].head-1] != 'O':
                        e2 = self.complete_e(words, postags, child_dict_list, arcs[arcs[ni].head-1].head-1)
                        mi = arcs[arcs[ni].head-1].head-1
                        li = mi
                        if netags[mi][0] == 'B':
                            while netags[mi][0] != 'E':
                                mi += 1
                            e = ''.join(words[li+1:mi+1])
                            e2 += e
                        if r in e2:
                            e2 = e2[(e2.index(r)+len(r)):]
                        if r+e2 in sentence:
                            #print "人名//地名//机构\t(%s, %s, %s)\n" % (e1, r, e2)
                            out_file.write("人名//地名//机构\t(%s, %s, %s)\n" % (e1, r, e2))
                            out_file.flush()
                
        AddressTp = list(set(AddressTp))
        LocateAddress=AddressTp
        Tp = LocateAddress
        for i in LocateAddress:
            for k in AddressTp:
                if i!=k and (i in k):
                    Tp.remove(i)
            address = ''
            for i in Tp:
                address+=i
            print("地点:",address)
                

    def build_parse_child_dict(self,words, postags, arcs):
        """
        为句子中的每个词语维护一个保存句法依存儿子节点的字典
        Args:
            words: 分词列表
            postags: 词性列表
            arcs: 句法依存列表
        """
        child_dict_list = []
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                if arcs[arc_index].head == index + 1:
                    if child_dict.has_key(arcs[arc_index].relation):
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            #if child_dict.has_key('SBV'):
            #    print words[index],child_dict['SBV']
            child_dict_list.append(child_dict)
        return child_dict_list
    
    def complete_e(self,words, postags, child_dict_list, word_index):
        """
        完善识别的部分实体
        """
        child_dict = child_dict_list[word_index]
        prefix = ''
        if child_dict.has_key('ATT'):
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])
        
        postfix = ''
        if postags[word_index] == 'v':
            if child_dict.has_key('VOB'):
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if child_dict.has_key('SBV'):
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix
    
        return prefix + words[word_index] + postfix

    def attribute_define0(self,text,keywords):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)#词性标注
        if keywords in text:
            for index in range(len(words)):
                if(words[index]==keywords):               
                    for i in range(index):
                        if(postags[index-i-2][0]=='n'):
                            continue
                        else:
                            #print "事件属性：","".join(words[index-i-1:index+1])
                            break
    
    def attribute_define1(self,text,keywords):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)#词性标注
        if keywords in text:
            for index in range(len(words)):
                if(words[index]==keywords):               
                    for i in range(index):
                        if(postags[index-i-2][0]=='n'):
                            continue
                        else:
                            if(i != 0):
                                pass
                                #print "事件属性：","".join(words[index-i-1:index+1])
                            break
    
    def attribute_define2(self,text,keywords):
        #print text
        words = self.segmentor.segment(text)
        print(words)
        #print self.segmentor
        #print '\t'.join(words)
        #postags = postagger.postag(words)#词性标注
        if keywords in text:
            for index in range(len(words)):
                #print words[index]
                if(words[index]==keywords):  
                    for i in range(index):
                        if(words[index-i-1]!=('发生' or '是')):#|(words[index-i-1]!='遭遇'):
                            continue
                        else:
                            if(i != 0):
                                attribute = "".join(words[index-i:index+1])
                                if attribute in '恐怖袭击事件':
                                    return
                                return attribute
                            else:
                                return
    
    
    def organization_define(self,text,keywords):
        words = self.segmentor.segment(text)
        postags = self.postagger.postag(words)#词性标注
        if keywords in text:
            for index in range(len(words)):
                if(words[index]==keywords):               
                    for i in range(index):
                        if(postags[index-i-1][0]=='n'):
                            continue
                        else:
                            if(words[index-1]=='组织')&(postags[index-2][0]!='n'):      
                                continue
                            if(i != 0):
                                #print "组织：","".join(words[index-i:index])
                                return "".join(words[index-i:index])
    
    
    
    def fact_attribute(self,in_file_name, out_file_name, begin_line, end_line):
        """
        事实三元组抽取的总控程序
        Args:
            in_file_name: 输入文件的名称
            #out_file_name: 输出文件的名称
            begin_line: 读文件的起始行
            end_line: 读文件的结束行
        """
        in_file = open(in_file_name, 'r')
        out_file = open(out_file_name, 'a')
        
        line_index = 1
        sentence_number = 0
        text_line = in_file.readline()
        while text_line:
            #小于起始段的直接跳过
            if line_index < begin_line:
                text_line = in_file.readline()
                line_index += 1
                continue
            if end_line != 0 and line_index > end_line:
                break
            sentence = text_line.strip()
            #长段（大于1000）直接跳过
            if sentence == "" or len(sentence) > 1000:
                text_line = in_file.readline()
                line_index += 1
                continue
            sentence_one = sentence.split(" ")#"。"
            
            for num in range(len(sentence_one)-1):
                attribute_define0(sentence_one[num],'事件')
                attribute_define2(sentence_one[num],'袭击')
            sentence_number += 1
            if sentence_number % 50 == 0:
                pass
                #print "%d done" % (sentence_number)
            text_line = in_file.readline()
            line_index += 1
        in_file.close()
        out_file.close()


if __name__ == "__main__":
    for root,dirs,files in os.walk(os.path.join(os.getcwd(),"data")):
        for filet in files:
            if filet.endswith(".txt"):
                filePath = os.path.join(root,filet)
                #extraction_start(in_file_name, out_file_name, begin_line, end_line)
                out_file_name = filet
                # extraction_start(filePath, out_file_name, begin_line, end_line)
