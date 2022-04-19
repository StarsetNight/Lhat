# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RegisterWindow.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QGridLayout, QLabel, QPlainTextEdit,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        if not RegisterWindow.objectName():
            RegisterWindow.setObjectName(u"RegisterWindow")
        RegisterWindow.resize(646, 375)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(RegisterWindow.sizePolicy().hasHeightForWidth())
        RegisterWindow.setSizePolicy(sizePolicy)
        RegisterWindow.setStyleSheet(u"")
        self.gridLayout = QGridLayout(RegisterWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_argee_disargee = QDialogButtonBox(RegisterWindow)
        self.button_argee_disargee.setObjectName(u"button_argee_disargee")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.button_argee_disargee.sizePolicy().hasHeightForWidth())
        self.button_argee_disargee.setSizePolicy(sizePolicy1)
        self.button_argee_disargee.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(18)
        self.button_argee_disargee.setFont(font)
        self.button_argee_disargee.setLayoutDirection(Qt.LeftToRight)
        self.button_argee_disargee.setOrientation(Qt.Horizontal)
        self.button_argee_disargee.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.button_argee_disargee, 3, 1, 1, 1)

        self.static_text_1 = QLabel(RegisterWindow)
        self.static_text_1.setObjectName(u"static_text_1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.static_text_1.sizePolicy().hasHeightForWidth())
        self.static_text_1.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(12)
        self.static_text_1.setFont(font1)

        self.gridLayout.addWidget(self.static_text_1, 0, 0, 1, 2)

        self.input_box_register_server_ip_port = QPlainTextEdit(RegisterWindow)
        self.input_box_register_server_ip_port.setObjectName(u"input_box_register_server_ip_port")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.input_box_register_server_ip_port.sizePolicy().hasHeightForWidth())
        self.input_box_register_server_ip_port.setSizePolicy(sizePolicy3)
        self.input_box_register_server_ip_port.setMaximumSize(QSize(16777215, 90))
        font2 = QFont()
        font2.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font2.setPointSize(14)
        self.input_box_register_server_ip_port.setFont(font2)

        self.gridLayout.addWidget(self.input_box_register_server_ip_port, 1, 0, 1, 3)

        self.static_line = QFrame(RegisterWindow)
        self.static_line.setObjectName(u"static_line")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.static_line.sizePolicy().hasHeightForWidth())
        self.static_line.setSizePolicy(sizePolicy4)
        self.static_line.setFrameShape(QFrame.HLine)
        self.static_line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.static_line, 2, 0, 1, 3)

        self.horizontalSpacer_2 = QSpacerItem(305, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)


        self.retranslateUi(RegisterWindow)
        self.button_argee_disargee.accepted.connect(RegisterWindow.accept)
        self.button_argee_disargee.rejected.connect(RegisterWindow.reject)

        QMetaObject.connectSlotsByName(RegisterWindow)
    # setupUi

    def retranslateUi(self, RegisterWindow):
        RegisterWindow.setWindowTitle(QCoreApplication.translate("RegisterWindow", u"Dialog", None))
        self.static_text_1.setText(QCoreApplication.translate("RegisterWindow", u"\u76ee\u524d\u4ec5\u652f\u6301Sakura Frp\u7684\u5b89\u5168\u8ba4\u8bc1\uff01\n"
"\u6709\u4e9b\u670d\u52a1\u5668\u6709\u53ef\u80fd\u8bbe\u7f6e\u4e86\u5b89\u5168\u9a8c\u8bc1\uff08\u6bd4\u5982Sakura Frp\uff09\uff0c\n"
"\u5bfc\u81f4\u65e0\u6cd5\u8fde\u63a5\uff0c\u6240\u4ee5\uff0c\u5982\u679c\u60a8\u7684\u670d\u52a1\u5668\u65e0\u6cd5\u8fde\u63a5.\n"
"\u8bf7\u5728\u4e0b\u9762\u6587\u672c\u6846\u4e2d\u8f93\u5165\u670d\u52a1\u5668\u7684IP\u5730\u5740\u53ca\u7aef\u53e3:", None))
    # retranslateUi

