# Lhat专用聊天扩展文件
import rsa


def encrypt(string, pubkey):
    """
    加密函数（文本）
    """
    return rsa.encrypt(string.encode('utf-8'), pubkey)


def decrypt(string, privkey):
    """
    解密函数（文本）
    """
    return rsa.decrypt(string, privkey).decode('utf-8')


def loadPublicKey(key: str):
    """
    加载公钥
    """
    return rsa.PublicKey.load_pkcs1(key)


def loadPrivateKey(key: str):
    """
    加载私钥
    """
    return rsa.PrivateKey.load_pkcs1(key)
