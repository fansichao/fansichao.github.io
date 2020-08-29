---
title: Module-Neo4j-使用文档
url_path: moudule/neo4j/neo4j2
tags:
  - Module
  - Graph
categories:
  - Module
description: Neo4j图库使用文档。Neo4j，最流行的图库软件之一，上手简单易用。
---

[Neo4j3.5-Config](https://neo4j.com/docs/operations-manual/3.5/reference/configuration-settings/)

## 功能模块

## 路径查询

```bash
# 节点之间的最短路径
MATCH p=shortestPath((a)-[*]->(b))

# 节点之前的所有最短路径
MATCH P = allShortestPaths((c:cust {id:'xxx'})-[*..5]-(t:cust {id:'xxxx'})) return P

# shortestPath & allShortestPaths 对比分析
cypher提供了两个查询最短路径的特殊函数 shortestPath 和 allShortestPath
在真实测试中发现，allShortestPath在已有两点间短路径情况下，会忽略两点之间额外更长的路径
allShortestPath ，因为它不会返回任何长度大于较短路径的路径

# Neo4j-系统预热
https://neo4j.com/developer/kb/warm-the-cache-to-improve-performance-from-cold-start/

# true-读取属性记录
call apoc.warmup.run(true)










# 两个节点间所有路径 方法1 (数据量较大时会存在性能问题)
MATCH p=(n1 {thingId:"11"})-[r*0..6]-(n2 {thingId:"222"})

5度交易无法展示，此cypher语句性能存在问题
match p=(c:cust {id:'aaa'})-[:tran*..5]-(t:cust {id:'bbb'}) WITH *, RELATIONSHIPS(p) as r
    WHERE ALL (
        e IN r where
        e.tran_date>=20000101 and e.tran_date <=20200805
        and e.tran_amt >= 0 and e.tran_amt <= 9223372036854775807
    )
UNWIND r AS x
WITH DISTINCT x
RETURN collect(x) as all_relation


MATCH (c)--(e)--(t)

      where
       c.id = "896332053110652" AND t.id = "6228480588998875573"


RETURN c,e,t


match p=(c:cust {id:'896332053110652'})--(t1)--(t2)--(t3)--(t:cust {id:'6228480588998875573'}) WITH *, RELATIONSHIPS(p) as r
    WHERE ALL (
        e IN r where
        e.tran_date>=20000101 and e.tran_date <=20200805
        and e.tran_amt >= 0 and e.tran_amt <= 9223372036854775807
    )
UNWIND r AS x
WITH DISTINCT x
RETURN collect(x) as all_relation

{
  "tran_date": 20190628,
  "tran_cnt": 1,
  "tran_amt": 1000,
  "dataset": "history_data"
}
37s



6217680601180727
370202198405065421
4000027219200208691
340302198803271634
33001616783059000667
372328199104063022
31050173530000000304


match p=(c:cust {id:'6217680601180727'})--(t1)--(t2)--(t3)--(t:cust {id:'33001616783059000667'}) WITH *, RELATIONSHIPS(p) as r
    WHERE ALL (
        e IN r where
        e.tran_date>=20000101 and e.tran_date <=20200805
        and e.tran_amt >= 0 and e.tran_amt <= 9223372036854775807
    )
UNWIND r AS x
WITH DISTINCT x
RETURN collect(x) as all_relation







# 两个节点间所有路径 方法2
MATCH (k)--(m)--(l)
WHERE k.id = "896332053110652" AND l.id = "6228480588998875573"
RETURN k,m,l





# 所有路径（按路径长度排序），并且仅限制返回的项目的深度和数量
MATCH p =(a)-[*2..5]-(b)
RETURN p, length(p)
order by length(p)
LIMIT 5;


```

https://www.shuzhiduo.com/A/A2dm6vjxze/

### 查询两个节点间所有路径

解决方案

性能优化

```bash
# 服务器预热后
match p=shortestPath(c:cust {id:'896332053110652'})-[:tran*..3]-(t:cust {id:'6228480588998875573'}) WITH *, RELATIONSHIPS(p) as r

  WHERE ALL (
      e IN r where
      e.tran_date>=20000101 and e.tran_date <=20200805
      and e.tran_amt >= 0 and e.tran_amt <= 9223372036854775807
  )

UNWIND r AS x
WITH DISTINCT x
RETURN collect(x) as all_relation
# 14s
```

http://neo4j.com.cn/topic/5818519dcdf6c5bf145675c7

https://www.cnblogs.com/ljhdo/p/5516793.html

https://juejin.im/post/6844903848553742349

https://jpanj.com/2017/neo4j-warms-up/

Neo4j 官方超时配置
https://neo4j.com/developer/kb/understanding-transaction-and-lock-timeouts/

## 问题记录

```bash
# Neo4j 配置了 超时后，未成功超时，后台报错！

2020-08-05 09:34:37.476+0000 ERROR [o.n.b.v.r.ErrorReporter] Client triggered an unexpected error [UnknownError]: Access to record Node[-3,used=false,rel=-1,prop=-1,labels=Inline(0x0:[]),light,secondaryUnitId=-1] went out of bounds of the page. The record size is 15 bytes, and the access was at offset -45 bytes into page 0, and the pages have a capacity of 8190 bytes. The mapped store file in question is /home/fdm/quick/data/databases/graph.db/neostore.nodestore.db, reference 894de038-457c-492f-8fe9-19533f720375.
2020-08-05 09:34:37.476+0000 ERROR [o.n.b.v.r.ErrorReporter] Client triggered an unexpected error [UnknownError]: Access to record Node[-3,used=false,rel=-1,prop=-1,labels=Inline(0x0:[]),light,secondaryUnitId=-1] went out of bounds of the page. The record size is 15 bytes, and the access was at offset -45 bytes into page 0, and the pages have a capacity of 8190 bytes. The mapped store file in question is /home/fdm/quick/data/databases/graph.db/neostore.nodestore.db, reference 894de038-457c-492f-8fe9-19533f720375. Access to record Node[-3,used=false,rel=-1,prop=-1,labels=Inline(0x0:[]),light,secondaryUnitId=-1] went out of bounds of the page. The record size is 15 bytes, and the access was at offset -45 bytes into page 0, and the pages have a capacity of 8190 bytes. The mapped store file in question is /home/fdm/quick/data/databases/graph.db/neostore.nodestore.db
org.neo4j.kernel.impl.store.UnderlyingStorageException: Access to record Node[-3,used=false,rel=-1,prop=-1,labels=Inline(0x0:[]),light,secondaryUnitId=-1] went out of bounds of the page. The record size is 15 bytes, and the access was at offset -45 bytes into page 0, and the pages have a capacity of 8190 bytes. The mapped store file in question is /home/fdm/quick/data/databases/graph.db/neostore.nodestore.db
	at org.neo4j.kernel.impl.store.CommonAbstractStore.throwOutOfBoundsException(CommonAbstractStore.java:1184)
	at org.neo4j.kernel.impl.store.CommonAbstractStore.checkForDecodingErrors(CommonAbstractStore.java:1173)
	at org.neo4j.kernel.impl.store.CommonAbstractStore.isInUse(CommonAbstractStore.java:400)
	at org.neo4j.kernel.impl.api.store.StorageLayer.nodeExists(StorageLayer.java:537)
	at org.neo4j.kernel.impl.api.StateHandlingStatementOperations.nodeExists(StateHandlingStatementOperations.java:1751)
	at org.neo4j.kernel.impl.api.ConstraintEnforcingEntityOperations.nodeExists(ConstraintEnforcingEntityOperations.java:646)
	at org.neo4j.kernel.impl.api.OperationsFacade.nodeExists(OperationsFacade.java:247)
	at org.neo4j.cypher.internal.spi.v3_3.TransactionBoundQueryContext$NodeOperations.getByIdIfExists(TransactionBoundQueryContext.scala:418)
	at org.neo4j.cypher.internal.compatibility.v3_3.ExceptionTranslatingQueryContext$ExceptionTranslatingOperations$$anonfun$getByIdIfExists$1.apply(ExceptionTranslatingQueryContext.scala:303)
	at org.neo4j.cypher.internal.compatibility.v3_3.ExceptionTranslatingQueryContext$ExceptionTranslatingOperations$$anonfun$getByIdIfExists$1.apply(ExceptionTranslatingQueryContext.scala:303)
	at org.neo4j.cypher.internal.spi.v3_3.ExceptionTranslationSupport$class.translateException(ExceptionTranslationSupport.scala:32)
	at org.neo4j.cypher.internal.compatibility.v3_3.ExceptionTranslatingQueryContext.translateException(ExceptionTranslatingQueryContext.scala:39)
	at org.neo4j.cypher.internal.compatibility.v3_3.ExceptionTranslatingQueryContext$ExceptionTranslatingOperations.getByIdIfExists(ExceptionTranslatingQueryContext.scala:303)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.IdSeekIterator.computeNextEntity(IdSeekIterator.scala:53)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.IdSeekIterator.<init>(IdSeekIterator.scala:32)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.NodeIdSeekIterator.<init>(IdSeekIterator.scala:64)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.NodeByIdSeekPipe.internalCreateResults(NodeByIdSeekPipe.scala:70)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.Pipe$class.createResults(Pipe.scala:41)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.NodeByIdSeekPipe.createResults(NodeByIdSeekPipe.scala:62)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.PipeWithSource.createResults(Pipe.scala:59)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.PipeWithSource.createResults(Pipe.scala:59)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.pipes.PipeWithSource.createResults(Pipe.scala:59)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.executionplan.DefaultExecutionResultBuilderFactory$ExecutionWorkflowBuilder.createResults(DefaultExecutionResultBuilderFactory.scala:102)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.executionplan.DefaultExecutionResultBuilderFactory$ExecutionWorkflowBuilder.build(DefaultExecutionResultBuilderFactory.scala:74)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.BuildInterpretedExecutionPlan$$anonfun$getExecutionPlanFunction$1.apply(BuildInterpretedExecutionPlan.scala:100)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.BuildInterpretedExecutionPlan$$anonfun$getExecutionPlanFunction$1.apply(BuildInterpretedExecutionPlan.scala:83)
	at org.neo4j.cypher.internal.compatibility.v3_3.runtime.BuildInterpretedExecutionPlan$InterpretedExecutionPlan.run(BuildInterpretedExecutionPlan.scala:116)
	at org.neo4j.cypher.internal.compatibility.v3_3.Compatibility$ExecutionPlanWrapper$$anonfun$run$1.apply(Compatibility.scala:183)
	at org.neo4j.cypher.internal.compatibility.v3_3.Compatibility$ExecutionPlanWrapper$$anonfun$run$1.apply(Compatibility.scala:179)
	at org.neo4j.cypher.internal.compatibility.v3_3.exceptionHandler$runSafely$.apply(exceptionHandler.scala:90)
	at org.neo4j.cypher.internal.compatibility.v3_3.Compatibility$ExecutionPlanWrapper.run(Compatibility.scala:179)
	at org.neo4j.cypher.internal.PreparedPlanExecution.execute(PreparedPlanExecution.scala:29)
	at org.neo4j.cypher.internal.ExecutionEngine.execute(ExecutionEngine.scala:120)
	at org.neo4j.cypher.internal.javacompat.ExecutionEngine.executeQuery(ExecutionEngine.java:62)
	at org.neo4j.bolt.v1.runtime.TransactionStateMachineSPI$1.start(TransactionStateMachineSPI.java:146)
	at org.neo4j.bolt.v1.runtime.TransactionStateMachine$State$1.run(TransactionStateMachine.java:247)
	at org.neo4j.bolt.v1.runtime.TransactionStateMachine.run(TransactionStateMachine.java:82)
	at org.neo4j.bolt.v1.runtime.BoltStateMachine$State$2.run(BoltStateMachine.java:408)
	at org.neo4j.bolt.v1.runtime.BoltStateMachine.run(BoltStateMachine.java:200)
	at org.neo4j.bolt.v1.messaging.BoltMessageRouter.lambda$onRun$3(BoltMessageRouter.java:93)
	at org.neo4j.bolt.v1.runtime.concurrent.RunnableBoltWorker.execute(RunnableBoltWorker.java:152)
	at org.neo4j.bolt.v1.runtime.concurrent.RunnableBoltWorker.run(RunnableBoltWorker.java:104)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
	at org.neo4j.helpers.NamedThreadFactory$2.run(NamedThreadFactory.java:109)
2020-08-05 09:35:52.808+0000 WARN [o.n.k.i.c.MonitorGc] GC Monitor: Application threads blocked for 228ms.

```
