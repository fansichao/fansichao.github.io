---
title: Yum源配置
url_path: linux/yum
tags:
  - linux
categories:
  - linux
description: Linux-yum 本地yum源 & 在线yum源 配置
---

## yum 源说明

配置文件说明

```bash
# 指定挂载的目录下的BaseOS以及AppStream目录
baseurl
# 是否校验
gpgcheck
# 是否启动该镜像
enable
```

## Centos8-本地源配置

CentOS8 yum 源本地配置

```bash
# 移除原有repo文件
mkdir /etc/yum.repos.d/bak
mv /etc/yum.repos.d/*.repo  /etc/yum.repos.d/bak/.

# 新增 本地 /etc/yum.repos.d/local.repo
[c8-media-BaseOS]
name=CentOS-BaseOS-$releasever - Media
baseurl=file:///data/yum_data/BaseOS
        file:///data/yum_data/BaseOS
        file:///data/yum_data/BaseOS
gpgcheck=0
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial

[c8-media-AppStream]
name=CentOS-AppStream-$releasever - Media
baseurl=file:///data/yum_data/AppStream
        file:///data/yum_data/AppStream
        file:///data/yum_data/AppStream
gpgcheck=0
enabled=1
gpgkey=file:///etc/pki/rpm-g

# 配置本地 yum 时，使用gpgcheck=0，不校验

# yum install -y epel-release 自动配置yum源仓库，非必需

# 重设定yum
yum clean all
yum makecache
# 查看镜像库
yum repolist
# 校验是否正常
yum install svn -y
```

问题记录

```bash
# 问题说明
Couldn t open file /etc/pki/rpm-g

# 解决方法
去除gpgcheck校验

# 详细日志
warning: /yum_data/AppStream/Packages/apr-1.6.3-9.el8.x86_64.rpm: Header V3 RSA/SHA256 Signature, key ID 8483c65d: NOKEY
CentOS-AppStream-8 - Media                                                                                                                                                        0.0  B/s |   0  B     00:00
Curl error (37): Couldn t read a file:// file for file:///etc/pki/rpm-g [Couldn t open file /etc/pki/rpm-g]
```

## CentOS6/7-本地源配置

注：如果 nfs 已经挂起，可以直接使用 NFS 挂起的镜像作为源镜像。

说明: **生成服务器内部不允许联网时，需要配置本地 yum。其他情况无需配置**

```bash
# > 获取当前CentOS版本的官网最全镜像，此处以6.9为例
# 切换root用户操作
su - root

# > 通过光驱配置本地yum源
# 配置DVD1
mkdir -p /data/software/centos6
mount -o loop CentOS-6.9-x86_64-bin-DVD1.iso /mnt
cp -r /mnt/* /data/software/centos6
umount /mnt
# 配置DVD2
mount -o loop CentOS-6.9-x86_64-bin-DVD1.iso /mnt
cp -r /mnt/* /data/software/centos6   # 其中部分文件夹需要覆盖，一直选择y即可
umount /mnt

# 配置yum
cd /etc/yum.repos.d/
mkdir bak
mv *repo bak/
vi local.repo

# local.repo 文件内容如下
[iso]
name=centos6
baseurl=file:///data/software/centos6
gpgcheck=0
enabled=1

# 重设定yum
yum clean all
yum makecache
# 配置验证
看是上述是否有报错。
# 安装 vim
yum install vim -y
安装vim成功, 即无报错
```
