---
title: Docker-Neo4j 部署文档
url_path: docker/docker_neo4j
tags:
  - docker
  - module
categories:
  - module
  - docker
description: Docker-Neo4j 图库技术部署文档
---

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
