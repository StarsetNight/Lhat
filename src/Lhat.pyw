import socket
import wx
import threading
import json
import sys
import re
import os

ip = ''
port = ''
user = ''
textbox = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = 'Lhat! Chatting Room'  # 聊天对象


class LoginWindow(wx.Frame):
    def __init__(self, parent, id_name):
        wx.Frame.__init__(self, parent=None, title='登录到一个Lhat！服务器', size=(400, 300))
        panel = wx.Panel(self)
        wx.Frame.SetMinSize(self, size=(400, 300))
        wx.Frame.SetMaxSize(self, size=(400, 300))
        wx.StaticText(panel, label='欢迎来到Lhat！请连接聊天服务器以开始你的聊天之旅！\n'
                                   '小提示：如果无法连接，请尝试安全认证！', pos=(40, 10))
        wx.StaticText(panel, label='IP地址及端口', pos=(40, 60))
        wx.StaticText(panel, label='显示昵称', pos=(40, 100))
        self.entryIP = wx.TextCtrl(panel, pos=(120, 55), size=(200, 25))
        self.entryUser = wx.TextCtrl(panel, pos=(120, 95), size=(200, 25))
        self.loginButton = wx.Button(panel, label='登录服务器', pos=(170, 140), size=(150, 80))
        self.loginRegister = wx.Button(panel, label='安全认证\n某些服务器需要', pos=(40, 140), size=(130, 80))
        self.loginButton.Bind(wx.EVT_BUTTON, self.OnLogin)
        self.loginRegister.Bind(wx.EVT_BUTTON, self.OnRegister)

    def OnLogin(self, event):
        global ip, port, user
        try:
            ip, port = self.entryIP.GetValue().split(':')
        except ValueError:
            wx.MessageBox('请输入正确的IP地址格式：\n<IP地址> : <外部端口>')
        user = self.entryUser.GetValue()
        if not user:
            dlg = wx.MessageDialog(self, '用户名为空，如果确定，将使用IP地址\n确认继续吗？',
                                   '警告', wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_NO:
                self.entryUser.SetFocus()
                return
            else:
                dlg.Destroy()
                self.Destroy()
                del dlg, self
        else:
            self.Destroy()
            del self
        chat_window = ChatWindow(parent=None, id_name=-1)
        chat_window.Show()

    def OnRegister(self, event):
        dlg = wx.TextEntryDialog(self, u'有些服务器有可能设置了安全验证（比如Sakura Frp），\n'
                                       u'导致无法连接，所以，如果您的服务器无法连接。\n'
                                       u'请在下面文本框中输入服务器的IP地址及端口:', u'服务器安全验证')
        if dlg.ShowModal() == wx.ID_OK:
            IpPort = dlg.GetValue()
        else:
            dlg.Destroy()
            del dlg
            return
        dlg.Destroy()
        dlg = wx.TextEntryDialog(self, u'如果服务器设置了安全认证，那么肯定有验证密码。\n'
                                       u'如果你被提前告知有密码，那么你应该拥有它。\n'
                                       u'请在下面文本框中输入验证密码:', u'服务器安全验证')
        if dlg.ShowModal() == wx.ID_OK:
            password = dlg.GetValue()
        else:
            dlg.Destroy()
            del dlg
            return
        dlg.Destroy()
        command = 'start /wait auth-guest -u https://' + IpPort + ' -p ' + password
        os.system(command)
        os.system('start /wait authpass_generated.exe')
        os.system('del /f /s /q authpass_generated.exe')


class ChatWindow(wx.Frame):
    def __init__(self, parent, id_name):
        global user

        wx.Frame.__init__(self, parent=None, title='欢迎来到Lhat！聊天室 登录为：' + user, size=(400, 300))
        panel = wx.Panel(self)
        self.SetMinSize((400, 300))
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((ip, int(port)))
        except ValueError:
            wx.MessageBox('非法的IP地址及端口，\n将退回登录界面。')
            self.BackLogin()
            return
        except ConnectionRefusedError as conn_error:
            wx.MessageBox('似乎无法连接到服务器……\n将退回登录界面。\n错误信息：\n' + str(conn_error))
            self.BackLogin()
            return
        if user:
            self.connection.send(user.encode('utf-8'))  # 发送用户名
        else:
            self.connection.send('用户名不存在'.encode('utf-8'))
            user = ip + ':' + port

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
        self.messageText.AppendText('欢迎进入群聊，大家开始聊天吧!\n'
                                    '小技巧：在输入框开头写 //tell <某个人名> 可以私聊！')
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

        self.StartReceive()

    def Send(self, event=None):
        global chat
        raw_message = self.entryMessage.GetValue()
        if raw_message == '':
            self.messageText.AppendText('\n[提示] 发送的消息不能为空！')
            return
        elif raw_message.startswith('//tell'):
            talk_with = raw_message.split(' ')
            chat = talk_with[1]
            raw_message = re.sub('//tell', '[私聊消息] 到', raw_message)
        message = raw_message + r'\+-*/' + user + r'\+-*/' + chat
        chat = 'Lhat! Chatting Room'
        self.connection.send(message.encode('utf-8'))
        self.entryMessage.SetValue('')

    def BackLogin(self):
        global main
        self.Destroy()
        main = LoginWindow(parent=None, id_name=-1)
        main.Show()
        del self

    def OnLogoff(self, event):
        dlg = wx.MessageDialog(self, '你真的要注销登录到本服务器吗？',
                               '警告', wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_NO:
            self.entryMessage.SetFocus()
            return
        else:
            self.connection.close()
            self.BackLogin()

    def OnExit(self, event):
        dlg = wx.MessageDialog(self, '你真的要退出Lhat！吗？',
                               '警告', wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_NO:
            self.entryMessage.SetFocus()
            return
        else:
            self.connection.close()
            dlg.Destroy()
            self.Destroy()
            sys.exit(0)

    def StartReceive(self):
        def receive():
            global uses
            while True:
                try:
                    data = self.connection.recv(1024)
                except ConnectionAbortedError:
                    return
                data = data.decode('utf-8')
                print(data)
                try:
                    uses = json.loads(data)
                    self.onlineUser.SetValue('')
                    self.onlineUser.AppendText('Lhat! Chatting Room\n')
                    self.onlineUser.AppendText('===在线用户===\n')
                    for user_index in range(len(uses)):
                        self.onlineUser.AppendText(uses[user_index] + '\n')
                    users.append('Lhat! Chatting Room')
                except Exception:
                    data = data.split(r'\+-*/')
                    message = data[0]
                    user_name = data[1]
                    chat_with = data[2]
                    message = '\n' + message
                    if chat_with == 'Lhat! Chatting Room':  # 群聊
                        if user_name == user:
                            self.messageText.AppendText(message)
                        else:
                            self.messageText.AppendText(message)
                    elif user_name == user or chat_with == user:  # 私聊
                        if user_name == user:
                            self.messageText.AppendText(message)
                        else:
                            self.messageText.AppendText(message)

        r = threading.Thread(target=receive)
        r.start()  # 开始线程接收信息


if __name__ == '__main__':
    app = wx.App()
    main = LoginWindow(parent=None, id_name=-1)
    main.Show()
    app.MainLoop()
