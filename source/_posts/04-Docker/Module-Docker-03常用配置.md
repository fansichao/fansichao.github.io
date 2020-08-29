---
title: Module-Docker-模块功能
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Docker
categories:
  - Module
description: Docker常用配置，例如设置时区、systemctl命令设置等等，此处也会记录docker相关的问题记录
---

## Docker-常用配置

可选配置/必需配置

- 可选配置
- 必需配置

### docker-快速登录(可选)

```bash
# 加入的.bash_profile
function dockerlogin(){
    docker exec -it --env COLUMNS=`tput cols` --env LINES=`tput lines` $1 /bin/bash
}
```

### Docker-时区配置(可选-建议)

docker 时区问题，容器时间和宿主机时间不一致问题

```bash
# 方法1：容器外部配置 Docker时区设置
docker cp /etc/localtime 容器id:/etc/localtime


# 方法2: 容器内部配置 容器外部配置报错，进入容器内部配置即可。
[fdm@fdm2 fdm_server]$ docker cp /etc/localtime fdm_server:/etc/localtime
Error response from daemon: Could not find the file /usr/share/zoneinfo/usr/share/zoneinfo/Asia in container fdm_server
[root@f3a3540cb8e5 ~]# ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
[root@f3a3540cb8e5 ~]# echo "Asia/Shanghai" > /etc/timezone
[root@f3a3540cb8e5 ~]# date
Fri Jul 31 09:42:08 CST 2020
```

## Docker-问题记录

### docker-systemctl 无法使用修复

问题：容器中不能使用-systemctl

```bash
# 在容器启动时增加 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup 与 /user/bin/init 即可

# 样例
docker run -itd --name xxxx --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup 与 /user/bin/init 即可
```

### docker-容器内部命令窗口大小设置

问题：容器内部 vim/vi 只能查看屏幕一部分内容，

```bash
# 查看宿主机屏幕大小
[fdm@fdm2 nfs_data]$ stty size
48 210
# 配置容器内部 stty 大小
stty rows 48 columns 210
# 写入 /etc/profile
sudo echo "stty rows 48 columns 210" >>  /etc/profile
```

TODO 当外部窗口变化时，容器内部需要对应修改。
