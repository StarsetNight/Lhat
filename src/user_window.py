import wx

class LoginWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='登录到一个Lhat！服务器', size=(400, 300))
        panel = wx.Panel(self)
        wx.Frame.SetMinSize(self, size=(400, 300))
        wx.Frame.SetMaxSize(self, size=(400, 300))
        wx.StaticText(panel, label="""\
欢迎来到Lhat！请连接聊天服务器以开始你的聊天之旅！
小提示：如果无法连接，请尝试安全认证！""", pos=(40, 10))
        wx.StaticText(panel, label='IP地址及端口', pos=(40, 60))
        wx.StaticText(panel, label='显示昵称', pos=(40, 100))
        self.entryIP = wx.TextCtrl(panel, pos=(120, 55), size=(200, 25))
        self.entryUser = wx.TextCtrl(panel, pos=(120, 95), size=(200, 25))
        self.loginButton = wx.Button(panel, label='登录服务器', pos=(170, 140), size=(150, 80))
        self.loginRegister = wx.Button(panel, label='安全认证\n某些服务器需要', pos=(40, 140), size=(130, 80))
        self.loginButton.Bind(wx.EVT_BUTTON, self.OnLogin)
        self.loginRegister.Bind(wx.EVT_BUTTON, self.OnRegister)
        self.Center()

    def OnLogin(self, event):
        event.Skip()

    def OnRegister(self, event):
        event.Skip()

class ChatWindow(wx.Frame):
    def __init__(self):
        global user

        wx.Frame.__init__(self, parent=None, title="", size=(400, 300))
        panel = wx.Panel(self)
        self.SetMinSize((400, 300))

        # 快捷键绑定
        key = wx.Menu()
        sendHotkey = key.Append(wx.ID_DEFAULT, u'发送\tCtrl+Enter', u'发送消息')
        Logoff = key.Append(wx.ID_CLOSE, u'断开连接', u'断开与服务器的连接并重新登录')
        Exit = key.Append(wx.ID_EXIT, u'退出', u'退出Lhat！')
        self.Bind(wx.EVT_MENU, self.Send, sendHotkey)
        self.Bind(wx.EVT_MENU, self.OnLogoff, Logoff)
        self.Bind(wx.EVT_MENU, self.OnExit, Exit)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        bar = wx.MenuBar()
        bar.Append(key, u'操作')
        self.SetMenuBar(bar)

        h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        # 消息界面
        self.messageText = wx.TextCtrl(panel, pos=(0, 0), size=(250, 180), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.messageText.AppendText('''\
欢迎进入群聊，大家开始聊天吧!
小技巧：在输入框开头写 //tell <某个人名> 可以私聊！''')
        h_sizer1.Add(self.messageText, 2, wx.ALL | wx.EXPAND)

        # 在线用户栏
        self.onlineUser = wx.TextCtrl(panel, pos=(250, 0), size=(150, 180), style=wx.TE_MULTILINE | wx.TE_READONLY)
        h_sizer1.Add(self.onlineUser, 0, wx.ALL | wx.EXPAND)

        h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # 发送输入框
        self.entryMessage = wx.TextCtrl(panel, pos=(0, 180), size=(300, 60), style=wx.TE_MULTILINE)
        self.entryMessage.SetFocus()
        h_sizer2.Add(self.entryMessage, 2, wx.ALL | wx.EXPAND)
        self.sendButton = wx.Button(panel, label='发送', pos=(300, 180), size=(80, 60))
        self.sendButton.Bind(wx.EVT_BUTTON, self.Send)
        h_sizer2.Add(self.sendButton, 0, wx.ALL | wx.EXPAND)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(h_sizer1, 1, wx.ALL | wx.EXPAND, 1)
        main_sizer.Add(h_sizer2, 1, wx.ALL | wx.EXPAND, 1)

        panel.SetSizer(main_sizer)

        self.Center()

    def Send(self, event):
        event.Skip()

    def OnExit(self, event):
        event.Skip()

    def OnLogoff(self, event):
        event.Skip()