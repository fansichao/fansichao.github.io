---
title: Module-Docker-容器快速部署
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Docker
  - Docker-compose
  - Docker-File
categories:
  - Module
description: Docker容器快速部署应用。Docker run, Docker-compose, Docker FIle. 用于快速开发搭建应用环境。
---

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

Docker-Neo4j-3.3.5

```bash
# 用于存储Docker化后存储数据的位置
export DOCKER_BASE_DATAPATH=/space/data_storage
mkdir -p $DOCKER_BASE_DATAPATH

#########################
# Neo4J部署             #
#########################
DeployNeo4J(){
    container_name=fdm_neo4j

    # Mkdir Container_Dir
    export NEO4J_DATAPATH=${DOCKER_BASE_DATAPATH}/${container_name}
    mkdir -p ${NEO4J_DATAPATH}

    # Clear Container
    docker stop ${container_name}
    docker rm ${container_name}

    # Pulling Neo4J
    # docker pull neo4j:3.3.5

    # 4.1
    # docker run -p=7474:7474 -p=7687:7687 \
    #     --volume=$NEO4J_DATAPATH/data:/data \
    #     --volume=$NEO4J_DATAPATH/logs:/logs \
    #     --volume=$NEO4J_DATAPATH/conf:/var/lib/neo4j/conf \
    #    --name fdm_neo4j -d neo4j:3.3.5

    # Create Neo4J Container
    # TODO 3.3.5版本logs目录无法映射，只能容器内部做logs软链接到data中
    docker run -p=7474:7474 -p=7687:7687 \
        --volume=$NEO4J_DATAPATH/data:/data \
        --volume=$NEO4J_DATAPATH/conf:/var/lib/neo4j/conf \
        --volume=$NEO4J_DATAPATH/import:/var/lib/neo4j/import \
        --env NEO4J_AUTH=neo4j/qwe123 \
        --name ${container_name} -d neo4j:3.3.5
}

DeployNeo4J

# dbms.directories.import=import
# dbms.default_listen_address=0.0.0.0
# dbms.memory.pagecache.size=60g
# dbms.memory.heap.initial_size=32g
# dbms.memory.heap.max_size=120g
# dbms.tx_log.rotation.retention_policy=100M size
# dbms.directories.logs=/logs


# >>>>> 3.3.5
# dbms.directories.import=/var/lib/neo4j/import
#
# wrapper.java.additional=-Dneo4j.ext.udc.source=docker
# ha.host.data=3188fa41c50b:6001
# ha.host.coordination=3188fa41c50b:5001
# dbms.tx_log.rotation.retention_policy=100M size
# dbms.memory.pagecache.size=512M
# dbms.memory.heap.max_size=512M
# dbms.memory.heap.initial_size=512M
# dbms.connectors.default_listen_address=0.0.0.0
# dbms.connector.https.listen_address=0.0.0.0:7473
# dbms.connector.http.listen_address=0.0.0.0:7474
# dbms.connector.bolt.listen_address=0.0.0.0:7687
# causal_clustering.transaction_listen_address=0.0.0.0:6000
# causal_clustering.transaction_advertised_address=3188fa41c50b:6000
# causal_clustering.raft_listen_address=0.0.0.0:7000
# causal_clustering.raft_advertised_address=3188fa41c50b:7000
# causal_clustering.discovery_listen_address=0.0.0.0:5000
# causal_clustering.discovery_advertised_address=3188fa41c50b:5000
# EDITION=community
```

### Docker-Doris
