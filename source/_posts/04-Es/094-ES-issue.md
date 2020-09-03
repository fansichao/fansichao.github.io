---
title: ES问题记录
url_path: module/es/issue
tags:
  - Module
  - Elasticsearch
categories:
  - Elasticsearch
description: ES问题记录
---

## 问题记录

### illegal_argument_exception [indices:admin/create]

问题日志

```bash
[2020-08-04 23:15:22,145] PID:7703-elasticsearch: [base.py-log_request_fail-244] WARNING: PUT http://192.168.101.73:9200/cust-daily-2010-08-06 [status:400 request:0.057s]
Traceback (most recent call last):
  File "tools.py", line 977, in <module>
    system_command()
  File "tools.py", line 973, in system_command
    tools_dispatcher(*opt_parser.parse_args())
  File "tools.py", line 832, in tools_dispatcher
    func(*opargs)
  File "tools.py", line 329, in make_mining_entity
    main_processer(date2str(run_dt, '%Y%m%d'), run_entity)
  File "/data/trunk/src/server/fdm/mining/model_entity.py", line 194, in main_processer
    set_indice(index_prefix, index_columns, doc_type='cust')
  File "/data/trunk/src/server/fdm/mining/mining_tools.py", line 58, in set_indice
    _es.indices.create(index=index_name, body={"settings": {"number_of_shards": Config.ES_NUMBER_OF_SHARDS, "number_of_replicas": Config.ES_NUMBER_OF_REPLICAS}},
  File "/data/trunk/src/server/fdm/database/es.py", line 76, in create
    return self.indices.create(*args, **kwargs)
  File "/home/fdm/env/lib/python3.8/site-packages/elasticsearch/client/utils.py", line 92, in _wrapped
    return func(*args, params=params, headers=headers, **kwargs)
  File "/home/fdm/env/lib/python3.8/site-packages/elasticsearch/client/indices.py", line 102, in create
    return self.transport.perform_request(
  File "/home/fdm/env/lib/python3.8/site-packages/elasticsearch/transport.py", line 355, in perform_request
    status, headers_response, data = connection.perform_request(
  File "/home/fdm/env/lib/python3.8/site-packages/elasticsearch/connection/http_urllib3.py", line 252, in perform_request
    self._raise_error(response.status, raw_data)
  File "/home/fdm/env/lib/python3.8/site-packages/elasticsearch/connection/base.py", line 281, in _raise_error
    raise HTTP_EXCEPTIONS.get(status_code, TransportError)(
elasticsearch.exceptions.RequestError: RequestError(400, 'illegal_argument_exception', '[22_es_master1][172.16.10.21:9300][indices:admin/create]')
```

解决方案

```bash
# ES数据清空后，此设置会丢失。

默认分片数1000,太少，导致后续数据无法创建。

# 修改最大分片数量
curl -XPUT 'http://xxx.xxx.xxx.xxx:9200/_cluster/settings'  -H 'Content-Type: application/json' -d '
{
  "transient": {
    "cluster": {
      "max_shards_per_node": 100000000
    }
  }
}
'
```

### search.max_open_scroll_context

错误信息

```bash
Trying to create too many scroll contexts. Must be less than or equal to: [500]. This limit can be set by changing the [search.max_open_scroll_context] setting
```

解决方案

```bash
# ES数据清空后，此设置会丢失。


# 方案1 - 增加滚动设置()
curl -X PUT http://192.168.101.71:9200/_cluster/settings -H 'Content-Type: application/json' -d '{
    "persistent" : {
        "search.max_open_scroll_context": 100000000
    },
    "transient": {
        "search.max_open_scroll_context": 100000000
    }
}'

# 方案2 - 使用滚动后清除
滚动超时后，会自动清理，不建议使用后清理。



# 查看当前滚动数
GET /_nodes/stats/indices/search
```

- [request-body-search-scroll](https://www.elastic.co/guide/en/elasticsearch/reference/7.6/search-request-body.html#request-body-search-scroll)

```bash
# 运行样例
[fdm@data1 ~]$ curl   -X PUT http://192.168.101.71:9200/_cluster/settings -H 'Content-Type: application/json' -d '{
>     "persistent" : {
>         "search.max_open_scroll_context": 10240
>     },
>     "transient": {
>         "search.max_open_scroll_context": 10240
>     }
> }'
{"acknowledged":true,"persistent":{"search":{"max_open_scroll_context":"10240"}},"transient":{"search":{"max_open_scroll_context":"10240"}}}
```

### driver failed programming external connectivity on endpoint

[参考链接](https://blog.csdn.net/whatday/article/details/86762264)

centos7.6，启动 docker 后，关闭防火墙，再开启容器导致此问题

重启 docker 服务即可解决问题

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

ERROR: for 21_es_master1  Cannot start service es_master1: driver failed programming external connectivity on endpoint 21_es_master1 (0d57a32139e6dc12a2e974ac98e23bd661fa6f8f72713dd6cc787d6d09319440):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 192.168.101.71 --dport 9300 -j DNAT --to-destination 172.16.10.21:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))
Creating 21_es_client1 ... error

ERROR: for 21_es_client1  Cannot start service es_client1: driver failed programming external connectivity on endpoint 21_es_client1 (cdc46a8f940337636e4baade076b41f78bc0527931268a02a4e1afd74343812c):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 192.168.101.71 --dport 9301 -j DNAT --to-destination 172.16.10.31:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))

ERROR: for es_node1  Cannot start service es_node1: driver failed programming external connectivity on endpoint 21_es_node1 (e6225dd9ae28ab432bc89cc6c9db97a62045efbd0207a6a0d737181b4222782a):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 192.168.101.71 --dport 9302 -j DNAT --to-destination 172.16.10.41:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))

ERROR: for es_master1  Cannot start service es_master1: driver failed programming external connectivity on endpoint 21_es_master1 (0d57a32139e6dc12a2e974ac98e23bd661fa6f8f72713dd6cc787d6d09319440):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 192.168.101.71 --dport 9300 -j DNAT --to-destination 172.16.10.21:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))

ERROR: for es_client1  Cannot start service es_client1: driver failed programming external connectivity on endpoint 21_es_client1 (cdc46a8f940337636e4baade076b41f78bc0527931268a02a4e1afd74343812c):  (iptables failed: iptables --wait -t nat -A DOCKER -p tcp -d 192.168.101.71 --dport 9301 -j DNAT --to-destination 172.16.10.31:9300 ! -i br-728aec2b9277: iptables: No chain/target/match by that name.
 (exit status 1))
ERROR: Encountered errors while bringing up the project.

```

### Elasticsearch is still initializing the Monitoring indices

```bash
# 删除监控索引， 重启 Kibana 即可
DELETE .monitor*
DELETE .kibana
DELETE .watch*
DELETE .triggered_watches
```

### Shard UNASSIGNED 修复(常见问题)

背景介绍

- 大数据量的 ES 集群中，对节点做配置更新或增减集群(未关闭节点自动均衡)，或者出现节点异常情况时，会发生此问题。

获取集群状态

```bash
[fdm@data1 ~]$ curl -XGET http://172.16.2.1:9200/_cluster/health\?pretty
{
  "cluster_name" : "es-docker-cluster2",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 9,
  "number_of_data_nodes" : 5,
  "active_primary_shards" : 13674,
  "active_shards" : 14936,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 12412,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 1,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 54.61459704548779
}

# 查看节点健康，可以看到 当前已分配的百分比
curl 192.168.106.58:9200/_cat/nodes?v
 
# 查看所有分片情况
curl 192.168.106.58:9200/_cat/shards?v
```

解决方案

```bash
# 方法1
对于非必要的索引，或者需要重新跑批的索引，可以将其副本数设置为0，从而避免此部分索引的分配，可以极大减少 分配时间，


# 方法2
通过/_cat/shards接口看看具体是哪个primary shard没分配，通过reroute接口强制分配下去，就可以变成yellow了。
Green：所有主分片和副本分片都可用；
Yellow：所有主分片可用，但不是所有副本分片都可用；
Red：不是所有的主分片都可用。


http://blog.csdn.net/hereiskxm/article/details/45717573
```

总结
在做集群更新时，务必先关闭集群的自动均衡

```bash
# 停止集群自动分配
curl -XGET 'http://192.168.17.201:9200/_cluster/settings' -d '{"transient" : {"cluster.routing.allocation.enable" : "none"}}'1 #
```

### 1.EsRejectedExecutionException

```bash
error: failure in bulk execution:[4]: index [teacher.tis1.teacher], type [teacher_comment], id [1265687], message [RemoteTransportException[[node-1][192.168.4.30:9300][indices:data/write/bulk[s][p]]]; nested: EsRejectedExecutionException[rejected execution of org.elasticsearch.transport.TransportService$7@5f21ed47 on EsThreadPoolExecutor[bulk, queue capacity = 50, org.elasticsearch.common.util.concurrent.EsThreadPoolExecutor@18160e59[Running, pool size = 4, active threads = 4, queued tasks = 50, completed tasks = 6362]]];]
```

原因: 说明 ES 索引数据的速度已经跟不上 client 端发送 bulk 请求的速度，请求队列已满以致开始拒绝新的请求。 这是 ES 集群的自我保护机制。可以适当睡眠一段时间或者将队列设置大点。默认设置是 bulk thead pool set queue capacity =50 可以设置大点。

解决办法：打开 elasticsearch.yml 在末尾加上
```bash
threadpool:
bulk:
type: fixed
size: 60
queue_size: 1000
```
重新启动服务即可
### 2.DocumentMissingException

```bash
error: [[teacher.tis1.teacher/YudbzduURsGhxHMRzyfNcA][teacher.tis1.teacher][1]] DocumentMissingException[[teacher][344]: document missing]]
```
原因: 找不到文档，可能是索引(index)或者类型(type)名称错误导致找不到文档，或者文档记录不存在时更新索引则报错。比如：更新 id 为 414 的记录，而此时 ES 中不存在 id 为 414 记录的数据，则抛出此异常
解决办法：

1.检查索引(index)名称是否正确 2.检查类型(type)名称是否正确 3.记录不存在时更新索引则报错 可以在更新索引是使用 upsert 属性，如果不存在则进行创建。代码如下：
IndexRequest indexRequest = new IndexRequest(index, type, id).source(jsonSource);
UpdateRequest updateRequest = new UpdateRequest(index, type, id).doc(jsonSource).upsert(indexRequest);3.RemoteTransportException:
error: org.elasticsearch.transport.RemoteTransportException: Failed to deserialize exception response from stream
原因: es 节点之间的 JDK 版本不一样
解决办法：统一 JDK 环境 

### 4.NoNodeAvailableException:
error: org.elasticsearch.client.transport.NoNodeAvailableException: No node available

原因: 节点不可用，
(1) es client 与 java client 的版本不一致
(2)端口号错误
(3)集群名字错误
(4)jar 包引用版本不匹配
解决办法：

1.检查 es client 与 java client 的版本是否一致 目前我们项目中使用的是 java1.8 对应 es5.5.2 2.检查端口号是否正确 使用 client 连接应使用 es 的 transport 端口号 3.检查集群名称是否正确 4.检查 es 与 es client 的版本号是否一致 目前我们项目中使用的均为 5.5.2

## 相关资源

- [ES 常见问题整理 - 蘇氏加多寶 - 博客园](https://www.cnblogs.com/lwhctv/p/12327627.html)
- [常见错误整理 - CSDN 博客](https://app.yinxiang.com/shard/s66/nl/15497112/dbb8023a-f8ee-4670-8e7e-33ecc5dcfbae)
