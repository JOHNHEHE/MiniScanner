# MiniScanner
包含多个网络安全中常见功能的系统

## 如何使用
本系统运行在操作系统Microsoft Windows 10上，针对更低版本的Microsoft Windows系统，未经过测试，尚不清楚运行状况。

系统采用JetBrains PyCharm进行编写，版本为Community Edition 2019.2.2 x64，编程语言使用python，版本为3.7.3，对于使用本系统的用户来说，建议使用3.6以上版本python，不支持2.x版本python。同时本系统的系统检测功能使用了nmap模块，该模块的正常运行需要用户安装Nmap，下载完成后请将Nmap安装在D盘，并检查D:/Nmap/目录下有文件nmap.exe（若将Nmap安装在其他路径，请拷贝nmap.exe所在路径，在MiniScanner\venv\Lib\site-packages\nmap\namp.py中的nmap_search_path中添加该路径），Nmap下载地址为：https://nmap.org/

建议在Python IDE上使用本系统，运行MiniScanner.py即可启动本系统，在运行窗口输入提示命令使用相应功能。

## 系统设计
系统功能结构图如下
![](https://img-blog.csdnimg.cn/20200404170437154.png?type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxNzQxNTcz,size_16,color_FFFFFF,t_70#pic_center)
功能具体描述如下：

**a. 主机存活扫描**
用户可以选择输入起始IP地址和终止IP地址，针对区间内所有的IP地址，系统采用基础的ping命令验证对应主机是否存活并打印出结果，结果保存到数据库中。在此基础上，针对用户可能输入的域名进行域名解析后再使用ping命令，并且系统会禁止对敏感域名的扫描。为提高程序运行速度，采用了线程池来执行扫描任务。

**b. 端口扫描**
用户可以选择输入IP地址或者是URL，针对该地址，系统向服务器发送请求建立连接并根据响应报文的特征来判断开放端口与对应服务，打印出开放端口与系统判定的对应服务，结果保存到数据库中。在此基础上，针对扫描到30个以上开放端口的情况，判定为port spoof并停止扫描。为提高程序运行速度，采用了线程池来执行扫描任务。

**c. 系统扫描**
用户可以选择输入IP地址或者是URL，针对该地址，系统基于python-nmap执行扫描并获取报告，提取其中检测到系统以及对应的预计正确率并打印，结果保存到数据库中。

**d. 网页爬取**
用户可以选择输入URL，针对该地址，系统从html页面中爬取邮箱、手机号、IP地址、链接的相关信息，并且针对爬取到的链接网址进行再次爬取，打印出URL和其对应爬取到的信息，结果保存到数据库中。为提高程序运行速度，采用了线程池来执行爬取任务。

## 部分功能展示
![主机存活扫描结果](https://img-blog.csdnimg.cn/20200404171323172.png?type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxNzQxNTcz,size_16,color_FFFFFF,t_70#pic_center)
*主机存活扫描*
![操作系统检测](https://img-blog.csdnimg.cn/2020040417160243.png?type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxNzQxNTcz,size_16,color_FFFFFF,t_70#pic_center)
*系统检测*
![爬取大连理工大学官网](https://img-blog.csdnimg.cn/20200404171711731.png?type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxNzQxNTcz,size_16,color_FFFFFF,t_70#pic_center)
*爬取大连理工大学官网*

## Tips
网络安全涉及到的扫描爬取等行为常常涉及到隐私法律等问题，所以需要谨慎使用。



