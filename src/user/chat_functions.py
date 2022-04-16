# Lhat专用聊天扩展文件
import rsa
import os
import socket
import json


def pack(msg, by, to, kind):
    """
    封装消息
    msg, by, to, kind
    """
    return json.dumps({'msg': msg, 'by': by, 'to': to, 'kind': kind})


def unpack(string):
    """
    解包函数
    """
    return json.loads(string)


def loadall(pubfile, privfile):
    """
    读取RSA公钥和私钥
    """
    with open(pubfile, 'rb') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read())
    with open(privfile, 'rb') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read())
    return pubkey, privkey


def encrypt(string, pubkey):
    """
    加密函数（文本）
    """
    return rsa.encrypt(string.encode(), pubkey)


def decrypt(string, privkey):
    """
    解密函数（文本）
    """
    return rsa.decrypt(string, privkey).decode()


def send_file(server, port, by, to, filename, widget):
    """
    发送文件
    """
    # 创建套接字
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # 连接服务器
        sock.connect((server, port))
        # 首先，告诉服务器文件大小
        sock.send(str(os.path.getsize(filename)).encode())
        widget.append('\n锵锵！文件正在火速奔往服务器！')
        with open(filename, 'rb') as f:
            sock.send(pack(f.read(), by, to, 'FILE_TYPE'))
        widget.append('\n哒哒！文件已经运输完毕！')
