---
title: Module-ES-740部署文档
url_path: module/es/install2
tags:
  - Module
  - Elasticsearch
categories:
  - Module
description: ....
---

tags: `2020年` `05月` `elasticsearch`

**环境说明:**

- CentOS8.1.19
- version: ES7.4.0
- 分词、拼音、python 的 elasticsearch 必须和 ES740 版本对应，否则可能存在使用异常情况。

## 安装部署

### 系统依赖


[ES官网系统配置](https://www.elastic.co/guide/en/elasticsearch/reference/7.4/system-config.html)


修改系统参数

```bash
# 修改文件 vi /etc/sysctl.conf
vm.max_map_count=655360
 

# 修改文件  vi /etc/security/limits.d/90-nproc.conf(文件名称可能存在差异, 文件不存在则不用修改)
找到如下内容：
soft nproc 1024
修改为
soft nproc 2048

# 修改文件 vim /etc/security/limits.conf, 添加如下内容
*                soft    nofile          65536
*                hard    nofile          65536

# 执行命令使其生效
sysctl -p

# 查看是否生效
ulimit -Hn # 显示 65536 则表示修改成功

# 特别说明，已有用户必须重新登录，重新连接ssh, 避免不生效的情况
```

### 简单部署

解压即用，ES7.4 自带 java 环境，无需安装 java 环境。

文件详见 `/03-常用工具/01-部署软件/es74.zip`

### 详细部署

```bash
# 获取 ES740 安装包
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.0-linux-x86_64.tar.gz
# 安装 对应版本 拼音插件
# 安装 对应版本 分词插件
```

## 部署后配置

### 服务启停

`ES740`的`restart.sh`软件

```bash
source ~/.bash_profile
echo ">> Restart Elasticsearch74 starting..."
echo "> Stop Es and Kibana ..."
ps anx | grep cli | grep -v grep| awk '{print $1}' | xargs kill -15
ps anx | grep elasticsearch | grep -v grep| awk '{print $1}' | xargs kill -15

echo "> Start Es and Kibana ..."
su - es -lc "cd /home/es/es/node_noly && bin/elasticsearch -d"
su - es -lc "cd /home/es/es/kibana && nohup bin/kibana &"
echo ">> Restart Elasticsearch74 end..."
```

可视化界面展示

```bash
# ES 界面
http://0.0.0.0:7401
# Kibana 界面
http://0.0.0.0:7402
```

### 配置文件

ES 的配置文件 `elasticsearch.yml`

```bash
# bootstrap
bootstrap.system_call_filter: false
# name
cluster.name: es74_cluste
node.name: node-only
# node
node.master: true
node.data: true
node.max_local_storage_nodes: 3
#node.zone: zone_one
# path
path.data: /data/data
path.logs: /data/logs
# host&port
network.host: 0.0.0.0
http.port: 7401
http.cors.enabled: true
http.cors.allow-origin: '*'
# xpack
xpack.security.enabled: false
# cluster zone
cluster.routing.allocation.awareness.attributes: zone
node.attr.zone: zone_two
#discovery.zen.minimum_master_nodes: 2
#http.max_content_length: 500mb
#
#thread_pool.bulk.queue_size: 5000

# discovery.seed_hosts: ["192.168.100.200"]
discovery.seed_hosts: ["0.0.0.0"]
cluster.initial_master_nodes: ["node-only"]
```

Kibana 的配置文件

```bash
server.host: "0.0.0.0"
server.port: 7402
elasticsearch.hosts: ["http://0.0.0.0:7401"]
```

### 增加分片数量

ES740 必须配置分片数量，避免分片过少，导致项目程序运行报错。

```bash
# 在kibana界面中更新
PUT _cluster/settings
{
  "transient": {
    "cluster": {
      "max_shards_per_node": 10000
    }
  }
}
# 直接更新
curl -XPUT 'http://0.0.0.0:7401/_cluster/settings'  -H 'Content-Type: application/json' -d '
{
  "transient": {
    "cluster": {
      "max_shards_per_node": 50000
    }
  }
}
'
```

#### es问题记录 driver failed programming external connectivity on endpoint
https://blog.csdn.net/whatday/article/details/86762264

centos7.6，启动docker后，关闭防火墙，再开启容器导致此问题

重启docker服务即可解决问题

```bash
[fdm@data1 es]$ docker-compose -f 21-es-docker-compose.yml up -d
Creating 21_es_master1 ... 
Creating 21_es_node1   ... 
Creating 21_es_node1   ... error
WARNING: Host is already in use by another container

ERROR: for 21_es_node1  Cannot start service es_node1: driver failed programming external connectivity on endpoint 21_es_node1 (e6225dd9ae28ab432bc89cc6c9db97a62045efbd0207a6a0d737181b4222782a):  (iptables failed: iptables --wait -t nat 
Creating 21_es_master1 ... error
 (exit status 1))
WARNING: Host is already in use by another container

ERROR: for 21_es_master1  Cannot start service es_master1: driver failed programming external connectivity on endpoint 21_es_master1 (0d57a32139e6dc12a2e974ac98e23bd661fa6f8f72713dd6cc787d6d09319440):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 172.16.2.1 --dport 9300 -j DNAT --to-destination 172.16.10.21:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))
Creating 21_es_client1 ... error

ERROR: for 21_es_client1  Cannot start service es_client1: driver failed programming external connectivity on endpoint 21_es_client1 (cdc46a8f940337636e4baade076b41f78bc0527931268a02a4e1afd74343812c):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 172.16.2.1 --dport 9301 -j DNAT --to-destination 172.16.10.31:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))

ERROR: for es_node1  Cannot start service es_node1: driver failed programming external connectivity on endpoint 21_es_node1 (e6225dd9ae28ab432bc89cc6c9db97a62045efbd0207a6a0d737181b4222782a):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 172.16.2.1 --dport 9302 -j DNAT --to-destination 172.16.10.41:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))

ERROR: for es_master1  Cannot start service es_master1: driver failed programming external connectivity on endpoint 21_es_master1 (0d57a32139e6dc12a2e974ac98e23bd661fa6f8f72713dd6cc787d6d09319440):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 172.16.2.1 --dport 9300 -j DNAT --to-destination 172.16.10.21:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))

ERROR: for es_client1  Cannot start service es_client1: driver failed programming external connectivity on endpoint 21_es_client1 (cdc46a8f940337636e4baade076b41f78bc0527931268a02a4e1afd74343812c):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 172.16.2.1 --dport 9301 -j DNAT --to-destination 172.16.10.31:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))
ERROR: Encountered errors while bringing up the project.

```

