import socket
import threading
import json
import sys
import re
import webbrowser

import Doc

from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory,QMessageBox,QDialog

from ui.ChatWindow import Ui_ChatWindow
from ui.LoginWindow import Ui_LoginWindow
from ui.RegisterWindow import Ui_RegisterWindow

from ui.Signal import chat_window_signal
from ui.Signal import login_window_signal
from ui.Signal import register_window_signal

ip = ''
port = ''
user = ''
textbox = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = 'Lhat! Chatting Room'  # 聊天对象

#---调试信息专用

class LoginApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()  # UI类的实例化()
        self.ui.setupUi(self)
        self.band()  # 信号和槽的绑定

        self.login_window_signal = login_window_signal

        self.setWindowTitle(f"登录到一个 Lhat！服务器   Lhat！版本{Doc.version}")

    def band(self):
        pass

    def onLogin(self):
        global ip, port, user
        try:
            ip, port = self.ui.input_box_server_ip_port.toPlainText().split(':')
        except ValueError:
            QMessageBox.warning(self,"警告",'请输入正确的IP地址格式：\n<IP地址> : <外部端口>',QMessageBox.Yes,QMessageBox.Yes)
        user = self.ui.input_box_nickname.text()
        if not user:
            dlg = QMessageBox.question(self,"警告","用户名为空，如果确定，将使用IP地址\n确认继续吗？",QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            if str(dlg)=="PySide6.QtWidgets.QMessageBox.StandardButton.Yes":
                self.close()
                #del dlg, self
            else:
                print("no")#---调试信息专用
                self.ui.input_box_nickname.setFocus()
                return

        else:
            self.close()
            #del self

        chat_window = ChatApplication()#销毁登录窗口，启动聊天窗口
        chat_window.show()

    def onRegister(self):  # 安全认证按钮事件
        dlg=RegisterApplication()
        #self.close()
        return dlg.exec()

class RegisterApplication(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RegisterWindow()  # UI类的实例化()
        #self.ui.setupUi(self)
        self.ui.setupUi(self)
        self.band()  # 信号和槽的绑定

        self.setModal(True)

        self.register_window_signal = register_window_signal

        self.setWindowTitle("服务器安全验证")

    def band(self):
        pass

    def accept(self):
        print("accept")#--
        webbrowser.open(f'https://{self.ui.input_box_register_server_ip_port.toPlainText()}')# 打开安全认证网页
        return self.done(0)

    def reject(self):
        print("reject")  # --
        return self.done(0)

class ChatApplication(QMainWindow):
    def __init__(self):
        global user

        super().__init__()
        self.ui = Ui_ChatWindow()  # UI类的实例化()
        self.ui.setupUi(self)
        self.band()  # 信号和槽的绑定

        self.chat_window_signal = chat_window_signal

        self.setWindowTitle(f'欢迎来到Lhat！聊天室 Lhat！版本{Doc.version} 登录为：{user}')

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((ip, int(port)))
        except ValueError:
            QMessageBox.critical(self,"错误",'非法的IP地址及端口，\n将退回登录界面。')
            self.backLoginWindow()
            return
        except ConnectionRefusedError as e:
            QMessageBox.critical(self,"错误",'似乎无法连接到服务器……\n将退回登录界面。\n错误信息：\n' + str(e))
            self.backLoginWindow()
            return
        if user:
            self.connection.send(user.encode('utf-8'))  # 发送用户名
        else:
            self.connection.send('用户名不存在'.encode('utf-8'))
            user = ip + ':' + port

        self.startReceive()

    def band(self):
        chat_window_signal.appendOutPutBox.connect(self.appendOutPut)
        chat_window_signal.setOutPutBox.connect(self.setOutPut)
        chat_window_signal.clearOutPutBox.connect(self.clearOutPut)

        chat_window_signal.appendInPutBox.connect(self.appendInPut)
        chat_window_signal.setInPutBox.connect(self.setInPut)
        chat_window_signal.clearInPutBox.connect(self.clearInPut)

        chat_window_signal.appendOnlineUserList.connect(self.appendOnlineUser)
        chat_window_signal.setOnlineUserList.connect(self.setOnlineUser)
        chat_window_signal.clearOnlineUserList.connect(self.clearOnlineUser)

    def appendOutPut(self, msg: str):
        self.ui.output_box_message.append(msg)

    def clearOutPut(self):
        self.ui.output_box_message.clear()

    def setOutPut(self, msg: str):
        self.ui.output_box_message.setText(msg)

    def appendInPut(self, msg: str):
        self.ui.input_box_message.append(msg)

    def clearInPut(self):
        self.ui.input_box_message.clear()

    def setInPut(self, msg: str):
        self.ui.input_box_message.setText(msg)

    def appendOnlineUser(self, msg: str):
        self.ui.output_box_online_user.append(msg)

    def clearOnlineUser(self):
        self.ui.output_box_online_user.clear()

    def setOnlineUser(self, msg: str):
        self.ui.output_box_online_user.setText(msg)

    def sendMessage(self):
        global chat
        raw_message = self.ui.input_box_message.toPlainText()
        if raw_message == '':
            self.chat_window_signal.appendOutPutBox.emit('\n[提示] 发送的消息不能为空！')
            return
        elif raw_message.startswith('//tell'):
            talk_with = raw_message.split(' ')
            chat = talk_with[1]
            raw_message = re.sub('//tell', '[私聊消息] 到', raw_message)
        message = raw_message + r'\+-*/' + user + r'\+-*/' + chat
        chat = 'Lhat! Chatting Room'
        self.connection.send(message.encode('utf-8'))
        chat_window_signal.clearInPutBox.emit()

    def startReceive(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()  # 开始线程接收信息

    def triggeredMenubar(self,triggeres):
        jump_map = {"发送": self.sendMessage,
                    "断开连接": self.onLogoff,
                    "退出": self.onExit
                    }
        jump_map[triggeres.text()]()


    def receive(self):
        global uses
        while True:
            try:
                data = self.connection.recv(1024)
            except ConnectionAbortedError:
                return
            data = data.decode('utf-8')
            print(data)#---
            try:
                uses = json.loads(data)
                chat_window_signal.clearOnlineUserList.emit()
                chat_window_signal.appendOnlineUserList.emit('Lhat! Chatting Room\n')
                chat_window_signal.appendOnlineUserList.emit('===在线用户===\n')
                for user_index,user in enumerate(uses):
                    chat_window_signal.appendOnlineUserList.emit(str(user))
                    #uses[user_index] + '\n')
                users.append('Lhat! Chatting Room')
            except Exception:
                data = data.split(r'\+-*/')
                message = data[0]
                user_name = data[1]
                chat_with = data[2]
                message = '\n' + message
                if chat_with == 'Lhat! Chatting Room':  # 群聊
                    if user_name == user:
                        chat_window_signal.appendOutPutBox.emit(message)
                    else:
                        chat_window_signal.appendOutPutBox.emit(message)
                elif user_name == user or chat_with == user:  # 私聊
                    if user_name == user:
                        chat_window_signal.appendOutPutBox.emit(message)
                    else:
                        chat_window_signal.appendOutPutBox.emit(message)

    def backLoginWindow(self):
        self.close()
        login_window = LoginApplication()
        login_window.show()
        return login_window.exec(0)
        #这里return会报错，但是删掉这一行就不显示了，所以留着

    def onLogoff(self):
        dlg = QMessageBox.warning(self, "警告", '你真的要注销登录到本服务器吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if str(dlg)=="PySide6.QtWidgets.QMessageBox.StandardButton.Yes":
            self.connection.close()
            self.backLoginWindow()
        else:
            self.ui.input_box_message.setFocus()
            return

    def onExit(self):
        dlg = QMessageBox.warning(self, "警告", '你真的要退出Lhat！吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if str(dlg)=="PySide6.QtWidgets.QMessageBox.StandardButton.Yes":
            self.connection.close()
            dlg.close()
            self.close()
            sys.exit(0)
        else:
            self.ui.input_box_message.setFocus()
            return

"""
勾勾选项是check_为前缀，
输出类output_box_为前缀，
输入类input_box_为前缀，
按钮为button_为前缀，
静态为static_为前缀，
静态文字为static_text_为前缀
菜单栏用menu_bar_为前缀

hello_world 变量全部小写，使用下划线连接
helloWorld 函数(def)和方法使用小驼峰式命名法，首单词字母小写，后面单词字母大写
HelloWorld 类名(Class)、文件名使用帕斯卡命名规则(大驼峰式命名法,每一个单词的首字母都采用大写字母)。
HELLO_WORLD 常量(NEVER_GIVE_UP)全部大写，使用下划线连接单词

"""

if __name__ == '__main__':
    app = QApplication([])  # 启动一个应用
    login_window = LoginApplication()  # 实例化主窗口

    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='PySide6'))
    app.setStyle(QStyleFactory.create("Fusion"))  # fusion风格
    login_window.show()  # 展示主窗口
    app.exec()  # 避免程序执行到这一行后直接退出
