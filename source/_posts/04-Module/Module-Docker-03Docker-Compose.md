---
title: Module-Docker-Docker Compose
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Docker
categories:
  - Module
description: ....
---

tags: `Docker` `Docker-Compose` `linux`

docker compose 是用来配置和运行多容器服务的工具，通过 docker-compose 命令可轻松对多个容器进行如下操作：

（1）启动，停止和重建服务

（2）查看正在运行的服务的状态

（3）通过流输出正在运行的服务的日志

（4）对某个服务执行命令

## Docker-Compose 安装

## 常用命令

常用命令

```bash

#启动并后台运行所有的服务

docker-compose up -d

#列出项目中目前的所有容器

docker-compose ps

#停止某个服务

docker-compose stop 服务名

#启动某个服务

docker-compose start 服务名

#停止并删除容器、网络、卷、镜像

docker-compose down


up

　　启动所有在Compose问中定义的容器，并且把它们的日志信息汇集在一起。通常会添加-d参数（在up后面），让容器在后台执行

start
　　启动指定的已经存在的容器

build
　　重新建造由Dockerfile构建的镜像。

ps
　　获取由Compose管理的容器的状态信息

run
　　启动一个容器，并允许一个一次性的命令。被连接的容器会同时启动，除非用了 --no-deps参数。

logs
　　汇集由Compose管理的容器的日志，并以彩色输出。

stop
　　停止容器，但不会删除它们

rm
　　删除已停止的容器。不要忘记使用-v参数来删除任何由Docker管理的数据卷

说明：

　　一个普通的工作流程以docker-compose up -d名利启动应用程序开始。docker-compose logs和ps命令可以用来验证应用程序的状态，还能帮助调试。
修改代码后，先执行docker-compose build 构建新的镜像，然后执行docker-compose up -d 取代运行中的容器。注意，Compose会保留原来容器中所有旧的数据卷，这意味着即使容器更新后，数据库和缓存也依旧在容器内（这很可能造成混淆，因此要特别小心）。
　　如果你修改了Compose的YAML文件，但不需要构建新的镜像，可以通过up -d参数使Compose以新的配置替换容器。如果想要强制停止Compose并重新创建所有容器，可以使用--force-recreate选项来达到目的。

```

## 使用样例

### Docker-Compose-es

### Docker-Compose-neo4j

## 附件

### 参考资源

- [Docker Compose Github 链接](https://github.com/docker/compose)
- [Docker Compose 官网链接](https://docs.docker.com/compose/)
