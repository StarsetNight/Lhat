# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChatWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTextBrowser, QTextEdit, QWidget)

class Ui_ChatWindow(object):
    def setupUi(self, ChatWindow):
        if not ChatWindow.objectName():
            ChatWindow.setObjectName(u"ChatWindow")
        ChatWindow.resize(766, 656)
        self.menubar_send = QAction(ChatWindow)
        self.menubar_send.setObjectName(u"menubar_send")
        self.menubar_logoff = QAction(ChatWindow)
        self.menubar_logoff.setObjectName(u"menubar_logoff")
        self.menubar_exit = QAction(ChatWindow)
        self.menubar_exit.setObjectName(u"menubar_exit")
        self.centralwidget = QWidget(ChatWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.hbox2 = QHBoxLayout()
        self.hbox2.setObjectName(u"hbox2")
        self.output_box_message = QTextBrowser(self.centralwidget)
        self.output_box_message.setObjectName(u"output_box_message")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.output_box_message.sizePolicy().hasHeightForWidth())
        self.output_box_message.setSizePolicy(sizePolicy)

        self.hbox2.addWidget(self.output_box_message)

        self.output_box_online_user = QTextBrowser(self.centralwidget)
        self.output_box_online_user.setObjectName(u"output_box_online_user")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(5)
        sizePolicy1.setHeightForWidth(self.output_box_online_user.sizePolicy().hasHeightForWidth())
        self.output_box_online_user.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        self.output_box_online_user.setFont(font)

        self.hbox2.addWidget(self.output_box_online_user)


        self.gridLayout.addLayout(self.hbox2, 0, 0, 1, 1)

        self.hbox1 = QHBoxLayout()
        self.hbox1.setObjectName(u"hbox1")
        self.input_box_message = QTextEdit(self.centralwidget)
        self.input_box_message.setObjectName(u"input_box_message")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.input_box_message.sizePolicy().hasHeightForWidth())
        self.input_box_message.setSizePolicy(sizePolicy2)

        self.hbox1.addWidget(self.input_box_message)

        self.button_send_message = QPushButton(self.centralwidget)
        self.button_send_message.setObjectName(u"button_send_message")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.button_send_message.sizePolicy().hasHeightForWidth())
        self.button_send_message.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(20)
        self.button_send_message.setFont(font1)

        self.hbox1.addWidget(self.button_send_message)


        self.gridLayout.addLayout(self.hbox1, 1, 0, 1, 1)

        ChatWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ChatWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 766, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        ChatWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ChatWindow)
        self.statusbar.setObjectName(u"statusbar")
        ChatWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.menubar_send)
        self.menu.addAction(self.menubar_logoff)
        self.menu.addAction(self.menubar_exit)

        self.retranslateUi(ChatWindow)
        self.button_send_message.clicked.connect(ChatWindow.sendMessage)
        self.menubar.triggered.connect(ChatWindow.triggeredMenubar)

        QMetaObject.connectSlotsByName(ChatWindow)
    # setupUi

    def retranslateUi(self, ChatWindow):
        ChatWindow.setWindowTitle(QCoreApplication.translate("ChatWindow", u"MainWindow", None))
        self.menubar_send.setText(QCoreApplication.translate("ChatWindow", u"\u53d1\u9001", None))
        self.menubar_logoff.setText(QCoreApplication.translate("ChatWindow", u"\u65ad\u5f00\u8fde\u63a5", None))
        self.menubar_exit.setText(QCoreApplication.translate("ChatWindow", u"\u9000\u51fa", None))
        self.button_send_message.setText(QCoreApplication.translate("ChatWindow", u"\u53d1\u9001", None))
        self.menu.setTitle(QCoreApplication.translate("ChatWindow", u"\u64cd\u4f5c", None))
    # retranslateUi

