# Lhat专用聊天扩展文件
import rsa


def key_Load(pubfile, privfile):
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
