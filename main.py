"""
1、需要注意有些提取的时候因为错误原文没有提取出来，因此要判断content是否为空
2、
"""
import wx
import time

from CrawlWebSite import ZaoBao, guangchazhe

class CrawlTotalDialog(wx.Dialog):
    def __init__(self, num):
        wx.Dialog.__init__(self, None, -1, 'finish', size=(180, 150))
        static1 = wx.StaticText(self, -1, label='新闻爬取完成', pos=(35, 15))
        str_total = '总计抽取新闻' + str(num) + '条'
        static2 = wx.StaticText(self, -1, label=str_total, pos=(35, 40))
        okButton = wx.Button(self, wx.ID_CANCEL, label='确定', pos=(40, 70))
        okButton.SetDefault()

class CheckSameDialog(wx.Dialog):
    def __init__(self, mesg1, mesg2):
        wx.Dialog.__init__(self, None, -1, 'Check', size=(300, 90))
        static1 = wx.StaticText(self, -1, label=str(mesg1), pos=(15, 10))
        static2 = wx.StaticText(self, -1, label=str(mesg2), pos=(30, 10))
        Button1 = wx.Button(self, label='全部保存', pos=(45, 50))
        Button1.SetDefault()
        Button2 = wx.Button(self, label='保存第一条', pos=(60, 50))
        Button3 = wx.Button(self, label='保存第二条', pos=(75, 50))

        Button1.Bind(wx.EVT_BUTTON, self.OnClickSaveall)
        Button2.Bind(wx.EVT_BUTTON, self.OnClickSave1)
        Button3.Bind(wx.EVT_BUTTON, self.OnClickSave2)

    def OnClickSaveall(self, e):
        pass

    def OnClickSave1(self, e):
        pass

    def OnClickSave2(self, e):
        pass


class CheckNews(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size=(650, 360))
        self.panel = wx.Panel(self, -1)
        self.today = [time.strftime("%Y"), time.strftime("%m"), time.strftime("%d")]
        self.before = 1
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
        self.Daybefore = wx.TextCtrl(self.panel, value=str(self.before), size=(25, 30), style=wx.ST_NO_AUTORESIZE)
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
        sizer.Add(self.TextNews, pos=(2, 0), span=(7, 4), flag=wx.LEFT, border=10)

        Text_time = wx.StaticText(self.panel, label='时间', style=wx.ST_NO_AUTORESIZE)
        Text_time.SetFont(self.font)
        sizer.Add(Text_time, pos=(2, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_Address = wx.StaticText(self.panel, label='地点', style=wx.ST_NO_AUTORESIZE)
        Text_Address.SetFont(self.font)
        sizer.Add(Text_Address, pos=(3, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_gname = wx.StaticText(self.panel, label='组织', style=wx.ST_NO_AUTORESIZE)
        Text_gname.SetFont(self.font)
        sizer.Add(Text_gname, pos=(4, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_type = wx.StaticText(self.panel, label='事件类型', style=wx.ST_NO_AUTORESIZE)
        Text_type.SetFont(self.font)
        sizer.Add(Text_type, pos=(5, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_total = wx.StaticText(self.panel, label='伤亡人数', style=wx.ST_NO_AUTORESIZE)
        Text_total.SetFont(self.font)
        sizer.Add(Text_total, pos=(6, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_nwound = wx.StaticText(self.panel, label='受伤人数', style=wx.ST_NO_AUTORESIZE)
        Text_nwound.SetFont(self.font)
        sizer.Add(Text_nwound, pos=(7, 4), span=(1, 1), flag=wx.TOP, border=0)
        Text_nkill = wx.StaticText(self.panel, label='死亡人数', style=wx.ST_NO_AUTORESIZE)
        Text_nkill.SetFont(self.font)
        sizer.Add(Text_nkill, pos=(8, 4), span=(1, 1), flag=wx.TOP, border=0)

        self.Time = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Time.SetFont(self.font)
        sizer.Add(self.Time, pos=(2, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.Address = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Address.SetFont(self.font)
        sizer.Add(self.Address, pos=(3, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.gname = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.gname.SetFont(self.font)
        sizer.Add(self.gname, pos=(4, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.type = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.type.SetFont(self.font)
        sizer.Add(self.type, pos=(5, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.total = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.total.SetFont(self.font)
        sizer.Add(self.total, pos=(6, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.nwound = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nwound.SetFont(self.font)
        sizer.Add(self.nwound, pos=(7, 5), span=(1, 3), flag=wx.LEFT, border=0)
        self.nkill = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nkill.SetFont(self.font)
        sizer.Add(self.nkill, pos=(8, 5), span=(1, 3), flag=wx.LEFT, border=0)

        line2 = wx.StaticLine(self.panel)
        sizer.Add(line2, pos=(9, 0), span=(1, 15), flag=wx.EXPAND | wx.TOP, border=10)

        self.upbotton = wx.Button(self.panel, label='上一条', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        self.upbotton.SetFont(self.font)
        sizer.Add(self.upbotton, pos=(10, 3), span=(1, 2), flag=wx.TOP, border=0)
        self.okbotton = wx.Button(self.panel, label='确定', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        self.okbotton.SetFont(self.font)
        self.okbotton.SetDefault()
        sizer.Add(self.okbotton, pos=(10, 5), span=(1, 2), flag=wx.TOP, border=0)
        self.savebotton = wx.Button(self.panel, label='保存', size=(80, 25), style=wx.ST_NO_AUTORESIZE)
        self.savebotton.SetFont(self.font)
        sizer.Add(self.savebotton, pos=(10, 7), span=(1, 2), flag=wx.TOP, border=0)

        self.panel.SetSizer(sizer)

    def boundBotton(self):
        self.CrawlBotton.Bind(wx.EVT_BUTTON, self.OnClickCraw)
        self.upbotton.Bind(wx.EVT_BUTTON, self.OnClickUp)
        self.okbotton.Bind(wx.EVT_BUTTON, self.OnClickOk)
        self.savebotton.Bind(wx.EVT_BUTTON, self.OnClickSave)

    def OnClickCraw(self, e):
        self.before = self.Daybefore.GetValue()
        self.zaobao = ZaoBao.Crawl_NEWS(timeFrame=int(self.before))
        self.guancha = guangchazhe.Crawl_NEWS(timeFrame=int(self.before))
        news1, index1 = self.zaobao.start_crawl()
        news2, index2 = self.guancha.start_crawl()

        self.news = news1 + news2
        self.index = index1 + index2
        print(self.index)
        modal = CrawlTotalDialog(self.index)
        modal.ShowModal()
        modal.Destroy()
        self.fillValue(0)


    def OnClickUp(self, e):
        pass

    def OnClickOk(self, e):
        pass

    def OnClickSave(self, e):
        pass


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

    def saveValue(self, id):
        curr_news = self.news[id]
        curr_news['content'] = self.TextNews.GetValue()
        curr_news['Event_time'] = self.Time.GetValue()
        curr_news['Event_address'] = self.Address.GetValue()
        curr_news['Event_gname'] = self.gname.GetValue()
        curr_news['Event_type'] = self.type.GetValue()
        curr_news['Event_total'] = self.total.GetValue()
        curr_news['Event_nkill'] = self.nkill.GetValue()
        curr_news['Event_nwound'] = self.nwound.GetValue()

if __name__ == '__main__':
    app = wx.App()
    frame = CheckNews()
    frame.Show()
    app.MainLoop()