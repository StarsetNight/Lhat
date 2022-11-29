#include "Lhat.h"

int main(int argc, char* argv[])
{
	QApplication app(argc, argv); //Qt应用程序对象
	LoginApplication loginwindow; //创建登录窗口
	loginwindow.show();
	return app.exec(); //主循环
}