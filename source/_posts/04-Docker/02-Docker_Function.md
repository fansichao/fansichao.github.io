---
title: Docker 功能模块
url_path: docker/function
tags:
  - docker
  - module
categories:
  - module
  - docker
description: Docker功能模块
---

TODO docker进入容器后，界面会出现问题，会进入容器登录界面，待解决

## 功能模块

### Docker 修改默认存储位置(可选)

由于 Docker 默认存储位置在 `/`, 但`/`空间不足时，可以将默认存储位置修改到其他位置。

```bash
# 先关闭 docker 容器
docker stop xxxx
# 关闭 docker 服务
systemctl stop docker
# 迁移数据
mv /var/lib/docker /home/fdm/docker_data
ln -s /home/fdm/docker_data /var/lib/docker
# 重启服务
systemctl start docker
```

### docker-快速登录(可选)

```bash
# 加入的.bash_profile
function dockerlogin(){
    docker exec -it --env COLUMNS=`tput cols` --env LINES=`tput lines` $1 /bin/bash
}
```

### Docker-时区配置(必选)

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

### docker-容器内部命令窗口大小设置(可选)

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

### Docker pull 加速(可选)

TODO 未成功

```bash
# 使用国内镜像源

# 修改文件 /etc/docker/daemon.json
{
    "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
# 重启服务(重启前记得手动关闭所有Docker容器)
systemctl daemon-reload
systemctl restart docker
```

## Docker 性能监控

不同方法：

- 官方 docker stats
- ps -e
- ctop

### docker stats

参考链接:

- [Docker 官方 stats](https://docs.docker.com/engine/reference/commandline/stats/?spm=a2c6h.13066369.0.0.1f661b135gtUOK)
- [Linux 内存监控，据说 Docker 官方 stats 不准确](https://www.cnblogs.com/xuxinkun/p/5541894.html)

docker stats -a
![Module_Docker_性能监控01.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/Module_Docker_%E6%80%A7%E8%83%BD%E7%9B%91%E6%8E%A701.png)

### ps -e

查看 Docker 运行情况

```bash
ps aux | grep  d276413151a0
ps -e -o 'pid,comm,args,pcpu,rsz,vsz,stime,user,uid'  | grep 8189

rsz 为实际占用内存
```

### ctop 安装(可选)

参考链接：[实时查看 Docker 容器占用的 CPU、内存状态](https://www.testwo.com/article/987)

```bash
wget https://github.com/bcicen/ctop/releases/download/v0.5/ctop-0.5-linux-amd64 -O ctop
sudo cp ctop /usr/local/bin/.
sudo chmod +x /usr/local/bin/ctop
ctop
```

![Module_Docker_性能监控02.png](https://raw.githubusercontent.com/fansichao/images/master/markdown/Module_Docker_%E6%80%A7%E8%83%BD%E7%9B%91%E6%8E%A702.png)

[查看 Docker 容器使用资源情况](https://blog.csdn.net/QMW19910301/article/details/88058769)
docker stats -a # 原生 docker 命令，效果略差于 ctop
