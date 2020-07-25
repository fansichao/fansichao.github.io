---
title: Linux-功能模块-HTTPS证书配置
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - 系统部署
  - Linux
  - Centos7
  - Centos8
  - HTTPS
categories:
  - Linux-功能模块
description: 证书配置
---

环境说明：

- CentOS8.1.19

## 配置 NFS

容器内部配置 NFS 特殊说明

- 在 docker 中开启 NFS 服务需要挂载主机的目录，才能通过 NFS 共享。
  - exp: docker run -dit -v /mnt:/data xxxx, 只有容器内的 nfs_data 才可以进行 nfs 共享

环境说明

- Docker 容器 服务器
  - IP 172.21.0.111
  - 容器内目录 /data
- Docker 容器 客户端
  - IP 172.21.0.150
  - 容器内目录 /nfs_data

**注意事项:**

- 服务器关机时，先关闭 NFS 客户端，最后关闭 NFS 服务端。
- 服务器开机时，先开启 NFS 服务端，最后开启 NFS 客户端。

### 服务器配置

因为 centos7 自带了 rpcbind，所以不用安装 rpc 服务，rpc 监听在 111 端口，可以使用 ss -tnulp | grep 111 查看 rpc 服务是否自动启动，如果没有启动，就 systemctl start rpcbind 启动 rpc 服务。rpc 在 nfs 服务器搭建过程中至关重要，因为 rpc 能够获得 nfs 服务器端的端口号等信息，nfs 服务器端通过 rpc 获得这些信息后才能连接 nfs 服务器端

```bash
# 安装 nfs 服务
yum -y install nfs-utils

# 查看 nfs 服务是否安装成功
[root@b9fed615b76b ~]#  
nfs-utils-2.3.3-31.el8.x86_64

# 修改文件 /etc/exports 添加如下内容
/data  172.21.0.0/24(rw,sync,no_root_squash,insecure)

# TODO exports 中 rw,sync,no_root_squash,insecure 参数说明

# 启动服务 耗时 10s-1min 不等
systemctl restart nfs-server

# 查看 NFS
[root@b9fed615b76b ~]# rpcinfo -p 172.21.0.111
   program vers proto   port  service
    100000    4   tcp    111  portmapper
    100000    3   tcp    111  portmapper
    100000    2   tcp    111  portmapper
    100000    4   udp    111  portmapper
    100000    3   udp    111  portmapper
    100000    2   udp    111  portmapper
    100005    1   udp  20048  mountd
    100005    1   tcp  20048  mountd
    100005    2   udp  20048  mountd
    100005    2   tcp  20048  mountd
    100005    3   udp  20048  mountd
    100005    3   tcp  20048  mountd
    100003    3   tcp   2049  nfs
    100003    4   tcp   2049  nfs
    100227    3   tcp   2049  nfs_acl
    100021    1   udp  43144  nlockmgr
    100021    3   udp  43144  nlockmgr
    100021    4   udp  43144  nlockmgr
    100021    1   tcp  44159  nlockmgr
    100021    3   tcp  44159  nlockmgr
    100021    4   tcp  44159  nlockmgr

# 检查 export 内容是否正常
[root@b9fed615b76b ~]# showmount -e localhost
Export list for localhost:
/data 172.21.0.0/24

# 修改 NFS 目录权限，不然其他用户无法修改
chown -R 777 /data

# 开机自启服务
systemctl enable nfs-server
systemctl enable rpcbind
```

### 客户端配置

```bash
# 安装 NFS 服务, 利用附带的 showmount 工具，查看nfs服务是否正常
yum -y install nfs-utils

# 检测rpc是否启动
rpcinfo -p

# 使用showmount -e 查看 nfs 服务
[root@85d31196f0c6 neo4j-community-3.3.5]# showmount -e 172.21.0.111
Export list for 172.21.0.111:
/data 172.21.0.0/24

# 挂载到本地目录(服务器重启后失效)
mount -t nfs 172.21.0.111:/data /nfs_data

# 自动挂载nfs功能 (可选) - 远程nfs存在问题时，会导致重启慢(需要根据需求配置)
# 加入 /etc/rc.d/rc.local 即可
```

## 必选配置

### Linux 关机或重启时提示 A stop job is running for

Linux 关机或重启时提示 A stop job is running for .. 导致关机慢。

修改方法

```bash
vim /etc/systemd/system.conf
修改下面两个变量为： 生产服务器60s,开发服务器10s
DefaultTimeoutStartSec=60s
DefaultTimeoutStopSec=60s
DefaultRestartSec=100ms
# 执行命令
systemctl daemon-reload
```

## 可选配置

### 挂载优化

在企业工作场景，一般来说，NFS 服务器共享的只是普通静态数据（图片、附件、视频），不需要执行 suid、exec 等权限，挂载的这个文件系统只能作为数据存取之用，无法执行程序，对于客户端来讲增加了安全性，例如：很多木马篡改站点文件都是由上传入口上传的程序到存储目录，然后执行的。 因此在挂载的时候，用下面的命令很有必要：

```bash
# 安全挂载 只做数据存取 无法执行程序 根据需求使用
mount -t nfs -o nosuid,noexec,nodev,rw 172.21.0.111:/data /nfs_data
```

## 附件

 
### 参考资源

- [Docker 下配置 nfs](https://www.jianshu.com/p/d1122d42d5cc)
- [详见此文档：Linux 下的 NFS 系统简介](https://www.jianshu.com/p/f85c4371a43d)
