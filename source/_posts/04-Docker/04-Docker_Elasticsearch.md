---
title: Docker-Elasticsearch 部署文档
url_path: docker/docker_es
tags:
  - docker
  - module
categories:
  - docker
description: Docker-Elasticsearch 部署文档. 分布式数据库
---

## Docker-ES 部署

### 宿主机部署

解压即用

### 使用 Docker-Compose 部署配置样例

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

## ES-配置

详见 [Es-配置](https://superscfan.top/module/es/config)
