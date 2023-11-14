#ifndef INIT_WINDOW_H
#define INIT_WINDOW_H
#define WIN32_LEAN_AND_MEAN
#include <iostream>
#include <strstream>
#include <tuple> //元组
#include <regex> //正则表达式
#include <Windows.h>
#include <io.h> //主要用到的_access和_mkdir函数
#include <ctime>
#include <fstream>
#include <direct.h> //不清楚为什么include这个头文件……
#include <thread> //多线程
#include <QtWidgets/qmessagebox.h>
#include <QtWidgets/qtreewidget.h>

#define lhatVersion "v2-alpha2-status-update"

namespace net {
#include <WinSock2.h> //socket功能
}

#include "json/json.h" //JSONCPP的头文件
#include "md5/md5.h" //MD5算法

using std::string, std::tuple, std::strstream, std::vector, std::make_tuple, std::out_of_range;

using net::WSAStartup, net::WSACleanup, net::socket, net::sockaddr, net::sockaddr_in,
net::WSADATA, net::SOCKET, net::inet_addr, net::inet_ntoa, net::htons, net::closesocket,
net::setsockopt, net::gethostbyname, net::IPPROTO_TCP, net::WSAGetLastError,
net::send, net::recv, net::hostent, net::in_addr;

#pragma comment(lib, "ws2_32.lib") //socket的库
#pragma comment(lib, "jsoncpp.lib") //json库
#pragma comment(lib, "LhatCore64.lib") //Lhat核心库
#pragma warning(disable:4996)

//pack和unpack函数都来自LhatCore64.lib，引用LhatCore64.dll的符号
//JsonCPP相关函数则引用了jsoncpp.dll的符号

extern string pack(string rawMessage, string chatFrom, string chatWith, string messageType);
extern Json::Value unpack(string jsonString);

#include "ui/LhatWindow.h"
#include "ui/LoginDialog.h"

extern string server_ip; //服务器地址
extern int server_port; //服务器端口
extern string username, password;
extern string onlinebox;  //在线用户列表框的内容
extern string default_chat; //默认聊天室名称
extern bool guest; //是否为访客
extern const bool logable; //是否记录日志
extern string chatting_rooms[32];
extern const string VERSION;
extern bool session; //会话是否在线

class ChatApplication : public QMainWindow
{
	Q_OBJECT
public:
	Ui::LhatWindow ui;
	ChatApplication();
	void bind();
	void startReceive();
	bool reConnect();
	bool reLogin();
	void onLogin();
	void onConnect();
	void onSessionMgr();
	void onAbout();
	void onLogoff(bool silentMode);
	void onExit();
	void onSend(string rawMessage);
	void onReceive();
	void readRecord();
	void log(string content);
signals:
	void appendOutPutBox(QString);
	void setOutPutBox(QString);
	void clearOutPutBox();

	void appendInPutBox(QString);
	void setInPutBox(QString);
	void clearInPutBox();

	void appendOnlineUserList(QString);
	void setOnlineUserList(QString);
	void clearOnlineUserList();
private slots: //由于槽函数必须得在slots声明中，所以不得不添加了这些繁琐的函数
	void appendOBoxSlot(QString content) { ui.output_message->append(content); }
	void setOBoxSlot(QString content) { ui.output_message->setText(content); }
	void clearOBoxSlot() { ui.output_message->clear(); }

	void appendIBoxSlot(QString content) { ui.input_message->appendPlainText(content); }
	void setIBoxSlot(QString content) { ui.input_message->setPlainText(content); }
	void clearIBoxSlot() { ui.input_message->clear(); }
	// TODO 用户列表及服务器状态
	void appendUBoxSlot(QString content);
	void setUBoxSlot(QString content);
	void clearUBoxSlot();

	void sendMessage();
	void triggeredMenubar(QAction* triggers);
	void onManage();
	void onTool();
private:
	WSADATA wsd;
	SOCKET cSocket;  //聊天用的套接字
	sockaddr_in cAddress;  //地址信息对象
	string recordPath; //聊天记录文件存储位置
	std::thread recvThread; //接收线程
};

class LoginApplication : public QMainWindow
{
	Q_OBJECT
public:
	Ui::LoginWindow ui;
	ChatApplication* parentWindow;
	LoginApplication(ChatApplication& parent);
	//private:
	void bind();
	tuple<string, int> procAddress(string addrData);
private slots:
	void onLogin();
	void onRegister();
};

#endif //INIT_WINDOW_H