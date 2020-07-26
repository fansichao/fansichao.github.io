---
title: Linux-性能测试工具
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Linux
categories:
  - Linux-工具
description: ...
---

TODO 待完善

详见文档 [《性能测试.docx文档》](Docx/Docx-性能测试.docx)

## 安装说明

```bash
说明:
1. 性能测试，安装系统后和安装项目后各测试一遍。并记录信息。
2. 记录 fio’以及systeminfo的信息。

根据nmon查看性能瓶颈。

文件如下：
nmon16d_x86.tar.gz
fio-2.1.10.tar.gz
dio.py
systeminfo.sh
libpcap-1.4.0-4.20130826git2dbcaa1.el6.x86_64.rpm
libpcap-devel-1.4.0-4.20130826git2dbcaa1.el6.x86_64.rpm
iftop-0.17.tar.gz
iperf-1.7.0-1.1.el3.rf.x86_64.rpm


## 依赖安装
yum install openssh-clients -y
yum install readline-devel.* gcc zlib zlib-devel openssl openssl-devel -y
yum install dmidecode -y


########## 安装nmon
root 用户
# 创建目录 nmon_file
mkdir nmon_file && cd nmon_file  && tail -zxvf /data/software/CetnOS/cmdn_packages/nmon16d_x86.tar.gz && ./nmon_x86_64_centos6
# 给予权限

####### 安装fio
tar -zxvf /data/software/CetnOS/cmdn_packages/fio-2.1.10.tar.gz
cd fio-2.1.10
./configure && make all && make install && make clean && make distclean
## 测试详细信息
fio -filename=/dev/sda -direct=1 -iodepth 1 -thread -rw=read -ioengine=psync -bs=16k -size=2G -numjobs=10 -runtime=60 -group_reporting -name=mytest

###### 使用systeminfo，查看系统大体性能。
sh /data/software/CetnOS/cmdn_packages/systeminfo.sh

###### nmon使用命令

c  cpu
m memory
d disk
n net

##### iftop 使用命令  看网络，端口使用情况  TODO  联网安装
参考链接：http://www.vpser.net/manage/iftop.html
yum install flex byacc libpcap ncurses ncurses-devel libpcap-devel -y
tar zxvf iftop-0.17.tar.gz
cd iftop-0.17

. /configure
make && make install
iftop

##### iftop 离线安装
rpm -ivh /data/software/CetnOS/cmdn_packages/libpcap-1.4.0-4.20130826git2dbcaa1.el6.x86_64.rpm
rpm -ivh /data/software/CetnOS/cmdn_packages/libpcap-devel-1.4.0-4.20130826git2dbcaa1.el6.x86_64.rpm
yum install flex byacc libpcap ncurses ncurses-devel libpcap-devel -y
tar zxvf /data/software/CetnOS/cmdn_packages/iftop-0.17.tar.gz
cd iftop-0.17

./configure && make && make install
iftop

iftop -B -i eth0

#### iperf测试带宽用的。
参考链接：http://blog.csdn.net/lin_credible/article/details/8670330

# 安装
rpm -ivh iperf-1.7.0-1.1.el3.rf.x86_64.rpm


参考链接：http://man.linuxde.net/iperf


详细使用参见如下文档：
```
