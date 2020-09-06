---
title: HugeGraph-问题记录
url_path: module/hugegraph/issue
tags:
  - module
  - hugegraph
categories:
  - module
  - graph
description: HugeGraph 问题记录
---

### 问题

#### 未停止服务,修改配置文件后,服务无法重启

hugegraph 服务启动失败
(env) [scfan@scfan hugegraph-0.9.2]$ bin/stop-hugegraph.sh
no crontab for scfan
The HugeGraphServer monitor has been closed
The pid file /home/scfan/software/hugegraph/hugegraph-0.9.2/bin/pid doesn't exist
(env) [scfan@scfan hugegraph-0.9.2]$ bin/start-hugegraph.sh
The port 8080 has already been used

解决方案:
先关闭 hugegraph-studio-0.9.0] 即可重启 hugegraph 服务

多库合并操作 查询等....

#### Failed to update/query TaskStore

问题场景: 使用 scylladb 初始化数据库时报错。

日志信息

```bash
(env) [scfan@scfan hugegraph-0.9.2]$ bin/init-store.sh
Initing HugeGraph Store...
2019-10-12 11:27:04 1478  [main] [INFO ] com.baidu.hugegraph.cmd.InitStore [] - Init graph with config file: conf/hugegraph.properties
2019-10-12 11:27:04 1683  [main] [INFO ] com.baidu.hugegraph.HugeGraph [] - Opening backend store 'rocksdb' for graph 'hugegraph'
2019-10-12 11:27:04 1789  [main] [INFO ] com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore [] - Opening RocksDB with data path: /home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/schema
2019-10-12 11:27:05 2126  [main] [ERROR] com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore [] - Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/schema'
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStdSessions.<init>(RocksDBStdSessions.java:122) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.openSessionPool(RocksDBStore.java:241) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:181) [hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:172) [hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:155) [hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.tx.AbstractTransaction.<init>(AbstractTransaction.java:72) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.IndexableTransaction.<init>(IndexableTransaction.java:30) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.SchemaTransaction.<init>(SchemaTransaction.java:68) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.cache.CachedSchemaTransaction.<init>(CachedSchemaTransaction.java:53) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.openSchemaTransaction(HugeGraph.java:250) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.access$300(HugeGraph.java:80) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.getOrNewTransaction(HugeGraph.java:730) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.schemaTransaction(HugeGraph.java:713) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.access$000(HugeGraph.java:588) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.schemaTransaction(HugeGraph.java:301) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.store.BackendStoreSystemInfo.info(BackendStoreSystemInfo.java:66) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.store.BackendStoreSystemInfo.exist(BackendStoreSystemInfo.java:78) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.cmd.InitStore.initGraph(InitStore.java:99) [hugegraph-dist-0.9.2.jar:?]
	at com.baidu.hugegraph.cmd.InitStore.main(InitStore.java:87) [hugegraph-dist-0.9.2.jar:?]
2019-10-12 11:27:05 2131  [main] [ERROR] com.baidu.hugegraph.HugeGraph [] - Failed to open schema transaction
com.baidu.hugegraph.backend.BackendException: Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/schema'
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:219) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:172) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:155) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.tx.AbstractTransaction.<init>(AbstractTransaction.java:72) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.IndexableTransaction.<init>(IndexableTransaction.java:30) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.SchemaTransaction.<init>(SchemaTransaction.java:68) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.cache.CachedSchemaTransaction.<init>(CachedSchemaTransaction.java:53) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.openSchemaTransaction(HugeGraph.java:250) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.access$300(HugeGraph.java:80) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.getOrNewTransaction(HugeGraph.java:730) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.schemaTransaction(HugeGraph.java:713) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph$TinkerpopTransaction.access$000(HugeGraph.java:588) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.HugeGraph.schemaTransaction(HugeGraph.java:301) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.store.BackendStoreSystemInfo.info(BackendStoreSystemInfo.java:66) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.store.BackendStoreSystemInfo.exist(BackendStoreSystemInfo.java:78) [hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.cmd.InitStore.initGraph(InitStore.java:99) [hugegraph-dist-0.9.2.jar:?]
	at com.baidu.hugegraph.cmd.InitStore.main(InitStore.java:87) [hugegraph-dist-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStdSessions.<init>(RocksDBStdSessions.java:122) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.openSessionPool(RocksDBStore.java:241) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:181) ~[hugegraph-rocksdb-0.9.2.jar:?]
2019-10-12 11:27:05 2155  [task-db-worker-1] [INFO ] com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore [] - Opening RocksDB with data path: /home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system
2019-10-12 11:27:05 2161  [task-db-worker-1] [ERROR] com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore [] - Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system'
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStdSessions.<init>(RocksDBStdSessions.java:122) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.openSessionPool(RocksDBStore.java:241) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:181) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:172) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:155) ~[hugegraph-rocksdb-0.9.2.jar:?]
	at com.baidu.hugegraph.backend.tx.AbstractTransaction.<init>(AbstractTransaction.java:72) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.IndexableTransaction.<init>(IndexableTransaction.java:30) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.backend.tx.GraphTransaction.<init>(GraphTransaction.java:119) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.task.TaskScheduler$TaskTransaction.<init>(TaskScheduler.java:406) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.task.TaskScheduler.tx(TaskScheduler.java:111) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
	at com.baidu.hugegraph.task.TaskScheduler.lambda$close$3(TaskScheduler.java:206) ~[hugegraph-core-0.9.2.jar:0.9.2.0]
Exception in thread "main" com.baidu.hugegraph.HugeException: Failed to update/query TaskStore
	at com.baidu.hugegraph.task.TaskScheduler.call(TaskScheduler.java:397)
	at com.baidu.hugegraph.task.TaskScheduler.call(TaskScheduler.java:389)
	at com.baidu.hugegraph.task.TaskScheduler.close(TaskScheduler.java:205)
	at com.baidu.hugegraph.task.TaskManager.closeScheduler(TaskManager.java:73)
	at com.baidu.hugegraph.HugeGraph.close(HugeGraph.java:460)
	at com.baidu.hugegraph.cmd.InitStore.initGraph(InitStore.java:107)
	at com.baidu.hugegraph.cmd.InitStore.main(InitStore.java:87)
Caused by: java.util.concurrent.ExecutionException: com.baidu.hugegraph.backend.BackendException: Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system'
	at java.util.concurrent.FutureTask.report(FutureTask.java:122)
	at java.util.concurrent.FutureTask.get(FutureTask.java:192)
	at com.baidu.hugegraph.task.TaskScheduler.call(TaskScheduler.java:395)
	... 6 more
Caused by: com.baidu.hugegraph.backend.BackendException: Failed to open RocksDB '/home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system'
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:219)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:172)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:155)
	at com.baidu.hugegraph.backend.tx.AbstractTransaction.<init>(AbstractTransaction.java:72)
	at com.baidu.hugegraph.backend.tx.IndexableTransaction.<init>(IndexableTransaction.java:30)
	at com.baidu.hugegraph.backend.tx.GraphTransaction.<init>(GraphTransaction.java:119)
	at com.baidu.hugegraph.task.TaskScheduler$TaskTransaction.<init>(TaskScheduler.java:406)
	at com.baidu.hugegraph.task.TaskScheduler.tx(TaskScheduler.java:111)
	at com.baidu.hugegraph.task.TaskScheduler.lambda$close$3(TaskScheduler.java:206)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: org.rocksdb.RocksDBException: While lock file: /home/scfan/software/hugegraph/hugegraph_data/rocksdb_data/system/LOCK: Resource temporarily unavailable
	at org.rocksdb.RocksDB.open(Native Method)
	at org.rocksdb.RocksDB.open(RocksDB.java:286)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStdSessions.<init>(RocksDBStdSessions.java:122)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.openSessionPool(RocksDBStore.java:241)
	at com.baidu.hugegraph.backend.store.rocksdb.RocksDBStore.open(RocksDBStore.java:181)
	... 13 more
```

#### HugeGraph*问题*使用 scylladb 数据库初始化报错.

![HugeGraph_问题_使用scylladb数据库初始化报错](https://img-blog.csdnimg.cn/20191012154029962.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxMTY1MDA3,size_16,color_FFFFFF,t_70)

问题原因：

- 初始化时，未关闭 hugegraph,导致报错, 关闭后正常执行。
