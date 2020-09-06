---
title: ES 常用命令
url_path: module/es/cmd
tags:
  - module
  - Elasticsearch
categories:
  - module
  - es
description: ES 常用命令
---

## ES 命令

## 基础命令

```bash
# 查看API
[root@540d820ba866 ~]# curl -XGET 'http://192.168.100.200:7403/_cat/'
=^.^=
/_cat/allocation
/_cat/shards
/_cat/shards/{index}
/_cat/master
/_cat/nodes
/_cat/tasks
/_cat/indices
/_cat/indices/{index}
/_cat/segments
/_cat/segments/{index}
/_cat/count
/_cat/count/{index}
/_cat/recovery
/_cat/recovery/{index}
/_cat/health
/_cat/pending_tasks
/_cat/aliases
/_cat/aliases/{alias}
/_cat/thread_pool
/_cat/thread_pool/{thread_pools}
/_cat/plugins
/_cat/fielddata
/_cat/fielddata/{fields}
/_cat/nodeattrs
/_cat/repositories
/_cat/snapshots/{repository}
/_cat/templates
```

## 常用命令

```bash
# 查看 ES 相关命令 ?v 查看表头 ?pretty 美化输出
curl -XGET 'http://191.110.110.53:9200/_cat'

# 查看集群健康
curl -XGET 'http://191.110.110.53:9200/_cat/health?v'

# 查看磁盘空间占用率
_cat/nodes?v&h=ip,heap.percent,ram.percent,cpu,load_1m,load_5m,load_15m,node.role,master,name,disk.used_percent

# 显示red shards，显示异常分片
http://<yourhost>:9200/_cluster/health/?level=shards


#  修改集群副本数
curl -XPUT 'http://191.110.110.53:9200/peer-tran-log-2016-01-21/_settings' -d '{"number_of_replicas":1}'

# 获取所有节点信息：
curl -XGET 'http://localhost:9200/_nodes';

# 获取所有索引的信息
curl -XGET 127.0.0.1:9200/_cat/indices

# 显示各节点的进程数
curl -XGET 'http://191.110.110.61:9200/_cat/thread_pool?v'

# 显示示不同索引的分片情况
curl -XGET 'http:/191.110.110.61:9200/_cat/shards?v'

# 显示索引的详细情况
curl -XGET 'http:/191.110.110.61:9200/_cat/indices?v'


# 显示副本的详细情况
curl -XGET 'http:/191.110.110.61:9200/_cat/recovery?v'


# 删除无用数据
time curl -XPOST 'http://191.110.110.53:9200/tranjrnl-01000000-2016-10-31/_forcemerge?max_num_segments=1'

# 一次性删除所有无用数据
curl -XPOST 'http://191.110.110.53:9200/_forcemerge?only_expunge_deletes=true' ;

# 统计yellow索引数量
curl -XGET 'http://191.110.110.53:9200/_cat/indices?v&health=yellow' | wc -l



# 开启节点分配自动均衡
curl -XPUT http://191.110.110.53:9200/_cluster/settings -d '
{
  "transient" : {
    "cluster.routing.allocation.enable" : "all"
    }
}'
```






## ES 语法

### 基础语法

### 常用语法

```bash
# ES564 精准查询 模糊字段(中文分词字段)
"query_string": {
  "default_field": "CARD_NO",
  "query": "45*"
}

```

### 常用命令 1

```bash



# 监听端口是否存活 yum install -y telnet
[root@540d820ba866 ~]# telnet 192.168.100.200 7413
Trying 192.168.100.200...
Connected to 192.168.100.200.
Escape character is '^]'.
Connection closed by foreign host.

# 查看集群状态
[root@540d820ba866 ~]# curl -XGET 'http://192.168.100.200:7403/_cluster/state?pretty'
{
  "error" : {
    "root_cause" : [
      {
        "type" : "master_not_discovered_exception",
        "reason" : null
      }
    ],
    "type" : "master_not_discovered_exception",
    "reason" : null
  },
  "status" : 503
}
```
