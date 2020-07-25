---
title: Linux-功能模块-FTP配置
date: 2018-11-12 15:38:13
updated: 2018-11-12 19:17:11
tags:
  - 系统部署
  - Linux
  - Centos7
  - Centos8
  - 文件传输
  - ftp
categories:
  - Linux-功能模块
description: FTP配置
---

环境说明:

- CentOS7.5+ or CentOS8

**注意事项：**

- 配置单向网关或防火墙策略时，外部网络变动时，容器内部不会变动，容器以及 docker 都需要重启才可以更新。

## ftplib 连接

前置依赖说明

- 信息说明
  - 服务器 A-本机服务器
  - 服务器 B-远程服务器
- 注意事项
  - 服务器 A 可以 ssh 连接访问服务器 B 用户
  - 服务器 AB 都要配置好 vsftpd

### Linux 系统配置

```bash
# 服务器AB都要配置

# 关闭selinux
sed -i "s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config
setenforce 0

# 安装 vsftpd
yum install vsftpd -y

# 修改 data_connection 超时时间默认120s,避免网络产生问题
/etc/vsftpd/vsftpd.conf
# 修改 idle_session_timeout=60000
/etc/vsftpd/vsftpd.conf

# Centos6
service vsftpd restart
chkconfig vsftpd on
# Centos8
systemctl restart vsftpd
systemctl enable vsftpd.service
```

#### Ubuntu 安装 vsftpd

Ubuntu 配置 vsftpd 不同于 CentOS8

```bash
# 安装 vsftpd
sudo apt-get install vsftpd -y
sudo systemctl start vsftpd
sudo systemctl enable vsftpd

# 备份配置文件
sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.bak

# 修改文件 /etc/vsftpd.conf, 添加如下内容
listen=NO
listen_ipv6=YES
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
chroot_local_user=YES
secure_chroot_dir=/var/run/vsftpd/empty
# pam_service_name=vsftpd
pam_service_name=ftp
pasv_enable=Yes
pasv_min_port=10000
pasv_max_port=11000
# user_sub_token=$USER
# local_root=/home/$USER/ftp
userlist_enable=YES
userlist_file=/etc/vsftpd.userlist
userlist_deny=NO

# sudo vim /etc/vsftpd.userlist 添加如下内容
ftdm # 远程连接的用户

# 重启服务
sudo systemctl restart vsftpd
sudo systemctl status vsftpd
```

- [在 Ubuntu 18.04 LTS 上安装和配置 VSFTPD 服务器](https://www.howtoing.com/ubuntu-vsftpd)

### 项目使用说明

```bash
# >>>>>>>> 服务器B-配置
useradd fdm
echo "qwe123"  | passwd fdm --stdin
mkdir /bank_data
chown fdm:fdm -R /bank_data

# >>>>>>>> 服务器A-配置

# 修改配置文件
#### item [FTP_CONFIG] 远程FTP目录,用于获取远程服务器文件
export FTP_HOSTADDR=192.168.100.162
export FTP_USERNAME=fdm
export FTP_PASSWORD=qwe123
export FTP_PORT=21
export FTP_MONITOR_DIR=/bank_data
export DAILY_MODE=SURVEY

# 建表
python tools.py --rebuild_orm sys_info_dataset
python tools.py --rebuild_orm sys_info_dataset_detail
# 开启FTP监控
python tools.py --start_ftp_monitor
# 开启日批模式
python tools.py --start_daily_job_monitor
```

## paramiko

参考链接: [Python SSH、FTP 连接](https://www.jianshu.com/p/31409eb2585b)

## 附件

### 参考链接

- [vsftpd.conf-Manager](http://vsftpd.beasts.org/vsftpd_conf.html)
- [vsftpd.conf.default](http://digital.mactux.se/Digital/vsftpd/vsftpd.conf/vsftpd.conf.default-0.1.html)
- [Python-ftplib](https://docs.python.org/3/library/ftplib.html)
- [vsftpd 主动模式&被动模式](https://www.cnblogs.com/rongkang/p/10005775.html)
- [VSFTP 配置说明](https://blog.csdn.net/Lockey23/article/details/76736665)

### 问题记录

#### 500 OOPS:cannot change directory:/root

ftplib 连接时 selinux 未关闭导致的这个错误。

解决方法

1. 关闭 selinux
2. setsebool ftpd_disable_trans 1 或者 setsebool ftp_home_dir 1

```bash
今天在使用Filezilla连接Linux的时候不能成功，显示"500 OOPS:cannot change directory:/root" 错误，如何解决呢？
参考链接：https://www.cnblogs.com/jinxiblog/p/6698698.html
默认下是没有开启FTP的支持，所以访问时都被阻止了
解决：
1. 查看SELinux设置
# getsebool -a | grep ftp
发现 ftpd_disable_trans –> off 或者 ftp_home_dir–>off
2. 使用setsebool命令开启
# setsebool ftpd_disable_trans 1 或者 # setsebool ftp_home_dir 1
3. 查看当前状态是否是on的状态
# getsebool -a|grep ftp
此时 ftpd_disable_trans –> on 或者 ftp_home_dir–>on
4. 最后重启 # service vsftpd restart
OK，问题解决了。
```

#### ftplib.FTP().connect Time Out

注：宿主机外部网络变更时，容器内部网络不会变更，需要重启容器和 docker.service.

```bash
# 问题背景
尝试修改防火墙策略，内容如下
1.仅当客户端在21端口向服务端发送数据请求时可以通过
2.服务器向客户端发送请求无法通过
3.VSftpd服务在服务器端，启动项目服务在客户端。
4.使用容器启动的项目服务，通过项目服务获取服务器的指定目录。

# 问题内容
客户端容器服务已关闭，修改防火墙策略之后，容器内部服务无法正常启动。

问题原因
# 解决方案
关闭 容器，重启docker service,重新启动项目服务

关键点: 宿主机外部网络变更时，容器内部网络不会变更，需要重启容器和docker.service
```
