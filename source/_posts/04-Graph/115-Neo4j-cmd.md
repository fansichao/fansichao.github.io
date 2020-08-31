---
title: Neo4j-常用命令
url_path: module/neo4j/cmd
tags:
  - module
  - Neo4j
categories:
  - module
  - grpah
description: Neo4j-常用命令
---

### Neo4j 运算符

| 运算名称   | 运算符                                    |
| ---------- | ----------------------------------------- |
| 常规运算   | DISTINCT, ., []                           |
| 算数运算   | +, -, \*, /, %, ^                         |
| 比较运算   | =, <>, <, >, <=, >=, IS NULL, IS NOT NULL |
| 逻辑运算   | AND, OR, XOR, NOT                         |
| 字符串操作 | +                                         |
| List 操作  | +, IN, [x], [x .. y]                      |
| 正则操作   | =~                                        |
| 字符串匹配 | STARTS WITH, ENDS WITH, CONTAINS          |

### 路径查询

```bash
# 节点之间的最短路径
MATCH p=shortestPath((a)-[*]->(b))

# 节点之前的所有最短路径
MATCH P = allShortestPaths((c:cust {id:'xxx'})-[*..5]-(t:cust {id:'xxxx'})) return P

# shortestPath & allShortestPaths 对比分析
cypher提供了两个查询最短路径的特殊函数 shortestPath 和 allShortestPath
在真实测试中发现，allShortestPath在已有两点间短路径情况下，会忽略两点之间额外更长的路径
allShortestPath ，因为它不会返回任何长度大于较短路径的路径

# true-读取属性记录
call apoc.warmup.run(true)

# 两个节点间所有路径  (数据量较大时会存在性能问题)
MATCH p=(n1 {thingId:"11"})-[r*0..6]-(n2 {thingId:"222"})

# 所有路径（按路径长度排序），并且仅限制返回的项目的深度和数量
MATCH p =(a)-[*2..5]-(b)
RETURN p, length(p)
order by length(p)
LIMIT 5;

```

### Cypher 语法

```python
# Create 语句

# Create语法
CREATE (<node-name>:<label-name>{<Property1-name>...<Propertyn-name>})
- node-name 节点名称。Neo4j使用。不能使用它来访问节点详细信息
- label-name 标签名称 使用此标签名称来访问节点详细信息。
- Property1-name 属性

# Create 节点+标签 + 属性
CREATE (node_name:label1:label2{id:123,name:"Lokesh",sal:35000,deptno:10})

# Match - 查询指定节点
match (lab:label1)
where lab.name = 'Lokesh'
RETURN lab.name,lab.id
# label1 标签名称
# lab 标签名称重命名。类似 as

# Match - 查询指定节点,创建关系
MATCH (cust:Customer),(cc:CreditCard)
WHERE cust.id = "1001" AND cc.id= "5001"
CREATE (cust)-[r:DO_SHOPPING_WITH{shopdate:"12/12/2014",price:55000}]->(cc)
RETURN r


# Sort排序 - 对 Match 结果升序或降序排序
MATCH (emp:Employee)
RETURN emp.empid,emp.name,emp.salary,emp.deptno
ORDER BY emp.name DESC

# UNION - 数据合并(字段名称类型必须一致) 不返回重复行

MATCH (cc:CreditCard)
RETURN cc.id as id,cc.number as number,cc.name as name,
   cc.valid_from as valid_from,cc.valid_to as valid_to
UNION
MATCH (dc:DebitCard)
RETURN dc.id as id,dc.number as number,dc.name as name,
   dc.valid_from as valid_from,dc.valid_to as valid_to

# UNION ALL - 数据合并(字段名称类型必须一致) 返回重复行
MATCH (cc:CreditCard)
RETURN cc.id as id,cc.number as number,cc.name as name,
   cc.valid_from as valid_from,cc.valid_to as valid_to
UNION ALL
MATCH (dc:DebitCard)
RETURN dc.id as id,dc.number as number,dc.name as name,
   dc.valid_from as valid_from,dc.valid_to as valid_to

# Limit 过滤或限制查询返回的行数. 去掉CQL查询结果集底部的结果
MATCH (emp:Employee)
RETURN emp
LIMIT 2

# skip 过滤或限制查询返回的行数. 去掉CQL查询结果集顶部的结果
MATCH (emp:Employee)
RETURN emp
SKIP 2

# Merge 合并

Neo4j使用CQL MERGE命令
- 创建节点，关系和属性
- 为从数据库检索数据
- 命令使用：Create+Match组合

MERGE (gp2:GoogleProfile2{ Id: 201402,Name:"Nokia"})


CREATE命令总是向数据库添加新的节点
Merge命令只有在不存在时创建节点。存在时更新


# NULL

Neo4j CQL将空值视为对节点或关系的属性的缺失值或未定义值。

当我们创建一个具有现有节点标签名称但未指定其属性值的节点时，它将创建一个具有NULL属性值的新节点。
# 查看存在 id 属性的节点
MATCH (e:Employee)
WHERE e.id IS NOT NULL
RETURN e.id,e.name,e.sal,e.deptno

# 移除属性
MATCH (n { name: 'Andres' })
SET n.name = NULL RETURN n.name, n.age

# IN 查询集合
MATCH (e:Employee)
WHERE e.id IN [123,124]
RETURN e.id,e.name,e.sal,e.deptno

```

Cypher 删除

- 两种删除方式。DELETE REMOVE
- Delete 用于删除节点和关系。Remove 用于删除标签和属性。
- Delete 和 Remove 都需要和 Match 配合使用。

```bash
# 删除节点
MATCH (e: Employee) DELETE e

# 删除节点及关系
MATCH (cc: CreditCard)-[rel]-(c:Customer)
DELETE cc,c,rel

# 删除属性
MATCH (book { id:122 })
REMOVE book.price
RETURN book

# 删除匹配 label1 数据. 标签 label2.
MATCH (m:label1)
REMOVE m:label2
```

Cypher 更新

- set 方式更新数据。可以和 match 等配合使用

```bash
# 更新节点属性
MATCH (dc:DebitCard)
SET dc.atm_pin = 3456
RETURN dc

# 移除属性
MATCH (n { name: 'Andres' })
SET n.name = NULL RETURN n.name, n.age


```

ssh

```bash
一，创建节点
1，创建空的节点

CREATE (n)
CREATE (a),(b)
2，创建带标签的节点

CREATE (n:Person)
CREATE (n:Person:Swedish)
3，创建带标签和属性的节点

CREATE (n:Person { name: 'Andres', title: 'Developer' })
二，创建关系
创建节点之前的关系

1，在两个节点之间创建关系

在两个节点之间创建关系，并设置关系类型

MATCH (a:Person),(b:Person)
WHERE a.name = 'A' AND b.name = 'B'
CREATE (a)-[r:RELTYPE]->(b)
RETURN type(r)
2，创建关系，并设置关系的属性

MATCH (a:Person),(b:Person)
WHERE a.name = 'A' AND b.name = 'B'
CREATE (a)-[r:RELTYPE { name: a.name + '<->' + b.name }]->(b)
RETURN type(r), r.name
3，CREATE子句和模式

在CREATE子句和模式中，对于模式中的任意部分，如果它不存在于图中，那么CREATE子句创建它；如果存在于图中，那么就会引用它。

CREATE p =(andres { name:'Andres' })-[:WORKS_AT]->(neo)<-[:WORKS_AT]-(michael { name: 'Michael' })
RETURN p
三，删除节点和关系
使用delete子句删除节点、关系和路径，当删除节点时，该节点必须是孤立的节点，也就是说，必须首先删除跟节点相关的所有关系。

detach delete： 表示删除一个节点或多个节点，跟节点相关的所有关系也都被删除。

1，删除节点

MATCH (n:Person { name: 'UNKNOWN' })
DELETE n
2，删除所有节点和关系

MATCH (n)
DETACH DELETE n
3，删除一个节点和它的所有关系

MATCH (n { name: 'Andres' })
DETACH DELETE n
4，删除关系

MATCH (n { name: 'Andres' })-[r:KNOWS]->()
DELETE r
四，更新属性或标签
set子句用于更新节点的标签，向节点和关系中添加属性

1，向节点或关系中添加属性

MATCH (n { name: 'Andres' })
SET n.surname = 'Taylor'
RETURN n.name, n.surname
2，移除属性

如果设置属性的值是NULL，相当于把该属性从节点或关系中移除

MATCH (n { name: 'Andres' })
SET n.name = NULL RETURN n.name, n.age
3，复制属性

把一个节点的属性复制给另一个节点

MATCH (at { name: 'Andres' }),(pn { name: 'Peter' })
SET at = pn
RETURN at.name, at.age, at.hungry, pn.name, pn.age
4，从Map中添加属性

MATCH (p { name: 'Peter' })
SET p += { hungry: TRUE , position: 'Entrepreneur' }
5，在一条set子句中添加多个属性

MATCH (n { name: 'Andres' })
SET n.position = 'Developer', n.surname = 'Taylor'
6，向节点中添加标签

MATCH (n { name: 'Stefan' })
SET n:German
RETURN n.name, labels(n) AS labels
7，向节点中添加多个标签

MATCH (n { name: 'Emil' })
SET n:Swedish:Bossman
RETURN n.name, labels(n) AS labels
五，移除属性
使用remove子句从节点中移除标签和属性，从关系中移除属性。

1，移除属性

默认情况下，Neo4j不允许存在值为null的属性；如果属性不存在，那么返回该属性的值是null。

MATCH (a { name: 'Andres' })
REMOVE a.age
RETURN a.name, a.age
2，移除节点的标签

MATCH (n { name: 'Peter' })
REMOVE n:German
RETURN n.name, labels(n)
3，移除节点的多个标签

当节点的标签为空时，labels(n)函数返回空的list

MATCH (n { name: 'Peter' })
REMOVE n:German:Swedish
RETURN n.name, labels(n)
六，foreach子句
列表和路径是Cypher中的关键概念，foreach子句用于更新数据，例如，对路径中的元素或通过聚合创建的列表执行更新命令。

1，对路径中的元素执行更新命令

对路径中匹配的所有节点，添加marked属性，并设置属性值为TRUE

MATCH p =(begin)-[*]->(END )
WHERE begin.name = 'A' AND END .name = 'D'
FOREACH (n IN nodes(p)| SET n.marked = TRUE )
```

### Cpyher 函数

### Cypher 常用语句

查询指定节点

```bash
MATCH (n:cust) where n.id = '623026199412212548' RETURN n LIMIT 25
```

更新指定节点

```bash
MATCH (n:cust) where n.id = '623026199412212548' set n.name='set_name_test' RETURN n LIMIT 25
```

查询节点和边

```bash
match (ee:cust)-[:tran]-(tranx) where ee.address='吉林省东莞市新城哈尔滨街D座 690272' return ee,tranx
```

节点数据导入-loadcsv 方式-merge(更新已存在数据)

```bash
USING PERIODIC COMMIT 10000 LOAD CSV WITH HEADERS
            FROM "file:///test.csv" AS line
            fieldterminator ','
            Merge (n:cust{id:line.id})
            set n.name = line.name
# PERIODIC COMMIT 10000 指定每10000条数据提交一次，减小内存压力
# WITH HEADERS 文件自带表头
# fieldterminator 指定文件分隔符
```

创建索引(加快查询，插入速度)

```bash
create index on :cust(id)
create index on :tran(id)
```
