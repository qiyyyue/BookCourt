import datetime, time

import wx
from wx import adv
from book_court import Book_Court

class MyFrame(wx.Frame):    #创建自定义Frame
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,id=-1,title="Hello World",size=(380,800)) #设置窗体

        self.init_component()

        self.Center()   #将窗口放在桌面环境的中间

    def init_component(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(5, 5)
        self.panel.SetSizer(self.sizer)

        self.datelabel = wx.StaticText(self.panel, -1, '请选择预定场地的日期:', pos=(20, 25))
        self.datepick = adv.DatePickerCtrl(self.panel, id=-1, size=(160, 40), pos=(200, 20),
                                           style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.datepick.Bind(adv.EVT_DATE_CHANGED, self.OnActionChangeDate)

        self.init_time()
        self.init_choice_box()
        self.addUserBox()

        self.beginBook = wx.Button(self.panel, label='开始预定', pos=(60, 375), size=(100, 40))
        self.beginBook.Bind(wx.EVT_BUTTON, self.OnActionBeginBook)

        self.stopBook = wx.Button(self.panel, label='停止预定', pos=(220, 375), size=(100, 40))
        self.stopBook.Bind(wx.EVT_BUTTON, self.OnActionStopBook)

        self.textLabel = wx.StaticText(self.panel, -1, '输出信息:', pos=(20, 430))

        self.addTimer()

        self.addOutPutText()

    def init_choice_box(self):
        # 最早开始时间
        self.beginTimeLabel = wx.StaticText(self.panel, -1, '可接受的最早开始时间:', pos=(20, 75))
        self.beginTimeChoice = wx.Choice(self.panel, -1, choices=self.time_list, pos=(200, 70), size=(160, 40))
        self.Bind(wx.EVT_CHOICE, self.OnActionChangeBeginTime, self.beginTimeChoice)
        self.beginTimeChoice.SetSelection(0)
        self.beginTime = self.time_list[0]

        # 最晚结束时间
        self.endTimeLabel = wx.StaticText(self.panel, -1, '可接受的最晚结束时间:', pos=(20, 125))
        self.endTimeChoice = wx.Choice(self.panel, -1, choices=self.time_list, pos=(200, 120), size=(160, 40))
        self.Bind(wx.EVT_CHOICE, self.OnActionChangeEndTime, self.endTimeChoice)
        self.endTimeChoice.SetSelection(len(self.time_list) - 1)
        self.endTime = self.time_list[len(self.time_list) - 1]

        # 最短持续时间
        self.minLastTimeLabel = wx.StaticText(self.panel, -1, '可接受的最短持续时间:', pos=(20, 175))
        self.minLastTimeChoice = wx.Choice(self.panel, -1, choices=self.last_list, pos=(200, 170), size=(160, 40))
        self.Bind(wx.EVT_CHOICE, self.OnActionChangeMinLast, self.minLastTimeChoice)
        self.minLastTimeChoice.SetSelection(0)
        self.minLast = self.last_list[0].split()[0]

        # 最长持续时间
        self.maxLastTimeLabel = wx.StaticText(self.panel, -1, '可接受的最长持续时间:', pos=(20, 225))
        self.maxLastTimeChoice = wx.Choice(self.panel, -1, choices=self.last_list, pos=(200, 220), size=(160, 40))
        self.Bind(wx.EVT_CHOICE, self.OnActionChangeMaxLast, self.maxLastTimeChoice)
        self.maxLastTimeChoice.SetSelection(4)
        self.maxLast = self.last_list[4].split()[0]

    def init_time(self):

        date = self.datepick.GetValue()
        self.week_day = date.GetWeekDay()
        self.year = date.GetYear()
        self.month = str(int(date.GetMonth()) + 1)
        self.day = date.GetDay()

        # 根据周几修改选择框选项
        if self.week_day >= 1 and self.week_day <= 5:
            self.time_list = [str(x // 2) + (':00' if x % 2 == 0 else ':30') for x in range(30, 43)]
        else:
            self.time_list = [str(x // 2) + (':00' if x % 2 == 0 else ':30') for x in range(18, 43)]
        self.last_list = [str(x / 2) + ' 小时' for x in range(2, len(self.time_list))]

    def addUserBox(self):
        self.userLabel = wx.StaticText(self.panel, -1, '请输入用户名:', pos=(20, 275))
        self.userText = wx.TextCtrl(self.panel, -1, u'username', pos=(200, 270), size=(160, 40))

        self.pwdLabel = wx.StaticText(self.panel, -1, '请输入密码:', pos=(20, 325))
        # self.showPwd = wx.Button(self.panel, label='显示密码', pos=(140, 327), size=(60, 25))
        # # self.showPwd.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))
        # # self.showPwd.Bind(wx.EVT_BUTTON, self.OnActionShowPwd)
        self.pwdText = wx.TextCtrl(self.panel, -1, u'password', pos=(200, 320), size=(160, 40), style=wx.TE_PASSWORD)

    def addOutPutText(self):
        self.area_text = wx.TextCtrl(self.panel, -1, u'', size=(340, 300), pos=(20, 460), style=(wx.TE_MULTILINE | wx.TE_DONTWRAP))
        self.area_text.SetInsertionPoint(0)

    def testLogIn(self, username, pwd, date):
        bc = Book_Court(username, pwd, date)
        bc.get_cookie()
        return bc.log_in()

    def addTimer(self):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

    def OnTimer(self, event):
        self.processTimer()

    def processTimer(self):
        self.time_now = datetime.datetime.now()
        # print(str(self.time_now.strftime('%Y-%m-%d %H:%M:%S') + '\t' + self.ddl.strftime('%Y-%m-%d %H:%M:%S')))
        if self.ddl <= self.time_now:
            self.area_text.AppendText(str(u'开始尝试预定场地!!!!\n'))
            self.timer.Stop()
            self.bookCourt()
            return
        if (self.ddl - self.time_now).seconds >= 3720:
            self.area_text.AppendText(str(self.time_now.strftime('%Y-%m-%d %H:%M:%S') + ",\twait for timing,\t" + self.ddl.strftime(
                '%Y-%m-%d %H:%M:%S') + '\n'))
            self.area_text.AppendText(str('sleep one hour\n'))
            self.timer.StartOnce(3600 * 1000)
        elif (self.ddl - self.time_now).seconds >= 80:
            self.area_text.AppendText(
                str(self.time_now.strftime('%Y-%m-%d %H:%M:%S') + ",\twait for timing,\t" + self.ddl.strftime(
                    '%Y-%m-%d %H:%M:%S') + '\n'))
            self.area_text.AppendText(str('sleep one miniute\n'))
            self.timer.StartOnce(60 * 1000)
        else:
            self.area_text.AppendText(
                str(self.time_now.strftime('%Y-%m-%d %H:%M:%S') + ",\twait for timing,\t" + self.ddl.strftime(
                    '%Y-%m-%d %H:%M:%S') + '\n'))
            self.area_text.AppendText(str('sleep one seconds\n'))
            self.timer.StartOnce(1 * 1000)

    def bookCourt(self):
        name = self.userText.GetValue()
        password = self.pwdText.GetValue()
        date = datetime.datetime(int(self.year), int(self.month), int(self.day))  # 目标日期

        bc = Book_Court(name, password, date)
        bc.get_cookie()
        bc.log_in()
        bc.get_userId()
        bc.get_court_info()

        # print(date, self.beginTime, self.endTime, self.minLast, self.maxLast)

        res = bc.book_court(start_time=str(self.beginTime), end_time=str(self.endTime), min_time=float(self.minLast), max_time=float(self.maxLast))
        if res['code'] == 0:
            msg = wx.MessageDialog(None, '成功预定场地,开始时间:{},结束时间:{},场地号:{}号'.format(res['msg']['startTime'], res['msg']['endTime'], res['msg']['courtNum']), style=wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()
            msgPay = wx.MessageDialog(None, '请在网页端,订单页面支付.（半小时订单不支付将自动取消.', style=wx.OK | wx.ICON_INFORMATION)
            msgPay.ShowModal()
            msgPay.Destroy()
        elif res['code'] == 1:
            msg = wx.MessageDialog(None, '没有符合要求的场地, 可预定的场地最短持续时常不满足要求!', style=wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()
        elif res['code'] == 2:
            msg = wx.MessageDialog(None, '没有空场可以预定!', style=wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()
        else:
            msg = wx.MessageDialog(None, '预定场地失败,请稍后再试!', style=wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()


    def OnActionShowPwd(self, event):
        self.pwdText.SetDefaultStyle(wx.TE_CENTRE)

        if self.pwdText.GetDefaultStyle() == wx.TE_PASSWORD:

            print(self.pwdText.GetDefaultStyle())

    def OnActionStopBook(self, event):
        self.timer.Stop()
        self.area_text.Clear()
        msg = wx.MessageDialog(None, '停止预定场地！', style=wx.OK | wx.ICON_INFORMATION)
        msg.ShowModal()
        msg.Destroy()

    def OnActionBeginBook(self, event):
        # self.area_text.AppendText(str('开始尝试预定场地\n'))
        name = self.userText.GetValue()
        password = self.pwdText.GetValue()

        self.date = datetime.datetime(int(self.year), int(self.month), int(self.day))  # 目标日期
        self.ddl = self.date + datetime.timedelta(days=-2, hours=18)  # 开放时间

        # test username & pwd
        if not self.testLogIn(name, password, self.date):
            msg = wx.MessageDialog(None, '账号/密码错误', style = wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()
            return

        self.processTimer()


    def OnActionChangeDate(self, event):
        date = self.datepick.GetValue()
        self.week_day = date.GetWeekDay()
        self.year = date.GetYear()
        self.month = str(int(date.GetMonth()) + 1)
        self.day = date.GetDay()

        # 根据周几修改选择框选项
        if self.week_day >= 1 and self.week_day <= 5:
            self.time_list = [str(x // 2) + (':00' if x % 2 == 0 else ':30') for x in range(30, 43)]
        else:
            self.time_list = [str(x // 2) + (':00' if x % 2 == 0 else ':30') for x in range(18, 43)]
        self.last_list = [str(x / 2) + ' 小时' for x in range(2, len(self.time_list))]

        self.init_choice_box()

    def OnActionChangeBeginTime(self, event):
        index = event.GetEventObject().GetSelection()
        self.beginTime = self.time_list[index]
        # print(self.beginTime)

    def OnActionChangeEndTime(self, event):
        index = event.GetEventObject().GetSelection()
        self.endTime = self.time_list[index]
        # print(self.endTime)

    def OnActionChangeMinLast(self, event):
        index = event.GetEventObject().GetSelection()
        self.minLast = self.last_list[index].split()[0]
        # print(self.minLast)

    def OnActionChangeMaxLast(self, event):
        index = event.GetEventObject().GetSelection()
        self.maxLast = self.last_list[index].split()[0]
        # print(self.maxLast)

if __name__ == '__main__':
    app = wx.App()

    frame = MyFrame(None)  # 为顶级窗口
    frame.Show(True)

    app.MainLoop()