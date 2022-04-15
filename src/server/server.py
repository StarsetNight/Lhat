import settings
import socket
import threading
import queue
import json  # json.dumps(some)打包   json.loads(some)解包
import os
import os.path
import sys

ip = settings.ip_address
port = settings.network_port

messages = queue.Queue()
users = []  # 0:userName 1:connection
lock = threading.Lock()


def OnOnline():
    online = []
    for new_index in range(len(users)):
        online.append(users[new_index][0])
    return online


class Server(threading.Thread):
    global users, lock

    def __init__(self):  # 构造函数
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        os.chdir(sys.path[0])
        print('Running server on ' + ip + ':' + str(port))
        print('  To change the ip address, \n  please visit settings.py')
        print('Waiting for connection...')

    # 接受来自客户端的用户名，如果用户名为空，使用用户的IP与端口作为用户名。如果用户名出现重复，则在出现的用户名依此加上后缀“2”、“3”、“4”……
    def receive(self, conn, address):  # 接收消息
        user = conn.recv(1024)  # 用户名称
        user = user.decode('utf-8')
        if user == '用户名不存在':
            user = address[0] + ':' + str(address[1])
        tag = 1
        temp = user
        for i in range(len(users)):  # 检验重名，则在重名用户后加数字
            if users[i][0] == user:
                tag = tag + 1
                user = temp + str(tag)
        users.append((user, conn))
        USERS = OnOnline()
        self.Load(USERS, address)
        # 在获取用户名后便会不断地接受用户端发来的消息（即聊天内容），结束后关闭连接。
        try:
            while True:
                message = conn.recv(1024)  # 发送消息
                message = message.decode('utf-8')
                self.Load(message, address)
        # 如果用户断开连接，将该用户从用户列表中删除，然后更新用户列表。
        except Exception as e:
            print(e)
            j = 0  # 用户断开连接
            for man in users:
                if man[0] == user:
                    users.pop(j)  # 服务器段删除退出的用户
                    break
                j = j + 1

            USERS = OnOnline()
            self.Load(USERS, address)
            conn.close()

    # 将地址与数据（需发送给客户端）存入messages队列。
    @staticmethod
    def Load(data, address):
        lock.acquire()
        try:
            messages.put((address, data))
        finally:
            lock.release()

            # 服务端在接受到数据后，会对其进行一些处理然后发送给客户端，如下图，对于聊天内容，服务端直接发送给客户端，而对于用户列表，便由json.dumps处理后发送。

    @staticmethod
    def sendData():  # 发送数据
        while True:
            if not messages.empty():
                message = messages.get()
                if isinstance(message[1], str):
                    for i in range(len(users)):
                        data = ' ' + message[1]
                        users[i][1].send(data.encode('utf-8'))
                        print(data)
                        print('\n')

                if isinstance(message[1], list):
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            users[i][1].send(data.encode('utf-8'))
                        except Exception as e:
                            print(e)

    def run(self):
        self.s.bind((ip, port))
        self.s.listen(5)
        q = threading.Thread(target=self.sendData)
        q.start()
        while True:
            conn, address = self.s.accept()
            print('Connection established: ' + address[0] + ':' + str(address[1]))
            t = threading.Thread(target=self.receive, args=(conn, address))
            t.start()


if __name__ == '__main__':
    server = Server()
    server.start()
