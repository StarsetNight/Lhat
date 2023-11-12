/********************************************************************************
** Form generated from reading UI file 'LhatWindow.ui'
**
** Created by: Qt User Interface Compiler version 6.4.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef LHATWINDOW_H
#define LHATWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *action_login;
    QAction *action_sessionmgr;
    QAction *action_3;
    QAction *action_Lhat;
    QAction *action_Lhat_2;
    QWidget *centralwidget;
    QHBoxLayout *horizontalLayout_3;
    QHBoxLayout *horizontalLayout_2;
    QTreeWidget *tree_status;
    QFrame *line;
    QVBoxLayout *verticalLayout_2;
    QTextBrowser *content_chat;
    QHBoxLayout *horizontalLayout;
    QPlainTextEdit *input_chat;
    QVBoxLayout *verticalLayout;
    QSpacerItem *verticalSpacer;
    QPushButton *key_send;
    QMenuBar *menubar;
    QMenu *menu;
    QMenu *menu_2;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(800, 500);
        action_login = new QAction(MainWindow);
        action_login->setObjectName("action_login");
        action_sessionmgr = new QAction(MainWindow);
        action_sessionmgr->setObjectName("action_sessionmgr");
        action_3 = new QAction(MainWindow);
        action_3->setObjectName("action_3");
        action_Lhat = new QAction(MainWindow);
        action_Lhat->setObjectName("action_Lhat");
        action_Lhat_2 = new QAction(MainWindow);
        action_Lhat_2->setObjectName("action_Lhat_2");
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        horizontalLayout_3 = new QHBoxLayout(centralwidget);
        horizontalLayout_3->setObjectName("horizontalLayout_3");
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName("horizontalLayout_2");
        tree_status = new QTreeWidget(centralwidget);
        tree_status->headerItem()->setText(0, QString());
        new QTreeWidgetItem(tree_status);
        new QTreeWidgetItem(tree_status);
        new QTreeWidgetItem(tree_status);
        tree_status->setObjectName("tree_status");
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Expanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(tree_status->sizePolicy().hasHeightForWidth());
        tree_status->setSizePolicy(sizePolicy);
        QFont font;
        font.setPointSize(9);
        tree_status->setFont(font);
        tree_status->header()->setVisible(false);

        horizontalLayout_2->addWidget(tree_status);

        line = new QFrame(centralwidget);
        line->setObjectName("line");
        line->setFrameShape(QFrame::VLine);
        line->setFrameShadow(QFrame::Sunken);

        horizontalLayout_2->addWidget(line);

        verticalLayout_2 = new QVBoxLayout();
        verticalLayout_2->setObjectName("verticalLayout_2");
        content_chat = new QTextBrowser(centralwidget);
        content_chat->setObjectName("content_chat");
        QSizePolicy sizePolicy1(QSizePolicy::Expanding, QSizePolicy::Expanding);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(200);
        sizePolicy1.setHeightForWidth(content_chat->sizePolicy().hasHeightForWidth());
        content_chat->setSizePolicy(sizePolicy1);
        QFont font1;
        font1.setPointSize(14);
        content_chat->setFont(font1);
        content_chat->setInputMethodHints(Qt::ImhNone);
        content_chat->setOpenExternalLinks(true);

        verticalLayout_2->addWidget(content_chat);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName("horizontalLayout");
        input_chat = new QPlainTextEdit(centralwidget);
        input_chat->setObjectName("input_chat");
        input_chat->setMaximumSize(QSize(16777215, 109));
        input_chat->setFont(font1);

        horizontalLayout->addWidget(input_chat);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName("verticalLayout");
        verticalSpacer = new QSpacerItem(20, 87, QSizePolicy::Minimum, QSizePolicy::Fixed);

        verticalLayout->addItem(verticalSpacer);

        key_send = new QPushButton(centralwidget);
        key_send->setObjectName("key_send");

        verticalLayout->addWidget(key_send);


        horizontalLayout->addLayout(verticalLayout);


        verticalLayout_2->addLayout(horizontalLayout);


        horizontalLayout_2->addLayout(verticalLayout_2);


        horizontalLayout_3->addLayout(horizontalLayout_2);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 800, 22));
        menu = new QMenu(menubar);
        menu->setObjectName("menu");
        menu_2 = new QMenu(menubar);
        menu_2->setObjectName("menu_2");
        MainWindow->setMenuBar(menubar);
        QWidget::setTabOrder(tree_status, input_chat);
        QWidget::setTabOrder(input_chat, key_send);
        QWidget::setTabOrder(key_send, content_chat);

        menubar->addAction(menu->menuAction());
        menubar->addAction(menu_2->menuAction());
        menu->addAction(action_login);
        menu->addAction(action_sessionmgr);
        menu->addAction(action_3);
        menu->addSeparator();
        menu->addAction(action_Lhat);
        menu_2->addAction(action_Lhat_2);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "Lhat", nullptr));
        action_login->setText(QCoreApplication::translate("MainWindow", "\350\277\236\346\216\245\344\274\232\350\257\235", nullptr));
        action_sessionmgr->setText(QCoreApplication::translate("MainWindow", "\344\274\232\350\257\235\347\256\241\347\220\206\345\231\250", nullptr));
        action_3->setText(QCoreApplication::translate("MainWindow", "\346\226\255\345\274\200\344\274\232\350\257\235", nullptr));
        action_Lhat->setText(QCoreApplication::translate("MainWindow", "\351\200\200\345\207\272Lhat", nullptr));
        action_Lhat_2->setText(QCoreApplication::translate("MainWindow", "\345\205\263\344\272\216Lhat", nullptr));

        const bool __sortingEnabled = tree_status->isSortingEnabled();
        tree_status->setSortingEnabled(false);
        QTreeWidgetItem *___qtreewidgetitem = tree_status->topLevelItem(0);
        ___qtreewidgetitem->setText(0, QCoreApplication::translate("MainWindow", "\344\274\232\350\257\235\344\277\241\346\201\257", nullptr));
        QTreeWidgetItem *___qtreewidgetitem1 = tree_status->topLevelItem(1);
        ___qtreewidgetitem1->setText(0, QCoreApplication::translate("MainWindow", "\350\201\212\345\244\251\345\256\244", nullptr));
        QTreeWidgetItem *___qtreewidgetitem2 = tree_status->topLevelItem(2);
        ___qtreewidgetitem2->setText(0, QCoreApplication::translate("MainWindow", "\346\210\220\345\221\230\345\210\227\350\241\250", nullptr));
        tree_status->setSortingEnabled(__sortingEnabled);

        key_send->setText(QCoreApplication::translate("MainWindow", "\345\217\221\351\200\201", nullptr));
        menu->setTitle(QCoreApplication::translate("MainWindow", "\344\274\232\350\257\235", nullptr));
        menu_2->setTitle(QCoreApplication::translate("MainWindow", "\345\205\263\344\272\216", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // LHATWINDOW_H
