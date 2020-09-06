---
title: Module-Docker-使用文档
url_path: docker/dockerdocker
tags:
  - Module
  - Docker
categories:
  - Module
description: ....
---

## Docker 使用

## Docker 功能

### Docker 网络配置使用

### Docker 性能监控

### 其他模块

```bash
其他模块
使用xshell登录docker -- 方式1 进入docker虚拟机
ssh 192.168.99.100 # docker的IP ，通过查看docker虚拟机的ip登入docker界面
用户名默认是: docker
密码默认: tcuser
端口: 22

# 涉及安装openssh-server
http://blog.csdn.net/vincent2610/article/details/52490397
yum install -y openssh-server
vi /etc/ssh/sshd_config
将PermitRootLogin的值从withoutPassword改为yes
登出容器，并将容器保存为新的镜像。
关闭原有容器，用新镜像生成新的容器
使用xshell登录docker -- 方式2 docker进入容器
1.安装配置好sshd，并进入后重启服务。
2.docker run 通过 -p 50001:22，将22端口映射到50001
3.打开cmd，查看windwosIP，例如 192.168.43.25
4.ssh 192.168.43.25 50001
或者 ssh 192.168.43.25 -p 50001
即可登录进入容器中


配置容器系统参数 - 需要从docker上配置
# sysctl: setting key "vm.max_map_count": Read-only file system 问题
参考链接: https://stackoverflow.com/questions/41064572/docker-elk-vm-max-map-count
说明: 由于docker是最高层级，容器是最低层级，部分系统参数需要从docker中修改，否则权限不足
解决方法:
docker-machine create -d virtualbox default # 创建默认虚拟机，涉及需要开启windows功能 Hyper-V
docker-machine start 机器名称 # 出现蓝屏问题，暂时未解决 PASS
docker-machine ssh
sudo sysctl -w vm.max_map_count=262144
配置容器系统参数 - 需要从docker上配置  -- 问题1: 登陆docker界面，但是docker中virtualbox不存在。

# 查看已有的docker-machine机器名称
docker-machine ls
# 进入docker
docker-machine ssh 机器名称ID


错误: Error: No machine name(s) specified and no "default" machine exists
错误原因: 本机没有machine，需要创建
# 创建docker机器
docker-machine create -d virtualbox default 机器名称

错误: Error with pre-create check: "This computer is running Hyper-V. VirtualBox won't boot a 64bits VM when Hyper-V is activated. Either use Hyper-V as a driver, or disable the Hyper-V hypervisor. (To skip this check, use --virtualbox-no-vtx-check)
错误原因: docker的virtualbox和已有的虚拟机VMware或virtualBox冲突
参考链接: http://blog.csdn.net/qwsamxy/article/details/50533007/
解决方法:
bcdedit /set hypervisorlaunchtype off
bcdedit /set hypervisorlaunchtype auto


bcdedit /copy {current} /d "Windows 10 (开启 Hyper-V)"
bcdedit /set {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX} hypervisorlaunchtype auto

![ce8948b05eeb29c99a714e80749170f0.png](en-resource://database/14842:0)




切换用户执行脚本
su - test -c "pwd"
删除images后，释放空间: （会删除未使用的的容器和已删除的镜像-慎重）
docker system prune -a




## docker-ce容器管理页面

参考链接: https://www.cnblogs.com/myzony/p/9071210.html

pass
CentOS7可用？
```

## 附件

### docker 问题记录

### 参考资源

- [Docker 部分组成](https://blog.csdn.net/sunzhiqiang6/article/details/80698436)

https://www.google.com/search?source=hp&ei=KNEnWqOFIIGu0gS2zZzYDQ&q=docker%20%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4

Docker 常用命令 待整理
https://www.jianshu.com/p/adaa34795e64
https://www.infoq.cn/article/KBTRC719-r6GHOPS3Cr8

docker 基础命令: https://www.server110.com/docker/201411/11122.html
docker run 参数: http://www.runoob.com/docker/docker-run-command.html
docker 官方英文文档: https://docs.docker.com/
docker 中文文档网站: http://www.docker.org.cn/
第一本 docker 书籍: https://download.csdn.net/download/qq_21165007/10276074

Docker 是一个开源的应用容器引擎，基于  Go 语言   并遵从 Apache2.0 协议开源。
Docker 可以让开发者打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。
容器是完全使用沙箱机制，相互之间不会有任何接口（类似 iPhone 的 app）,更重要的是容器性能开销极低。

- Docker 官方中文网: [http://www.docker.org.cn/](http://www.docker.org.cn/)
- Docker 官网: [https://www.docker.com/](https://www.docker.com/)
- Docker 菜鸟教程: [http://www.runoob.com/docker/docker-tutorial.html](http://www.runoob.com/docker/docker-tutorial.html)
