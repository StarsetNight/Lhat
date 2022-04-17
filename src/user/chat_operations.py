import re
import json

ip = ''
port = ''
user = ''
textbox = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = 'Lhat! Chatting Room'  # 聊天对象


'''
注意：
receive函数里的用json判断用户列表和普通消息是要改的，
所以后续专门改这个东西，还有打包函数。
'''


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


def receive(username, window_object, signals, tips_box):
    """
    接收消息，但是得要TCP连接。
    :param username: 当前接收的用户名
    :param window_object: 窗口对象，内含connection，是TCP连接
    :param signals: 绑定的信号，用于触发方法
    :param tips_box: 对话框
    """
    while True:
        try:
            received_data = window_object.connection.recv(1024)  # 接收信息
        except ConnectionAbortedError or ConnectionResetError or ConnectionRefusedError as conn_err:
            tips_box.critical(window_object, "错误", f'与服务器的连接已中断或无法连接到服务器，\n将退回登录界面。\n'
                                                   f'错误原因：{conn_err}')
            window_object.backLoginWindow()  # 退回登录界面
            return
        received_data = received_data.decode('utf-8')
        print(received_data)  # ---
        try:  # 如果JSON解码成功，则是用户列表
            online_users = json.loads(received_data)
            signals.clearOnlineUserList.emit()
            signals.appendOnlineUserList.emit('Lhat! Chatting Room\n')
            signals.appendOnlineUserList.emit('===在线用户===\n')
            for user_index, online_username in enumerate(online_users):
                # online_username是用于显示在线用户的，不要与username混淆
                signals.appendOnlineUserList.emit(str(online_username))
                # online_users[user_index] + '\n')
            online_users.append('Lhat! Chatting Room')
        except json.decoder.JSONDecodeError:  # 如果JSON解码失败，则说明是普通消息
            received_data = received_data.split(r'\+-*/')
            article = received_data[0]  # 正文
            send_from = received_data[1]  # 发送者
            send_to = received_data[2]  # 接收者
            article = '\n' + article  # 添加换行符
            if send_to == 'Lhat! Chatting Room':  # 群聊
                # if send_from == username:
                #     chat_window_signal.appendOutPutBox.emit(article)
                # else:
                #     chat_window_signal.appendOutPutBox.emit(article)
                signals.appendOutPutBox.emit(article)
            elif send_from == username or send_to == username:  # 私聊
                # if send_from == username:
                #     chat_window_signal.appendOutPutBox.emit(article)
                # else:
                #     chat_window_signal.appendOutPutBox.emit(article)
                signals.appendOutPutBox.emit(article)
