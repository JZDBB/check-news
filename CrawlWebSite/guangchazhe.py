# -*- coding: utf-8 -*-

# from urllib import urlretrieve
from bs4 import BeautifulSoup
import random
import re
from datetime import datetime, timedelta
#import db_connect
import time
import urllib.request
import logging
from CrawlWebSite import auto_abstract, EventInfo_extract, saveData, lr_text
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
        self.starturl = "http://www.guancha.cn/Search/?k=%E6%81%90%E6%80%96%E8%A2%AD%E5%87%BB&y=1&ps=20&pi=1"

    def get_page_count(self,url,headers):
        '''
        获取新华网中，该关键词的总页面信息
        '''
        html =None

        html=self.getUrl_multiTry(url,headers)
        # 对获取到的文本进行解析
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8') 
        # 从解析文件中通过select选择器定位指定的元素，返回一个列表
        result_count = soup.select("dt")
        # result_count = result_count[0].encode('gbk')
        result_count = str(result_count)
        result_count = list(filter(str.isdigit, result_count))
        resultCount = 0
        for i in range(len(result_count)):
            resultCount = resultCount*10 + int(result_count[i])
        if resultCount%20==0:
            page_count = resultCount/20
        else:
            page_count = resultCount/20 + 1
        pacgeCount = int(page_count)

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
        soup = BeautifulSoup(html,'html.parser')
        
        a = []
        b = []
        c = []
        d = []
        for news in soup.select('dd'):
            h4 =  news.select('h4')
            if len(h4) >0:
                #新闻时间
                time = news.select('span')[0].text
                times = time.replace(u'\u2219',u' ') 
                a.append(times)
                #新闻标题
                title = h4[0].text
                title1 = title.replace(u'\u2219',u' ')
                title2 = title1.replace(u'\u200b',u' ')
                titles = title2.replace(u'\u2022',u' ')
                b.append(titles)
                #新闻链接
                href = h4[0].select('a')[0]['href']
                c.append(href)   
                #新闻摘要
                abst = news.select('p')[0].text
                abst1 = abst.replace(u'\u2219',u' ')
                abst2 = abst1.replace(u'\u200b',u' ')
                absts = abst2.replace(u'\u2022',u' ')
                d.append(absts)
                

        for j in range(len(b)):
            url_temp ='http://www.guancha.cn' + str(c[j])
            index_result={}
            index_result["title"]=b[j]
            index_result["content"]=""
            index_result["pubtime"]=a[j]
            index_result["url"]=url_temp
            index_result["des"]=d[j]
            index_result["keyword"] = 'img'
            result.append(index_result)
        return result
    def get_html_soup_txt(self,url,headers):#获取解编码后的HTML
        html = None
        html=self.getUrl_multiTry(url,headers)
        soup=BeautifulSoup(html, 'html.parser', from_encoding='utf-8') 
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
        self.index+=1
        soup=BeautifulSoup(html, 'html.parser', from_encoding='utf-8') 
        return soup
    
    def page_url(self,url, page_num):#生成带页面的URL
        '''
        获取页面的url
        '''
        if page_num == 1:
            return url
        index = url.rfind(".")
        return url[0 : index] + "_" + str(page_num) + url[index : ]
    
    def get_title_link(self,url, pattern):#获取新闻的标题和正文链接
        #这里的pattern指的是获取的模式。
        soup = self.get_html_soup(url,self.my_headers)
        news_link = {}
    
        scroll_list = BeautifulSoup(str(soup.find("div", attrs = pattern)), "lxml")
        for link in scroll_list.find_all("a"):
            if len(link.get_text().strip()) > 0 and link.get("href").find("http") != -1:
                news_link[link.get_text()] = link.get('href')
        return news_link
    
    def get_news_body(self,url,headers):#抓取新闻主体内容
        '''
        获取新闻的主要内容
        '''
        result={}
        #使用循环处理有分页的新闻
        soup = self.get_html_soup(url,self.my_headers)
        if soup == None:
            return None
        texts = soup.find_all('p')
        content_text = ""
        for index in range(len(texts)):
            text=texts[index]
            content_text += text.get_text()
        content_text1 = content_text.replace(u'\xa9',u' ')
        content_text2 = content_text1.replace(u'\xa0',u' ')
        content_text3 = content_text2.replace(u'\u2022',u' ')
        content_text4 = content_text3.replace(u'\u2219',u' ')
        content_text5 = content_text4.replace(u'\xf4',u' ')
        content_text6 = content_text5.replace(u'\u200b',u' ')
        content_texts = content_text6.replace(u'\u30fb',u' ')
        result["content"]=content_texts
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
        stopFlag = False
        #FilterData={}
        pages,indexcount = self.get_page_count(self.starturl,self.my_headers)
        #根据是否需要记录文件来进行
        index = 0
        CrawlData=[]
        #遍历所有的新闻页
        for i in range(1,pages+1):
            if (i!=2 and i!=10):
                urls =self.starturl.replace("pi=1","pi=%d" % i)
            #返回数组对象，每个元素表示一条新闻的简略信息
                infodexs = self.index_info(urls,self.my_headers)
                if len(infodexs)>0:
                    for infodex in infodexs:
                    #判断是否达到终止天数
                        NewInfo={}
                        if self.deadlineTime!=0 and infodex["pubtime"][0:10]<self.deadlineTime: #终止爬取
                            stopFlag=True
                            break
                        if(infodex["keyword"]=="视频"):
                            continue
                        body = self.get_news_body(infodex["url"],self.my_headers)
                        if body!=None:
                            NewInfo["reporter"]=u"观察者"
                            NewInfo["pubtime"]=infodex["pubtime"]
                            NewInfo["title"]=infodex["title"]
                            NewInfo["des"]=infodex["des"]
                            NewInfo["content"]=body["content"]
                            NewInfo["url"]=infodex["url"]
                            NewInfo["imgurl"]=""
                            summary=auto_abstract.abstract(body["content"])
                            if summary!=None:
                                NewInfo["summary"]=summary
                        result = lr_text.text_classify([NewInfo["content"]])
                        #print result
                        NewInfo["result"]=result

                        # 进一步获取时间信息

                        if self.extract:
                            EventInfo=EventInfo_extract.EventInfo_extraction(body["content"])
                        else:
                            EventInfo=None
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
                            #CrawlData.append(NewInfo)
                        # saveData.saveData(NewInfo["url"],NewInfo)
                        # DataSend.sendata("localhost",50001,NewInfo)
                        if len(NewInfo) > 0:
                            CrawlData.append(NewInfo)
                            index += 1
                        if stopFlag == True:
                            break

        return CrawlData, index
        
    def get_content(self,html):
        # 内容分割的标签
        soup = BeautifulSoup(html,'lxml')
        #content = soup.select("ul.list > h3. ")
        content = soup.select("h3.  > a.modeless ")
        return content # 得到搜索列表的新闻标题和链接
    
    def getUrl_multiTry(self,url,headers):
        time.sleep(1)
        maxTryNum = 10
        for tries in range(maxTryNum):
            randddom_header = random.choice(headers)
            req = urllib.request.Request(url)
            req.add_header("User-Agent", randddom_header)
            req.add_header("GET", url)
            
            proxy_info = { 'host' : 'imagesoft.dynu.com',
                          'port' : 8000}   #设置你想要使用的代理  
            proxy_support = urllib.request.ProxyHandler({"http" : "http://%(host)s:%(port)d" % proxy_info})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
            
            html = urllib.request.urlopen(req).read().decode(encoding="utf8", errors='ignore')
            #html = urllib2.urlopen(req).read()
            return html


# #获取新闻的标题和链接
# if __name__=="__main__":
#     #print "hello world"
#     xinhuaCrawl = Crawl_NEWS(timeFrame=100)
#     craw, index = xinhuaCrawl.start_crawl()
#     print(craw, index)
    
    
    
