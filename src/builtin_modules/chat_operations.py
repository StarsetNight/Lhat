import os.path
import re
import json
import sys
import time
import threading

# import os.path

# import crypt_module as crypt

ip = ''
port = ''
user = ''
textbox = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
default_chat = ''  # 聊天对象，先定义为空，因为不同的服务端，需要的聊天对象不同
chatting_rooms = []  # 自己所在的聊天室列表


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
        'by': send_from,
        'to': chat_with,
        'type': message_type,
        'time': time.time(),
        'message': raw_message,
        'file': file_name,
    }  # 先把收集到的信息存储到字典里
    return json.dumps(message).encode('utf-8')  # 再用json打包


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
    by_color = 'blue'
    try:
        message = json.loads(json_message)  # JSON加载
    except json.decoder.JSONDecodeError:  # 如果加载失败，两种可能，第一种，长消息，第二种，断了。
        return 'NOT_JSON_MESSAGE', json_message

    if message['type'] == 'TEXT_MESSAGE' or message['type'] == 'COLOR_MESSAGE':  # 如果是纯文本消息
        message_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(message['time']))  # 将时间戳转成日期时间
        if message['by'] == 'Server':
            by_color = 'red'
        message_body = re.sub('&', '&amp;', message['message'])  # 将&替换成&amp;
        message_body = re.sub(r'\t', '&nbsp;&nbsp;&nbsp;&nbsp;', message_body)  # 替换tab符
        if message['type'] == 'TEXT_MESSAGE':
            message_body = re.sub('<', '&lt;', message_body)  # 替换<
            message_body = re.sub('>', '&gt;', message_body)  # 替换>
        message_body = re.sub(' ', '&nbsp;', message_body)  # 替换空格
        message_body = re.sub(r'\n', '<br/>', message_body)  # 替换换行符
        message_body = f"<font color='{by_color}'>{message['by']}</font> <font color='grey'>[{message_time}]" \
                       f"</font> : <br/>&nbsp;&nbsp;{message_body}"
        return message['type'], message['to'], \
               message_body, message['by']
    elif message['type'] == 'USER_MANIFEST' or \
            message['type'] == 'ROOM_MANIFEST' or \
            message['type'] == 'MANAGER_LIST':  # 如果是用户列表
        try:
            manifest = json.loads(message['message'])  # 将用户列表转成列表
            return message['type'], manifest
        except json.decoder.JSONDecodeError:  # 如果转换失败，则返回错误
            return 'MANIFEST_NOT_JSON'  # 用户名单不是JSON格式
    elif message['type'] == 'DEFAULT_ROOM':
        return message['type'], message['message']
    else:
        return 'UNKNOWN_MESSAGE_TYPE'


def send(connection, raw_message: str, send_from, output_box):
    """
    发送消息，但是得要TCP连接。
    """
    chat_with = default_chat
    color = False
    if not raw_message.strip():  # 如果消息为空，则不发送，strip的作用是去掉首尾空格
        output_box.emit('[提示] 发送的消息不能为空！<br/>')
        return  # 因为无法发送空消息，所以直接返回
    elif raw_message.startswith('//tell '):  # 如果是私聊
        if sys.getsizeof(raw_message) <= 968:  # 经过计算，1024个字节的消息以968个字节为正文差不多可以。
            command_message = raw_message.split(' ')  # 分割完之后，分辨一下是否为命令
            chat_with = command_message[1]
            raw_message = re.sub('^//tell', '[私聊消息] 到', raw_message)  # 命令转正文，使用正则替换
        else:
            output_box.emit('[提示] 发送的私聊消息长度不能大于968字节！<br/>'
                            '&nbsp;&nbsp;建议不要大于300个汉字或900个英文字母和数字！')  # 私聊消息不能超过1024个字节
    elif raw_message.startswith('//color '):  # 如果是彩色消息
        command_message = raw_message.split(' ')
        raw_message = re.sub('^//color .* ', f'<font color={" ".join(command_message[1:])}>', raw_message)
        raw_message += '</font>'
        color = True
    elif raw_message.startswith('//help'):  # 如果是帮助请求
        os.system('notepad help.txt')
        return
    elif raw_message.startswith('//'):  # 如果是命令
        raw_message = re.sub('^//', '', raw_message)
        message = pack(raw_message, send_from, None, 'COMMAND')
        connection.send(message)
        time.sleep(0.05)
        return
    if not color:
        message = pack(raw_message, send_from, chat_with, 'TEXT_MESSAGE')
    else:
        message = pack(raw_message, send_from, chat_with, 'COLOR_MESSAGE')
    # 发送消息直到发送完毕
    connection.sendall(message)
    time.sleep(0.05)


def receive(window_object, signals):
    """
    接收消息，但是得要TCP连接。
    :param window_object: 窗口对象，内含connection，是TCP连接
    :param signals: 绑定的信号，用于触发方法
    """
    global default_chat, chatting_rooms  # 这个要引用的是全局变量
    # received_long_data = ''
    if os.path.exists(f'chat_{window_object.server_address}.txt'):
        print('已找到聊天记录文件，正在读取旧服务器聊天记录……')
        threading.Thread(target=read_record, args=(signals.appendOutPutBox,
                                                   window_object.server_address)).start()
    else:
        signals.appendOutPutBox.emit('哒哒！欢迎来到Lhat聊天室！大家开始聊天吧！<br/>'
                                     '更多操作提示请输入 //help 并发送！<br/>')

    while True:
        try:
            received_data = window_object.connection.recv(1024)  # 接收信息
        except ConnectionError:  # 如果与服务器断开连接
            signals.appendOutPutBox.emit(f'<font color="red">[严重错误] 呜……看起来与服务器断开了连接，服务姬正在努力修复呢……</font><br/>'
                                         f'主人可以试试断开连接并重新登录哦！<br/>')
            return
        received_data = received_data.decode('utf-8')
        print(received_data)  # ---
        # if received_long_data:  # 如果有长消息，则尝试读取长消息
        #     message = unpack(received_long_data)  # 解包消息
        # else:
        #     message = unpack(received_data)  # 解包消息
        message = unpack(received_data)  # 解包消息
        message_type = message[0]
        if message_type == 'TEXT_MESSAGE' or message_type == 'COLOR_MESSAGE':  # 如果是文本消息
            message_body = message[2]
            signals.appendOutPutBox.emit(message_body + '<br/>')
            with open(f'chat_{window_object.server_address}.txt', 'a', encoding='utf-8') as chat_file:
                chat_file.write(received_data + '\n')
            # received_long_data = ''  # 正常解包之后，清空长消息

        elif message_type == 'USER_MANIFEST':
            message_body = message[1]
            online_users = message_body
            signals.clearOnlineUserList.emit()
            signals.appendOnlineUserList.emit(default_chat)
            signals.appendOnlineUserList.emit('<font color="#3333FF">====在线用户====</font>')
            for user_index, online_username in enumerate(online_users):
                # online_username是用于显示在线用户的，不要与username混淆
                signals.appendOnlineUserList.emit(str(online_username))
            # received_long_data = ''  # 正常解包之后，清空长消息

        elif message_type == 'MANAGER_LIST':
            if message[1]:
                signals.appendOutPutBox.emit('在线的维护者有：<br/>')
                for manager_index, manager_username in enumerate(message[1]):
                    signals.appendOutPutBox.emit(f'{manager_index + 1} {manager_username}<br/>')
            else:
                signals.appendOutPutBox.emit('暂无在线的维护者！<br/>')

        elif message_type == 'ROOM_MANIFEST':
            chatting_rooms = message[1]

        elif message_type == 'FILE_RECV_DATA':
            file_name = message[1]
            file_data = message[2]
            signals.appendOutPutBox.emit('[文件] 锵锵！正在接收文件！<br/>')
            with open(file_name, 'ab') as chat_file:
                if isinstance(file_data, str):
                    chat_file.write(file_data.encode('utf-8'))
                else:
                    chat_file.write(file_data)
            signals.appendOutPutBox.emit('[文件] 锵锵！文件已接收！<br/>')
            # received_long_data = ''  # 正常解包之后，清空长消息

        elif message_type == 'NOT_JSON_MESSAGE':
            # 匹配JSON字符串
            # login_message = re.match(r'{"by": null, "to": null, "type": "(.+|[^,])", "time": (.+|[^,]), '
            # r'"message": (.+|[^,}])}', received_data)
            signals.appendOutPutBox.emit('呜……可能登录失败了，重进一下试试？<br/>')

        elif message_type == 'DEFAULT_ROOM':
            default_chat = message[1]
            signals.appendOutPutBox.emit(f'[提示] 锵锵！已分配至默认聊天室：<font color="blue">{default_chat}</font><br/>')


def read_record(output_box, server_address):
    """
    读取聊天记录，这个不算入四大函数，因为这是Lhat专有的。
    :param output_box: 输出框
    :param server_address: 服务器地址
    """
    with open(f'chat_{server_address}.txt', 'r', encoding='utf-8') as f:
        data = 'RECORD READ START'
        while data:
            data = f.readline().strip()
            message = unpack(data)  # 解包消息
            try:
                message_body = message[2]
            except IndexError:
                continue
            output_box.emit(message_body + '<br/>')
    output_box.emit('哒哒！欢迎来到Lhat聊天室！大家开始聊天吧！<br/>'
                    '更多操作提示请输入 //help 并发送！<br/>')
