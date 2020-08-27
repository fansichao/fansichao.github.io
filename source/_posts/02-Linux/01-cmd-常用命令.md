---
title: 【*】Linux-常用命令大全
url_path: linux/cmd
tags:
  - linux
categories:
  - linux
description: Linux-常用命令大全
---

## NeedTODO

[数据清洗 -大规模数据清洗的利器 文字解析、文字替换等， 速度远快于 replace](https://flashtext.readthedocs.io/en/latest/)

## 常用命令

### split

split 文件切割软件

```python
# 按照大小切割文件
split -b 10M a.csv  a.csv.
切割后得到
a.csv.aa a.csv.ab

# 字符串分割函数split
str.split(str="", num=string.count(str))
- str :分隔符，默认为空格。
- num :分割次数。
```

### ls 文件长度统计

```bash
# 统计当前文件夹下文件的个数:
ls -l |grep "^-"|wc -l

# 统计当前文件夹下目录的个数:
ls -l |grep "^d"|wc -l

# 统计当前文件夹下文件的个数，包括子文件夹里的 :
ls -lR|grep "^-"|wc -l

# 统计文件夹下目录的个数，包括子文件夹里的:
ls -lR|grep "^d"|wc -l

# 统计输出信息的行数
wc -l
```

### sed

sed 文件替换

```bash
# 在文件的首行插入指定内容：
sed -i "1i#! /bin/sh -" a
执行后，在a文件的第一行插入#! /bin/sh -

# 在文件的指定行（n）插入指定内容：
sed -i "niecho "haha"" a
执行后，在a文件的第n行插入echo "haha"

# 在文件的末尾行插入指定内容：
echo “haha” >> a
执行后，在a文件的末尾行插入haha

# 删除正文首行的#号注释
sed 's/\#//g' /etc/crontab

# 替换文件中字符串
sed -i "s/str1/str2/g" filname

# 删除a.txt中含"abc"的行，但不改变a.txt文件本身，操作之后的结果在终端显示
sed -e '/abc/d'  a.txt  
# 删除a.txt中含"abc"的行，将操作之后的结果保存到a.log
sed -e '/abc/d'  a.txt  > a.log
# 删除含字符串"abc"或“efg"的行，将结果保存到a.log
sed '/abc/d;/efg/d' a.txt > a.log
# 查找多个空格
/\s\+
# 删除第1000行输出  a不变 b删除一条数据
sed -e '/1000/d'  a> b

# 获取第二行到末尾
sed -n '2,$p'  filename > new_filename
# 删除Linux文件重复行
sort -n filename | uniq

# 删除空行 删除空格/回车组成的空行
sed -i '/^ *$/d' file

# 将目录下所有文件 替换字符串
sed -i "s/d3b387c031dd/1000db7324ff/g" `grep "d3b387c031dd" -rl /u01 `

# 替换目录下所有文件 sed和grep搭配使用
sed -i 's/ id="content-main"//g'   ` grep -rl  'content-main' `
```

### rpm

**资源链接:**

- rpm 镜像网：[http://rpmfind.net/](http://rpmfind.net/)

rpm 相关命令

```bash
# 查询包版本
rpm -qa | grep vim
# 安装包
rpm -ivh xxxxx.rpm
# 卸载
rpm -e --nodeps vim-minimal-7.4.629-5.el6_8.1.x86_64

```

### yum

yum 相关命令

```bash
# 安装
yum install  -y vim
# 卸载
yum remove vim
# 重置缓存
yum clean all
yum makecache
#  yum配置目录
 /etc/yum.repos.d/xx.repo
 # 只下载安装包 方法1
yum install yum-plugin-downloadonly -y # centos6之前需要此命令
yum install mysql-server --downloadonly --downloaddir=/data/packages
# 只下载安装包 方法2
yum install yum-utils -y # 专门的下载工具
yum downloader lsof --resolve --destdir=/data/mydepot/ # 默认不会下载对应的依赖文件，需要添加 resolve参数

# 查看可用的rpm包
yum list available 'graphviz*'

# yum 下载 rpm 包
yum install --downloaddir=/tmp/whj/ --downloadonly glibc-devel.i686



1. 获取镜像源： 例如 CentOS-6.6-x4_64-bin-DVD1.iso
2. 清理yum文件： yum clean all
3. 缓存yum文件： yum makecache
4. 挂载镜像： monut -t iso9660 -o loop CentOS-6.6-x4_64-bin-DVD1.iso /iso_mnt  # mount挂载的源不同对应的目录不同
5. 修改配置文件：/etc/yum.repos.d/xxx.repo # 例如 file.repo
[file]
baseurl=file:///iso_mnt/ # 对应目录位置 修改
gpgcheck=1
enabled=1
gpgkey=file:///iso_mnt/RPM-GPG-KEY-CentOS-6  # 对应目录位置 修改
6.清理yum文件&缓存yum文件：yum clean all  && yum makecache

```

### date

```bash
Bash命令定义时间变量

LOG_TIME=`date +%H:%M:%S`

获取前天日期：`date -d -2day +%Y%m%d`
依次类推比如获取10天前的日期：`date -d -10day +%Y%m%d`
或n天前的 `date -d "n days ago" +%y%m%d`
明天：`date -d tomorrow +%y%m%d`
注意以上中间有空格

至于你需要什么样的日期时间格式，就需要应用相关的时间域参数来实现咯
相关时间域如下：
% H 小时（00..23）
% I 小时（01..12）
% k 小时（0..23）
% l 小时（1..12）
% M 分（00..59）
% p 显示出AM或PM
% r 时间（hh：mm：ss AM或PM），12小时
% s 从1970年1月1日00：00：00到目前经历的秒数
% S 秒（00..59）
% T 时间（24小时制）（hh:mm:ss）
% X 显示时间的格式（％H:％M:％S）
% Z 时区 日期域
% a 星期几的简称（ Sun..Sat）
% A 星期几的全称（ Sunday..Saturday）
% b 月的简称（Jan..Dec）
% B 月的全称（January..December）
% c 日期和时间（ Mon Nov 8 14：12：46 CST 1999）
% d 一个月的第几天（01..31）
% D 日期（mm／dd／yy）
% h 和%b选项相同
% j 一年的第几天（001..366）
% m 月（01..12）
% w 一个星期的第几天（0代表星期天）
% W 一年的第几个星期（00..53，星期一为第一天）
% x 显示日期的格式（mm/dd/yy）
% y 年的最后两个数字（ 1999则是99）
% Y 年（例如：1970，1996等）
```

### pip

pip 相关常用命令

```bash
# 搜索包
pip search xlrd
# 查看包版本
pip list
# 生成环境依赖文件
pip freeze > requirement.txt
# 下载安装包 方式1
pip --downloadonly --downloaddir=/tmp/  xlrd
# 下载安装包 方式2 - 会下载对应依赖
pip download xx
# 查看可更新包：
pip list  --outdated --format=columns
# 批量下载并更新：
pip install pip-review
pip-review --local --interactive
# 寻找pip中是否存在此安装包
pip search file
# 查看安装包时安装了哪些文件：
pip show --files SomePackage
# 查看哪些包有更新：
pip show --files SomePackage
# 更新一个软件：
pip install --upgrade SomePackage
# 安装
pip install xlrd
# 卸载
pip uninstall xlrd
```

配置国内 pip 源

```bash
# 配置 国内pip源   ~/.pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com

#豆瓣：https://pypi.douban.com/simple
#中国科学技术大学：https://mirrors.ustc.edu.cn/pypi/web/simple/
#清华大学TUNA：https://pypi.tuna.tsinghua.edu.cn/simple
#https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/
```

其他命令

```bash
# pip安装包 --no-index 不使用requirement.txt的顺序
pip install -r /data/xcdw_pacakages/requirement_rqma.txt --find-link=/data/xcdw_pacakages/packages_sgq--no-index
# 使用豆瓣源下载
pip instal Pillow -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```

```bash


# 该命令可以跳过安装错误的库，继续安装
while read requirement; do pip2 install $requirement; done < requirements.txt
```

### tar

```bash
# 压缩常用命令
tar -zcf xxx.tar.gz xxx_dir_xxx

-v 显示详细的处理文件

# 解压常用命令
tar -zxvf xxx.tar.gz

# 解压 xz 压缩包
tar xvJf  node-v6.10.1-linux-x64.tar.xz
```

### zip/unzip

zip -P qwe123 a.zip -r ssss

```bash
# zip 参数说明

-P 加密
-r 压缩目录

# 压缩并指定目录
zip -r /home/kms/kms.zip /home/kms/server/kms
# 解压并指定目录
unzip /home/kms/kms.zip -d /home/kms/server/kms

```

### alias

```bash
# ~/.bash_profile
alias pip=" pip --trusted-host mirrors.aliyun.com "
```

### wget

wget 参数解释、用法: [https://blog.csdn.net/endall/article/details/1571220](https://blog.csdn.net/endall/article/details/1571220)

```bash
# 做站点镜像
wget xxxx -r -np  下载整个目录，不包含上层目录
```

### grep

grep -r 递归查询子目录
grep -i 查询不区分大小写
grep -n 显示查询出来的文件行号
grep -w 精准匹配
grep -l 只显示（包含文件内容的）文件名

grep -rn xxx . "." 只查询本目录以及其下的目录---公司电脑只有这样才能查询，具体原因，可能是设置了相关权限等

### find

忽略大小写 -iname
find / -iname '_csv_'

```bash
# 查找500M以上的文件
sudo find / -size +500M /swap.img

# 查找整整500M的文件
sudo find / -size 500M

# 查找小于500M的文件
sudo find / -size -500M

# 查找大于100M且小于500M的文件
sudo find / -size -500M -size +100M

其他查找单位
- b 512-byte blocks (this is the default if no suffix is used)
- c bytes
- w two-byte words
- k Kilobytes
- M Megabytes
- G Gigabytes
```

### vim

#### vim 键盘图

![Linux-VIm](https://github.com/fansichao/file/blob/master/picture/Linux%20vi.png?raw=true)

#### vim 使用技巧

vim 使用技巧

```bash
# 全局替换
%s/old/new/g
# 指定行数替换
100,120/old/new/g
# 文字字符
\ 格式化字符，
\r 换行符
/g 全局替换
%s 全局查找
\+ 表重复一次或多次  x+  
/c 确认替换
# 删除文章中的空行
g/^s*$/d
^s*$ ：匹配空行，其中^表示行首，s表示空字符，包括空格和制表符，*重复0到n个前面的字符，$表示行尾。连起来就是匹配只有空字符的行，也就是空行。
/d ：删除该行
# 删除行尾空格：
:%s= *$==
%s全局查找替换
=为%s命令的分隔符，如果把=换为/，则该命令可以写为:%s/ *$//
” *$”, $表示行尾，*匹配前面0个到n个字符，*前面是空格，因此此正则表达式匹配行尾的0个到n个字符。
==，分隔符没有中间没有内容，表示删除匹配空格, 在这里表示删除行尾空格。
# 去掉文件中^M
^M = Ctrl v + Ctrl m


# 删除换行符：
:%s/\n//g
# 将连续的两个空行替换成一个空行：
:%s/\n\n/\r/g
# 删除三行空行：
:%s/^\n\{3}//

# 合并行
命令J使两行合并为一行，同时用空格分隔这两行。
# 替换str为str+回车
回车在vim的输入方法是ctrl+V,会得到^,此时再按回车.会得到^M这个就是回车了
因此把全文件所有str换成str回车的语句是:
: 1,$ s/str/str^M/g
^M用上面的方法输入
1,$表示从1到最后一行,s是switch,g是global

### vim删除包含指定字符串的所有行
:g/something/d   # 删除包含something的所有行
```

#### .vimrc 配置

```bash
set nu
set ts=4     # 设置 长度为四个空格
set expandtab # tab键设置为空格
set paste # 智能粘贴
set shiftwidth # 程序自动缩进
set softtabstop=4/8/16 # tab键为四个空格或者制表符，8为制表符，4为空格，可以同时产生制表符和空格

```

#### vim-set

Vim 中的一些设置

```bash
:set fileformat 设置文件格式
:set endofline 设置文件结束符
:set noendofline 取消文件结束符

:%s/\n//g 删除换行符
:set textwidth 设置行宽
:set textwidth 设置行边距
:join 合并多行J合并两行


```

## 模块命令

### 端口相关

```bash
一、查看哪些端口被打开  netstat -anp
二、关闭端口号:iptables -A INPUT -p tcp --drop 端口号-j DROP
  iptables -A OUTPUT -p tcp --dport 端口号-j DROP
三、打开端口号：iptables -A INPUT -ptcp --dport  端口号-j ACCEPT
四、以下是linux打开端口命令的使用方法。
  nc -lp 23 &(打开23端口，即telnet)
  netstat -an | grep 23 (查看是否打开23端口)
五、linux打开端口命令每一个打开的端口，都需要有相应的监听程序才可以

db2 top，查看db2进程
```

### 文件权限

```bash
文件默认权限 umask
文件隐藏属性 chattr lsatrr
which 查找path下的命令
whereis查找文件 读取数据库。
locate查找文件 快于find 读取数据库，但是存在更新慢导致无法查询的情况。
文件特殊权限 suid sgid sbit
nc -tl 8000
```

### 自启动

```bash
Linux启动时自动执行命令或脚本


方法 #1 - 使用 cron 任务

要求;
1.cron 守护进程必须处于运行状态（通常情况下都会运行）
2. 脚本或 crontab 文件必须包含需要的环境变量

方法 #2 - 使用 /etc/rc.d/rc.local
要点：
1.chmod +x /etc/rc.d/rc.local
2.chmod +x /home/gacanepa/script2.sh
3.在rc.local文件末尾添加需要执行的脚本命令 sh /home/gacanepa/script2.sh
```

## Tips 大全

- **env** 查看当前环境变量
- **history** 查看输入的历史命令
- **chmod** 文件授权 需要一层层授权， 或者 chmod -R xxx 授权其下的所有文件以及文件夹

```
注意：不要拿Decimal和str进行比较，会导致结果完全错误。
注意：字段的格式
```

- **ctrl + w** 回退输入的单词
- **pstree** 进程树
- **time python xxxx** sh 脚本中加 time 执行可以显示执行的时间详细情况
- **nohup time xxx** sh 文件中 使用 nohup 调度多个文件，可以多个文件同时执行，（文件之间不能存在依赖）

**Linux 文件比对**
vimdiff a.txt b.txt # 效果 左右分割 颜色标记显示 (需要安装 vim 包)
diff -wy --suppress-common-lines a.txt b.txt # 效果 左右分割 推荐使用

**查看端口**
netstat -lntp | grep 5000

### Linux 命令去重

```bash
常用命令：sort -u xxx

uniq # 去重重复连续出现的记录
sort -u 等价于 sort xxx | uniq

# 删除Linux文件重复行
sort -n test.txt | uniq
```

### 删除用户数据

userdel -r xxx # 完全删除用户
userdel xxx # 只能删除部分用户，像/home/xxx 等需要手动删除
Linux 去重

### Linux 查看当前占用 CPU 或内存最多的几个进程：

```bash
1. ps命令
    1. ps -aux | sort -k4nr | head -10
2. top工具
    1. top之后，大写M，按照内存倒序排序
    2. top之后，大写C，按照CPU倒序排序
3. ps -aux | sort -k4,4n

```

切换用户运行 sh 脚本
su - fdm -c "Command"

### 电源关机

poweroff
reboot
shutdown

### Linux 登录或注销时执行脚本

分别使用~.bash_profile 和 ~.bash_logout 可以做到

### tailf、tail -f、tail -F 三者区别

```bash
tail -f      等同于--follow=descriptor，根据文件描述符进行追踪，当文件改名或被删除，追踪停止
tail -F     等同于--follow=name  --retry，根据文件名进行追踪，并保持重试，即该文件被删除或改名后，如果再次创建相同的文件名，会继续追踪
tailf        等同于tail -f -n 10（貌似tail -f或-F默认也是打印最后10行，然后追踪文件），与tail -f不同的是，如果文件不增长，它不会去访问磁盘文件，所以tailf特别适合那些便携机上跟踪日志文件，因为它减少了磁盘访问，可以省电

```

### 程序转入前台或者后台运行 Linux ctrl 组合命令

jobs //查看任务，返回任务编号 n 和进程号
free 查看当前内存使用情况
bg %n //将编号为 n 的任务转后台运行
fg %n //将编号为 n 的任务转前台运行
ctrl+z //挂起当前任务
ctrl+c //结束当前任务 发送 Terminal 到当前的程序，强制结束当前程序，比较暴力
ctrl+d //结束当前任务或退出 shell, 发送 exit 信号
ctrl+|
ctrl+s 暂停屏幕输出
ctrl+q 恢复屏幕输出
ctrl+a 切换到命令行开始
ctrl+e 切换到命令行末尾
ctrl+y 在光标处粘贴剪切的内容

### Linux 查看系统安转的所有源包

rpm -qa
pcp-pmda-kvm-3.10.6-2.el7.x86_64
unoconv-0.6-7.el7.noarch
texlive-fp-svn15878.0-38.el7.noarch
abrt-python-2.1.11-36.el7.centos.x86_64
libcanberra-gtk3-0.30-5.el7.x86_64

### Linux 查看 virtualenv 的所有包

pip freeze
效果如下：
tornado==4.3
Tornado-JSON==1.2.1
urlgrabber==3.10
urllib3==1.10.2
urwid==1.1.1

## 其他命令

**Linux-Tips 功能:**

```bash
# 查看可安装包:
rpm -qa | grep filename
yum search filename
pip search filename
# 2.动态查看日志，多方查看日志nohup
tail -f nohup.out  -f
# 3.建立文件链接
ln -s  xx/xxx/xxx/xx.py     test.link     建立软链接，相当于快捷方式
ln -d  xx/xxx/xxx/xx.py     test.link     建立硬链接，相当于拷贝一份文件
# 4.wget命令
wget命令下载某个文件的命令为：
wget-P, –directory-prefix=PREFIX  [URL地址]，将url连接中的文件保存到目录 PREFIX/下。
 2.与目录相关的参数有：-nd –no-directories 不创建目录；
    -x, –force-directories 强制创建目录；
    -nH, –no-host-directories 不创建主机目录；
    –cut-dirs=NUMBER 忽略 NUMBER层远程目录
# 6.虚拟机之间的文件传输
第一种就是ftp，也就是其中一台Linux安装ftp Server，这样可以另外一台使用ftp的client程序来进行文件的copy。

第二种方法就是采用samba服务，类似Windows文件copy 的方式来操作，比较简洁方便。

第三种就是利用scp命令来进行文件复制。

scp是有Security的文件copy，基于ssh登录。操作起来比较方便，比如要把当前一个文件copy到远程另外一台主机上，可以如下命令。

scp /home/daisy/full.tar.gz root@172.19.2.75:/home/root

然后会提示你输入另外那台172.19.2.75主机的root用户的登录密码，接着就开始copy了。

# 7.Linux 文件的处理 read，open，write等
# 8.Linux atime ctime mtime
atime access time
ctime change time
mtime modify time

# 10.nosetests 单元测试

用于测试某个程序中单独模块的功能
nosetests -s xxx.py
只会执行 函数名包含test的函数
ps：
     可以吧其他函数放入test_all():中

# 11.获取每月的最大天数
import datetime
import calendar
calendar.monthrange(now_year,now_month)[1]

# 12.sqlalchemy.orm框架 - orm字段缺失，导致对应值缺失。

当表中有10个字段。但是对应的orm只有8个字段，会导致 数据导入正常执行，但是缺失的两个字段无任何值。
注:数据库修改，对应的orm必须修改一致

# 14.使用copy模块深拷贝对象
浅拷贝，拷贝对应的引用，例如工厂函数，
深拷贝，拷贝对象以及引用和引用指向的具体内容

# Decimal取两位小数，精度
y = Decimal(0.2356).quantize(Decimal('0.00'))
y = Deciaml(0.24)

# 查看文件夹大小
du -ah --max-depth=1
```

### 关机命令

linux 下常用的关机命令有：shutdown、halt、poweroff、init；重启命令有：reboot。下面本文就主要介绍一些常用的关机命令以及各种关机命令之间的区别和具体用法。

首先来看一下 linux 下比较常用的一些关机命令

关机命令：

- halt 立刻关机
- poweroff 立刻关机
- shutdown -h now 立刻关机(root 用户使用)
- shutdown -h 10 10 分钟后自动关机 如果是通过 shutdown 命令设置关机的话，可以用 shutdown -c 命令取消重启

重启命令：

- reboot
- shutdown -r now 立刻重启(root 用户使用)
- shutdown -r 10 过 10 分钟自动重启(root 用户使用)
- shutdown -r 20:35 在时间为 20:35 时候重启(root 用户使用) 如果是通过 shutdown 命令设置重启的话，可以用 shutdown -c 命令取消重启

在 linux 下一些常用的关机/重启命令有 shutdown、halt、reboot、及 init，它们都可以达到重启系统的目的，但每个命令的内部工作过程是不同的。

如果是通过 shutdown 命令设置重启或关机的话，可以用 shutdown -c 命令取消重启

几种不同关机命令详解

```bash
1.shutdown 安全地将系统关机

shutdown 命令安全地将系统关机。 有些用户会使用直接断掉电源的方式来关闭 linux，这是十分危险的。因为 linux 与 windows 不同，其后台运行着许多进程，所以强制关机可能会导致进程的数据丢失﹐使系统处于不稳定的状态﹐甚至在有的系统中会损坏硬件设备。

而在系统关机前使用 shutdown 命令﹐系统管理员会通知所有登录的用户系统将要关闭。并且 login 指令会被冻结﹐即新的用户不能再登录。直接关机或者延迟一定的时间才关机都是可能的﹐还可能重启。这是由所有进程〔process〕都会收到系统所送达的信号〔signal〕决定的。这让像 vi 之类的程序有时间储存目前正在编辑的文档﹐而像处理邮件〔mail〕和新闻〔news〕的程序则可以正常地离开等等。

shutdown 执行它的工作是送信号〔signal〕给 init 程序﹐要求它改变 runlevel。Runlevel 0 被用来停机〔halt〕﹐runlevel 6 是用来重新激活〔reboot〕系统﹐而 runlevel 1 则是被用来让系统进入管理工作可以进行的状态﹔这是预设的﹐假定没有-h 也没有-r 参数给 shutdown。要想了解在停机〔halt〕或者重新开机〔reboot〕过程中做了哪些动作﹐你可以在这个文件/etc/inittab 里看到这些 runlevels 相关的资料。

shutdown 参数说明:
　　 [-t] 在改变到其它 runlevel 之前﹐告诉 init 多久以后关机。
　　 [-r] 重启计算器。
　　 [-k] 并不真正关机﹐只是送警告信号给每位登录者〔login〕。
　　 [-h] 关机后关闭电源〔halt〕。
　　 [-n] 不用 init﹐而是自己来关机。不鼓励使用这个选项﹐而且该选项所产生的后果往往不总是你所预期得到的。
　　 [-c] cancel current process 取消目前正在执行的关机程序。所以这个选项当然没有时间参数﹐但是可以输入一个用来解释的讯息﹐而这信息将会送到每位使用者。
　　 [-f] 在重启计算器〔reboot〕时忽略 fsck。
[-F] 在重启计算器〔reboot〕时强迫 fsck。
　　 [-time] 设定关机〔shutdown〕前的时间。

2.halt 调用 shutdown -h, 文件系统写操作完成后就会停止内核

其实 halt 就是调用 shutdown -h。halt 执行时﹐杀死应用进程﹐执行 sync 系统调用﹐文件系统写操作完成后就会停止内核。
　　 参数说明:
　　 [-n] 防止 sync 系统调用﹐它用在用 fsck 修补根分区之后﹐以阻止内核用老版本的超级块〔superblock〕覆盖修补过的超级块。
　　 [-w] 并不是真正的重启或关机﹐只是写 wtmp〔/var/log/wtmp〕纪录。
　　 [-d] 不写 wtmp 纪录〔已包含在选项[-n]中〕。
　　 [-f] 没有调用 shutdown 而强制关机或重启。
　　 [-i] 关机〔或重启〕前﹐关掉所有的网络接口。
　　 [-p] 该选项为缺省选项。就是关机时调用 poweroff。

3.reboot 引发主机重启
　　 reboot 的工作过程差不多跟 halt 一样﹐不过它是引发主机重启﹐而 halt 是关机。它的参数与 halt 相差不多。

4.init 终止所有的用户进程﹑守护进程等
　　 init 是所有进程的祖先﹐它的进程号始终为 1﹐所以发送 TERM 信号给 init 会终止所有的用户进程﹑守护进程等。shutdown 就是使用这种机制。init 定义了 8 个运行级别(runlevel)， init 0 为关机﹐init 1 为重启。关于 init 可以长篇大论﹐这里就不再叙述。另外还有 telinit 命令可以改变 init 的运行级别﹐比如﹐telinit -iS 可使系统进入单用户模式﹐并且得不到使用 shutdown 时的信息和等待时间。
```

## TODO 其他命令

```bash
ps -ef 查看进程异常否，是否存在攻击。
js查看数据类型  alert(typeof xxx)
test -e filenaem 判断文件名是否存在。
vi中 ctrl按键配合方向键 有奇效---对于调到句首 句尾
grep -rn "xxx" .  当前路径中搜索，公司电脑也可使用

crtl+p/n  vi中的命令补全
grep精准查找 grep -w "xxx" 或者 grep "\<xxx\>"
vi中查看文件名，文件路径:file  :pwd  :ls#历史打开的文件


```
