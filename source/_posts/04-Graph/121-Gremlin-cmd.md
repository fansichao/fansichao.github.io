---
title: Gremlin-常用命令
url_path: module/gremlin/cmd
tags:
  - module
  - gremlin
categories:
  - module
  - grpah
description: gremlin-常用命令
---

## 路径查询

```python
hugegraph.traversal()
想要同时获得经过的边的信息，可以用 bothE().otherV()替换 both()

# 最短路径
g.V("1:4822")
.repeat(bothE().otherV().simplePath()).until(hasId("1:9947")
.or().loops().is(gte(4))).hasId("1:9947")
.path().limit(-1)

# 邻居节点
g.V("1:130133198506126945")
.repeat(bothE().has('tran_amt',gte(10000000)).has('tran_amt',lte(10000000000))
.has('tran_date',gte(20170210)).has('tran_date',lte(20170230))
.otherV().simplePath())
.until(loops().is(gte(2))) .path().limit(200)

# K neighbor API，根据起始顶点，查找 N 步以内可达的所有邻居
g.V("1:3301167").repeat(__.out("MyEdge")).times(2).dedup().count().next()
g.V(1).repeat(out().simplePath()).until(hasId(5)).path().limit(1)
```


- [使用 gremlin 执行 k nearest neighbor](https://github.com/hugegraph/hugegraph/issues/716)