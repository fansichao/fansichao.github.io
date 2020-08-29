---
title: Module-ES-版本差异对比
url_path: module/es/es_version
tags:
  - Module
  - Elasticsearch
categories:
  - Module
description: ....
---

ES564 & ES740 差异对比分析

## 官方版本迭代说明

### 6.0.0 版本

2017 年 8 月 31 日发布，重要特性：

1. 稀疏性 Doc Values 的支持
2. Index sorting，即索引阶段的排序。
3. 顺序号的支持，每个 es 的操作都有一个顺序编号（类似增量设计）
4. 无缝滚动升级
5. Removal of types，在 6.0 里面，开始不支持一个 index 里面存在多个 type
6. Index-template inheritance，索引版本的继承，目前索引模板是所有匹配的都会合并，这样会造成索引模板有一些冲突问题， 6.0 将会只匹配一个，索引创建时也会进行验证
7. Load aware shard routing， 基于负载的请求路由，目前的搜索请求是全节点轮询，那么性能最慢的节点往往会造成整体的延迟增加，新的实现方式将基于队列的耗费时间自动调节队列长度，负载高的节点的队列长度将减少，让其他节点分摊更多的压力，搜索和索引都将基于这种机制。
8. 已经关闭的索引将也支持 replica 的自动处理，确保数据可靠。

### 7.0.0 版本

2019 年 4 月 10 日发布，重要特性：

1. 集群连接变化：TransportClient 被废弃
2. ES 程序包默认打包 jdk
3. Lucene9.0
4. 重大改进-正式废除单个索引下多 Type 的支持 es6 时，官方就提到了 es7 会删除 type，并且 es6 时已经规定每一个 index 只能有一个 type。在 es7 中使用默认的\_doc 作为 type，官方说在 8.x 版本会彻底移除 type。 api 请求方式也发送变化，如获得某索引的某 ID 的文档：GET index/\_doc/id 其中 index 和 id 为具体的值
5. 7.1 开始，Security 功能免费使用
6. ECK-ElasticSearch Operator on Kubernetes
7. 引入了真正的内存断路器，它可以更精准地检测出无法处理的请求，并防止它们使单个节点不稳定
8. Zen2 是 Elasticsearch 的全新集群协调层，提高了可靠性、性能和用户体验，变得更快、更安全，并更易于使用
9. 新功能
   - New Cluster coordination
   - Feature - Complete High Level REST Client
   - Script Score Query
10. 性能优化
    - Weak-AND 算法提高查询性能
    - 默认的 Primary Shared 数从 5 改为 1，避免 Over Sharding
    - 更快的前 k 个查询
    - 间隔查询(Intervals queries) 某些搜索用例（例如，法律和专利搜索）引入了查找单词或短语彼此相距一定距离的记录的需要。 Elasticsearch 7.0 中的间隔查询引入了一种构建此类查询的全新方式，与之前的方法（跨度查询 span queries）相比，使用和定义更加简单。 与跨度查询相比，间隔查询对边缘情况的适应性更强。

## 安装区别

### 配置文件

- 74 版本不支持 thread_pool.bulk.queue_size 参数
- 74 版本必须“discovery.seed_hosts”以及“cluster.initial_master_nodes”参数

### 插件安装

- 74 版本自带 x-pack 插件，无序额外安装
- 56 版本安装插件使用 elasticsearch-plugin install 命令，74 版本只需要把安装包解压至 es 安装路径下的 plugins 文件夹中即可
- 74 版本和 56 版本需使用不同版本插件（目前用到的插件为 analysis-ik 插件和 analysis-pinyin 插件，74 版本所需插件在 coding 文件 13-安装包文件下）

### python-连接区别

- 官方 pypi 推荐安装和 es 数据库同大版本的 elasticsearch 包
- 74 版本创建索引时不再包含\_type

Config 为 fdm.base.settings.py 里现有的 Config，74 版本\_es.indices.create 函数 body 不再有\_type 层
5.6 版本创建索引

```python
    mapping = Config._INDEX_NP[data_type]['mapping']
    _es.indices.create(index=index, body=mapping, params={'request_timeout': 120})
```

7.4 版本创建索引

```python
    mapping = Config._INDEX_NP[data_type]['mapping']['mappings']['tranjrnl']['properties']
    _es.indices.create(index=index, body={'mappings': {'properties': mapping}}, params={'request_timeout': 120})
```

- 7.4 版本批量导入 documents 时不再需要\_type 字段
  5.6 版本

```python
    for a in actions:
        a.update({"_index": index, "_type": doc_type})
    helpers.bulk(_es, actions=actions)
```

7.4 版本

```python
    for a in actions:
        a.update({"_index": index})
    helpers.bulk(_es, actions=actions)
```

- 7.4 版本查询时不接受 doc_type 参数
  7.4 版本 helpers.scan 和\_es.search 函数传入的参数不可包含 doc_type 参数

```python
cust_rst = helpers.scan(_es, cust_query, index=index, request_timeout=timeout, size=size, raise_on_error=False)
cust_rst = _es.search(body=_query_conds, index=index, request_timeout=timeout, scroll=scroll, size=size)
```

- 7.4 版本查询结果的行数在['hits']['total']['value']中，而 5.6 版本在['hits']['total']
  7.4 版本

```python
total = es_result['hits']['total']['value']
```

5.6 版本

```python
total = es_result['hits']['total']
```

## 问题记录

### 测试时磁盘使用量在 95%以上时，索引会被标记为已读，无法写入数据

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

### 7 版本以上的 elasticsearch，默认只允许 1000 个分片

```python
elasticsearch.exceptions.RequestError: RequestError(400, u'validation_exception', u'Validation Failed: 1: this action would add [16] total shards, but this cluster currently has [995]/[1000] maximum shards open;')
```

**解决方法:** 通过 kibana 修改分片使用上限为 10000

```python
PUT _cluster/settings
{
  "transient": {
    "cluster": {
      "max_shards_per_node": 10000
    }
  }
}
```

### Trying to create too many scroll contexts

```python
TransportError(500, u'search_phase_execution_exception', u'Trying to create too many scroll contexts. Must be less than or equal to: [500]. This limit can be set by changing the [search.max_open_scroll_context] setting.')
```

**解决方法:** 通过 kibana 修改参数

```python
PUT _cluster/settings
{
  "persistent": {
    "search.max_open_scroll_context": 5000
  },
  "transient": {
    "search.max_open_scroll_context": 5000
  }
}
```

### java.lang.OutOfMemoryError: Java heap space

**解决方法:** 修改 config/jvm.options 文件
默认值

```python
-Xms1g
-Xmx1g
```

修改后的值

```python
-Xms2g
-Xmx2g
```

**建议的配置如下：**

将最小堆大小（Xms）和最大堆大小（Xmx）设置为彼此相等。

Elasticsearch 可用的堆越多，它可用于缓存的内存就越多。但请注意，过多的堆可能会陷入长时间的垃圾收集暂停。所以设置的堆不能太大， 尽量设置到内存的 50%。

将 Xmx 设置为不超过物理 RAM 的 50％，以确保有足够的物理内存给内核文件系统缓存。

内存 heap size 配置不要超过 32G, 基本上大多数系统最多只配置到 26G.
