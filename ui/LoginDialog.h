/********************************************************************************
** Form generated from reading UI file 'LoginDialog.ui'
**
** Created by: Qt User Interface Compiler version 6.4.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef LOGINDIALOG_H
#define LOGINDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_Dialog
{
public:
    QHBoxLayout *horizontalLayout_2;
    QVBoxLayout *verticalLayout;
    QLabel *label_login;
    QSpacerItem *verticalSpacer;
    QGridLayout *InputArea;
    QLabel *label_username;
    QLineEdit *input_server;
    QLabel *label_server;
    QLabel *label_password;
    QLineEdit *input_password;
    QLineEdit *input_username;
    QSpacerItem *verticalSpacer_2;
    QFrame *line_2;
    QLabel *label_status;
    QHBoxLayout *DialogButtonArea;
    QSpacerItem *horizontalSpacer;
    QPushButton *key_register;
    QPushButton *key_login;
    QPushButton *key_cancel;

    void setupUi(QDialog *Dialog)
    {
        if (Dialog->objectName().isEmpty())
            Dialog->setObjectName("Dialog");
        Dialog->resize(310, 191);
        horizontalLayout_2 = new QHBoxLayout(Dialog);
        horizontalLayout_2->setObjectName("horizontalLayout_2");
        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName("verticalLayout");
        label_login = new QLabel(Dialog);
        label_login->setObjectName("label_login");

        verticalLayout->addWidget(label_login);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer);

        InputArea = new QGridLayout();
        InputArea->setObjectName("InputArea");
        label_username = new QLabel(Dialog);
        label_username->setObjectName("label_username");

        InputArea->addWidget(label_username, 1, 0, 1, 1);

        input_server = new QLineEdit(Dialog);
        input_server->setObjectName("input_server");

        InputArea->addWidget(input_server, 0, 1, 1, 1);

        label_server = new QLabel(Dialog);
        label_server->setObjectName("label_server");

        InputArea->addWidget(label_server, 0, 0, 1, 1);

        label_password = new QLabel(Dialog);
        label_password->setObjectName("label_password");

        InputArea->addWidget(label_password, 2, 0, 1, 1);

        input_password = new QLineEdit(Dialog);
        input_password->setObjectName("input_password");

        InputArea->addWidget(input_password, 2, 1, 1, 1);

        input_username = new QLineEdit(Dialog);
        input_username->setObjectName("input_username");

        InputArea->addWidget(input_username, 1, 1, 1, 1);


        verticalLayout->addLayout(InputArea);

        verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer_2);

        line_2 = new QFrame(Dialog);
        line_2->setObjectName("line_2");
        line_2->setFrameShape(QFrame::HLine);
        line_2->setFrameShadow(QFrame::Sunken);

        verticalLayout->addWidget(line_2);

        label_status = new QLabel(Dialog);
        label_status->setObjectName("label_status");

        verticalLayout->addWidget(label_status);

        DialogButtonArea = new QHBoxLayout();
        DialogButtonArea->setObjectName("DialogButtonArea");
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        DialogButtonArea->addItem(horizontalSpacer);

        key_register = new QPushButton(Dialog);
        key_register->setObjectName("key_register");

        DialogButtonArea->addWidget(key_register);

        key_login = new QPushButton(Dialog);
        key_login->setObjectName("key_login");

        DialogButtonArea->addWidget(key_login);

        key_cancel = new QPushButton(Dialog);
        key_cancel->setObjectName("key_cancel");

        DialogButtonArea->addWidget(key_cancel);


        verticalLayout->addLayout(DialogButtonArea);


        horizontalLayout_2->addLayout(verticalLayout);

        QWidget::setTabOrder(input_server, input_username);
        QWidget::setTabOrder(input_username, input_password);
        QWidget::setTabOrder(input_password, key_login);
        QWidget::setTabOrder(key_login, key_cancel);

        retranslateUi(Dialog);

        QMetaObject::connectSlotsByName(Dialog);
    } // setupUi

    void retranslateUi(QDialog *Dialog)
    {
        Dialog->setWindowTitle(QCoreApplication::translate("Dialog", "Lhat - \346\226\260\344\274\232\350\257\235", nullptr));
        label_login->setText(QCoreApplication::translate("Dialog", "\347\231\273\345\275\225\345\210\260\344\270\200\344\270\252Lhat\346\234\215\345\212\241\345\231\250", nullptr));
        label_username->setText(QCoreApplication::translate("Dialog", "\347\224\250\346\210\267\345\220\215", nullptr));
        label_server->setText(QCoreApplication::translate("Dialog", "\346\234\215\345\212\241\345\231\250\344\270\273\346\234\272", nullptr));
        label_password->setText(QCoreApplication::translate("Dialog", "\345\257\206\347\240\201", nullptr));
        label_status->setText(QCoreApplication::translate("Dialog", "\347\255\211\345\276\205\350\277\233\344\270\200\346\255\245\346\223\215\344\275\234\344\270\255\343\200\202", nullptr));
        key_register->setText(QCoreApplication::translate("Dialog", "\346\263\250\345\206\214", nullptr));
        key_login->setText(QCoreApplication::translate("Dialog", "\347\231\273\345\275\225", nullptr));
        key_cancel->setText(QCoreApplication::translate("Dialog", "\345\217\226\346\266\210", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Dialog: public Ui_Dialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // LOGINDIALOG_H
