import re
import json

ip = ''
port = ''
user = ''
textbox = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = 'Lhat! Chatting Room'  # 聊天对象


def send(connection, raw_message: str, send_from, output_box):
    """
    发送消息，但是得要TCP连接。
    """
    chat_with = 'Lhat! Chatting Room'
    if not raw_message:
        output_box.emit('\n[提示] 发送的消息不能为空！')
        return
    elif raw_message.startswith('//tell'):  # 如果是私聊
        command_message = raw_message.split(' ')  # 分割完之后，分辨一下是否为命令
        chat_with = command_message[1]
        raw_message = re.sub('//tell', '[私聊消息] 到', raw_message)
    message = raw_message + r'\+-*/' + send_from + r'\+-*/' + chat_with  # 打包消息
    connection.send(message.encode('utf-8'))  # 发送消息
