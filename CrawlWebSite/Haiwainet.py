# -*- coding: utf-8 -*-
# coding:utf-8
"""
Created on Mon Nov 13 15:33:54 2017
@author: john
"""
 # retrieve(self, url, filename=None, reporthook=None, data=None)
 #     retrieve(url) returns (filename, headers) for a local object
 #     or (tempfilename, headers) for a remote object.
# from urllib import urlretrieve #urllib仅可以接受URL。这意味着，你不可以伪装你的User Agent字符串等。
#但是urllib提供urlencode方法用来GET查询字符串的产生，而urllib2没有。这是就是为何urllib常和urllib2一起使用的原因
from bs4 import BeautifulSoup #提供树功能
import urllib.request
import random
import re
from hashlib import md5 #retrun a md5 hashing object
from CrawlWebSite import EventInfo_extract, auto_abstract, saveData, lr_text
from datetime import datetime, timedelta
import time
import logging
import DataSend
logging.basicConfig(level=logging.DEBUG,
                format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                datefmt="%a, %d %b %Y %H:%M:%S",
                filename="myapp.log",
                filemode="w")

class Crawl_NEWS():
    def __init__(self,timeFrame=0,saveFile=True,extract=False):
        self.saveFile = saveFile
        self.extract=extract
        self.deadlineTime = 0
        self.index=0
        self.titles=[]
        if timeFrame==0:
            self.deadlineTime=0
        else:
            self.deadlineTime=(datetime.now()-timedelta(days=timeFrame)).strftime("%Y-%m-%d")
        self.my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14", 
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"  ] 
        self.starturl = "http://search.haiwainet.cn/?q=%E6%81%90%E6%80%96%E8%A2%AD%E5%87%BB&p=1"
#怎么构成的：

    def get_page_count(self,url,headers):
        '''
        获取新华网中，该关键词的总页面信息
        '''
        html =None
        html=self.getUrl_multiTry(url,headers)#返回的是完整的html文件，不是json
        soup = BeautifulSoup(html,"html.parser")
        soup_string = str(soup.select('.result')[0])
        count_string = soup_string[soup_string.find("<b>")+3:soup_string.find("</b>")]
        resultCount = int(count_string.replace(',','').strip()) #返回结果总条数
        pacgeCount=int(1+resultCount/15) #返回页数
        return pacgeCount,resultCount
    def index_info(self,url,headers):
        '''
        获取一个页面中的所有的条目相关信息:
        页面中所有条目的标题、关键词、报道时间、报道内容以及图片链接
        '''
        #返回的结果数组，为每个新闻的一些简略信息，包括title、des、url等
        result = []
        #爬虫获取url结果

        html=self.getUrl_multiTry(url,headers)
        # print(html)
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        list_mtitle = soup.find_all(class_="mtitle")#find the title and url by class name
        list_link_ri = soup.find_all(class_="link_ri")#find the report time bye class name
        list_title = [i.text for i in list_mtitle ]#title
        list_url = [str(i)[str(i).find("href=")+5:str(i).find("target=")].replace('"','') for i in list_mtitle ]#get the url
        list_date = [i.text for i in list_link_ri ]#date
        result = []
        if(len(list_date)!=(len(list_url)+len(list_title))/2):
            return False
        for i in range(0,len(list_url),1):
            index_result = {}
            index_result["title"] = list_title[i]
            index_result["url"] =  list_url[i]
            index_result["reporttime"] = list_date[i]
            result.append(index_result)
        return result

    def get_html_soup_txt(self,url,headers):#获取解编码后的HTML
        html = None
        html=self.getUrl_multiTry(url,headers)#通过网址和头部信息返回网页
        soup=BeautifulSoup(html, 'html.parser', from_encoding='utf-8') #将html文档装换为树形结构，然后对对象进行分类
        return soup
    def get_html_soup(self,url,headers):#获取解编码后的HTML
        '''
        获取页面编码后的内容
        '''
        if not url.startswith("http://"):
            url = "http://"+url
        #print url
        html = None
        html =self.getUrl_multiTry(url,headers)
        if html == None:
            return None
        self.index+=1
        soup=BeautifulSoup(html, 'html.parser', from_encoding='utf-8') 
        return soup
    
    def page_url(self, url, page_num):#生成带页面的URL
        '''
        获取页面的url
        '''
        if page_num == 1:
            return url
        index = 1+url.rfind("=")
        #print "{{{{{{{{{{{{{{{}}}}}}}}}}}}}}",url[0 : index] + "_" + str(page_num) + url[index : ]
        print(url[0 : index]  + str(page_num))
        return url[0 : index]  + str(page_num)
    #--------------------------------华丽的分割线------------------------------------------#
    #涉及到不同网站的风格
    def get_news_body(self,url,headers):#抓取新闻主体内容
        '''
        获取新闻的主要内容
        '''
        result={}
        #使用循环处理有分页的新闻
        soup = self.get_html_soup(url,self.my_headers)
        if soup is None:
            return None
        texts = soup.find_all('p')
        if soup.find('p') is None:
            des_string = None
        else:
            des_string = soup.find('p').text
        content_text = ""
        for index in range(len(texts)):
            text=texts[index]
            content_text += text.get_text()
        if content_text.strip() is None:
            content_text = None
        result["content"]=content_text
        imgurl = str(soup.find('img',src = re.compile("http://images.haiwainet.*")))
        # print imgurl
        imgurl_string=imgurl[imgurl.find("src=")+5:imgurl.find(".jpg")+4]
        result["imgUrl"]=imgurl_string
        if des_string is None:
            des_string=" "
        result["des"] = des_string
        return result
    
    def clean_chinese_character(self,text):
        '''处理特殊的中文符号,将其全部替换为'-' 否则在保存时Windows无法将有的中文符号作为路径'''
        chars = chars = ["/", "\"", "'", "·", "。","？", "！", "，", "、", "；", "：", "‘", "’", "“", "”", "（", "）", "…", "–", "．", "《", "》"];
        new_text = ""
        for i in range(len(text)):
            if text[i] not in chars:
                new_text += text[i]
            else:
                new_text += "_"
        return new_text
    def start_crawl(self):
        '''
        这个函数开始爬取数据
        '''
        #获取到页面和条目统计信息
        fileName=''
        stopFlag = False
        CrawlData=[]
        #FilterData={}
        pages,indexcount = self.get_page_count(self.starturl,self.my_headers)
        fields = ["reporttime","reporter","title","sitename","keyword","content","imgUrl"]
        #根据是否需要记录文件来进行
        index = 0
        # 缩进调整！！！

        #遍历所有的新闻页
        for i in range(1,pages+1):
            #得到当前页的url
            urls =self.starturl.replace("p=1","p=%d" % i)
            #返回数组对象，每个元素表示一条新闻的简略信息
            infodexs = self.index_info(urls,self.my_headers)
            if len(infodexs)>0:
                for infodex in infodexs:
                    #判断是否达到终止天数
                    NewInfo={}
                    if self.deadlineTime!=0 and (infodex["reporttime"].strip())[:-8]<self.deadlineTime: #终止爬取
                        stopFlag=True
                        break
                    body = self.get_news_body(infodex["url"],self.my_headers)
                    if body == None:
                        continue
                    if body!=None:
                        NewInfo["reporter"]=u"海外网"
                        NewInfo["pubtime"]=infodex["reporttime"]
                        NewInfo["title"]=infodex["title"]
                        NewInfo["des"]=body["des"]
                        NewInfo["content"]=body["content"]
                        NewInfo["url"]=infodex["url"]
                        NewInfo["imgurl"]=body["imgUrl"]
                        summary=auto_abstract.abstract(body["content"])
                        if summary!=None:
                            NewInfo["summary"]=summary
                    result = lr_text.text_classify([NewInfo["content"]])
                    #print result
                    NewInfo["result"]=result

                    EventInfo=EventInfo_extract.EventInfo_extraction(body["content"])

                    if EventInfo!=None:
                        NewInfo["Event_time"]=EventInfo["Event_time"]
                        NewInfo["Event_address"]=EventInfo['Event_address']
                        NewInfo["Event_type"]=EventInfo['Event_type']
                        NewInfo["Event_total"]=EventInfo['Event_total']
                        NewInfo["Event_gname"]=EventInfo["Event_gname"]
                        NewInfo["Event_nwound"]=EventInfo['Event_nwound']
                        NewInfo["Event_nkill"]=EventInfo['Event_nkill']
                    else:
                        NewInfo["Event_time"]=''
                        NewInfo["Event_address"]=''
                        NewInfo["Event_type"]=''
                        NewInfo["Event_total"]=''
                        NewInfo["Event_gname"]=''
                        NewInfo["Event_nwound"]=''
                        NewInfo["Event_nkill"]=''
                    # saveData.saveData(NewInfo["url"],NewInfo)
                    # DataSend.sendata("localhost",50001,NewInfo)
                    #CrawlData.append(NewInfo)
                    if len(NewInfo) > 0:
                        print(NewInfo)
                        CrawlData.append(NewInfo)
                        index += 1
            if stopFlag == True:
                break

        return CrawlData, index

    def getUrl_multiTry(self,url,headers):
        time.sleep(1)
        maxTryNum = 10
        for tries in range(maxTryNum):
            randddom_header = random.choice(headers)#使用随机一个头部,伪装成随机浏览器
            req = urllib.request.Request(url)
            req.add_header("User-Agent", randddom_header)
            req.add_header("GET", url)#以get方式访问网页
            try:
                html = urllib.request.urlopen(req).read().decode(encoding="utf8", errors='ignore')#utf-8编码返回网页
            except:
                print(url)
                break
            return html

#获取新闻的标题和链接
if __name__=="__main__":
    haiwainetCrawl = Crawl_NEWS(timeFrame=10)
    craw, index = haiwainetCrawl.start_crawl()
    print(craw, index)
