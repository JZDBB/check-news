import wx
import time

# from CrawlWebSite import ZaoBao, guangchazhe, sputniknews, Haiwainet

class CheckNews(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size=(700, 350))
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
        sizer.Add(self.Texttime, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.Textbefore1 = wx.StaticText(self.panel, label='爬取前', style=wx.ST_NO_AUTORESIZE)
        self.Textbefore1.SetFont(self.font)
        sizer.Add(self.Textbefore1, pos=(0, 4), flag=wx.TOP, border=5)
        self.Daybefore = wx.TextCtrl(self.panel, value=str(self.before), size=(25, 20), style=wx.ST_NO_AUTORESIZE)
        self.Daybefore.SetFont(self.font)
        sizer.Add(self.Daybefore, pos=(0, 5), flag=wx.TOP, border=5)
        self.Textbefore2 = wx.StaticText(self.panel, label='天', style=wx.ST_NO_AUTORESIZE)
        self.Textbefore2.SetFont(self.font)
        sizer.Add(self.Textbefore2, pos=(0, 6), flag=wx.TOP | wx.EXPAND, border=5)
        self.CrawlBotton = wx.Button(self.panel, label='新闻爬取', size=(80, 20), style=wx.ST_NO_AUTORESIZE)
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



        self.panel.SetSizer(sizer)


    def boundBotton(self):
        pass



if __name__ == '__main__':
    app = wx.App()
    frame = CheckNews()
    frame.Show()
    app.MainLoop()