---
title: Neo4j-数据导入
url_path: module/neo4j/load
tags:
  - module
  - Neo4j
categories:
  - module
  - grpah
description: Neo4j-数据导入
---

- Version
  - Neo4j-3.3.5

## 数据导入

数据导入的几种方式

- Cypher create 语句，为每一条数据写一个 create
- Cypher load csv 语句，将数据转成 CSV 格式，通过 LOAD CSV 读取数据。
- 官方提供的 neo4j-import 工具，未来将被 neo4j-admin import 代替
- 官方提供的 Java API - BatchInserter
- 大牛编写的 batch-import 工具
- neo4j-apoc load.csv + apoc.load.relationship
- 针对实际业务场景，定制化开发

参考链接:

- [海量数据导入 Neo4j 的几种方式](https://blog.csdn.net/zhanaolu4821/article/details/80820434)
- [Neo4j 批量导入数据的几种方式](http://weikeqin.cn/2017/04/14/neo4j-import-data/)
- [使用 batch-import 工具向 neo4j 中导入海量数据](https://my.oschina.net/u/2538940/blog/883829)
- [batch-import 已经编译好的工具 3.0，对应 neo4j-3.0.4](https://github.com/mo9527/batch-import-tool)
- [batch-import 的 github](https://github.com/mo9527/batch-import)
- [batch-import 的相关说明](https://github.com/jexp/batch-import/tree/20)

本节主要说明三种导入方式 loadcsv、neo4j-import、batch-import

本文数据导入使用唯一 ID(node)

数据导入的注意事项

- 如果设定唯一主键时，ID 必须唯一
- 边中的 ID 必须存在于节点中，否则关系导入会跳过。

### Neo4j-import

注意事项

#### 文件格式

文件格式样例

```bash
# cust.csv
id:ID,certno,name,label,cust_certtype:string,cust_namespell:string,birthday:int,sex:string,address:string,mob_phone:string
# tran.csv
:START_ID,:END_ID,Type,tran_date:int,amount:int,count:int
```

文件格式说明

- 文件中 ID 必须唯一

#### 导入命令

```bash
neo4j-import适应场景
neo4j-import参数  (bin/neo4j-import help)
    - 指定最大进程数 --processors <max processor count>
    - 跳过重复节点 --skip-duplicate-nodes <true/false>
    - 跳过异常关系 --skip-bad-relationships <true/false>
    - 最大跳过数量 --bad-tolerance <max number of bad entries, or true for unlimited>
    - 跳过异常行(例如行列数异常) --ignore-extra-columns <true/false>


命令样例:

bin/neo4j-import --bad-tolerance=1000000 --skip-duplicate-nodes=true --skip-bad-relationships=true --into data/databases/graph.db --id-type string --nodes:cust import/c.csv  --relationships:tran import/t.csv

```

### batch-import

注意事项:

- batch-import 不支持多进程调用。
- batch-import 版本必须和 neo4j 版本一致。
  - (否则导致数据库自动升级后虽然正常使用，但是 batch-import 已经无法读取升级后的数据库了)

#### 文件格式

```bash
# cust.csv
id:string:id_index,certno:string:id_index,name,Label:label,cust_certtype:string,cust_namespell:string,birthday:int,sex:string,address:string,mob_phone:string
874018718864465,874018718864465,鞠瑜,cust,其他证件,juyu,19801010,男,河北省岩市龙潭东莞街d座 188848,15767524738
# tran.csv
id:string:id_index,certno:string:id_index,Type,tran_date:int,amount:int,count:int
874018718864465,411224195908138440,tran,20180108,20,2
```

文件格式说明：

- id:string:id_index ID 唯一,指定类型,设置索引

#### 导入命令

```bash
# batch-import命令
sh import.sh /home/fdm/neo4j_test/neo4j-community-3.0.4/data/databases/fdm.db /home/fdm/import_data/c.csv /home/fdm/import_data/t.csv

# batch-import3.0已经编译好的软件包
https://github.com/mo9527/batch-import-tool

# batch.properties配置文件
dump_configuration=false
cache_type=none
use_memory_mapped_buffers=true
neostore.propertystore.db.index.keys.mapped_memory=1000M
neostore.propertystore.db.index.mapped_memory=10M
neostore.nodestore.db.mapped_memory=10240M
neostore.relationshipstore.db.mapped_memory=10240M
neostore.propertystore.db.mapped_memory=5120M
neostore.propertystore.db.strings.mapped_memory=2000M
#batch_import.csv.quotes=true
#batch_import.csv.delim=,workInfoId
#contactRecordId deviceId workInfoId
#batch_array_separator=,

batch_import.csv.quotes=true
batch_import.csv.delim=,
batch_import.keep_db=true
batch_import.node_index.id_index=exact
batch_import.node_index.id_index2=exact
batch_import.node_index.id_index3=exact
```

### Load-csv

#### 文件格式

```bash
load csv 导入格式要求

# cust.csv
id,certno,name,label,cust_certtype,cust_namespell,birthday,sex,address,mob_phone
# tran.csv
start_id,end_id,type,tran_date,amount,count

# create 节点
LOAD CSV WITH HEADERS FROM "file:///cust.csv" AS line create
(p:cust{id:line.id,certno:line.certno,name:line.name,label:line.label,cust_certtype:line.cust_certtype,cust_namespell:line.cust_namespell,birthday:toInteger(line.birthday),sex:line.sex,address:line.address,mob_phone:line.mob_phone})

# 创建索引
CREATE INDEX ON :cust(id)

# create 边
LOAD CSV WITH HEADERS FROM "file:///tran.csv" AS line match
(from:cust{id:line.start_id}),(to:cust{id:line.end_id}) create (from)-[r:tran{ type:line. type,tran_date:line.tran_date,amount:line.amount,count:line.count}]->(to)
```

## 其他说明

### 特殊说明

csv 数据导入失败：可能性有多种

文件 head 头不对。 存在节点和交易关系头不对的情况

节点或交易边数据，ID 存在重复。 csv 文件中 ID 必须唯一。且所有实体表中的:ID 是必须写的，并且 ID 全局唯一，也就是三个表格中的 ID 都是唯一的，不可以有重复，在关系表中，不可以存在没有 ID 指向的实体。

### 参考资源

- [Neo4j 语句入门](https://www.w3cschool.cn/neo4j/neo4j_cql_set.html)
- [Neo4j 数据导入参考博客](http://weikeqin.com/2017/04/11/neo4j-load-csv/)
- [Python-Neo4j 语法](https://neo4j.com/developer/python/)
- [官网 Neo4j 语法简图](https://neo4j.com/docs/pdf/cypher-refcard-3.3.pdf)

### 性能测试

neo4j-import 方式

IMPORT DONE in 1m 17s 799ms. Imported:
7295460 nodes
10000000 relationships
112954600 properties

real 1m19.456s
user 5m51.375s
sys 0m15.706s

耗时 79.73S 速度 216,916.30 条/s
