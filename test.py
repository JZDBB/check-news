import wx

class CheckSameDialog(wx.Frame):
    def __init__(self, mesg1, mesg2):
        wx.Frame.__init__(self, None, -1, 'Check', size=(700, 520))
        self.list_result = []
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

        self.Time1 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Time1.SetFont(self.font)
        sizer.Add(self.Time1, pos=(1, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.Address1 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Address1.SetFont(self.font)
        sizer.Add(self.Address1, pos=(2, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.gname1 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.gname1.SetFont(self.font)
        sizer.Add(self.gname1, pos=(3, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.type1 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.type1.SetFont(self.font)
        sizer.Add(self.type1, pos=(4, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.total1 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.total1.SetFont(self.font)
        sizer.Add(self.total1, pos=(5, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.nwound1 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nwound1.SetFont(self.font)
        sizer.Add(self.nwound1, pos=(6, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.nkill1 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nkill1.SetFont(self.font)
        sizer.Add(self.nkill1, pos=(7, 2), span=(1, 3), flag=wx.LEFT, border=0)
        self.content1 = wx.TextCtrl(self.panel, value='', style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 100))
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

        self.Time2 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Time2.SetFont(self.font)
        sizer.Add(self.Time2, pos=(1, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.Address2 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.Address2.SetFont(self.font)
        sizer.Add(self.Address2, pos=(2, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.gname2 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.gname2.SetFont(self.font)
        sizer.Add(self.gname2, pos=(3, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.type2 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.type2.SetFont(self.font)
        sizer.Add(self.type2, pos=(4, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.total2 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.total2.SetFont(self.font)
        sizer.Add(self.total2, pos=(5, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.nwound2 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nwound2.SetFont(self.font)
        sizer.Add(self.nwound2, pos=(6, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.nkill2 = wx.TextCtrl(self.panel, value='', size=(200, 20), style=wx.ST_NO_AUTORESIZE)
        self.nkill2.SetFont(self.font)
        sizer.Add(self.nkill2, pos=(7, 7), span=(1, 3), flag=wx.LEFT, border=0)
        self.content2 = wx.TextCtrl(self.panel, value='', style=wx.TE_MULTILINE | wx.TE_READONLY, size=(200, 100))
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
        self.list_result.append(self.mesg1)
        self.list_result.append(self.mesg2)

    def OnClickSave1(self, e):
        pass

    def OnClickSave2(self, e):
        pass

    def returemesg(self):
        return self.list_result



if __name__ == '__main__':
    # app = wx.App()
    # frame = CheckSameDialog([1], [2])
    # frame.Show()
    # app.MainLoop()

    a = '2018.01.01'
    b = a.split('.')[0] + a.split('.')[1] + a.split('.')[2]
    print(b)