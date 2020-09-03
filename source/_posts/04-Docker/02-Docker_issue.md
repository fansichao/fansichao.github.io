---
title: Docker常见问题
url_path: docker/docker_issue
tags:
  - docker
  - module
categories:
  - docker
description: Docker常见问题
---

## 常见问题

### /var/run/docker.sock: permission denied

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

### docker-systemctl 无法使用修复

问题：容器中不能使用-systemctl

```bash
# 在容器启动时增加 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup 与 /user/bin/init 即可

# 样例
docker run -itd --name xxxx --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup 与 /user/bin/init 即可
```

### 问题: dial unix /var/run/docker.sock: permission denied. Are you trying to connect to a TLS-enabled daemon without TLS

参考链接: [Are you trying to connect to a TLS-enabled daemon without TLS?](https://www.cnblogs.com/ppgs8903/p/5041919.html)

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

### 问题: Repository dgraph/dgraph already being pulled by another client. Waiting

解决方法: 重启服务

```bashe
[root@WOdocker pull dgraph/dgraph:latest
Repository dgraph/dgraph already being pulled by another client. Waiting.

[root@WOM ~]#
[root@WOM ~]# service docker restart
停止 docker:                                               [确定]
Starting docker:                                       [确定]
[root@WOM ~]#
[root@WOM ~]# docker pull dgraph/dgraph:latest




[root@WOM ~]# docker pull dgraph/dgraph:latest
latest: Pulling from dgraph/dgraph
f2b818b26f75: Pulling fs layer
c87298e9b6ec: Pulling fs layer
d29d3718cea9: Pulling fs layer
55982ec1ed3b: Pulling fs layer
a5019d93caef: Pulling fs layer
cea85299b18b: Pulling fs layer
4696dbf656b6: Pulling fs layer
c2c5bc4dfb3f: Pulling fs layer
bd8f9f1a25f5: Pulling fs layer
ca927ff9c37d: Pulling fs layer
8e51752bd503: Pulling fs layer
c58a4ff12da9: Pulling fs layer
Pulling repository dgraph/dgraph
Tag latest not found in repository dgraph/dgraph # 1.说明标签错误
[root@WOM ~]# docker search dgraph  # 2.搜索这个镜像，看是否可以找到标签

# 3.去官网查看标签  查询URL为:  https://hub.docker.com/r/【镜像名】/tags/
# https://hub.docker.com/r/dgraph/dgraph/tags/
```

### 问题:Segmentation Fault or Critical Error encountered

提示: Segmentation Fault or Critical Error encountered. Dumping core and aborting.
Aborted
解答: 安装错误安装 docker 了，应该安装 docker-io

### 问题:docker-io-1.7.1-2.el6.x86_64

提示: Transaction Check Error:
  file /usr/bin/docker from install of docker-io-1.7.1-2.el6.x86_64 conflicts with file from package docker-1.5-5.el6.x86_64
解答: 这个是因为先装了 docker，再装 docker-io 后的结果，解决方法是 yum remove docker 后再 yum install docker-io 即可。

### 问题:/var/run/docker.sock: no such file or directory

```bash
# 错误日志
Get http:///var/run/docker.sock/v1.19/images/search?term=centos: dial unix /var/run/docker.sock: no such file or directory. Are you trying to connect to a ?

# 问题原因
解答: docker 没有启动，

# 解决方法
/etc/init.d/docker start
```

### 问题: 容器内中文乱码

```bash
[root@c7c57188b482 test_data]# ll
total 4
drwxrwxrwx 5 root root 4096 Oct 15 02:58 graph_data
-rwxr-xr-x 1 root root    0 Oct 15 02:58 ????????????
```

**方案 1:**

```bash
yum install -y kde-l10n-Chinese
yum reinstall -y glibc-common

# 定义字符集
localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
# 确认载入成功
locale -a
# echo
echo 'LANG="zh_CN.UTF-8"' > /etc/locale.conf
source /etc/locale.conf

```

如果不能解决,可以用如下方法

**方案 2:**

```bash
echo "export LC_ALL=en_US.utf8" >> ~/.bash_profile
# 在用户中加入这个, 或者在 /etc/profie 中加入
# 不是一个好方法，但是可以解决问题
```

### `/var/run/docker.sock: connect: permission denied`

解决方法

```bash
(env) [scfan@fdm docker_cmd]$  docker import docker_7.tar docker_7
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post http://%2Fvar%2Frun%2Fdocker.sock/v1.26/images/create?fromSrc=-&message=&repo=docker_7&tag=: dial unix /var/run/docker.sock: connect: permission denied
(env) [scfan@fdm docker_cmd]$ sudo chmod 777 /var/run/docker.sock
```

### docker: Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "exec: \"/usr/sbin/init\": stat /usr/sbin/init: no such file or directory": unknown

解决方法

```bash
docker运行出现这个错误有可能是保存镜像使用的保存方式可导入的方式不同

如果是使用import导入的镜像，应该注意是：import可以导入save保存的镜像包和export保存的容器包。但是如果导入的是save保存的镜像包，导入时没有错。但是run运行时就会出此错误。
所以可以尝试使用load再次导入镜像，run一下试试


# 使用 load, 而非 import
(env) [fdm@fdm docker_tar]$ docker load -i centos7.tar
edf3aa290fb3: Loading layer  211.1MB/211.1MB
Loaded image: centos:7
(env) [fdm@fdm docker_tar]$ docker images | grep centos
centos                                                 7                   b5b4d78bc90c        6 weeks ago         203MB
```

## 参考链接

[docker 遇到 bash: No such file or directory 或 sh: not found 等问题](https://blog.csdn.net/czhdolyec/article/details/103424234)
