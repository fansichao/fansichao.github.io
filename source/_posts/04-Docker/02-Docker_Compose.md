---
title: Docker-Compose使用文档
url_path: docker/docker_compose
tags:
  - docker
  - module
categories:
  - docker
description: Docker-Compose 使用文档。容器快速部署。
---

## 简介

[docker compose](https://docs.docker.com/compose/) 是用来配置和运行多容器服务的工具，通过 docker-compose 命令可轻松对多个容器进行如下操作：

（1）启动，停止和重建服务

（2）查看正在运行的服务的状态

（3）通过流输出正在运行的服务的日志

（4）对某个服务执行命令

## Docker-Compose 安装

Centos7 安装 Docker-Compose

```bash
# 下载：
# https://github.com/docker/compose/releases

# 下载文件
# wget https://github.com/docker/compose/releases/download/1.26.2/docker-compose-Linux-x86_64

sudo cp docker-compose-Linux-x86_64 /usr/local/bin/docker-compose
sudo chmod a+x /usr/local/bin/docker-compose

docker-compose --version
```

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


# 启动所有容器
docker-compose -f 21-es-docker-compose.yml start

# 查看最新日志  配置文件 service 名称
docker-compose -f 21-es-docker-compose.yml logs -t -f es_client1 

# 运行命令
docker-compose -f es-docker-compose.yml up -d

# 查看 compose 日志
docker-compose  -f 12-es-docker-compose.yml  logs



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

## 常用参数

```bash
# 自动无限次重启服务
restart:always

```

## 使用样例

- 参考文档 [Docker_es](https://www.superscfan.top/docker/docker_es)

创建网络

```bash
docker network create --subnet=172.19.0.0/16 esnetwork
```

`es-docker-compose.yml` 文件内容

```yml
# 部分ES环境变量类型的参数需要使用双引号, 其他参数均可在此处映射，同时注意外部映射
# 存储目录只能是data，且需要预先创建. 若映射其他目录启动将出错.
version: "2.2"
services:
  es_master:
    image: elasticsearch:7.4.2
    container_name: 12_es_master1
    environment:
      - bootstrap.system_call_filter=false
      - node.name=12_es_master1
      - node.master=true
      - node.data=false
      - cluster.name=es-docker-cluster1
      #- discovery.seed_hosts=192.168.172.73:9300,192.168.172.73:9301,172.16.1.3:9300,172.16.1.3:9301,172.16.1.3:9302
      - discovery.seed_hosts=192.168.172.73
      - transport.publish_host=192.168.172.73
      - transport.publish_port=9300
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
      - cluster.initial_master_nodes=12_es_master1
      - Des.discovery.zen.minimum_master_nodes=1
      - "network.host:0.0.0.0"
      - http.port=9200
      - http.cors.enabled=true
      - http.cors.allow-origin="*"
      - http.publish_host=192.168.172.73
      - http.publish_port=9200
      - xpack.security.enabled:false
      - thread_pool.get.queue_size=1000
      - thread_pool.write.queue_size=1000
      - thread_pool.analyze.queue_size=1000
      - thread_pool.search.queue_size=1000
      - thread_pool.listener.queue_size=1000
      - discovery.zen.ping_timeout=120s
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - "/data_storage/12_es_master1:/usr/share/elasticsearch/data"
      - "/data_storage/es_plugins:/usr/share/elasticsearch/plugins"
    ports:
      - 192.168.172.73:9200:9200
      - 192.168.172.73:9300:9300
    networks:
      es_network:
        ipv4_address: 172.19.10.21
    # deploy:
    #   resources:
    #     limits:
    #       #cpus: '2'
    #       memory: 16G

  es_node1:
    image: elasticsearch:7.4.2
    container_name: 12_es_node1
    environment:
      - bootstrap.system_call_filter=false
      - node.name=12_es_node1
      - node.master=false
      - node.data=true
      - cluster.name=es-docker-cluster1
      #- discovery.seed_hosts=192.168.172.73:9300,192.168.172.73:9301,172.16.1.3:9300,172.16.1.3:9301,172.16.1.3:9302
      - discovery.seed_hosts=192.168.172.73
      - transport.publish_host=192.168.172.73
      - transport.publish_port=9301
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
      - cluster.initial_master_nodes=12_es_master1
      - Des.discovery.zen.minimum_master_nodes=1
      - "network.host:0.0.0.0"
      - http.port=9200
      - http.cors.enabled=true
      - http.cors.allow-origin="*"
      - http.publish_host=192.168.172.73
      - http.publish_port=9201
      - xpack.security.enabled:false
      - thread_pool.get.queue_size=1000
      - thread_pool.write.queue_size=1000
      - thread_pool.analyze.queue_size=1000
      - thread_pool.search.queue_size=1000
      - thread_pool.listener.queue_size=1000
      - discovery.zen.ping_timeout=120s
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - "/data_storage/12_es_node1:/usr/share/elasticsearch/data"
      - "/data_storage/es_plugins:/usr/share/elasticsearch/plugins"
    ports:
      - 192.168.172.73:9201:9200
      - 192.168.172.73:9301:9300
    networks:
      es_network:
        ipv4_address: 172.19.10.41
    # deploy:
    #   resources:
    #     limits:
    #       #cpus: '2'
    #       memory: 16G
    # 添加 --compatibility 参数运行

# 使用现成的桥接网络，指定名称即可
networks:
  es_network:
    external:
      name: esnetwork
```

更新容器

```bash
docker-compose  -f es-docker-compose.yml up -d
```

## 附件

### 参考资源

- [Docker Compose Github 链接](https://github.com/docker/compose)
- [Docker Compose 官网链接](https://docs.docker.com/compose/)
