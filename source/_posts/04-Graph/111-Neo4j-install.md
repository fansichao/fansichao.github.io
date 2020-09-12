---
title: Neo4j-部署文档
url_path: module/neo4j/install
tags:
  - module
  - Neo4j
categories:
  - module
  - grpah
description: Neo4j部署文档
---

## 部署

- Version
  - Neo4j-3.3.5
  - CentOS8.1.19

### 容器部署

参考 [Docker-Neo4j 安装文档](https://www.superscfan.top/docker/neo4j)

### 宿主机部署

解压即用

- 环境依赖
  - Java1.8+
  - 系统文件数 40000+

配置系统文件数

```bash
# vi /etc/security/limits.conf
fdm              soft    nofile          65535
fdm              hard    nofile          65535

sysctl -p
# 修改后重新进入ssh
# fdm为用户名称
```

建议配置 apoc-3.3.0.3-all.jar 以支持 Neo4j 更多功能

## 基础使用

```bash
# 重启服务
[fdm@5e272144faf5 neo4j-community-3.3.5]$ bin/neo4j restart
Stopping Neo4j.. stopped
Starting Neo4j.
Started neo4j (pid 1420). It is available at http://0.0.0.0:7474/
There may be a short delay until the server is ready.
See /home/fdm/neo4j/neo4j-community-3.3.5/logs/neo4j.log for current status.

# 查看前端页面
0.0.0.0:7474

默认用户名 neo4j
默认密码 qwe123
```
