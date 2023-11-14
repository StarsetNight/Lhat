#include "Lhat.h"

int main(int argc, char* argv[])
{
	QApplication app(argc, argv); //Qt应用程序对象
	ChatApplication *lhatwindow = new ChatApplication; //创建登录窗口
	lhatwindow->show();
	lhatwindow->onConnect(); //软件启动后打开登录窗口
	return app.exec(); //主循环
}