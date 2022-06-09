from PySide6.QtWidgets import QApplication, QStyleFactory
import sys
from builtin_modules import LoginApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 启动一个应用
    login_window = LoginApplication()  # 实例化主窗口
    app.setStyle(QStyleFactory.create("Fusion"))  # fusion风格
    login_window.show()  # 展示主窗口
    sys.exit(app.exec())  # 避免程序执行到这一行后直接退出
