---
title: ES部署文档
url_path: module/es/install
tags:
  - Module
  - Elasticsearch
categories:
  - Module
description: ES部署文档
---

## 部署文档

### ES740

**环境说明:**

- CentOS8.1.19
- version: ES7.4.0
- 分词、拼音、python 的 elasticsearch 必须和 ES740 版本对应，否则可能存在使用异常情况。

#### 系统依赖

[ES 官网系统配置](https://www.elastic.co/guide/en/elasticsearch/reference/7.4/system-config.html)

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

#### 简单部署

解压即用，ES7.4 自带 java 环境，无需安装 java 环境。

文件详见 `/03-常用工具/01-部署软件/es74.zip`

```bash
# 获取 ES740 安装包
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.0-linux-x86_64.tar.gz
# 安装 对应版本 拼音插件
# 安装 对应版本 分词插件
```

#### 服务启停

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
http://0.0.0.0:9200
# Kibana 界面
http://0.0.0.0:5601
```

#### 配置文件

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
http.port: 9200
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
server.port: 5601
elasticsearch.hosts: ["http://0.0.0.0:9200"]
```

### 564 部署文档

**环境说明:**

- CentOS8.1.19
- version: ES7.4.0
- 分词、拼音、python 的 elasticsearch 必须和 ES 版本对应，否则可能存在使用异常情况。
- ES5.6.4 x-pack 收费,只能试用一个月
- ES5.6.4 和 Es7.4.0 存在较大语法差异，详见 [ES 版本差异对比](B-ES版本差异对比.md)

部署依赖

- 系统参数依赖
- JDK1.8+依赖

```bash
# 下载 5.6.4 文件
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.4.tar.gz
```
