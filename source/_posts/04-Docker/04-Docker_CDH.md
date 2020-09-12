---
title: Docker-CDH部署文档
url_path: docker/cdh
tags:
  - docker
  - module
categories:
  - module
  - docker
description: CDH大数据平台部署，Spark、HDFS、Hive等等一键部署。
---

## 文档说明

文档内容如下

- [文档说明](#文档说明)
- [部署步骤](#部署步骤)
- [详细使用](#详细使用)
- [参考资源](#参考资源)

## 部署步骤

```bash
# 拉取镜像
docker pull cloudera/quickstart

# 运行容器
docker run  -id  --hostname=quickstart.cloudera --privileged=true   \
-p 8020:8020 -p 7180:7180 -p 21050:21050 -p 50070:50070 \
-p 50075:50075  -p 50010:50010 -p 50020:50020 -p 8890:8890 \
-p 60010:60010 -p 10002:10002   -p 25010:25010 -p 25020:25020 \
-p 18088:18088 -p 8088:8088 -p 19888:19888  -p 7187:7187 \
-p 11000:11000 -t -p 8888:8888  \
--name=cdh1  cloudera/quickstart /usr/bin/docker-quickstart

# 配置 快速登录容器命令 dockerlogin
# 放置在 ~/.bash_profile 中 source ~/.bash_profile
function dockerlogin(){
    docker exec -it --env COLUMNS=`tput cols` --env LINES=`tput lines` $1 /bin/bash
}

# 登录容器
dockerlogin cdh1

# 启动CDH服务
[root@quickstart /]# /home/cloudera/cloudera-manager --enterprise
[QuickStart] Shutting down CDH services via init scripts...
kafka-server: unrecognized service
JMX enabled by default
Using config: /etc/zookeeper/conf/zoo.cfg
[QuickStart] Disabling CDH services on boot...
error reading information on service kafka-server: No such file or directory
[QuickStart] Starting Cloudera Manager server...
[QuickStart] Waiting for Cloudera Manager API...
[QuickStart] Starting Cloudera Manager agent...
[QuickStart] Activating trial license for Enterprise...
[QuickStart] Configuring deployment...
Submitted jobs: 16
[QuickStart] Deploying client configuration...
Submitted jobs: 17
[QuickStart] Starting Cloudera Management Service...
Submitted jobs: 25
[QuickStart] Enabling Cloudera Manager daemons on boot...
________________________________________________________________________________

Success! You can now log into Cloudera Manager from the QuickStart VM s browser:

    http://quickstart.cloudera:7180

    Username: cloudera
    Password: cloudera


# 宿主机 配置 CDH-Hosts 添加 quickstart.cloudera 内容
(env) [fdm@fdm ~]$ sudo vim /etc/hosts
127.0.0.1   localhost fdm quickstart.cloudera
192.168.172.73 fdm quickstart.cloudera
```

查看 CDH 界面 `http://192.168.172.73:7180/cmf/home`
![Docker-CDH-首页图片](https://raw.githubusercontent.com/fansichao/images/master/markdown/Docker-CDH-%E9%A6%96%E9%A1%B5%E5%9B%BE%E7%89%87.png)

## 详细使用

详见 站内文档 [CDH 使用文档](www.superscfan.top/05-Module/CDH-Docs)

## 参考资源

- [Docker 部署 CDH](https://blog.csdn.net/eyeofeagle/article/details/85159600)
