---
title: Module-Docker-容器快速部署
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Docker
categories:
  - Module
description: ....
---

tags: `Docker`

说明:

- Docker 快速部署，详见《Docker-Compose》

## Docker-快速部署样例

### Docker-Oracle11g

```bash
前提最新版Docker安装好，配置阿里云镜像库
# 获取镜像
docker pull registry.cn-hangzhou.aliyuncs.com/qida/oracle-xe-11g

# 运行命令
docker run --name oracle11g -d -p 1521:1521 -v /docker/oracle/v/oradata/:/u01/app/oracle/oradata/oracle11g-data/ -e ORACLE_ALLOW_REMOTE=true --restart=always registry.cn-hangzhou.aliyuncs.com/qida/oracle-xe-11g

# 进入容器：
docker exec -it oracle11g bash

# 安装好的 Oracle 默认参数
- 系统用户：root 密码：admin
- 数据库链接
    - hostname: localhost
    - port: 1521
    - sid: xe
    - username: system
    - password: oracle

切换用户：su oracle
进入SQL交互：sqlplus / as sysdba

# 创建数据库用户
create user fdm identified by qwe123;
# 授权给用户
GRANT CREATE USER,DROP USER,ALTER USER ,CREATE ANY VIEW ,DROP ANY VIEW,EXP_FULL_DATABASE,IMP_FULL_DATABASE,DBA,CONNECT,RESOURCE,CREATE SESSION TO fdm;
```

参考资源: [Docker 安装 Oracle11g-超简单教程](https://www.jianshu.com/p/fc85bb7e2d90)

### Docker-ES

### Docker-Neo4j

### Docker-Doris
