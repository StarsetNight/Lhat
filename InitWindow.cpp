#include "InitWindow.h"

const bool logable = true;
string server_ip;
int server_port;
string username, password;
string onlinebox;
string default_chat;
bool guest;
string chatting_rooms[32];
bool session = false;



string subReplace(string resource_str, string sub_str, string new_str)
//替换一个字符串所有的子字符串，直到替换完毕，返回替换后的字符串，原字符串不变
{
    string dst_str = resource_str;
    string::size_type pos = 0;
    while ((pos = dst_str.find(sub_str)) != string::npos)   //替换所有指定子串
    {
        dst_str.replace(pos, sub_str.length(), new_str);
    }
    return dst_str;
}

string trim(string s)
//删除字符串开头和末尾的空格，原字符串不变
{
    if (!s.empty())
    {
        s.erase(0, s.find_first_not_of(" "));
        s.erase(s.find_last_not_of(" ") + 1);
    }
    return s;
}

string lToStringTime(time_t t1, string format)
//通过format参数指定时间格式，并将t1时间戳格式化
{
    time_t t = t1;
    char tmp[64];
    struct tm* timinfo;
    timinfo = localtime(&t);

    strftime(tmp, sizeof(tmp), format.c_str(), timinfo);
    return tmp;
}

bool isIP(string ip)
//判断是否是IPv4地址
{
    std::regex pattern("((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)");
    std::smatch res;
    if (regex_match(ip, res, pattern)) {
        return true;
    }
    return false;
}

string getIP(const char* domain)
//域名解析成IP地址
{
    WSADATA wsd;
    WSAStartup(MAKEWORD(2, 2), &wsd);
    struct hostent* host = gethostbyname(domain);
    WSACleanup();
    if (host == NULL)
        return "";
    return inet_ntoa(*(struct in_addr*)host->h_addr_list[0]);
}

vector<string> split(string str, string pattern)
//分割字符串
{
    string::size_type pos;
    vector<string> result;
    str += pattern;//扩展字符串以方便操作
    int size = str.size();
    for (int i = 0; i < size; i++)
    {
        pos = str.find(pattern, i);
        if (pos < size)
        {
            string s = str.substr(i, pos - i);
            result.push_back(s);
            i = pos + pattern.size() - 1;
        }
    }
    return result;
}

bool isNum(string str)
//判断一个字符串是否为数字
{
    strstream sin;
    sin << str;
    double d;
    char c;
    if (!(sin >> d))
    {
        /*解释：
            sin>>t表示把sin转换成double的变量（其实对于int和float型的都会接收），
            如果转换成功，则值为非0，如果转换不成功就返回为0
        */
        return false;
    }
    if (sin >> c)
    {
        /*解释：
        此部分用于检测错误输入中，数字加字符串的输入形式（例如：34.f），在上面的的部分（sin>>t）
        已经接收并转换了输入的数字部分，在stringstream中相应也会把那一部分给清除，
        此时接收的是.f这部分，所以条件成立，返回false
        */
        return false;
    }
    return true;
}

LoginApplication::LoginApplication(ChatApplication& parent) : QMainWindow()
{
    ui.setupUi(this); //初始化窗口UI
    bind(); //绑定信号槽（其实并没有定义）
    parentWindow = &parent; //把父窗口对象指针赋给登录窗口
}
void LoginApplication::bind() {}
tuple<string, int> LoginApplication::procAddress(string addrData)
//处理地址，返回值为元组，类型为std::string和int
{
    string ip; //临时用
    int port; //临时用
    //意思是，如果在addrData里找到.字符，或找到localhost，则以域名形式或ipv4地址形式处理
    if (addrData.find(".") != addrData.npos || !addrData.rfind("localhost", 0))
    {
        try {
            vector<string> inetData = split(addrData, ":");
            if (inetData.size() != 2) //如果分割出来的长度不是2，那就是有问题！
                return make_tuple("", 0);
            if (!isNum(inetData.at(1))) //如果分割出来的“端口”并不是数字，那就更有问题！
                return make_tuple("", 0);
            ip = inetData.at(0);
            port = stoi(inetData.at(1));

            if (!isIP(ip)) ip = getIP(ip.c_str());
        }
        catch (out_of_range) //如果下标越界，问题大了！
        {
            return make_tuple("", 0);
        }
    }
    else //IPv6解析方式
    {
        try {
            vector<string> inetData = split(addrData, "]");
            if (!isNum(inetData.at(1)))
                return make_tuple("", 0);
            if (inetData.size() > 2)
                return make_tuple("", 0);
            ip = inetData.at(0).substr(1); //去掉[
            port = stoi(inetData.at(1).substr(1)); //去掉:
        }
        catch (out_of_range) //下标越界
        {
            return make_tuple("", 0);
        }
    }
    return make_tuple(ip, port);
}
void LoginApplication::onLogin()
//即使函数名更改，它仍然肩负的是检查登录信息是否符合格式，而不是负责登录。
{
    if (session)
    {
        QMessageBox::StandardButton choice = QMessageBox::question(this, "询问 - 覆盖会话", "当前Lhat已有在线会话，要连接到新的会话，必须断开当前会话，你确定要这么做吗？", QMessageBox::Yes | QMessageBox::No, QMessageBox::No);
        if (choice == QMessageBox::Yes) parentWindow->onLogoff(true);
    }
    string rawAddrData = ui.input_server->text().toStdString();
    tuple<string, int> tmpAddr = procAddress(rawAddrData); //处理地址
    server_ip = std::get<0>(tmpAddr);
    server_port = std::get<1>(tmpAddr);
    if (server_ip == "") //如果处理不成功
    {
        QMessageBox::warning(this, "警告 - 服务器地址格式错误", "请输入正确的服务器地址格式，下述为三种标准格式：\n[<IPV6地址>]:<外部端口>\n<IPV4地址>:<外部端口>\n<域名>:<外部端口>");
        ui.input_server->setFocus();
        return;
    }
    username = ui.input_username->text().toStdString(); //获取用户名
    password = ui.input_password->text().toStdString(); //获取密码
    if (username == "") //如果用户名为空
    {
        QMessageBox::warning(this, "警告 - 用户名为空", "用户名不能为空，请给定一个用户名。");
        ui.input_username->setFocus();
        return;
    }
    else if (username.length() > 32 || username.length() < 2)
    {
        QMessageBox::warning(this, "警告 - 用户名长度不规范", "用户名长度应大于2字节且小于32字节。");
        ui.input_username->setFocus();
        return;
    }
    password = MD5(password).toStr();
    
    close();

    //清空输入内容
    ui.input_username->setText("");
    ui.input_server->setText("");
    ui.input_password->setText("");

    parentWindow->onLogin();
    delete this;
}
void LoginApplication::onRegister()
//用于注册
{
    WSADATA wsd;
    WSAStartup(MAKEWORD(2, 2), &wsd);
    SOCKET regSocket;  //注册用的套接字
    sockaddr_in cAddress;  //地址信息对象
    int status;
    char recvMsg[64];

    setWindowTitle(QString::fromStdString("Lhat - 正在提交注册信息……"));

    string rawAddrData = ui.input_server->text().toStdString();
    auto [server_ip, server_port] = procAddress(rawAddrData);

    if (server_ip == "") //解析错误
    {
        QMessageBox::warning(this, "警告 - 服务器地址格式错误", "请输入正确的服务器地址格式，下述为三种标准格式：\n[<IPV6地址>]:<外部端口>\n<IPV4地址>:<外部端口>\n<域名>:<外部端口>");
        ui.input_server->setFocus();
        return;
    }
    username = ui.input_username->text().toStdString(); //获取用户名
    password = ui.input_password->text().toStdString(); //获取密码
    if (username == "") //如果用户名为空
    {
        QMessageBox::warning(this, "警告 - 用户名为空", "用户名不能为空，请给定一个用户名。");
        ui.input_username->setFocus();
        return;
    }
    else if (username.length() > 32 || username.length() < 2) //用户名长度错误
    {
        QMessageBox::warning(this, "警告 - 用户名长度不规范", "用户名长度应大于2字节且小于32字节。");
        ui.input_username->setFocus();
        return;
    }
    if (username.find(" ") != username.npos) //用户名包含空格
    {
        QMessageBox::warning(this, "警告 - 用户名设置不规范", "用户名不应含有空格，\n同时，我们建议你将用户名严格按照以下格式设置：\n只应出现数字、英文字母、下划线，不应包含其他特殊字符。");
        ui.input_username->setFocus();
        return;
    }
    if (password.empty()) //密码为空
    {
        QMessageBox::warning(this, "警告 - 密码设置不规范", "注册时，不应选用空密码。");
        ui.input_password->setFocus();
        return;
    }
    password = MD5(password).toStr(); //密码转MD5

    cAddress.sin_family = AF_INET;
    cAddress.sin_addr.S_un.S_addr = inet_addr(server_ip.c_str()); //ip地址转32位整数
    cAddress.sin_port = htons(server_port);
    regSocket = socket(AF_INET, SOCK_STREAM, 0);

    status = net::connect(regSocket, (sockaddr*)&cAddress, sizeof(cAddress)); //建立连接
    if (status > 0)
    {
        QString errorMessage = "请检查服务器是否在线，或检查网络连接。错误代码：" + QString::number(WSAGetLastError());
        QMessageBox::critical(this, "错误 - 无法连接服务器", errorMessage);
        return;
    }
    //将注册信息打包成JSON消息格式
    string regContent = pack(username + "\r\n" + password, "", "", "REGISTER");
    net::send(regSocket, regContent.c_str(), regContent.length(), 0);
    status = net::recv(regSocket, recvMsg, 64, 0);
    if (status < 0)
    {
        strcpy(recvMsg, "failed"); //失败，则赋值failed
    }
    if (!strcmp(recvMsg, "successful"))
    {
        QMessageBox::information(this, "提示 - 注册成功", "注册成功，请进行登录！");
    }
    else
    {
        QMessageBox::warning(this, "警告 - 注册并不成功", "服务器拒绝了注册信息，请检查输入格式。");
    }
    setWindowTitle(QString::fromStdString("Lhat - 新会话"));
    closesocket(regSocket);
    WSACleanup(); //清理socket库
}

ChatApplication::ChatApplication() : QMainWindow()
{
    ui.setupUi(this); //初始化UI
    bind();

    //初始化文件系统
    if (_access("logs/", 0) == -1) _mkdir("logs/");
    if (_access("records/", 0) == -1) _mkdir("records/");
    setWindowTitle(QString::fromStdString("Lhat " lhatVersion));

    emit appendOutPutBox("欢迎使用Lhat " lhatVersion "，本软件使用AGPL 3.0许可证。");
}
void ChatApplication::bind()
//自定义信号槽的绑定
{
    connect(this, SIGNAL(appendInPutBox(QString)), this, SLOT(appendIBoxSlot(QString)));
    connect(this, SIGNAL(setInPutBox(QString)), this, SLOT(setIBoxSlot(QString)));
    connect(this, SIGNAL(clearInPutBox()), this, SLOT(clearIBoxSlot()));

    connect(this, SIGNAL(appendOutPutBox(QString)), this, SLOT(appendOBoxSlot(QString)));
    connect(this, SIGNAL(setOutPutBox(QString)), this, SLOT(setOBoxSlot(QString)));
    connect(this, SIGNAL(clearOutPutBox()), this, SLOT(clearOBoxSlot()));

    connect(this, SIGNAL(appendOnlineUserList(QString)), this, SLOT(appendUBoxSlot(QString)));
    connect(this, SIGNAL(setOnlineUserList(QString)), this, SLOT(setUBoxSlot(QString)));
    connect(this, SIGNAL(clearOnlineUserList()), this, SLOT(clearUBoxSlot()));
}
void ChatApplication::sendMessage()
{
    onSend(ui.input_message->toPlainText().toStdString()); //发送消息
    emit clearInPutBox();
}
void ChatApplication::startReceive()
{
    log("已启动消息接收线程。");
    //是，线程启动成员函数必须得这么写：std::thread <线程名>(&<类名>::<成员函数，不带括号>, <对象指针，通常为this>);
    std::thread recvThread(&ChatApplication::onReceive, this);
    recvThread.detach(); //允许后台运行线程
}
void ChatApplication::triggeredMenubar(QAction* triggers)
{
    QString buttonSignal = triggers->text();
    if (buttonSignal == "连接会话")
        onConnect();
    else if (buttonSignal == "会话管理器")
        // TODO onSessionMgr();
        QMessageBox::information(this, "Lhat - 功能未完成", "Lhat会话管理器正在积极开发中！");
    else if (buttonSignal == "断开会话")
        onLogoff(false);
    else if (buttonSignal == "退出Lhat")
        onExit();
    else if (buttonSignal == "关于Lhat")
        onAbout();
}
bool ChatApplication::reConnect()
{
    int disableNagle = 0;

    emit appendOutPutBox("正在尝试重新连接……<br/>");
    log("正在尝试重新连接……");
    closesocket(cSocket);
    cSocket = socket(AF_INET, SOCK_STREAM, 0);
    int status = net::connect(cSocket, (sockaddr*)&cAddress, sizeof(cAddress));
    setsockopt(cSocket, IPPROTO_TCP, TCP_NODELAY, (char*)&disableNagle, sizeof(int)); //禁掉他妈的Nagle
    if (status > 0)
    {
        log("重新连接失败");
        return false;
    }
    log("重新连接成功");
    return true;
}
bool ChatApplication::reLogin()
{
    string loginInformation;
    for (int chanceCount = 0; chanceCount < 3; chanceCount++)
    {
        emit appendOutPutBox("<font color=\"red\">[严重错误] 呜……看起来与服务器断开了连接，服务姬正在努力修复呢……</font><br/>\
            正在尝试在5秒后重新连接（还剩" + QString::fromStdString(std::to_string(3 - chanceCount)) + "次重连机会）……<br/>");
        log("与服务器断开了连接，也许服务端宕机了。");
        Sleep(5000); //延迟5秒
        if (reConnect())
        {
            emit appendOutPutBox("[提示] 已重新连接！<br/>");
            log("重新连接成功！正在重新登录……");
            loginInformation = pack(username + "\r\n" + password, "", "", "USER_NAME");
            send(cSocket, loginInformation.c_str(), loginInformation.length(), 0);
            return true;
        }
        else
            log("重新连接失败，重新尝试中。");
    }
    emit appendOutPutBox("[提示] 尝试重连失败，请重新启动程序！<br/>");
    return false;
}
void ChatApplication::onLogin()
{
    int disableNagle = 0;
    string loginInformation;

    WSAStartup(MAKEWORD(2, 2), &wsd);
    cSocket = socket(AF_INET, SOCK_STREAM, 0);
    cAddress.sin_family = AF_INET;
    cAddress.sin_addr.S_un.S_addr = inet_addr(server_ip.c_str());
    cAddress.sin_port = htons(server_port);

    int status = net::connect(cSocket, (sockaddr*)&cAddress, sizeof(cAddress)); //连接
    setsockopt(cSocket, IPPROTO_TCP, TCP_NODELAY, (char*)&disableNagle, sizeof(int)); //禁掉他妈的Nagle
    log(username + "登录了服务器" + server_ip + ":" + std::to_string(server_port));
    if (status > 0)
    {
        QString errorMessage = "请检查服务器是否在线，或检查网络连接。错误代码：" + WSAGetLastError();
        QMessageBox::critical(this, "错误 - 无法连接服务器", errorMessage);
        return;
    }
    loginInformation = pack(username + "\r\n" + password, "", "", "USER_NAME");
    send(cSocket, loginInformation.c_str(), loginInformation.length(), 0);
    recordPath = "records/chat" + server_ip + "," + std::to_string(server_port) + ".txt";
    startReceive();
    session = true;
}
void ChatApplication::onConnect()
{
    LoginApplication* loginwindow = new LoginApplication(*this);
    loginwindow->show();
}
void ChatApplication::onAbout(){}
void ChatApplication::onManage() {}
void ChatApplication::onTool() {}
void ChatApplication::onLogoff(bool silentMode = true)
{
    QMessageBox::StandardButton choice = QMessageBox::No;
    if (!silentMode) QMessageBox::StandardButton choice = QMessageBox::question(this, "询问 - 断开连接", "你真的要从服务器注销并断开连接吗？", QMessageBox::Yes | QMessageBox::No, QMessageBox::No);
    if (choice == QMessageBox::Yes || silentMode)
    {
        closesocket(cSocket);
        session = false;
        emit appendOutPutBox("会话已断开连接。<br/>");
    }
    else
    {
        ui.input_message->setFocus();
    }
}
void ChatApplication::onExit()
{
    QMessageBox::StandardButton choice = QMessageBox::question(this, "询问 - 退出Lhat", "你真的要退出Lhat吗？", QMessageBox::Yes | QMessageBox::No, QMessageBox::No);
    if (choice == QMessageBox::Yes)
    {
        //如果确定，关闭socket，并退出
        closesocket(cSocket);
        close();
        QApplication::exit();
    }
    else
    {
        ui.input_message->setFocus();
    }
}
void ChatApplication::onSend(string rawMessage)
{
    string message;
    string chatWith = default_chat;
    
    if (trim(rawMessage).empty())
    {
        emit appendOutPutBox("[提示] 发送的消息不能为空！<br/>");
        return;
    }
    else if (!rawMessage.rfind("//tell ", 0))
    {
        vector<string> commandMessage = split(rawMessage, " ");
        chatWith = commandMessage.at(1);
        rawMessage = rawMessage.replace(rawMessage.find("//tell"), 6, "[私聊消息] 到");
    }
    else if (!rawMessage.rfind("//help", 0))
    {
        system("start notepad help.txt");
        return;
    }
    else if (!rawMessage.rfind("//", 0))
    {
        rawMessage = rawMessage.replace(rawMessage.find("//"), 2, "");
        message = pack(rawMessage, username, chatWith, "COMMAND");
        send(cSocket, message.c_str(), message.length(), 0);
        Sleep(50);
        return;
    }
    message = pack(rawMessage, username, chatWith, "TEXT_MESSAGE");
    send(cSocket, message.c_str(), message.length(), 0);
    Sleep(50);
}
void ChatApplication::onReceive()
{
    char recvData[1024]; //接收的数据
    string byColor; //消息发送者的显示颜色
    Json::Value recvJson; //解码的JSON对象
    Json::Value userManifest; //在线用户列表的JSON数组
    string msgType, msgBy, msgTo, msgTime, msgBody;
    string finalMessage; //最终显示到输出框的是以这个字符串为介质
    int status; //接受状态码
    log("消息接收线程启动完毕。");
    if (_access(recordPath.c_str(), 0) == 0)
    {
        log("找到旧聊天记录，正在读取……");
        std::thread readThread(&ChatApplication::readRecord, this);
        readThread.detach();
    }
    else
    {
        emit appendOutPutBox("欢迎来到Lhat聊天室！<br/>更多操作提示请键入//help！<br/>");
    }

    while (1)
    {
        memset(recvData, 0, sizeof(recvData)); //字符数组容易被不完全清理，所以需要手动清理
        status = recv(cSocket, recvData, 1024, 0);

        /*recv函数返回值有三种
        * 1.大于0，代表接收到了消息，接收成功。
        * 2.等于0，代表远程主机未响应。
        * 3.小于0，代表系统级别的错误（比如socket被关闭）。
        */

        if (status == 0)
        {
            log("由于服务器未响应，故断开了连接，代码：" + std::to_string(WSAGetLastError()));
            if (reLogin()) continue;
            else return;
        }
        else if (status < 0)
        {
            log("因为用户主动断开连接或系统错误，接收线程被停止，代码：" + std::to_string(WSAGetLastError()));
            return;
        }
        else if (strlen(recvData) == 0)
        {
            log("因为接收空消息，与服务器断开连接！");
            if (reLogin()) continue;
            else return;
        }

        byColor = "blue";
        recvJson = unpack(recvData);
        msgType = recvJson["type"].asString();
        if (msgType == "NOT_JSON_MESSAGE")
        {
            log("服务端发来的消息不是JSON格式，消息内容为：" + (string)recvData);
            continue;
        }
        msgBody = recvJson["message"].asString();
        msgBy = recvJson["by"].asString();
        msgTo = recvJson["to"].asString();
        //===开始JSON消息解析===-===-===-===-===-===-===-===-===
        if (msgType == "TEXT_MESSAGE" || msgType == "COLOR_MESSAGE")
        {
            msgTime = lToStringTime(recvJson["time"].asDouble(), "%Y-%m-%d %H:%M:%S");
            if (msgBy == "Server")
                byColor = "red";
            msgBody = subReplace(msgBody, "&", "&amp;");
            msgBody = subReplace(msgBody, "\t", "&nbsp;&nbsp;&nbsp;&nbsp;");
            if (msgType == "TEXT_MESSAGE")
            {
                msgBody = subReplace(msgBody, "<", "&lt;");
                msgBody = subReplace(msgBody, ">", "&gt;");
                msgBody = subReplace(msgBody, " ", "&nbsp;");
            }
            msgBody = subReplace(msgBody, "\n", "<br/>");
            finalMessage = "<font color = '" + byColor + "'>" + msgBy + "</font> <font color='grey'>[" + msgTime + "]\
                </font> : <br/>&nbsp;&nbsp;" + msgBody + "<br/>";
            emit appendOutPutBox(QString::fromStdString(finalMessage));
            if (msgBy != "Server")
            {
                std::ofstream recordFile(recordPath, std::ios::app);
                recordFile.write(recvData, strlen(recvData));
                recordFile.close();
            }
        }
        else if (msgType == "USER_MANIFEST")
        {
            userManifest = unpack(msgBody);
            emit clearOnlineUserList();
            emit appendOnlineUserList(QString::fromStdString(default_chat));
            emit appendOnlineUserList("<font color=\"#3333FF\">====在线用户====</font>");
            // 遍历JSON数组，添加用户列表（指针遍历）
            for (Json::Value::iterator it = userManifest.begin(); it != userManifest.end(); it++)
                emit appendOnlineUserList(QString::fromStdString(it->asString()));
        }
        else if (msgType == "MANAGER_LIST")
        {
            if (!msgBody.empty())
            {
                userManifest = unpack(msgBody);
                emit appendOutPutBox("在线的维护者有：<br/>");
                for (Json::Value::iterator it = userManifest.begin(); it != userManifest.end(); it++)
                    emit appendOutPutBox(QString::fromStdString(it->asString() + "<br/>"));
            }
            else
                emit appendOutPutBox("暂无在线的维护者！<br/>");
        }
        else if (msgType == "ROOM_MANIFEST")
        {
            chatting_rooms->clear();
            userManifest = unpack(msgBody);
            for (Json::Value::iterator it = userManifest.begin(); it != userManifest.end(); it++)
                chatting_rooms[it.index()] = it->asString();
            log("聊天室列表已更新。");
        }
        else if (msgType == "DEFAULT_ROOM")
        {
            default_chat = msgBody;
            emit appendOutPutBox(QString::fromStdString("[提示] 锵锵！已分配至默认聊天室：<font color=\"blue\">" + default_chat + "</font><br/>"));
            log("已分配至默认聊天室。");
        }
        else if (msgType == "KICK_NOTICE" && msgBy == "Server")
        {
            emit appendOutPutBox("服务器主动断开了与客户端的连接。原因为：" + QString::fromStdString(msgBody));
            closesocket(cSocket);
            return;
        }
        strcpy(recvData, "\0"); //清空接收的字符
    }
}
void ChatApplication::readRecord()
{
    string msgType, msgBy, msgTo, msgTime, msgBody;
    string finalMessage;
    Json::Value recvJson;
    char msg[1024];
    std::ifstream recordFile(recordPath);
    while (!recordFile.eof())
    {
        recordFile.getline(msg, 1024);
        if (!strcmp(msg, "")) continue;
        recvJson = unpack(msg);
        msgType = recvJson["type"].asString();
        msgBy = recvJson["by"].asString();
        msgTo = recvJson["to"].asString();
        msgTime = lToStringTime(recvJson["time"].asDouble(), "%Y-%m-%d %H:%M:%S");
        msgBody = recvJson["message"].asString();
        msgBody = subReplace(msgBody, "\n", "<br/>");
        finalMessage = "<font color='blue'>" + msgBy + "</font> <font color='grey'>[" + msgTime + "]\
                </font> : <br/>&nbsp;&nbsp;" + msgBody + "<br/>";
        emit appendOutPutBox(QString::fromStdString(finalMessage));
    }
    emit appendOutPutBox("欢迎来到Lhat聊天室！<br/>" "更多操作提示请键入//help！<br/>");
}
void ChatApplication::log(string content)
{
    time_t nowTime = time(0);
    std::cout << "[" << lToStringTime(nowTime, "%Y-%m-%d %H:%M:%S") << "] " << content << std::endl;
    if (logable)
    {
        std::ofstream logFile("logs\\lhat" + lToStringTime(nowTime, "%Y-%m-%d") + ".log", std::ios::app);
        string logContent = "[" + lToStringTime(nowTime, "%Y-%m-%d %H:%M:%S") + "] " + content + "\n";
        logFile.write(logContent.c_str(), logContent.length());
        logFile.close();
    }
}