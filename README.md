# Lhat 客户端

## 开发说明

**请勿向主分支提交内容！**

很抱歉，因为Visual Studio和Qt6出了问题，一年来我一直没有维护这个项目。等待JetBrains的开源许可证下来后，我才能在CLion上继续工作。项目使用C++和Qt6开发，可以手动构建或直接从Release页面下载成品软件。

## 介绍

欢迎使用Lhat，一个基于Qt6的简易聊天程序。我们的开发理念是安全、简约和实用。

**如何使用：**
- 下载软件即可使用，分为客户端和服务端：
  - 客户端：一个“简单”的聊天客户端。
  - 服务端：一个“简单”的聊天服务器。

## 构建步骤

### 环境要求：
- MSVC 2022编译器
- Qt6（版本：6.4.0）

1. 安装所需的MSVC 2022编译器。
2. 安装Qt6，版本为6.4.0。
3. 按照Qt的配置指南进行配置。
4. 从 [Lhat-Core](https://github.com/3rdBit/Lhat-Core) 下载对应版本的LIB和DLL文件。
5. 下载JSONcpp库文件（LIB文件），项目已包含所需的JSON头文件。
6. 生成项目，然后使用命令 `windeployqt Lhat.exe --no-opengl-sw --no-system-d3d-compiler --no-plugins --release` 完成Qt库文件的补全。

## 下载

欲下载该软件，请访问[发布页面](https://github.com/3rdBit/Lhat-C-Plan/releases)。

## 贡献者名单

- 星夕Starset：[GitHub](https://github.com/StarsetNight), [BiliBili](https://space.bilibili.com/477677552)
- HowieHz：[GitHub](https://github.com/HowieHz), [BiliBili](https://space.bilibili.com/176670190)

## 鸣谢名单

- 一位匿名贡献者：信息未知

**由 3rdBit Studio 提供支持**
