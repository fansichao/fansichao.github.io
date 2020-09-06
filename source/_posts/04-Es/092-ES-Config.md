---
title: ES配置文件
url_path: module/es/config
tags:
  - module
  - Elasticsearch
categories:
  - module
  - es
description: ES配置文件详解
---

环境说明:

- ES7.4.0 [官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/7.4/)

## 系统配置项说明

### Disable swap 以提升性能(可选)

```bash
# 方法1 临时禁用，无需重启ES节点, 永久禁用它，您将需要编辑/etc/fstab文件并注释掉所有包含单词的行swap
sudo swapoff -a

# 方法2 配置系统参数，减少了内核的交换
vm.swappiness=1

# 方法3 配置es参数，需要重启ES节点
bootstrap.memory_lock: true
```

### 修改文件描述符数量(必选)

```bash
# 临时修改
ulimit -n 65535

# 永久修改
/etc/security/limits.conf
增加 nofile to 65535

# 检查ES是否配置正常
curl -X GET "localhost:9200/_nodes/stats/process?filter_path=**.max_file_descriptors&pretty"
```

### 虚拟内存数量(必选)

```bash
# 临时修改
sysctl -w vm.max_map_count=262144

# 永久修改
/etc/sysctl.conf 中增加
vm.max_map_count=262144
sysctl -p 使其生效
```

### 线程数量(必选)

```bash
# 临时设置
ulimit -u 4096

# 永久设置
/etc/security/limits.conf
nproc to 4096 in /etc/security/limits.conf
```

### DNS 缓存设置(可选)

```bash
networkaddress.cache.ttl=<timeout>
networkaddress.cache.negative.ttl=<timeout>
```

## ES 配置项说明

### 增加分片数量(必选)

ES740 必须配置分片数量，避免分片过少，导致项目程序运行报错。

```bash
# 直接更新
curl -XPUT 'http://0.0.0.0:9200/_cluster/settings'  -H 'Content-Type: application/json' -d '
{
  "transient": {
    "cluster": {
      "max_shards_per_node": 50000
    }
  }
}
'
```

### 增加 scroll 数量(生产必选)

```bash
# scroll 使用 24小时后自动回收. 默认1000
方案1 - 增加滚动设置()
curl -X PUT http://192.168.101.71:9200/_cluster/settings -H 'Content-Type: application/json' -d '{
    "persistent" : {
        "search.max_open_scroll_context": 100000000
    },
    "transient": {
        "search.max_open_scroll_context": 100000000
    }
}'

```

### 磁盘使用量在 95%以上时，索引会被标记为已读，无法写入数据(可选)

```python
flood stage disk watermark [95%] exceeded on [KeyWFmZzQdy101sSic1ilA][node-only][/ssd_datapath/data/nodes/0] free: 42.3gb[4.6%], all indices on this node will be marked read-only
```

**解决方法:** 通过 kibana 修改磁盘使用上限为 99%

```python
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.disk.watermark.low": "99%",
    "cluster.routing.allocation.disk.watermark.high": "99%",
    "cluster.routing.allocation.disk.watermark.flood_stage": "99%",
    "cluster.info.update.interval": "1m"
  }
}
```

### ES 进程数修改(必选)

```bash
# 默认 100
- thread_pool.get.queue_size=1000
- thread_pool.write.queue_size=1000
- thread_pool.analyze.queue_size=1000
- thread_pool.search.queue_size=1000
- thread_pool.listener.queue_size=1000
```

### 待测试配置

```bash
# 任何的元数据变动都会涉及集群更新，设置该参数
# 默认 30 s
discovery.zen.commit_timeout

# 集群健康的检查参数
# default 3 s
dicovery.zen.ping_timeout

# 以下配置可以减少，当ES节点短时间重启或宕机导致的shards重新分配带来的IO浪费
# ES-Version 5.6.4
discovery.zen.fd.ping_timeout: 180s
discovery.zen.fd.ping_retries: 6
discovery.zen.fd.ping_interval: 30s
discovery.zen.ping_timeout: 120s
```

### 修改 ES 内存大小(生产必选配置)

修改 config/jvm.options 文件

```python
# 根据实际修改，默认1g 两个值必须相同, 不能超过32G
-Xms2g
-Xmx2g
```

建议的配置如下：

将最小堆大小（Xms）和最大堆大小（Xmx）设置为彼此相等。

Elasticsearch 可用的堆越多，它可用于缓存的内存就越多。但请注意，过多的堆可能会陷入长时间的垃圾收集暂停。所以设置的堆不能太大， 尽量设置到内存的 50%。

将 Xmx 设置为不超过物理 RAM 的 50％，以确保有足够的物理内存给内核文件系统缓存。

内存 heap size 配置不要超过 32G, 基本上大多数系统最多只配置到 26G.

## ES 参数说明

文件 `config/elasticsearch.yml` 参数配置说明

```bash

#修改以下项
#表示集群标识，同一个集群中的多个节点使用相同的标识
cluster.name: elasticsearch
#节点名称
node.name: "es-node1"
#数据存储目录
path.data: /data/elasticsearch1/data
#日志目录
path.logs: /data/elasticsearch1/logs
#节点所绑定的IP地址，并且该节点会被通知到集群中的其他节点
network.host: 192.168.1.11
#绑定监听的网络接口，监听传入的请求，可以设置为IP地址或者主机名
network.bind_host: 192.168.1.11
#发布地址，用于通知集群中的其他节点，和其他节点通讯，不设置的话默认可以自动设置。必须是一个存在的IP地址
network.publish_host: 192.168.1.11
#es7.x 之后新增的配置，初始化一个新的集群时需要此配置来选举master
cluster.initial_master_nodes: ["192.168.1.11"]
#集群通信端口
transport.tcp.port: 9300
#对外提供服务的http端口，默认为9200
http.port: 9200
#集群中主节点的初始列表，当主节点启动时会使用这个列表进行非主节点的监测
discovery.zen.ping.unicast.hosts: ["192.168.1.11:9300","192.168.1.12:9300"]
#下面这个参数控制的是，一个节点需要看到的具有master节点资格的最小数量，然后才能在集群中做操作。官方推荐值是(N/2)+1；
#其中N是具有master资格的节点的数量（我们的情况是2，因此这个参数设置为1)
#但是：但对于只有2个节点的情况，设置为2就有些问题了，一个节点DOWN掉后，肯定连不上2台服务器了，这点需要注意
discovery.zen.minimum_master_nodes: 1
#集群ping过程的超时
discovery.zen.ping_timeout: 120s
#客户端连接超时
client.transport.ping_timeout: 60s
#cache缓存大小，10%（默认），可设置成百分比，也可设置成具体值，如256mb。
indices.queries.cache.size: 20%
#索引期间的内存缓存，有利于索引吞吐量的增加。
indices.memory.index_buffer_size: 30%
#开启了内存地址锁定，为了避免内存交换提高性能。但是Centos6不支持SecComp功能，启动会报错，所以需要将其设置为false
bootstrap.memory_lock: true
bootstrap.system_call_filter: false
#设置该节点是否具有成为主节点的资格以及是否存储数据。
node.master: true
node.data: true
#ElasticSearch 更改search线程池，search 线程设置过小导致程序崩溃
thread_pool.search.queue_size: 1000
#queue_size允许控制没有线程执行它们的挂起请求队列的初始大小。
thread_pool.search.size: 200
#size参数控制线程数，默认为核心数乘以5。
thread_pool.search.min_queue_size: 10
#min_queue_size设置控制queue_size可以调整到的最小量。
thread_pool.search.max_queue_size: 1000
#max_queue_size设置控制queue_size可以调整到的最大量。
thread_pool.search.auto_queue_frame_size: 2000
#auto_queue_frame_size设置控制在调整队列之前进行测量的操作数。它应该足够大，以便单个操作不会过度偏向计算。
thread_pool.search.target_response_time: 6s
#target_response_time是时间值设置，指示线程池队列中任务的目标平均响应时间。如果任务通常超过此时间，则将调低线程池队列以拒绝任务。


# 增加以下内容
# 集群名称必须相同
cluster.name: es-test

node.name: node-3
# 当前节点是否可以被选举为master节点，是：true、否：false
node.master: true
# 当前节点是否用于存储数据，是：true、否：false
node.data: true

# 数据和日志存储的地方，建议与es的安装目录区分，方式es删除后数据的丢失
path.data: /data/es/data
path.logs: /data/es/logs

# 需求锁住物理内存，是：true、否：false
bootstrap.memory_lock: false

# SecComp检测，是：true、否：false
bootstrap.system_call_filter: false

network.host: 0.0.0.0
# 有些时候并不需要此配置，我的没有设置
network.publish_host: 10.240.0.8

# 主机访问的端口号
http.port: 9200

# es7.x 之后新增的配置，写入候选主节点的设备地址，在开启服务后可以被选为主节点
# es7之后，不需要discover.zen.ping.unicast.hosts这个参数，用discovery.seed_hosts替换
discovery.seed_hosts: ["10.10.10.1","10.10.10.2","10.10.10.3"]

# es7.x 之后新增的配置，初始化一个新的集群时需要此配置来选举master
cluster.initial_master_nodes:["10.10.10.1","10.10.10.2","10.10.10.3"]

# 是否支持跨域，是：true，在使用head插件时需要此配置
http.cors.enabled: true

# "*" 表示支持所有域名
http.cors.allow-origin: "*"
```

### ES 配置文件

[ES7.4 官网配置详细说明](https://www.elastic.co/guide/en/elasticsearch/reference/7.4/settings.html)

```bash

# 数据和日志路径设置 数据支持存放在多个目录下
path:
  logs:
    - /var/log/elasticsearch
  data:
    - /mnt/elasticsearch_1
    - /mnt/elasticsearch_2
    - /mnt/elasticsearch_3
# 集群名称 决定是否所属于统一集群
cluster.name: logging-prod
# 节点名称 节点唯一标识，集群内节点名称唯一
node.name: prod-data-2
# 网络地址 此节点的网络地址
# 单节点时绑定到回环地址0.0.0.0即可，集群时需要绑定到非回环地址，内网IP
# 也可设置特殊值，_local_，_site_，_global_等，设置特殊值后，自动升级为生产模式，日志从警告升级为异常
network.host: 192.168.1.10
# es7.x 之后新增的配置，写入候选主节点的设备地址，在开启服务后可以被选为主节点
# es7之后，不需要discover.zen.ping.unicast.hosts这个参数，用discovery.seed_hosts替换
# Elasticsearch将绑定到可用的环回地址，并将扫描本地端口9300至9305
discovery.seed_hosts: ["10.10.10.1","10.10.10.2","10.10.10.3"]

# 集群初始化引导步骤，列出有资质的master节点，从中选举，初始化时需要。
# es7.x 之后新增的配置，初始化一个新的集群时需要此配置来选举master
cluster.initial_master_nodes:["10.10.10.1","10.10.10.2","10.10.10.3"]
```

## 附件

### ES 说明

```bash

Elasticsearch保留端口9300-9400用于集群通信，而端口9200-9300保留用于访问Elasticsearch API

出现master not discovered异常的根本原因是节点无法在端口9300上相互ping通。这需要同时进行。即node1应该能够在9300上ping node2，反之亦然


```
