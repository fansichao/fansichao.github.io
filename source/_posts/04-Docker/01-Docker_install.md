---
title: Docker部署文档
url_path: docker/install
tags:
  - docker
  - module
categories:
  - module
  - docker
description: Docker容器部署文档
---

## Docker Install

### CentOS6

**安装说明:**

1. CentOS6.10 环境，要求 6.8+
2. Docker 版本 1.7.1

**步骤 1:** 配置下载镜像 `docker.repo` 文件

CentOS6 安装方法

```bash
[root@yinsho ~]# cat /etc/yum.repos.d/docker.repo
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/6
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
```

CentOS7 安装方法

```bash
[root@yinsho ~]# cat /etc/yum.repos.d/docker.repo
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
```

**步骤 2:** 重建元数据

```bash
yum clean all
yum makecache
```

**步骤 3:** 安装 docker

```bash
yum install docker-engine  -y
```

问题: docker-engine conflicts

```bash
# 如果执行报错 docker-engine conflicts with xxxxx
# 先卸载 docker，再安装 docker-engine
yum remove docker -y
```

**步骤 4:** 启动 docker 服务

```bash
service docker start
chkconfig docker on
```

**步骤 5:** 非 root 用户使用 docker. 将用户添加到 docker 用户组

```bash
sudo groupadd docker
sudo usermod -aG docker $USER


# 添加用户组后 必须重启服务
# Centos7
sudo systemctl restart docker
sudo systemctl enable docker
# CentOS6
sudo service restart docker
sudo chkconfig on docker

# 添加用户组后 必须切换当前会话到新 group 或者重启 X 会话
newgrp - docker 或  pkill X
```

**参考说明:**

[安装参考链接](https://blog.csdn.net/abcd_d_/article/details/53996791)

```bash
yum update -y
如果报错 No module named yum
参考: https://www.cnblogs.com/clover-siyecao/p/5650893.html

rpm -Uvh http://ftp.riken.jp/Linux/fedora/epel/6Server/x86_64/epel-release-6-8.noarch.rpm

yum remove docker -y
yum install -y docker-io
```

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
