---
title: Neo4j图库目录
url_path: module/neo4j
tags:
  - Module
  - Neo4j
  - index
categories:
  - module
  - grpah
description: Neo4j 目前最流行的图形数据库，支持完整的事务，操作上手简单快速。
---

## 介绍

[Neo4j 官网](https://neo4j.com/)

![xx](http://dl2.iteye.com/upload/attachment/0120/3433/e84b4219-9e96-31fb-927f-241366d91c74.png)

> Neo4j 是目前最流行的图形数据库，支持完整的事务，在属性图中，图是由顶点（Vertex），边（Edge）和属性（Property）组成的，
> 顶点和边都可以设置属性，顶点也称作节点，边也称作关系，每个节点和关系都可以由一个或多个属性。
> Neo4j 创建的图是用顶点和边构建一个有向图，其查询语言 cypher 已经成为事实上的标准。

它包括如下几个显著特点：

- 完整的 ACID 支持
- 高可用性
- 轻易扩展到上亿级别的节点和关系
- 通过遍历工具高速检索数据

其他的图形数据库还包括 Oracle NoSQL 数据库，OrientDB，HypherGraphDB，GraphBase，InfiniteGraph，AllegroGraph。

软件目录说明：

- bin 目录：用于存储 Neo4j 的可执行程序；
- conf 目录：用于控制 Neo4j 启动的配置文件；
- data 目录：用于存储核心数据库文件；
- plugins 目录：用于存储 Neo4j 的插件；
- import 目录：用于存放 load csv 文件,作为根目录(配置文件中可修改)

目前累积最多它有 34.4 亿个节点，344 亿的关系，和 6870 亿条属性。

### Neo4j 语法

Cypher 是图形数据库 Neo4j 的声明式查询语言。

CQL 代表 Cypher 查询语言。 像 Oracle 数据库具有查询语言 SQL，Neo4j 具有 CQL 作为查询语言。

[neo4j 入门教程](https://www.w3cschool.cn/neo4j/neo4j_id_property.html)

### Neo4j 术语/概念

基础术语/概念

下面介绍下 neo4j 的几个核心概念：

- Nodes（节点，类似地铁图里的一个地铁站）
  图谱的基本单位主要是节点和关系，他们都可以包含属性，一个节点就是一行数据，一个关系也是一行数据，里面的属性就是数据库里面的 row 里面的字段。
  除了属性之外，关系和节点还可以有零到多个标签，标签也可以认为是一个特殊分组方式。

- Relationships（关系，类似两个相邻地铁站之间路线）
  关系的功能是组织和连接节点，一个关系连接 2 个节点，一个开始节点和一个结束节点。当所有的点被连接起来，就形成了一张图谱，通过关系可以组织节点形成任意的结构，比如 list，tree，map，tuple，或者更复杂的结构。关系拥有方向进和出，代表一种指向。

- Properties（属性，类似地铁站的名字，位置，大小，进出口数量等）
  属性非常类似数据库里面的字段，只有节点和关系可以拥有 0 到多个属性，属性类型基本和 java 的数据类型一致，分为 数值，字符串，布尔，以及其他的一些类型，字段名必须是字符串。

- Labels（标签，类似地铁站的属于哪个区）
  标签通过形容一种角色或者给节点加上一种类型，一个节点可以有多个类型，通过类型区分一类节点，这样在查询时候可以更加方便和高效，除此之外标签在给属性建立索引或者约束时候也会用到。label 名称必须是非空的 unicode 字符串，另外 lables 最大标记容量是 int 的最大值，近似 21 亿。

- Traversal（遍历，类似我们看地图找路径）
  查询时候通常是遍历图谱然后找到路径，在遍历时通常会有一个开始节点，然后根据 cpyher 提供的查询语句，遍历相关路径上的节点和关系，从而得到最终的结果。

- Paths（路径，类似从一个地铁站到另一个地铁站的所有的到达路径）
  路径是一个或多个节点通过关系连接起来的产物，例如得到图谱查询或者遍历的结果。

- Schema（模式，类似存储数据的结构）
  neo4j 是一个无模式或者 less 模式的图谱数据库，像 mongodb，solr，lucene 或者 es 一样，你可以使用它不需要定义任何 schema，

- Indexes（索引）
  遍历图通过需要大量的随机读写，如果没有索引，则可能意味着每次都是全图扫描，这样效率非常低下，为了获得更好的性能，我们可以在字段属性上构建索引，这样任何查询操作都会使用索引，从而大幅度提升 seek 性能，

构建索引是一个异步请求，并不会立刻生效，会再后台创建直至成功后，才能最终生效。如果创建失败，可以重建索引，先删除索引，在创建即可，然后从 log 里面找出创建失败的原因然后分析。

- Constraints（约束）
  约束可以定义在某个字段上，限制字段值唯一，创建约束会自动创建索引。

参考链接:

[Neo4j 术语与概念](https://blog.csdn.net/u010454030/article/details/52949031)

## Neo4j-index

## 相关资源

内部资源

- [Neo4j 安装部署](http://www.suerpscfan.top/module/neo4j/install)
- [Neo4j 配置详解](http://www.suerpscfan.top/module/neo4j/config)
- [Neo4j 数据导入](http://www.suerpscfan.top/module/neo4j/load)
- [Neo4j 功能模块](http://www.suerpscfan.top/module/neo4j/function)
- [Neo4j 常用命令](http://www.suerpscfan.top/module/neo4j/cmd)

外部资源

- [Neo4j 的使用与 java 调用案例](https://blog.csdn.net/sunroyi666/article/details/80801859)
- [Neo4j-admin import 大数据量导入](https://blog.csdn.net/u013946356/article/details/82629014)
- [neo4j 之'neo4j-import(neo4j-admin import)实战'](https://blog.csdn.net/shuibuzhaodeshiren/article/details/88559383)
- [图形数据库 Neo4j 开发实战](https://www.ibm.com/developerworks/cn/java/j-lo-neo4j/)
- [Neo4j 学习笔记(1)——使用 Java API 实现简单的增删改查](https://www.cnblogs.com/justcooooode/p/8179202.html)
- [如何使用 org.neo4j.graphdb.Relationship 的最佳示例](https://www.helplib.com/Java_API_Classes/article_67946)
- [neo4j 遍历和图算法](https://blog.csdn.net/jason691353279/article/details/84597509)

[Graph 图库排名](https://db-engines.com/en/ranking/graph+dbms)
