# -*- coding: utf-8 -*-
# coding:utf-8
"""
Created on Mon Nov 13 15:33:54 2017
@author: john
开启多线程，爬取网页信息
"""
# -*- coding: utf-8 -*-

import threading
from CrawlWebSite import ZaoBao, sputniknews, Haiwainet, guangchazhe

def Zaobao():
	CrawlOBJ = ZaoBao.Crawl_NEWS(timeFrame=1000)
	result=CrawlOBJ.start_crawl()

def sputniknewsA():
	CrawlOBJ = sputniknews.Crawl_NEWS(timeFrame=1000)
	result=CrawlOBJ.start_crawl()


def HaiwainetA():
	CrawlOBJ = Haiwainet.Crawl_NEWS(timeFrame=1000)
	result=CrawlOBJ.start_crawl()


def guangchazheA():
	CrawlOBJ = guangchazhe.Crawl_NEWS(timeFrame=1000)
	result=CrawlOBJ.start_crawl()


def StartCrawl():
	Thread=[]
	T1=threading.Thread(target=Zaobao)
	T1.setDaemon(True)
	T1.start()
	print(T1)
	Thread.append(T1)

	T2=threading.Thread(target=sputniknewsA)
	T2.setDaemon(True)
	T2.start()
	print(T2)
	Thread.append(T2)

	T3=threading.Thread(target=HaiwainetA)
	T3.setDaemon(True)
	T3.start()
	Thread.append(T3)

	T4=threading.Thread(target=guangchazheA)
	T4.setDaemon(True)
	T4.start()
	Thread.append(T4)
	return Thread
	

if __name__=="__main__":
	StartCrawl()
