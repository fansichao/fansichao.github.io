---
title: ES-技术文档
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Elasticsearch
categories:
  - Module
description: ES技术文档
---

ES-version: 7.4.2

参考资源:

- [ES74 官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/7.4/settings.html)
- [ES7.X-Node 种类](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#modules-node)

文档清单

- [Module-Elasticsearch-01ES 版本差异对比.md](Module-Elasticsearch-01ES版本差异对比.md)
- python-knowledge-tree\04-Module\Module-Elasticsearch-02V564 部署文档.md
- python-knowledge-tree\04-Module\Module-Elasticsearch-02V564 使用文档.md
- python-knowledge-tree\04-Module\Module-Elasticsearch-03V740 部署文档.md
- python-knowledge-tree\04-Module\Module-Elasticsearch-03V740 使用文档.md

## ES 常用配置

### 修改最大分片数

TODO 如何配置在 yml 文件中？

```bash

# 查看 ES 集群配置
GET /_cluster/settings
```

## 问题记录

### illegal_argument_exception [indices:admin/create]

问题日志

```bash
[2020-08-04 23:15:22,145] PID:7703-elasticsearch: [base.py-log_request_fail-244] WARNING: PUT http://172.16.2.3:9200/cust-daily-2010-08-06 [status:400 request:0.057s]
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
curl -X PUT http://172.16.2.1:9200/_cluster/settings -H 'Content-Type: application/json' -d '{
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
[fdm@data1 ~]$ curl   -X PUT http://172.16.2.1:9200/_cluster/settings -H 'Content-Type: application/json' -d '{
>     "persistent" : {
>         "search.max_open_scroll_context": 10240
>     },
>     "transient": {
>         "search.max_open_scroll_context": 10240
>     }
> }'
{"acknowledged":true,"persistent":{"search":{"max_open_scroll_context":"10240"}},"transient":{"search":{"max_open_scroll_context":"10240"}}}
```
