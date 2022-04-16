# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QWidget)

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName(u"LoginWindow")
        LoginWindow.resize(530, 429)
        self.centralwidget = QWidget(LoginWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.static_text_3 = QLabel(self.centralwidget)
        self.static_text_3.setObjectName(u"static_text_3")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.static_text_3.setFont(font)
        self.static_text_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.static_text_3, 4, 1, 1, 1)

        self.button_register = QPushButton(self.centralwidget)
        self.button_register.setObjectName(u"button_register")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.button_register.sizePolicy().hasHeightForWidth())
        self.button_register.setSizePolicy(sizePolicy)
        self.button_register.setMaximumSize(QSize(16777215, 80))
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.button_register.setFont(font1)

        self.gridLayout.addWidget(self.button_register, 5, 1, 1, 1)

        self.input_box_server_ip_port = QPlainTextEdit(self.centralwidget)
        self.input_box_server_ip_port.setObjectName(u"input_box_server_ip_port")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.input_box_server_ip_port.sizePolicy().hasHeightForWidth())
        self.input_box_server_ip_port.setSizePolicy(sizePolicy1)
        self.input_box_server_ip_port.setMaximumSize(QSize(16777215, 90))
        font2 = QFont()
        font2.setPointSize(14)
        self.input_box_server_ip_port.setFont(font2)

        self.gridLayout.addWidget(self.input_box_server_ip_port, 2, 2, 1, 1)

        self.input_box_nickname = QLineEdit(self.centralwidget)
        self.input_box_nickname.setObjectName(u"input_box_nickname")
        self.input_box_nickname.setFont(font2)

        self.gridLayout.addWidget(self.input_box_nickname, 4, 2, 1, 1)

        self.vSpacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.vSpacer2, 0, 1, 1, 1)

        self.vSpacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.vSpacer1, 6, 2, 1, 1)

        self.hSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.hSpacer2, 2, 0, 1, 1)

        self.static_text_2 = QLabel(self.centralwidget)
        self.static_text_2.setObjectName(u"static_text_2")
        self.static_text_2.setFont(font)
        self.static_text_2.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.static_text_2.setLayoutDirection(Qt.LeftToRight)
        self.static_text_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.static_text_2, 2, 1, 1, 1)

        self.button_login = QPushButton(self.centralwidget)
        self.button_login.setObjectName(u"button_login")
        sizePolicy.setHeightForWidth(self.button_login.sizePolicy().hasHeightForWidth())
        self.button_login.setSizePolicy(sizePolicy)
        self.button_login.setMaximumSize(QSize(16777215, 80))
        self.button_login.setFont(font1)

        self.gridLayout.addWidget(self.button_login, 5, 2, 1, 1)

        self.static_text_1 = QLabel(self.centralwidget)
        self.static_text_1.setObjectName(u"static_text_1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.static_text_1.sizePolicy().hasHeightForWidth())
        self.static_text_1.setSizePolicy(sizePolicy2)
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.static_text_1.setFont(font3)

        self.gridLayout.addWidget(self.static_text_1, 1, 1, 1, 2)

        self.hSpacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.hSpacer1, 2, 3, 1, 1)

        LoginWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(LoginWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 530, 22))
        LoginWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(LoginWindow)
        self.statusbar.setObjectName(u"statusbar")
        LoginWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.input_box_server_ip_port, self.button_login)
        QWidget.setTabOrder(self.button_login, self.button_register)

        self.retranslateUi(LoginWindow)
        self.button_login.clicked.connect(LoginWindow.onLogin)
        self.button_register.clicked.connect(LoginWindow.onRegister)

        QMetaObject.connectSlotsByName(LoginWindow)
    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QCoreApplication.translate("LoginWindow", u"MainWindow", None))
        self.static_text_3.setText(QCoreApplication.translate("LoginWindow", u"\u663e\u793a\u6635\u79f0", None))
        self.button_register.setText(QCoreApplication.translate("LoginWindow", u"\u5b89\u5168\u8ba4\u8bc1", None))
        self.input_box_server_ip_port.setPlainText("")
        self.static_text_2.setText(QCoreApplication.translate("LoginWindow", u"\u670d\u52a1\u5668IP\u53ca\u7aef\u53e3", None))
        self.button_login.setText(QCoreApplication.translate("LoginWindow", u"\u767b\u5f55\u670d\u52a1\u5668", None))
        self.static_text_1.setText(QCoreApplication.translate("LoginWindow", u"\u6b22\u8fce\u6765\u5230Lhat\uff01\u8bf7\u8fde\u63a5\u804a\u5929\u670d\u52a1\u5668\u4ee5\u5f00\u59cb\u4f60\u7684\u804a\u5929\u4e4b\u65c5\uff01\n"
"\u5c0f\u63d0\u793a\uff1a\u5982\u679c\u65e0\u6cd5\u8fde\u63a5\uff0c\u8bf7\u5c1d\u8bd5\u5b89\u5168\u8ba4\u8bc1\uff01", None))
    # retranslateUi

