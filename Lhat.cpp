#include "Lhat.h"

int main(int argc, char* argv[])
{
	QApplication app(argc, argv); //Qt应用程序对象
	ChatApplication *lhatwindow = new ChatApplication; //创建登录窗口
	lhatwindow->show();
	return app.exec(); //主循环
}