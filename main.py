import wx
import time

# from CrawlWebSite import ZaoBao, guangchazhe, sputniknews, Haiwainet

class CheckNews(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None)
		self.panel = wx.Panel(self, -1)
		self.today = [time.strftime("%Y"), time.strftime("%m"), time.strftime("%d")]
		self.before = 1
		self.initUI()
		self.boundBotton()


	def initUI(self):
		self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

		sizer = wx.GridBagSizer(7, 7)

		str_time = self.today[0] + '年' + self.today[1] + '月' + self.today[2] + '日'
		self.Texttime = wx.StaticText(self.panel, label=str_time)
		self.Texttime.SetFont(self.font)
		sizer.Add(self.Texttime, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=15)
		self.Textbefore1 = wx.StaticText(self.panel, label='爬取前')
		self.Textbefore1.SetFont(self.font)
		sizer.Add(self.Textbefore1, pos=(0, 1), flag=wx.TOP | wx.EXPAND, border=15)
		self.Daybefore = wx.TextCtrl(self.panel, value=str(self.before), size=(25, 20))
		self.Daybefore.SetFont(self.font)
		sizer.Add(self.Daybefore, pos=(0, 2), flag=wx.TOP, border=15)
		self.Textbefore2 = wx.StaticText(self.panel, label='天')
		self.Textbefore2.SetFont(self.font)
		sizer.Add(self.Textbefore2, pos=(0, 3), flag=wx.TOP | wx.EXPAND, border=15)


		self.panel.SetSizer(sizer)


	def boundBotton(self):
		pass



if __name__ == '__main__':
	app = wx.App()
	frame = CheckNews()
	frame.Show()
	app.MainLoop()