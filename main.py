# -*- coding: utf-8 -*-

"""
1、测试的时候出现时间问题，没有具体发生时间，但是记录的时候需要记录时间以便确定id
"""
import wx
import time
import csv

from CrawlWebSite import sputniknews, DataManager
from ChineseNER import extract

def read_csv(title, path):
    reader = []
    csv_reader = csv.reader(open(path, encoding='utf-8'))
    for row in csv_reader:
        reader.append(row)
    del reader[0]
    result = []
    for mesg in reader:
        news = {}
        news['Event_time'] = mesg[title.index('time')]
        news['Event_address'] = mesg[title.index('city')]
        news['Event_gname'] = mesg[title.index('gname')]
        news['Event_type'] = mesg[title.index('attacktype1')]
        news['Event_nkill'] = mesg[title.index('nkill')]
        news['Event_nwound'] = mesg[title.index('nwound')]
        news['Event_total'] = str(int(news['Event_nkill']) + int(news['Event_nwound']))
        result.append(news)
    return result

class CrawlTotalDialog(wx.Dialog):
    def __init__(self, num):
        wx.Dialog.__init__(self, None, -1, 'finish', size=(200, 150))
        self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        static1 = wx.StaticText(self, -1, label='新闻爬取完成', pos=(35, 15))
        str_total = '总计抽取新闻' + str(num) + '条'
        static2 = wx.StaticText(self, -1, label=str_total, pos=(35, 40))
        okButton = wx.Button(self, wx.ID_CANCEL, label='确定', pos=(40, 70))
        okButton.SetDefault()
        static1.SetFont(self.font)
        static2.SetFont(self.font)
        okButton.SetFont(self.font)

class CheckDialog(wx.Dialog):
    def __init__(self, mesg1, mesg2):
        wx.Dialog.__init__(self, None, -1, 'Check', size=(700, 520))
        self.mesg1 = mesg1
        self.mesg2 = mesg2

        self.panel = self.panel = wx.Panel(self, -1)
        self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        sizer = wx.GridBagSizer(15, 15)

        static1 = wx.StaticText(self.panel, label='第一条', style=wx.ST_NO_AUTORESIZE)
        static1.SetFont(self.font)
        sizer.Add(static1, pos=(0, 1), span=(1, 1), flag=wx.TOP, border=15)
        static2 = wx.StaticText(self.panel, label='第二条', style=wx.ST_NO_AUTORESIZE)
        static2.SetFont(self.font)
        sizer.Add(static2, pos=(0, 6), span=(1, 1), flag=wx.TOP, border=15)

        Text_time1 = wx.StaticText(self.panel, label='时间', style=wx.ST_NO_AUTORESIZE)
        Text_time1.SetFont(self.font)
        sizer.Add(Text_time1, pos=(1, 1), span=(1, 1), flag=wx.TOP, border=0)
        Text_Address1 = wx.StaticText(self.panel, label='地点', style=wx.ST_NO_AUTORESIZE)
        Text_Address1.SetFont(self.font)
        sizer.Add(Text_Address1, pos=(2, 1), span=(1, 1), flag=wx.TOP, border=0)
        Text_gname1 = wx.StaticText(self.panel, label='组织', style=wx.ST_NO_AUTORESIZE)
        Text_gname1.SetFont(self.font)
        sizer.Add(Text_gname1, pos=(3, 1), span=(1, 1), flag=wx.TOP, border=0)
        Text_type1 = wx.StaticText(self.panel, label='事件类型', style=wx.ST_NO_AUTORESIZE)
        Text_type1.SetFont(self.font)
        sizer.Add(Text_type1, pos=(4, 1), span=(1, 1), flag=wx.TOP, border=0)
        Text_total1 = wx.StaticText(self.panel, label='伤亡人数', style=wx.ST_NO_AUTORESIZE)
        Text_total1.SetFont(self.font)
        sizer.Add(Text_total1, pos=(5, 1), span=(1, 1), flag=wx.TOP, border=0)
        Text_nwound1 = wx.StaticText(self.panel, label='受伤人数', style=wx.ST_NO_AUTORESIZE)
        Text_nwound1.SetFont(self.font)
        sizer.Add(Text_nwound1, pos=(6, 1), span=(1, 1), flag=wx.TOP, border=0)
        Text_nkill1 = wx.StaticText(self.panel, label='死亡人数', style=wx.ST_NO_AUTORESIZE)
        Text_nkill1.SetFont(self.font)
        sizer.Add(Text_nkill1, pos=(7, 1), span=(1, 1), flag=wx.TOP, border=0)
        Text_content1 = wx.StaticText(self.panel, label='内容', style=wx.ST_NO_AUTORESIZE)
        Text_content1.SetFont(self.font)
        sizer.Add(Text_content1, pos=(8, 1), span=(1, 1), flag=wx.TOP, border=0)

        self.Time1 = wx.TextCtrl(self.panel, value=mesg1['Event_time'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Time1.SetFont(self.font)
        sizer.Add(self.Time1, pos=(1, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.Address1 = wx.TextCtrl(self.panel, value=mesg1['Event_address'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Address1.SetFont(self.font)
        sizer.Add(self.Address1, pos=(2, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.gname1 = wx.TextCtrl(self.panel, value=mesg1['Event_gname'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.gname1.SetFont(self.font)
        sizer.Add(self.gname1, pos=(3, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.type1 = wx.TextCtrl(self.panel, value=mesg1['Event_type'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.type1.SetFont(self.font)
        sizer.Add(self.type1, pos=(4, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.total1 = wx.TextCtrl(self.panel, value=mesg1['Event_total'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.total1.SetFont(self.font)
        sizer.Add(self.total1, pos=(5, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.nwound1 = wx.TextCtrl(self.panel, value=mesg1['Event_nwound'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nwound1.SetFont(self.font)
        sizer.Add(self.nwound1, pos=(6, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.nkill1 = wx.TextCtrl(self.panel, value=mesg1['Event_nkill'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nkill1.SetFont(self.font)
        sizer.Add(self.nkill1, pos=(7, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.content1 = wx.TextCtrl(self.panel, value=mesg1['content'], style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 100))
        self.content1.SetFont(self.font)
        sizer.Add(self.content1, pos=(8, 2), span=(3, 3), flag=wx.LEFT, border=0)

        Text_time2 = wx.StaticText(self.panel, label='时间', style=wx.ST_NO_AUTORESIZE)
        Text_time2.SetFont(self.font)
        sizer.Add(Text_time2, pos=(1, 6), span=(1, 1), flag=wx.TOP, border=0)
        Text_Address2 = wx.StaticText(self.panel, label='地点', style=wx.ST_NO_AUTORESIZE)
        Text_Address2.SetFont(self.font)
        sizer.Add(Text_Address2, pos=(2, 6), span=(1, 1), flag=wx.TOP, border=0)
        Text_gname2 = wx.StaticText(self.panel, label='组织', style=wx.ST_NO_AUTORESIZE)
        Text_gname2.SetFont(self.font)
        sizer.Add(Text_gname2, pos=(3, 6), span=(1, 1), flag=wx.TOP, border=0)
        Text_type2 = wx.StaticText(self.panel, label='事件类型', style=wx.ST_NO_AUTORESIZE)
        Text_type2.SetFont(self.font)
        sizer.Add(Text_type2, pos=(4, 6), span=(1, 1), flag=wx.TOP, border=0)
        Text_total2 = wx.StaticText(self.panel, label='伤亡人数', style=wx.ST_NO_AUTORESIZE)
        Text_total2.SetFont(self.font)
        sizer.Add(Text_total2, pos=(5, 6), span=(1, 1), flag=wx.TOP, border=0)
        Text_nwound2 = wx.StaticText(self.panel, label='受伤人数', style=wx.ST_NO_AUTORESIZE)
        Text_nwound2.SetFont(self.font)
        sizer.Add(Text_nwound2, pos=(6, 6), span=(1, 1), flag=wx.TOP, border=0)
        Text_nkill2 = wx.StaticText(self.panel, label='死亡人数', style=wx.ST_NO_AUTORESIZE)
        Text_nkill2.SetFont(self.font)
        sizer.Add(Text_nkill2, pos=(7, 6), span=(1, 1), flag=wx.TOP, border=0)
        Text_content1 = wx.StaticText(self.panel, label='内容', style=wx.ST_NO_AUTORESIZE)
        Text_content1.SetFont(self.font)
        sizer.Add(Text_content1, pos=(8, 6), span=(1, 1), flag=wx.TOP, border=0)

        self.Time2 = wx.TextCtrl(self.panel, value=mesg2['Event_time'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Time2.SetFont(self.font)
        sizer.Add(self.Time2, pos=(1, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.Address2 = wx.TextCtrl(self.panel, value=mesg2['Event_address'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Address2.SetFont(self.font)
        sizer.Add(self.Address2, pos=(2, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.gname2 = wx.TextCtrl(self.panel, value=mesg2['Event_gname'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.gname2.SetFont(self.font)
        sizer.Add(self.gname2, pos=(3, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.type2 = wx.TextCtrl(self.panel, value=mesg2['Event_type'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.type2.SetFont(self.font)
        sizer.Add(self.type2, pos=(4, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.total2 = wx.TextCtrl(self.panel, value=mesg2['Event_total'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.total2.SetFont(self.font)
        sizer.Add(self.total2, pos=(5, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.nwound2 = wx.TextCtrl(self.panel, value=mesg2['Event_nwound'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nwound2.SetFont(self.font)
        sizer.Add(self.nwound2, pos=(6, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.nkill2 = wx.TextCtrl(self.panel, value=mesg2['Event_nkill'], size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nkill2.SetFont(self.font)
        sizer.Add(self.nkill2, pos=(7, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.content2 = wx.TextCtrl(self.panel, value=mesg2['content'], style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 100))
        self.content2.SetFont(self.font)
        sizer.Add(self.content2, pos=(8, 7), span=(3, 3), flag=wx.LEFT, border=0)

        line2 = wx.StaticLine(self.panel)
        sizer.Add(line2, pos=(11, 0), span=(1, 15), flag=wx.EXPAND | wx.TOP, border=10)

        Button1 = wx.Button(self.panel, label='全部保存', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        Button1.SetDefault()
        Button1.SetFont(self.font)
        sizer.Add(Button1, pos=(12, 3), span=(1, 2), flag=wx.TOP, border=0)
        Button2 = wx.Button(self.panel, label='保存第一条', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        Button2.SetFont(self.font)
        sizer.Add(Button2, pos=(12, 5), span=(1, 2), flag=wx.TOP, border=0)
        Button3 = wx.Button(self.panel, label='保存第二条', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        Button3.SetFont(self.font)
        sizer.Add(Button3, pos=(12, 7), span=(1, 2), flag=wx.TOP, border=0)
        Button1.Bind(wx.EVT_BUTTON, self.OnClickSaveall)
        Button2.Bind(wx.EVT_BUTTON, self.OnClickSave1)
        Button3.Bind(wx.EVT_BUTTON, self.OnClickSave2)

        self.panel.SetSizer(sizer)

    def OnClickSaveall(self, e):
        self.list_result = []
        self.list_result.append(self.mesg1)
        self.list_result.append(self.mesg2)

    def OnClickSave1(self, e):
        self.list_result = []
        curr_news = {}
        curr_news['content'] = self.content1.GetValue()
        curr_news['Event_time'] = self.Time1.GetValue()
        curr_news['Event_address'] = self.Address1.GetValue()
        curr_news['Event_gname'] = self.gname1.GetValue()
        curr_news['Event_type'] = self.type1.GetValue()
        curr_news['Event_total'] = self.total1.GetValue()
        curr_news['Event_nkill'] = self.nkill1.GetValue()
        curr_news['Event_nwound'] = self.nwound1.GetValue()
        self.list_result.append(curr_news)

    def OnClickSave2(self, e):
        self.list_result = []
        curr_news = {}
        curr_news['content'] = self.content2.GetValue()
        curr_news['Event_time'] = self.Time2.GetValue()
        curr_news['Event_address'] = self.Address2.GetValue()
        curr_news['Event_gname'] = self.gname2.GetValue()
        curr_news['Event_type'] = self.type2.GetValue()
        curr_news['Event_total'] = self.total2.GetValue()
        curr_news['Event_nkill'] = self.nkill2.GetValue()
        curr_news['Event_nwound'] = self.nwound2.GetValue()
        self.list_result.append(curr_news)

    def returemesg(self):
        return self.list_result

class CheckNews(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size=(660, 380))
        self.panel = wx.Panel(self, -1)
        self.today = [time.strftime("%Y"), time.strftime("%m"), time.strftime("%d")]
        self.before = 1
        self.strTitle = ['eventid', 'eventname', 'iyear', 'imonth', 'iday', 'time', 'approxdate',
                         'country_txt', 'provstate', 'city', 'latitude', 'longitude', 'location',
                         'summary', 'alternative_txt', 'multiple', 'suicide', 'attacktype1',
                         'attacktype1_txt', 'attacktype2', 'attacktype2_txt', 'attacktype3',
                         'attacktype3_txt', 'targtype1_txt', 'targsubtype1_txt', 'corp1', 'target1',
                         'natlty1_txt', 'targtype2_txt', 'targsubtype2_txt', 'corp2', 'target2',
                         'natlty2_txt', 'targtype3_txt', 'targsubtype3_txt', 'corp3', 'target3',
                         'natlty3_txt', 'gname', 'motive', 'nperps', 'nperpcap', 'weaptype1_txt',
                         'weapsubtype1_txt', 'weaptype2_txt', 'weapsubtype2_txt', 'weaptype3_txt',
                         'weapsubtype3_txt', 'weaptype4_txt', 'weapsubtype4_txt', 'weapdetail', 'nkill',
                         'nkillter', 'nwound', 'nwoundte', 'property', 'propvalue', 'propcomment',
                         'ishostkid', 'nhostkid', 'nhours', 'divert', 'ransom', 'ransomamt', 'ransompaid',
                         'ransomnote', 'hostkidoutcome_txt', 'nreleased', 'addnotes', 'scite1', 'scite2',
                         'scite3', 'related']

        filename = 'data.csv'
        self.orig_data = read_csv(self.strTitle, filename)

        self.initUI()
        self.boundBotton()

    def initUI(self):
        self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        sizer = wx.GridBagSizer(9, 15)

        str_time = self.today[0] + '年' + self.today[1] + '月' + self.today[2] + '日'
        self.Texttime = wx.StaticText(self.panel, label=str_time, style=wx.ST_NO_AUTORESIZE)
        self.Texttime.SetFont(self.font)
        sizer.Add(self.Texttime, pos=(0, 0), flag=wx.TOP | wx.LEFT, border=10)
        self.Textbefore1 = wx.StaticText(self.panel, label='爬取前', style=wx.ST_NO_AUTORESIZE)
        self.Textbefore1.SetFont(self.font)
        sizer.Add(self.Textbefore1, pos=(0, 4), flag=wx.TOP | wx.LEFT, border=10)
        self.Daybefore = wx.TextCtrl(self.panel, value=str(self.before), size=(40, 25), style=wx.ST_NO_AUTORESIZE)
        self.Daybefore.SetFont(self.font)
        sizer.Add(self.Daybefore, pos=(0, 5), flag=wx.TOP|wx.LEFT, border=5)
        self.Textbefore2 = wx.StaticText(self.panel, label='天', style=wx.ST_NO_AUTORESIZE)
        self.Textbefore2.SetFont(self.font)
        sizer.Add(self.Textbefore2, pos=(0, 6), flag=wx.TOP | wx.EXPAND, border=10)
        self.CrawlBotton = wx.Button(self.panel, label='新闻提取', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        self.CrawlBotton.SetFont(self.font)
        sizer.Add(self.CrawlBotton, pos=(0, 7), flag=wx.TOP, border=5)

        line = wx.StaticLine(self.panel)
        sizer.Add(line, pos=(1, 0), span=(1, 15), flag=wx.EXPAND | wx.BOTTOM, border=5)

        self.TextNews = wx.TextCtrl(self.panel, value='', style=wx.TE_MULTILINE | wx.TE_READONLY, size=(300, 200))
        self.TextNews.SetFont(self.font)
        sizer.Add(self.TextNews, pos=(2, 0), span=(8, 4), flag=wx.LEFT, border=10)

        Text_pubTime = wx.StaticText(self.panel, label='发布时间：', style=wx.ST_NO_AUTORESIZE)
        Text_pubTime.SetFont(self.font)
        sizer.Add(Text_pubTime, pos=(2, 4), span=(1, 1), flag=wx.TOP, border=0)
        self.pubTime = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.pubTime.SetFont(self.font)
        sizer.Add(self.pubTime, pos=(2, 5), span=(1, 3), flag=wx.LEFT, border=0)

        Text_time = wx.StaticText(self.panel, label='时间', style=wx.ST_NO_AUTORESIZE)
        Text_time.SetFont(self.font)
        sizer.Add(Text_time, pos=(3, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_Address = wx.StaticText(self.panel, label='地点', style=wx.ST_NO_AUTORESIZE)
        Text_Address.SetFont(self.font)
        sizer.Add(Text_Address, pos=(4, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_gname = wx.StaticText(self.panel, label='组织', style=wx.ST_NO_AUTORESIZE)
        Text_gname.SetFont(self.font)
        sizer.Add(Text_gname, pos=(5, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_type = wx.StaticText(self.panel, label='事件类型', style=wx.ST_NO_AUTORESIZE)
        Text_type.SetFont(self.font)
        sizer.Add(Text_type, pos=(6, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_total = wx.StaticText(self.panel, label='伤亡人数', style=wx.ST_NO_AUTORESIZE)
        Text_total.SetFont(self.font)
        sizer.Add(Text_total, pos=(7, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_nwound = wx.StaticText(self.panel, label='受伤人数', style=wx.ST_NO_AUTORESIZE)
        Text_nwound.SetFont(self.font)
        sizer.Add(Text_nwound, pos=(8, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_nkill = wx.StaticText(self.panel, label='死亡人数', style=wx.ST_NO_AUTORESIZE)
        Text_nkill.SetFont(self.font)
        sizer.Add(Text_nkill, pos=(9, 4), span=(1, 1), flag=wx.TOP, border=0)

        self.Time = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Time.SetFont(self.font)
        sizer.Add(self.Time, pos=(3, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.Address = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Address.SetFont(self.font)
        sizer.Add(self.Address, pos=(4, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.gname = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.gname.SetFont(self.font)
        sizer.Add(self.gname, pos=(5, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.type = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.type.SetFont(self.font)
        sizer.Add(self.type, pos=(6, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.total = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.total.SetFont(self.font)
        sizer.Add(self.total, pos=(7, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.nwound = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nwound.SetFont(self.font)
        sizer.Add(self.nwound, pos=(8, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.nkill = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nkill.SetFont(self.font)
        sizer.Add(self.nkill, pos=(9, 5), span=(1, 3), flag=wx.LEFT, border=0)

        line2 = wx.StaticLine(self.panel)
        sizer.Add(line2, pos=(10, 0), span=(1, 15), flag=wx.EXPAND | wx.TOP, border=10)

        self.TextTip = wx.StaticText(self.panel, label=' 0 / 0 ',size=(100, 25), style=wx.ST_NO_AUTORESIZE)
        self.TextTip.SetFont(self.font)
        sizer.Add(self.TextTip, pos=(11, 0), span=(1, 1), flag=wx.LEFT, border=30)

        self.upbotton = wx.Button(self.panel, label='上一条', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        self.upbotton.SetFont(self.font)
        sizer.Add(self.upbotton, pos=(11, 3), span=(1, 2), flag=wx.TOP, border=0)
        self.okbotton = wx.Button(self.panel, label='确定', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        self.okbotton.SetFont(self.font)
        self.okbotton.SetDefault()
        sizer.Add(self.okbotton, pos=(11, 5), span=(1, 2), flag=wx.TOP, border=0)
        self.savebotton = wx.Button(self.panel, label='保存', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        self.savebotton.SetFont(self.font)
        sizer.Add(self.savebotton, pos=(11, 7), span=(1, 2), flag=wx.TOP, border=0)

        self.panel.SetSizer(sizer)

    def boundBotton(self):
        self.CrawlBotton.Bind(wx.EVT_BUTTON, self.OnClickCraw)
        self.upbotton.Bind(wx.EVT_BUTTON, self.OnClickUp)
        self.okbotton.Bind(wx.EVT_BUTTON, self.OnClickOk)
        self.savebotton.Bind(wx.EVT_BUTTON, self.OnClickSave)

    def OnClickCraw(self, e):
        self.before = self.Daybefore.GetValue()
        # self.zaobao = ZaoBao.Crawl_NEWS(timeFrame=int(self.before))
        self.sputnik = sputniknews.Crawl_NEWS(timeFrame=int(self.before))
        # news1, index1 = self.zaobao.start_crawl()
        news2, index2 = self.sputnik.start_crawl()

        # news = news1 + news2
        self.index = 0
        self.news = []
        for strNews in news2:
            if strNews['result'] == '暴恐':
                self.news.append(strNews)
                self.index += 1
        self.news = extract.EventInfo_extract(self.news)
        print(self.index)
        modal = CrawlTotalDialog(self.index)
        modal.ShowModal()
        modal.Destroy()
        # self.index = 4
        # news1 = {"content":"卡收到啦开始的断代史六块腹肌暗红色的防守打法哈里斯的看法还是得分离的合法楼上的发哈东风浩荡发生的合法阿萨德雷锋号拉婚纱店对方拉黑谁的浪费空间暗红色的枫林华府阿萨德发挥打死都会发生的；大水电费离开的说法东方会计师电话费电话费拉开多久发货的给客户绿卡的复合弓发过哈人派人和人配合领导看见过很多非公开发的卡号是的开发好的都会发两块闪电发货大是大非拉克丝得分机会大街上的法律框架爱的说法",
        #          "Event_time":"2018.01.02",
        #          "Event_address":" ",
        #          "Event_gname":"",
        #          "Event_type":"暴恐",
        #          "Event_total":" ",
        #          "Event_nkill":"",
        #          "Event_nwound":" "}
        # news2 = {
        #     "content": "卡收到啦开始发就是打发点上了飞机快递师傅噢诶与人文人未还收代理费会计师电话费阿里看到回复啦可是对方好落实到付款就好说的福利卡决定是否拉宽带缴费号类似的看法好里的疯狂就啊哈到了发卡机的福利卡交电话费埃里克的舒服就好里的咖啡好的发快递金凤凰爱看的房价还是里的咖啡好的福利卡的护肤拉宽带缴费hiUR全业务如以前我饿人哟诶UR要求欧伟复活点时空房间爱好的的断代史六块腹肌暗红色的防守打法哈里斯的看法还是得分离的合法楼上的发哈东风浩荡发生的合法阿萨德雷锋号拉婚纱店对方拉黑谁的浪费空间暗红色的枫林华府阿萨德发挥打死都会发生的；大水电费离开的说法东方会计师电话费电话费拉开多久发货的给客户绿卡的复合弓发过哈人派人和人配合领导看见过很多非公开发的卡号是的开发好的都会发两块闪电发货大是大非拉克丝得分机会大街上的法律框架爱的说法",
        #     "Event_time": "2018.01.01",
        #     "Event_address": " ",
        #     "Event_gname": "",
        #     "Event_type": "暴恐",
        #     "Event_total": " ",
        #     "Event_nkill": "",
        #     "Event_nwound": " "}
        # news3 = {
        #     "content": "2、卡收到啦开始的断代史六块腹肌暗红色的防守打法哈里斯的看法还是得分离的合法楼上的发哈东风浩荡发生的合法阿萨德雷锋号拉婚纱店对方拉黑谁的浪费空间暗红色的枫林华府阿萨德发挥打死都会发生的；大水电费离开的说法东方会计师电话费电话费拉开多久发货的给客户绿卡的复合弓发过哈人派人和人配合领导看见过很多非公开发的卡号是的开发好的都会发两块闪电发货大是大非拉克丝得分机会大街上的法律框架爱的说法",
        #     "Event_time": "2018.01.01",
        #     "Event_address": " ",
        #     "Event_gname": "",
        #     "Event_type": "暴恐",
        #     "Event_total": " ",
        #     "Event_nkill": "",
        #     "Event_nwound": " "}
        # news4 = {
        #     "content": "3、卡收到啦开始的断代史六块腹肌暗红色的防守打法哈里斯的看法还是得分离的合法楼上的发哈东风浩荡发生的合法阿萨德雷锋号拉婚纱店对方拉黑谁的浪费空间暗红色的枫林华府阿萨德发挥打死都会发生的；大水电费离开的说法东方会计师电话费电话费拉开多久发货的给客户绿卡的复合弓发过哈人派人和人配合领导看见过很多非公开发的卡号是的开发好的都会发两块闪电发货大是大非拉克丝得分机会大街上的法律框架爱的说法",
        #     "Event_time": "2018.01.01",
        #     "Event_address": " ",
        #     "Event_gname": "",
        #     "Event_type": "暴恐",
        #     "Event_total": " ",
        #     "Event_nkill": "",
        #     "Event_nwound": " "}
        # self.news = [news1, news2, news3, news4]
        self.id = 0
        self.fillValue(self.id)

    def OnClickUp(self, e):
        if self.Time.GetValue() == '':
            state = 0
        else:
            state = 1
        self.saveValue(self.id, state)
        self.id -= 1
        if self.id < 0:
            self.id = self.index - 1
        self.fillValue(self.id)

    def OnClickOk(self, e):
        if self.Time.GetValue() == '':
            state = 0
        else:
            state = 1
        self.saveValue(self.id, state)
        self.id += 1
        if self.id >= self.index:
            self.id = 0
        self.fillValue(self.id)

    def OnClickSave(self, e):
        if self.Time.GetValue() == '':
            state = 0
        else:
            state = 1
        self.saveValue(self.id, state)
        compare_result = self.compareNews(self.news)
        stream_news = self.change_list(compare_result)
        str_path = 'data.csv'
        DataManager.write_csv(str_path, stream_news)

    def fillValue(self, id):
        curr_news = self.news[id]
        self.TextNews.SetValue(curr_news['content'])
        self.Time.SetValue(curr_news['Event_time'])
        self.Address.SetValue(curr_news['Event_address'])
        self.gname.SetValue(curr_news['Event_gname'])
        self.type.SetValue(curr_news['Event_type'])
        self.total.SetValue(curr_news['Event_total'])
        self.nkill.SetValue(curr_news['Event_nkill'])
        self.nwound.SetValue(curr_news['Event_nwound'])
        self.pubTime.SetValue(curr_news['pubtime'])
        str_tip = " " + str(self.id + 1) + " / " + str(self.index)# + " " + "pubTime:" + curr_news['pubtime']
        self.TextTip.SetLabel(str_tip)

    def saveValue(self, id, state):
        curr_news = self.news[id]
        curr_news['content'] = self.TextNews.GetValue()
        curr_news['Event_time'] = self.Time.GetValue()
        curr_news['Event_address'] = self.Address.GetValue()
        curr_news['Event_gname'] = self.gname.GetValue()
        curr_news['Event_type'] = self.type.GetValue()
        curr_news['Event_total'] = self.total.GetValue()
        curr_news['Event_nkill'] = self.nkill.GetValue()
        curr_news['Event_nwound'] = self.nwound.GetValue()
        curr_news['state'] = state
        str_tip = " " + str(self.id + 1) + " / " + str(self.index)# + " " + "pubTime:" + curr_news['pubtime']
        self.TextTip.SetLabel(str_tip)

    def compareNews(self, lists):
        list = []
        for news in lists:
            if news['state'] == 1:
                list.append(news)
        list.extend(self.orig_data)
        result = []
        while list:
            mesg1 = list[0]
            del list[0]
            event_num = 0
            event_id = mesg1['Event_time'].split('.')[0] + mesg1['Event_time'].split('.')[1] + mesg1['Event_time'].split('.')[2] + '0000'
            delete_id = []
            for i in range(len(list)):
                mesg2 = list[i]
                if mesg2['Event_time'] == mesg1['Event_time']:
                    modal = CheckDialog(mesg1, mesg2)
                    modal.ShowModal()
                    return_mesg= modal.returemesg()
                    modal.Destroy()
                    if len(return_mesg) > 1:
                        event_num += 1
                        return_mesg[1]['Event_id'] = str(int(event_id) + event_num)
                        result.append(return_mesg[1])

                    else:
                        mesg1 = return_mesg[0]

                    delete_id.append(i)

            event_num += 1
            mesg1['Event_id'] = str(int(event_id) + event_num)
            result.append(mesg1)
            num = 0
            for id in delete_id:
                del list[id - num]
                num += 1
        return result

    def change_list(self, lists):
        streams = []
        streams.append(self.strTitle)
        new_lists = sorted(lists, key=lambda e: e.__getitem__('Event_id'))
        for list in new_lists:
            stream = []
            for title in self.strTitle:
                if title == 'eventid':
                    stream.append(list['Event_id'])
                elif title == 'iyear':
                    stream.append(list['Event_time'].split('.')[0])
                elif title == 'imonth':
                    stream.append(list['Event_time'].split('.')[1])
                elif title == 'iday':
                    stream.append(list['Event_time'].split('.')[2])
                elif title == 'time':
                    stream.append(list['Event_time'])
                elif title == 'city':
                    stream.append(list['Event_address'])
                elif title == 'gname':
                    stream.append(list['Event_gname'])
                elif title == 'nkill':
                    stream.append(list['Event_nkill'])
                elif title == 'nwound':
                    stream.append(list['Event_nwound'])
                elif title == 'attacktype1_txt':
                    stream.append(list['Event_type'])
                else:
                    stream.append('')
            streams.append(stream)
        return streams

if __name__ == '__main__':
    app = wx.App()
    frame = CheckNews()
    frame.Show()
    app.MainLoop()

