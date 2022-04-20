from PySide6.QtCore import Signal,QObject

class ChatWindowSignal(QObject):
    setOutPutBox = Signal(str)
    clearOutPutBox = Signal()
    appendOutPutBox = Signal(str)
    setInPutBox = Signal(str)
    clearInPutBox = Signal()
    appendInPutBox = Signal(str)
    setOnlineUserList = Signal(str)
    clearOnlineUserList = Signal()
    appendOnlineUserList = Signal(str)
    saveRsaPublicKey = Signal(str)
    saveRsaPrivateKey = Signal(str)

class LoginWindowSignal(QObject):
    setOutPutBox = Signal(str)
    clearOutPutBox = Signal()
    appendOutPutBox = Signal(str)

class RegisterWindoSignal(QObject):
    setOutPutBox = Signal(str)
    clearOutPutBox = Signal()
    appendOutPutBox = Signal(str)

chat_window_signal = ChatWindowSignal()
login_window_signal = LoginWindowSignal()
register_window_signal= RegisterWindoSignal()