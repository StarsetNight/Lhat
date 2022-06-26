import socket
import os.path
import re
import json
import sys
import time
import threading
import hashlib
from typing import Union  # 导入Union类型

# 记得改chatwindow和loginwindow里面的图片资源导入路径再打包

from . import Doc

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyleFactory,
    QMessageBox,
)

from .ui.ChatWindow import Ui_ChatWindow
from .ui.LoginWindow import Ui_LoginWindow

from .ui.Signal import chat_window_signal
from .ui.Signal import login_window_signal
from .ui.Signal import register_window_signal

server_ip: str = ""
server_port: int = 0
username: str = ""
password: str = ""
guest: bool = True
textbox: str = ""  # 用于显示在线用户的列表框
show: int = 1  # 用于判断是开还是关闭列表框
users: list = []  # 在线用户列表
default_chat: str = ""  # 聊天对象，先定义为空，因为不同的服务端，需要的聊天对象不同
chatting_rooms: list = []  # 自己所在的聊天室列表
logable: bool = True  # 定义是否可以记录日志

server_exit_messages: tuple[str, ...] = (
    "你已被管理员踢出服务器。",
    "用户名或密码错误。",
    "请不要重复登录。",
    "该服务器启用了强制用户系统，请使用帐号登录。",
    "该用户名已存在。",
    "你已被管理员封禁。",
)


class LoginApplication(QMainWindow):
    def __init__(self):
        """
        UI窗口初始化
        """
        super().__init__()
        self.ui = Ui_LoginWindow()  # UI类的实例化()
        self.ui.setupUi(self)
        self.band()  # 信号和槽的绑定

        self.login_window_signal = login_window_signal  # 将信号绑定到登录窗口

        self.setWindowTitle(f"Lhat！{Doc.version} - 登录到一个 Lhat！服务器")

        if not os.path.exists("logs/"):
            os.mkdir("logs")
        if not os.path.exists("records/"):
            os.mkdir("records")

    def band(self):
        pass

    @staticmethod
    def processAddress(raw_ip_data: str) -> Union[tuple[str, int], bool]:
        """
        输入原始ipv6 ipv4 域名 解析出ip和端口
        """
        if "." in raw_ip_data or raw_ip_data.startswith("localhost"):  # v4解析 域名解析
            (ip, port, *_) = raw_ip_data.split(
                ":"
            )  # 获取服务器IP和端口
            if not port.isdigit():
                return False
            port = int(port)
            if _:  # 如果输入的不是IP:端口的格式，则报错
                return False
        else:  # v6解析
            (ip, port, *_) = raw_ip_data.split("]")
            port = port[1:]  # 去掉:
            if not port.isdigit():
                return False
            port = int(port)
            ip = ip[1:]  # 去掉[
            if _:  # 如果输入的不是IP:端口的格式，则报错
                return False
        return ip, port

    def onCheckLogin(self):
        """
        其实这个方法并不能真正实现登录，登陆方法都在ChatApplication中实现，这只是在处理登录前的事情罢了。
        """
        global server_ip, server_port, username, password, guest

        raw_ip_data = self.ui.input_box_server_ip_port.toPlainText()
        (server_ip, server_port) = self.processAddress(raw_ip_data)
        if server_ip is False:  # 解析不成功
            QMessageBox.warning(
                self,
                "警告",
                "请输入正确的服务器地址格式：\n[<IPV6地址>]:<外部端口> 或 <IPV4地址> : <外部端口> 或 <域名> : <外部端口>",
                QMessageBox.Yes,
                QMessageBox.Yes,
            )
            self.ui.input_box_server_ip_port.setFocus()
            return

        username = self.ui.input_box_nickname.text()  # 获取用户名
        password = self.ui.input_box_password.text()  # 获取密码
        if not username:  # 如果用户名为空
            dlg = QMessageBox.question(
                self,
                "警告",
                "用户名为空，如果确定，将使用socket地址，\n确认继续吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if str(dlg) == "PySide6.QtWidgets.QMessageBox.StandardButton.Yes":
                self.close()
            else:
                self.ui.input_box_nickname.setFocus()
                return
        elif (
            len(username.encode("utf-8")) > 32 or len(username.encode("utf-8")) < 2
        ):  # 因为TCP会粘包
            QMessageBox.warning(
                self, "警告", "用户名长度不能超过32个字节或少于2个字节。", QMessageBox.Yes, QMessageBox.Yes
            )
            self.ui.input_box_nickname.setFocus()  # 设置焦点
            return
        elif password:
            password = hashlib.md5(password.encode()).hexdigest()  # 对密码进行加密
            guest = False
        if " " in username:
            QMessageBox.warning(
                self,
                "警告",
                "用户名不能包含空格，\n" "将自动替换为下划线。",
                QMessageBox.Yes,
                QMessageBox.Yes,
            )
            username = re.sub(" ", "_", username.strip())
        self.close()
        self.ui.input_box_nickname.setText("")
        self.ui.input_box_server_ip_port.setPlainText("")
        self.ui.input_box_password.setText("")
        chat_window = ChatApplication()  # 销毁登录窗口，启动聊天窗口
        chat_window.show()

    def onRegister(self):  # 注册按钮事件
        # 提交注册信息
        self.setWindowTitle(f"Lhat！{Doc.version} - 正在提交注册信息……")
        reg_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        raw_ip_data = self.ui.input_box_server_ip_port.toPlainText()
        (reg_server_ip, *reg_server_port) = self.processAddress(raw_ip_data)
        if reg_server_ip is False:  # 解析不成功
            QMessageBox.warning(
                self,
                "警告",
                "请输入正确的服务器地址格式：\n[<IPV6地址>]:<外部端口> 或 <IPV4地址> : <外部端口> 或 <域名> : <外部端口>",
                QMessageBox.Yes,
                QMessageBox.Yes,
            )
            self.ui.input_box_server_ip_port.setFocus()
            return

        reg_username = self.ui.input_box_nickname.text()  # 获取用户名
        reg_password = self.ui.input_box_password.text()  # 获取密码
        if not reg_username:  # 如果用户名为空
            dlg = QMessageBox.question(
                self,
                "警告",
                "用户名为空，如果确定，将使用socket地址，\n确认继续吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if str(dlg) == "PySide6.QtWidgets.QMessageBox.StandardButton.Yes":
                self.close()
            else:
                self.ui.input_box_nickname.setFocus()
                return
        if (
            len(reg_username.encode("utf-8")) > 20
            or len(reg_username.encode("utf-8")) < 2
        ):  # 因为TCP会粘包
            QMessageBox.warning(
                self, "警告", "用户名长度不能超过20个字节或少于2个字节。", QMessageBox.Yes, QMessageBox.Yes
            )
            self.ui.input_box_nickname.setFocus()  # 设置焦点
            return
        if reg_password:
            reg_password = hashlib.md5(reg_password.encode()).hexdigest()  # 对密码进行加密
        else:
            QMessageBox.warning(self, "警告", "密码不能为空。", QMessageBox.Yes, QMessageBox.Yes)
            self.ui.input_box_password.setFocus()
            return
        if " " in reg_username:
            QMessageBox.warning(
                self,
                "警告",
                "用户名不能包含空格，\n" "将自动替换为下划线。",
                QMessageBox.Yes,
                QMessageBox.Yes,
            )
            reg_username = re.sub(" ", "_", reg_username.strip())
        reg_connection.connect((reg_server_ip, reg_server_port))  # 连接服务器
        reg_content = {
            "by": None,
            "to": None,
            "type": "REGISTER",
            "time": time.time(),
            "message": f"{reg_username}\r\n{reg_password}",
            "file": None,
        }
        reg_connection.send(json.dumps(reg_content).encode("utf-8"))  # 发送注册信息
        try:
            re_message = reg_connection.recv(64).decode("utf-8")  # 接收服务器的回应
        except ConnectionResetError:
            re_message = "failed"
        if re_message == "successful":
            QMessageBox.information(
                self, "提示", "注册成功，请登录。", QMessageBox.Yes, QMessageBox.Yes
            )
        if re_message == "failed":
            QMessageBox.warning(self, "警告", "注册失败。", QMessageBox.Yes, QMessageBox.Yes)
            self.setWindowTitle(f"Lhat！{Doc.version} - 登录到一个 Lhat！服务器")
            return
        self.ui.input_box_nickname.setText("")
        self.ui.input_box_server_ip_port.setPlainText("")
        self.ui.input_box_password.setText("")
        self.setWindowTitle(f"Lhat！{Doc.version} - 登录到一个 Lhat！服务器")


class ChatApplication(QMainWindow):
    def __init__(self):
        global username  # 用户名是需要在窗口关闭时重新赋值的，所以需要全局变量
        self.receive_thread = None  # 定义接收线程

        super().__init__()
        self.ui = Ui_ChatWindow()  # UI类的实例化()
        self.ui.setupUi(self)
        self.band()  # 信号和槽的绑定

        self.chat_window_signal = chat_window_signal

        self.setWindowTitle(f"欢迎来到Lhat！{Doc.version} - 登录为：{username}")
        self.server_address = (server_ip, int(server_port))  # 服务器地址

        self.connection = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # 创建一个socket对象
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.log(f"{username} 登录了服务器 {server_ip}:{server_port}")
        try:
            self.connection.connect(self.server_address)
        except ValueError:  # 如果端口输入不是数字，则报错
            QMessageBox.critical(self, "错误", "抱歉，地址无效，请输入正确的服务器地址，\n将退回登录界面。")
            self.backLoginWindow()
        except ConnectionError as conn_err:  # 如果连接失败，则报错
            QMessageBox.critical(
                self, "错误", "呜……似乎无法连接到服务器……\n将退回登录界面。\n错误信息：\n" + str(conn_err)
            )
            self.backLoginWindow()
        except socket.gaierror:  # 如果输入的地址无效，则报错
            QMessageBox.critical(self, "错误", "获取地址信息失败，\n将退回登录界面。")
            self.backLoginWindow()
        else:
            if username:
                self.connection.send(
                    self.pack(f"{username}\r\n{password}", None, None, "USER_NAME")
                )  # 发送用户名
            else:
                self.connection.send(
                    self.pack("用户名不存在", None, None, "USER_NAME")
                )  # 发送用户名
                username = server_ip + ":" + server_port

            self.startReceive()  # 创建线程用于接收消息

    def band(self) -> None:
        """绑定信号和槽"""
        chat_window_signal.appendOutPutBox.connect(
            lambda msg: self.ui.output_box_message.append(msg)
        )
        chat_window_signal.setOutPutBox.connect(
            lambda msg: self.ui.output_box_message.setText(msg)
        )
        chat_window_signal.clearOutPutBox.connect(self.ui.output_box_message.clear)

        chat_window_signal.appendInPutBox.connect(
            lambda msg: self.ui.input_box_message.append(msg)
        )
        chat_window_signal.setInPutBox.connect(
            lambda msg: self.ui.input_box_message.setText(msg)
        )
        chat_window_signal.clearInPutBox.connect(self.ui.input_box_message.clear)

        chat_window_signal.appendOnlineUserList.connect(
            lambda msg: self.ui.output_box_online_user.append(msg)
        )
        chat_window_signal.setOnlineUserList.connect(
            lambda msg: self.ui.output_box_online_user.setText(msg)
        )
        chat_window_signal.clearOnlineUserList.connect(
            self.ui.output_box_online_user.clear
        )

    def sendMessage(self) -> None:
        raw_message = self.ui.input_box_message.toPlainText()
        self.send(raw_message)
        chat_window_signal.clearInPutBox.emit()  # 清空输入框

    def startReceive(self) -> None:
        # 你懂的，这是一个线程，用于接收消息，函数呢？在模块里面的函数，可以直接调用，但是要加模块名
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()  # 开始线程接收信息
        self.log("已启动消息接收线程。")

    def triggeredMenubar(self, triggeres) -> None:
        jump_map = {"发送": self.sendMessage, "断开连接": self.onLogoff, "退出": self.onExit}
        jump_map[triggeres.text()]()

    def backLoginWindow(self) -> None:
        global login_window  # 登录窗口实例总是要被覆盖的，所以要全局变量，以便后续开发
        self.close()
        login_window = LoginApplication()
        login_window.show()

    def reConnect(self) -> bool:
        self.chat_window_signal.appendOutPutBox.emit("正在尝试重新连接……<br/>")
        self.log("正在尝试重新连接……")
        self.connection.close()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        try:
            self.connection.connect(self.server_address)
        except ConnectionError:
            self.log("重新连接失败。")
            return False
        else:
            self.log("重新连接成功。")
            return True

    def reLogin(self) -> bool:
        global username
        for try_time in range(3):
            self.chat_window_signal.appendOutPutBox.emit(
                f'<font color="red">[严重错误] 呜……看起来与服务器断开了连接，服务姬正在努力修复呢……</font><br/>'
                f"正在尝试在5秒后重新连接（还剩{3 - try_time}次重连机会）……<br/>"
            )
            self.log("与服务器断开了连接，也许服务端宕机了。")
            if not self.isVisible() and not login_window.isVisible():
                self.log("发生了后台滞留，退出程序。")
                QMessageBox.critical(self, "严重错误", "后台滞留，将自动退出Lhat。")
                sys.exit()
            time.sleep(5)
            if self.reConnect():
                self.chat_window_signal.appendOutPutBox.emit("[提示] 已重新连接！<br/>")
                self.log("重新连接成功！正在重新登录……")
                if username:
                    self.connection.send(
                        self.pack(f"{username}\r\n{password}", None, None, "USER_NAME")
                    )  # 发送用户名
                else:
                    self.connection.send(
                        self.pack("用户名不存在", None, None, "USER_NAME")
                    )  # 发送用户名
                    username = server_ip + ":" + server_port
                return True
            else:
                self.log("重新连接失败，重新尝试中。")
        self.chat_window_signal.appendOutPutBox.emit("[提示] 尝试重连失败，请重新启动程序！<br/>")
        # 如果没有窗口存在，则自动退出
        return False

    def onLogoff(self) -> None:
        dlg = QMessageBox.warning(
            self,
            "警告",
            "你真的要注销登录到本服务器吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if str(dlg) == "PySide6.QtWidgets.QMessageBox.StandardButton.Yes":
            self.connection.close()
            # 强制结束接收线程
            self.backLoginWindow()
        else:
            self.ui.input_box_message.setFocus()
            return

    def onExit(self) -> None:
        dlg = QMessageBox.warning(
            self,
            "警告",
            "你真的要退出Lhat！吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if str(dlg) == "PySide6.QtWidgets.QMessageBox.StandardButton.Yes":
            self.connection.close()
            self.close()
            sys.exit(0)
        else:
            self.ui.input_box_message.setFocus()
            return

    # ==================================================================================================================
    # 四大函数开始

    @staticmethod
    def pack(raw_message: str, send_from, chat_with, message_type, file_name=None):
        """
        打包消息，用于发送
        :param raw_message: 正文消息
        :param send_from: 发送者
        :param chat_with: 聊天对象
        :param message_type: 消息类型
        :param file_name: 文件名，如果不是文件类型，则为None
        """
        message = {
            "by": send_from,
            "to": chat_with,
            "type": message_type,
            "time": time.time(),
            "message": raw_message,
            "file": file_name,
        }  # 先把收集到的信息存储到字典里
        return json.dumps(message).encode("utf-8")  # 再用json打包

    @staticmethod
    def unpack(json_message: str):
        """
        解包消息，用于接收JSON格式的消息
        看不懂message字典对应的东西吗？message_types里面有。

        :param json_message: JSON消息
        :return: 返回的东西有很多，也有可能是报错
        ==================================================
        return返回值大全：
        JSON_MESSAGE_NOT_EOF: 消息不完整
        NOT_JSON_MESSAGE: 不是JSON格式的消息
        MANIFEST_NOT_JSON: 用户名单不是JSON格式
        UNKNOWN_MESSAGE_TYPE: 未知消息类型
        --------------------------------------------------
        FILE_SAVED: 文件保存成功
        <一个列表>: 这是用户名单，有用的
        """
        by_color = "blue"
        try:
            message = json.loads(json_message)  # JSON加载
        except json.decoder.JSONDecodeError:  # 如果加载失败，两种可能，第一种，长消息，第二种，断了。
            return "NOT_JSON_MESSAGE", json_message

        if (
            message["type"] == "TEXT_MESSAGE" or message["type"] == "COLOR_MESSAGE"
        ):  # 如果是纯文本消息
            message_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(message["time"])
            )  # 将时间戳转成日期时间
            if message["by"] == "Server":
                by_color = "red"
            message_body = re.sub("&", "&amp;", message["message"])  # 将&替换成&amp;
            message_body = re.sub(
                r"\t", "&nbsp;&nbsp;&nbsp;&nbsp;", message_body
            )  # 替换tab符
            if message["type"] == "TEXT_MESSAGE":
                message_body = re.sub("<", "&lt;", message_body)  # 替换<
                message_body = re.sub(">", "&gt;", message_body)  # 替换>
                message_body = re.sub(" ", "&nbsp;", message_body)  # 替换空格
            message_body = re.sub(r"\n", "<br/>", message_body)  # 替换换行符
            message_body = (
                f"<font color='{by_color}'>{message['by']}</font> <font color='grey'>[{message_time}]"
                f"</font> : <br/>&nbsp;&nbsp;{message_body}"
            )
            return (
                message["type"],
                message["to"],
                message_body,
                message["by"],
                message["message"],
            )
        elif (
            message["type"] == "USER_MANIFEST"
            or message["type"] == "ROOM_MANIFEST"
            or message["type"] == "MANAGER_LIST"
        ):  # 如果是用户列表
            try:
                manifest = json.loads(message["message"])  # 将用户列表转成列表
                return message["type"], manifest
            except json.decoder.JSONDecodeError:  # 如果转换失败，则返回错误
                return "MANIFEST_NOT_JSON"  # 用户名单不是JSON格式
        elif message["type"] == "DEFAULT_ROOM":
            return message["type"], message["message"]
        else:
            return "UNKNOWN_MESSAGE_TYPE"

    def send(self, raw_message: str):
        """
        发送消息。
        """
        chat_with = default_chat
        color = False
        if not raw_message.strip():  # 如果消息为空，则不发送，strip的作用是去掉首尾空格
            self.chat_window_signal.appendOutPutBox.emit("[提示] 发送的消息不能为空！<br/>")
            return  # 因为无法发送空消息，所以直接返回
        elif raw_message.startswith("//tell "):  # 如果是私聊
            if sys.getsizeof(raw_message) <= 968:  # 经过计算，1024个字节的消息以968个字节为正文差不多可以。
                command_message = raw_message.split(" ")  # 分割完之后，分辨一下是否为命令
                chat_with = command_message[1]
                raw_message = re.sub("^//tell", "[私聊消息] 到", raw_message)  # 命令转正文，使用正则替换
            else:
                self.chat_window_signal.appendOutPutBox.emit(
                    "[提示] 发送的私聊消息长度不能大于968字节！<br/>"
                    "&nbsp;&nbsp;建议不要大于300个汉字或900个英文字母和数字！"
                )  # 私聊消息不能超过1024个字节
        elif raw_message.startswith("//color "):  # 如果是彩色消息
            command_message = raw_message.split(" ")
            raw_message = re.sub(
                r"^//color \w* ", f"<font color={command_message[1]}>", raw_message
            )
            raw_message += "</font>"
            color = True
        elif raw_message.startswith("//help"):  # 如果是帮助请求
            os.system("start notepad help.txt")
            return
        elif raw_message.startswith("//"):  # 如果是命令
            raw_message = re.sub("^//", "", raw_message)
            message = self.pack(raw_message, username, None, "COMMAND")
            self.connection.send(message)
            time.sleep(0.05)
            return
        if not color:
            message = self.pack(raw_message, username, chat_with, "TEXT_MESSAGE")
        else:
            message = self.pack(raw_message, username, chat_with, "COLOR_MESSAGE")
        # 发送消息直到发送完毕
        self.connection.sendall(message)
        time.sleep(0.05)

    def receive(self):
        """
        接收消息，但是得要TCP连接。
        """
        global default_chat, chatting_rooms, username, server_exit_messages  # 这个要引用的是全局变量
        # received_long_data = ''
        if os.path.exists(f"records/chat_{self.server_address}.txt"):
            print("已找到聊天记录文件，正在读取旧服务器聊天记录……")
            threading.Thread(target=self.read_record).start()
        else:
            self.chat_window_signal.appendOutPutBox.emit(
                "哒哒！欢迎来到Lhat聊天室！大家开始聊天吧！<br/>" "更多操作提示请输入 //help 并发送！<br/>"
            )

        while True:
            try:
                received_data = self.connection.recv(1024)  # 接收信息
            except ConnectionResetError as error:  # 如果与服务器断开连接
                self.log(f"与服务器断开了连接，因为{error}")
                if self.reLogin():  # 如果重新连接成功
                    continue
                else:
                    return
            except ConnectionAbortedError:  # 如果与服务器断开连接
                self.log("用户主动断开连接。")
                return
            if not received_data:  # 如果接收到的数据为空，则说明服务器已经关闭
                self.log("因为接收空消息，与服务器断开连接！")
                if self.reLogin():  # 如果重新连接成功
                    continue
                else:
                    return
            if not self.isVisible():
                self.log("退出了接收线程。")
                return
            received_data = received_data.decode("utf-8")
            print(received_data)  # ---
            # if received_long_data:  # 如果有长消息，则尝试读取长消息
            #     message = unpack(received_long_data)  # 解包消息
            # else:
            #     message = unpack(received_data)  # 解包消息
            message = self.unpack(received_data)  # 解包消息
            message_type = message[0]
            if (
                message_type == "TEXT_MESSAGE" or message_type == "COLOR_MESSAGE"
            ):  # 如果是文本消息
                message_body = message[2]
                self.chat_window_signal.appendOutPutBox.emit(message_body + "<br/>")
                if message[3] != "Server":
                    with open(
                        f"records/chat_{self.server_address}.txt", "a", encoding="utf-8"
                    ) as chat_file:
                        chat_file.write(received_data + "\n")
                if message[4] in server_exit_messages and message[3] == "Server":
                    self.chat_window_signal.appendOutPutBox.emit("与服务器断开了连接。<br/>")
                    self.connection.close()
                    return
                # received_long_data = ''  # 正常解包之后，清空长消息

            elif message_type == "USER_MANIFEST":
                message_body = message[1]
                online_users = message_body
                self.chat_window_signal.clearOnlineUserList.emit()
                self.chat_window_signal.appendOnlineUserList.emit(default_chat)
                self.chat_window_signal.appendOnlineUserList.emit(
                    '<font color="#3333FF">====在线用户====</font>'
                )
                for user_index, online_username in enumerate(online_users):
                    # online_username是用于显示在线用户的，不要与username混淆
                    self.chat_window_signal.appendOnlineUserList.emit(
                        str(online_username)
                    )
                # received_long_data = ''  # 正常解包之后，清空长消息

            elif message_type == "MANAGER_LIST":
                if message[1]:
                    self.chat_window_signal.appendOutPutBox.emit("在线的维护者有：<br/>")
                    for manager_index, manager_username in enumerate(message[1]):
                        self.chat_window_signal.appendOutPutBox.emit(
                            f"{manager_index + 1} {manager_username}<br/>"
                        )
                else:
                    self.chat_window_signal.appendOutPutBox.emit("暂无在线的维护者！<br/>")

            elif message_type == "ROOM_MANIFEST":
                chatting_rooms = message[1]
                self.log(f"聊天室列表更新为：{chatting_rooms}")

            # elif message_type == 'FILE_RECV_DATA':
            # file_name = message[1]
            # file_data = message[2]
            # signals.appendOutPutBox.emit('[文件] 锵锵！正在接收文件！<br/>')
            # with open(file_name, 'ab') as chat_file:
            # if isinstance(file_data, str):
            # chat_file.write(file_data.encode('utf-8'))
            # else:
            # chat_file.write(file_data)
            # signals.appendOutPutBox.emit('[文件] 锵锵！文件已接收！<br/>')
            # received_long_data = ''  # 正常解包之后，清空长消息

            elif message_type == "NOT_JSON_MESSAGE":
                self.log(f"服务端发来的消息不是JSON格式，消息内容为：{received_data}")

            elif message_type == "DEFAULT_ROOM":
                default_chat = message[1]
                self.chat_window_signal.appendOutPutBox.emit(
                    f'[提示] 锵锵！已分配至默认聊天室：<font color="blue">{default_chat}</font><br/>'
                )
                self.log(f"已分配至默认聊天室：{default_chat}")

    # ==================================================================================================================
    # 四大函数结束

    def read_record(self):
        """
        读取聊天记录，这个不算入四大函数，因为这是Lhat专有的。
        """
        with open(
            f"records/chat_{self.server_address}.txt", "r", encoding="utf-8"
        ) as f:
            data = "RECORD READ START"
            while data:
                data = f.readline().strip()
                message = self.unpack(data)  # 解包消息
                try:
                    message_body = message[2]
                except IndexError:
                    continue
                self.chat_window_signal.appendOutPutBox.emit(message_body + "<br/>")
        self.chat_window_signal.appendOutPutBox.emit(
            "哒哒！欢迎来到Lhat聊天室！大家开始聊天吧！<br/>" "更多操作提示请输入 //help 并发送！<br/>"
        )

    @staticmethod
    def log(content: str, end="\n", show_time=True):
        """
        日志
        :param content: 日志内容
        :param end: 日志结尾
        :param show_time: 是否显示时间
        :return: 无返回值
        """
        if show_time:
            print(
                f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] {content}',
                end=end,
            )
        else:
            print(content, end=end)
        if logable:
            with open(
                f'logs/lhat{time.strftime("%Y-%m-%d", time.localtime())}.log',
                "a",
                encoding="utf-8",
            ) as f:
                f.write(
                    f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] {content}{end}'
                )


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

if __name__ == "__main__":
    app = QApplication([])  # 启动一个应用
    login_window = LoginApplication()  # 实例化主窗口
    app.setStyle(QStyleFactory.create("Fusion"))  # fusion风格
    login_window.show()  # 展示主窗口
    app.exec()  # 避免程序执行到这一行后直接退出
