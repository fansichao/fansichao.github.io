---
title: Neo4j-功能模块
url_path: module/neo4j/function
tags:
  - module
  - Neo4j
categories:
  - module
  - grpah
description: Neo4j-数据导入
---

## 功能清单

### 用户管理(可选配置)

```bash
Neo4j密码配置(可视化界面)
1. 新增用户
# 用户 密码 是否需要修改密码
# CALL dbms.security.createUser(name,password,requridchangepassword)
# 命令样例
CALL dbms.security.createUser('fdm','qwe123',true)

2.修改密码
# 修改密码
:server change-password
# 直接修改密码， password参数不能为空，或者跟原密码相同。
CALL dbms.security.changePassword('password')

3.其他命令
# 查看当前用户
CALL dbms.security.showCurrentUser()
# 查看所有用户：
CALL dbms.security.listUsers()
# 删除用户
CALL dbms.security.deleteUser("username")
```

[Neo4j 用户管理-参考链接](https://www.cnblogs.com/zhanglf4498/archive/2019/04/10/10686395.html)

### Neo4j 数据预热

使用 bin/neo4j-shell 进入 neo4j 命令行界面，执行以下语句预热：

```bash
MATCH (n)
OPTIONAL MATCH (n)-[r]->()
RETURN count(n.prop) + count(r.prop);
```

建立 index 可以使得查询性能得到巨大提升。如果不建立 index，则需要对每个 node 的每一个属性进行遍历，所以比较慢。 并且 index 建立之后，新加入的数据都会自动编入到 index 中。 注意 index 是建立在 label 上的，不是在 node 上，所以一个 node 有多个 label，需要对每一个 label 都建立 index.

[Neo4j-系统预热](https://neo4j.com/developer/kb/warm-the-cache-to-improve-performance-from-cold-start/)

### 检查 Neo4j 是否启动

检查 neo4j 是否启动,通常 10s 左右可以启动成功。
[https://neo4j.com/docs/operations-manual/current/configuration/wait-for-start/](https://neo4j.com/docs/operations-manual/current/configuration/wait-for-start/)

### 执行语句查询超时配置

方法 1: 配置 `conf/neo4j.conf` 参数

```bash
# TODO 存在偶发不生效的情况
# query timeout
dbms.lock.acquisition.timeout=60s
dbms.transaction.timeout=60s
```

- 优点
  - 便于控制
  - 超时时会抛出异常，便于把控
- 缺点
  - 偶发失效
  - 无法动态控制变更,需要重启服务.

方法 2: 配置 `runTimeboxed`

```bash
CALL apoc.cypher.runTimeboxed('
    执行命令
' ,{{}}, 90000) # ms 毫秒
```

- 优点
  - 精准控制
  - 必定生效
- 缺点
  - 修改大量语句
  - 超时时返回数据为空
  - 正常返回时和没有 `CALL` 数据结构不同

[Neo4j 官方超时配置](https://neo4j.com/developer/kb/understanding-transaction-and-lock-timeouts/)
