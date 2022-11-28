# Lhat C Plan
## 开发说明 DEVELOPING INSTRUCTIONS 
> 不！要！往！main分支里塞东西啊！  
项目基于C++和Qt6开发。  
本项目只含有源代码，所以构建后并不能马上运行，另请参阅[构建说明](## 如何构建 HOW TO BUILD)。  
## 介绍 INTRODUCE  
欢迎使用Lhat，这是一个基于Qt6的简易聊天程序。  
安全、简约、实用，这是我们的开发理念。
> 欢迎使用这款软件！  
> 要使用这款软件，下载它！  
软件分为两部分：客户端和服务端。  
- 客户端：一个“简单”的聊天客户端。  
- 服务端：一个《简单》的聊天服务器。  
## 如何构建 HOW TO BUILD
你需要安装一个msvc2022编译器，这是首先要做的事情。  
接着，安装Qt6，我正在使用的版本是6.4.0。  
配置Qt的教程很多，这里就不详细赘述了。  
然后，从[Lhat消息处理核心](https://github.com/3rdBit/LhatCore)项目中下载对应版本的LIB和DLL文件。  
接着是下载jsoncpp库文件（LIB文件），办法很多，也不详细赘述了。本项目已经自带需要include的JSON头文件。  
最后生成项目就可以了，生成后再用`windeployqt Lhat.exe --no-opengl-sw --no-system-d3d-compiler --no-plugins --release`命令进行Qt库文件补全，构建即为完成。  
## 下载 DOWNLOADS  
欲下载本软件，请访问 [发布页面](https://github.com/3rdBit/Lhat-C-Plan/releases)  
## 贡献者名单 CONTRIBUTORS
- Advanced_Killer: [GitHub](https://github.com/ThirdBlood) 
[BiliBili](https://space.bilibili.com/477677552)  
- HowieHz: [GitHub](https://github.com/HowieHz) 
[BiliBili](https://space.bilibili.com/176670190)
## 鸣谢名单 THANKS
- 一位不愿意透露姓名的人 信息：未知  
**Powered by 3rdBit Studio**  