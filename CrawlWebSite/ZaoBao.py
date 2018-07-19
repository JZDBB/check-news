# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:33:54 2017
@author: john
"""
# from urllib import urlretrieve
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import logging
import re
from CrawlWebSite import auto_abstract, lr_text, saveData, EventInfo_extract
import urllib.request

import DataSend
from CrawlWebSite.data.cnews_loader import *
logging.basicConfig(level=logging.DEBUG,
                format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                datefmt="%a, %d %b %Y %H:%M:%S",
                filename="myapp.log",
                filemode="w")


class Crawl_NEWS():
    def __init__(self, timeFrame=0,saveFile=True, crawtime=0):
        self.saveFile = saveFile
        self.crawTime = crawtime
        self.deadlineTime = 0
        self.index=0
        self.titles=[]
        if timeFrame==0:
            self.deadlineTime=0
        else:
            self.deadlineTime=(datetime.now()-timedelta(days=timeFrame)).strftime("%Y-%m-%d")
        self.my_headers=[
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14", 
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"  ] 
        self.starturl = "http://www.zaobao.com/search/site/%E6%81%90%E6%80%96%E8%A2%AD%E5%87%BB?page=0"

    def get_page_count(self, url, headers):
        """
        通过尾页href提取
        关键词搜索结果总页数
        """
        pages = 0
        html = self.getUrl_multiTry(url, headers)
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        css_class = soup.find(attrs={'class': 'pager-last'})
        link = css_class.find("a").get("href")
        pages = re.findall(r'\d+', link)
        for match in pages:
            pages = match
        return pages
    
    def index_info(self, url, headers):
        '''
    获取一个页面中的所有的条目相关信息:
    页面中所有条目的标题、url、报道时间等简要信息
    '''
        result = []
        # 爬虫获取url结果
        html = self.getUrl_multiTry(url, headers)
        # 使用BeautifulSoup解析返回的网页信息
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        css_class = soup.find_all(attrs={'class': 'search-result'})
        for event in css_class:
            index_result = {}
            index_result["title"] = event.a.string
            index_result["url"] = "http://www.zaobao.com" + event.a.get("href")
            index_result["reporttime"] = event.span.string.lstrip()
            # # 正则去除标签中的HTML样式,提取简报
            result.append(index_result)
        return result

    # 获取解编码后的HTML
    def get_html_soup_txt(self, url, headers):
        html = None
        html = self.getUrl_multiTry(url, headers)
        soup=BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        return soup

    # 生成带页面的URL
    def page_url(self, url, page_num):
        '''
        获取页面的url
        '''
        if page_num == 1:
            return url
        index = url.rfind(".")
        return url[0 : index] + "_" + str(page_num) + url[index : ]
    
    def get_title_link(self,url, pattern):#获取新闻的标题和正文链接
        # 这里的pattern指的是获取的模式。
        soup = self.get_html_soup(url, self.my_headers)
        news_link = {}
    
        scroll_list = BeautifulSoup(str(soup.find("div", attrs = pattern)), "lxml")
        for link in scroll_list.find_all("a"):
            if len(link.get_text().strip()) > 0 and link.get("href").find("http") != -1:
                news_link[link.get_text()] = link.get('href')
        return news_link

    def get_news_body(self, url, headers):
        '''
    获取新闻的主要内容
    正文，记者，热词等信息
    '''
        result = {}
        # 使用循环处理有分页的新闻
        html = self.getUrl_multiTry(url, headers)
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        if soup is None:
            return None
        # 提取新闻正文
        texts = soup.find_all('p')
        content_text = ""
        for index in range(len(texts)):
            text = texts[index]
            content_text += text.get_text()
        result["content"]=content_text
        # 提取新闻关键词
        try:
            get_hotwords = soup.find(attrs={'class': 'tagcloud'}).find_all('a')
            keyword = ""
            for text in get_hotwords:
                keyword += text.get_text() + " "
            result["keyword"] = keyword
        except:
            result["keyword"] = ""
        # 获取新闻图片url
        try:
            result["imgUrl"] = soup.find(attrs={'property': 'og:image:url'}).get('content')
        except:
            result["imgUrl"] = ""
        # 获取网站名称
        try:
            result["sitename"] = soup.find(attrs={'property': 'og:site_name'}).get('content')
        except:
            result["sitename"] = ""
        # 获取新闻简介
        try:
            result["des"] = soup.find(attrs={'property': 'og:description'}).get('content')
        except:
            result["des"] = ""
        return result

    def clean_chinese_character(self, text):
        '''
        处理特殊的中文符号,将其全部替换为'-' 
        否则在保存时Windows无法将有的中文符号作为路径
        '''
        chars = chars = ["/", "\"", "'", "·", "。","？", "！", "，", "、", "；", "：", "‘", "’", "“", "”", "（", "）", "…", "–", "．", "《", "》"];
        new_text = ""
        for i in range(len(text)):
            if text[i] not in chars:
                new_text += text[i]
            else:
                new_text += "_"
        return new_text

    def start_crawl(self):
        """
        爬虫函数
        """
        # 获取到页面和条目统计信息
        stopFlag = False
        CrawlData =[]
        # 获取搜索结果总页数
        pages = int(self.get_page_count(self.starturl, self.my_headers))
        # 根据是否需要记录文件来进行
        index = 0
        # 遍历所有的新闻页
        for i in range(0, pages+1):
            # 得到当前页的url
            urls = self.starturl.replace("page=0", "page=%d" % i)
            # 返回数组对象，每个元素表示一条新闻的简略信息
            infodexs = self.index_info(urls, self.my_headers)
            if len(infodexs) > 0:
                for infodex in infodexs:
                    NewInfo={}
                    if self.deadlineTime!=0 and infodex["reporttime"][0:10].strip()<self.deadlineTime: #终止爬取
                        stopFlag=True
                        break
                    body = self.get_news_body(infodex["url"], self.my_headers)
                    if body!=None:
                        print("hahhah===")
                        NewInfo["reporter"]=u"联合早报"
                        NewInfo["pubtime"]=infodex["reporttime"]
                        NewInfo["title"]=infodex["title"]
                        NewInfo["des"]=body["des"]
                        NewInfo["content"]=body["content"]
                        NewInfo["url"]=infodex["url"]
                        NewInfo["imgurl"]=body["imgUrl"]
            #result =object.test(NewInfo["content"])
			#print NewInfo["content"]
                    result = lr_text.text_classify([NewInfo["content"]])
                    #print result
                    NewInfo["result"]=result
                    summary=auto_abstract.abstract(body["content"])
                    #print "summary========="
                    #print summary
                    if summary!=None:
                        NewInfo["summary"]=summary
                        EventInfo=None
                    '''
                    进一步获取时间信息
                    '''
                    EventInfo=EventInfo_extract.EventInfo_extraction(body["content"])

                    if EventInfo!=None:
                        NewInfo["Event_time"]=EventInfo["Event_time"]
                        print(EventInfo["Event_time"].decode("utf-8"))
                        NewInfo["Event_address"]=EventInfo['Event_address']
                        # NewInfo["Event_type"]=EventInfo['Event_type']
                        NewInfo["Event_total"]=EventInfo['Event_total']
                        NewInfo["Event_gname"]=EventInfo["Event_gname"]
                        NewInfo["Event_nwound"]=EventInfo['Event_nwound']
                        NewInfo["Event_nkill"]=EventInfo['Event_nkill']

                        #将返回消息通过列表形式返回上一层统一进行入库处理。
                    else:
                        NewInfo["Event_time"]='unknown'
                        NewInfo["Event_address"]='unknown'
                        NewInfo["Event_type"]='unknown'
                        NewInfo["Event_total"]='unknown'
                        NewInfo["Event_gname"]='unknown'
                        NewInfo["Event_nwound"]='unknown'
                        NewInfo["Event_nkill"]='unknown'

                    # print(NewInfo)
                    if len(NewInfo)>0:
                        index += 1
                        CrawlData.append(NewInfo)
                    #     #print "aaaaaaaaaaaaaaaaaa"
                        # saveData.saveData(NewInfo["url"],NewInfo)
                        # DataSend.sendata("localhost",50001,NewInfo)

                        #CrawlData.append(NewInfo)
                    if stopFlag ==True:
                        break
        return CrawlData, index

    def getUrl_multiTry(self, url, headers):
        import random
        time.sleep(1)
        maxTryNum = 10
        for tries in range(maxTryNum):
            #try:
            randddom_header = random.choice(headers)
            req = urllib.request.Request(url)
            req.add_header("User-Agent", randddom_header)
            req.add_header("GET", url)
            html = urllib.request.urlopen(req).read().decode(encoding="utf8", errors='ignore')
            return html

            # except:
            #     if tries < (maxTryNum - 1):
            #         continue
            #     else:
            #         logging.error("Has tried %d times to access url %s, all failed!", maxTryNum, url)
            #         break

# 获取新闻的标题和链接
# if __name__=="__main__":
#     zaobaoCrawl = Crawl_NEWS(timeFrame=20)
#     craw, index = zaobaoCrawl.start_crawl()
#     print(craw, index)
    # db_connect.close()

