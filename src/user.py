import socket
import wx
import threading
import json
import sys
import re
import os
import webbrowser

import user_window

ip = ''
port = ''
user = ''
textbox = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = 'Lhat! Chatting Room'  # 聊天对象


class LoginApplication(user_window.LoginWindow):
    def __init__(self):
        super().__init__()

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

        chat_window = ChatApplication()#销毁登录窗口，启动聊天窗口
        chat_window.Show()

    def OnRegister(self, event):  # 安全认证按钮事件
        dlg = wx.TextEntryDialog(self, u'''\
目前仅支持Sakura Frp的安全认证！
有些服务器有可能设置了安全验证（比如Sakura Frp），
导致无法连接，所以，如果您的服务器无法连接.
请在下面文本框中输入服务器的IP地址及端口:''', u'服务器安全验证')
        if dlg.ShowModal() == wx.ID_OK:
            IpPort = dlg.GetValue()
        else:
            dlg.Destroy()
            del dlg
            return
        dlg.Destroy()
        webbrowser.open('https://' + IpPort)  # 打开安全认证网页


class ChatApplication(user_window.ChatWindow):
    def __init__(self):
        global user

        super().__init__()

        self.SetTitle('欢迎来到Lhat！聊天室 登录为：' + user)
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

        self.StartReceive()

    def StartReceive(self):
        r = threading.Thread(target=self.receive)
        r.start()  # 开始线程接收信息

    def receive(self):
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


    def Send(self, event):
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
        main = LoginApplication()
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


if __name__ == '__main__':
    app = wx.App()
    main = LoginApplication()
    main.Show()
    app.MainLoop()
