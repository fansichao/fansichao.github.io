---
title: Module-Docker-部署文档
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Docker
categories:
  - Module
description: ....
---

环境说明:

- CentOS8.1.19
- docker

## Centos8-在线部署

```bash
dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
dnf repolist -v
# 列出当前支持的 docker-ce 版本
dnf list docker-ce --showduplicates | sort -r
# 前置依赖
dnf install containerd.io -y
yum install podman-manpages -y

dnf install https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.2.6-3.3.el7.x86_64.rpm
dnf install docker-ce -y

# 开启Docker服务
systemctl start docker
# Docker开机自启
/bin/systemctl enable docker.service
```

## CentOS7-离线部署

参考链接: [centos7-离线安装 docker](https://blog.csdn.net/u013058742/article/details/80075633)

```bash
在 https://download.docker.com/linux/centos/7/x86_64/stable/Packages 下载docker-ce-17.12.0.ce-1.el7.centos.x86_64.rpm

2.下载9个依赖

在 http://mirrors.163.com/centos/7/os/x86_64/Packages 下载8个依赖

audit-libs-python-2.7.6-3.el7.x86_64.rpm
checkpolicy-2.5-4.el7.x86_64.rpm
libcgroup-0.41-13.el7.x86_64.rpm
libseccomp-2.3.1-3.el7.x86_64.rpm
libsemanage-python-2.5-8.el7.x86_64.rpm
policycoreutils-python-2.5-17.1.el7.x86_64.rpm
python-IPy-0.75-6.el7.noarch.rpm
setools-libs-3.3.8-1.1.el7.x86_64.rpm

在http://rpm.pbone.net/index.php3?stat=3&limit=1&srodzaj=1&dl=40&search=container-selinux&field[]=1&field[]=2 下载container-selinux-2.9-4.el7.noarch.rpm

下载链接：ftp://mirror.switch.ch/pool/4/mirror/scientificlinux/7x/external_products/extras/x86_64/container-selinux-2.9-4.el7.noarch.rpm

3.安装

将8个依赖复制到服务器上如：/root/docker/

将docker-ce-17.12.0.ce-1.el7.centos.x86_64.rpm和container-selinux-2.9-4.el7.noarch.rpm复制到/root/docker/rpm/

rpm -ivh /root/docker/*.rpm

rpm -ivh /root/docker/rpm/container-selinux-2.9-4.el7.noarch.rpm

rpm -ivh/root/docker/rpm/docker-ce-17.12.0.ce-1.el7.centos.x86_64.rpm

4.启动

service docker start

docker -v
```

## CentOS8-离线部署

参考链接: [CentOS8 离线安装 docker](https://blog.csdn.net/haveqing/article/details/105277605)

```bash
# 下载文件 tgz
https://download.docker.com/linux/static/stable/x86_64/
# 下载文件 rpm
https://download.docker.com/linux/centos/7/x86_64/stable/Packages/

# 卸载冲突软件 podman(虚拟化软件)
rpm -q podman
yum remove podman
# 安装docker
yum install containerd.io-1.2.6-3.3.el7.x86_64.rpm -y
yum install docker-ce-cli-19.03.9-3.el7.x86_64.rpm -y
yum install docker-ce-19.03.9-3.el7.x86_64.rpm -y
# 元数据检查
yum module enable perl:5.26
```

## ctop 安装(可选)

```bash
wget https://github.com/bcicen/ctop/releases/download/v0.5/ctop-0.5-linux-amd64 -O ctop
sudo cp ctop /usr/local/bin/.
sudo chmod +x /usr/local/bin/ctop
ctop
```

## Docker 修改默认存储位置(可选)

由于 Docker 默认存储位置在 `/`, 但`/`空间不足时，可以将默认存储位置修改到其他位置。

```bash
# 先关闭 docker 容器
docker stop xxxx
# 关闭 docker 服务
systemctl stop docker
# 迁移数据
mv /var/lib/docker /home/docker_data
ln -s /home/docker_data /var/lib/docker
# 重启服务
systemctl start docker
```

## 附件

### 参考链接

- 主要安装部署参考链接： [How to install Docker CE on RHEL 8 / CentOS 8](https://linuxconfig.org/how-to-install-docker-in-rhel-8)

### 问题: /var/run/docker.sock: permission denied

参考链接: [Are you trying to connect to a TLS-enabled daemon without TLS?](https://www.cnblogs.com/ppgs8903/p/5041919.html)

详细日志

```bash
FATA[0000] Get http:///var/run/docker.sock/v1.18/images/json: dial unix /var/run/docker.sock: permission denied. Are you trying to connect to a TLS-enabled daemon without TLS?
```

问题原因: 非 root 用户未成功添加到用户组或未生效

解决方法:

```bash
# 创建 docker 用户组
sudo groupadd docker
# 添加用户到用户组
sudo gpasswd -a ${USER} docker
# 重启服务
sudo service docker restart
# 切换当前会话到新 group 或者重启 X 会话 [必须步骤]
newgrp - docker 或 pkill X
```

### containerd 版本依赖问题

redhat 直接安装 docker-ce 会显示 containerd-io 版本依赖不满足

```bash
[root@fdm ~]# dnf install docker-ce -y
Last metadata expiration check: 0:09:30 ago on Tue 26 May 2020 11:03:38 AM CST.
Error:
 Problem: package docker-ce-3:19.03.9-3.el7.x86_64 requires containerd.io >= 1.2.2-3, but none of the providers can be installed
  - conflicting requests
  - package containerd.io-1.2.10-3.2.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.13-3.1.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.13-3.2.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.2-3.3.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.2-3.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.4-3.1.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.5-3.1.el7.x86_64 is filtered out by modular filtering
  - package containerd.io-1.2.6-3.3.el7.x86_64 is filtered out by modular filtering
(try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
```

解决方案

```bash
# 方案1
# 手动安装最新 containerd.io
dnf install https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.2.6-3.3.el7.x86_64.rpm
yum install docker-ce -y

# 方案2
# 安装特定版本 docker-ce
dnf install docker-ce-3:18.09.1-3.el7
```
