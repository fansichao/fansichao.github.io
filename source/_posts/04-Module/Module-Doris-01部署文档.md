---
title: Module-Doirs-部署文档
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Doirs
categories:
  - Module
description: ....
---

```bash

# 服务器1 fe be1
# 服务器2 be2 be3

mysql> SHOW PROC '/backends';
+-----------+-----------------+----------------+----------+---------------+--------+----------+----------+---------------------+---------------------+-------+----------------------+-----------------------+-----------+------------------+---------------+---------------+---------+----------------+--------+---------------+--------------------------------------------------------+
| BackendId | Cluster         | IP             | HostName | HeartbeatPort | BePort | HttpPort | BrpcPort | LastStartTime       | LastHeartbeat       | Alive | SystemDecommissioned | ClusterDecommissioned | TabletNum | DataUsedCapacity | AvailCapacity | TotalCapacity | UsedPct | MaxDiskUsedPct | ErrMsg | Version       | Status                                                 |
+-----------+-----------------+----------------+----------+---------------+--------+----------+----------+---------------------+---------------------+-------+----------------------+-----------------------+-----------+------------------+---------------+---------------+---------+----------------+--------+---------------+--------------------------------------------------------+
| 10011     | default_cluster | 192.168.172.73 | fdm      | 9051          | 9061   | 8041     | 8061     | 2020-07-18 18:14:23 | 2020-07-18 18:14:23 | true  | false                | false                 | 0         | .000             | 35.496 GB     | 141.201 GB    | 74.86 % | 74.86 %        |        | trunk-8c608bb | {"lastSuccessReportTabletsTime":"2020-07-18 18:14:24"} |
| 10008     | default_cluster | 192.168.172.74 | fdm2     | 9053          | 9063   | 8043     | 8063     | 2020-07-18 18:10:14 | 2020-07-18 18:14:23 | true  | false                | false                 | 0         | .000             | 113.427 GB    | 143.137 GB    | 20.76 % | 20.76 %        |        | trunk-8c608bb | {"lastSuccessReportTabletsTime":"2020-07-18 18:13:56"} |
| 10002     | default_cluster | 192.168.172.74 | fdm2     | 9052          | 9062   | 8042     | 8062     | 2020-07-18 18:09:44 | 2020-07-18 18:14:23 | true  | false                | false                 | 0         | .000             | 113.427 GB    | 143.137 GB    | 20.76 % | 20.76 %        |        | trunk-8c608bb | {"lastSuccessReportTabletsTime":"2020-07-18 18:14:22"} |
+-----------+-----------------+----------------+----------+---------------+--------+----------+----------+---------------------+---------------------+-------+----------------------+-----------------------+-----------+------------------+---------------+---------------+---------+----------------+--------+---------------+--------------------------------------------------------+
3 rows in set (0.01 sec)
```




Apache Doris 文档(201812)
https://www.bookstack.cn/read/Doris/README.md





# Doris-部署文档

TODO 待完善

详见 [fisams-Doris](https://fisams.coding.net/p/FISAMS/wiki/428#user-content-%E4%BD%BF%E7%94%A8docker%E9%83%A8%E7%BD%B2apache-doris)

Doris 部署流程说明

- 编译(耗时较长)
- 部署
- 说明
  - 部署和编译环境建议不要相同，只需编译后文件用于部署即可。

参考链接；[官网 Doris 详细部署文档](http://doris.incubator.apache.org/master/zh-CN/installing/install-deploy.html)

TODO 待完善

## Doris 部署

### 编译

编译推荐使用 官网 docker 环境，

pass

### 部署

```bash
# 环境前依赖
yum install -y mariadb.x86_64 mariadb-libs.x86_64
jdkk1.8目录给予777权限，避免容器内部无法访问。



# 启动fe服务 cd /opt/doris
bin/stop_fe.sh
sh bin/start_fe.sh --daemon

# 启动be服务 cd /opt/doris
bin/stop_be.sh
sh bin/start_be.sh --daemon
```

在 fe 容器内操作

```bash
# 进入mysql
[root@b88a32bec16f /]# mysql -h 172.20.0.160 -P 9030 -u root


# 增加 be节点
MySQL [(none)]> ALTER SYSTEM ADD BACKEND "172.20.0.161:9050";
Query OK, 0 rows affected (0.03 sec)

MySQL [(none)]> ALTER SYSTEM ADD BACKEND "172.20.0.162:9050";
Query OK, 0 rows affected (0.01 sec)

MySQL [(none)]> ALTER SYSTEM ADD BACKEND "172.20.0.163:9050";
Query OK, 0 rows affected (0.01 sec)

# 查看 be 节点
MySQL [(none)]> SHOW PROC '/backends';
+-----------+-----------------+--------------+--------------+---------------+--------+----------+----------+---------------+---------------+-------+----------------------+-----------------------+-----------+------------------+---------------+---------------+---------+----------------+----------------------------------------------------+---------+----------------------------------------+
| BackendId | Cluster         | IP           | HostName     | HeartbeatPort | BePort | HttpPort | BrpcPort | LastStartTime | LastHeartbeat | Alive | SystemDecommissioned | ClusterDecommissioned | TabletNum | DataUsedCapacity | AvailCapacity | TotalCapacity | UsedPct | MaxDiskUsedPct | ErrMsg                                             | Version | Status                                 |
+-----------+-----------------+--------------+--------------+---------------+--------+----------+----------+---------------+---------------+-------+----------------------+-----------------------+-----------+------------------+---------------+---------------+---------+----------------+----------------------------------------------------+---------+----------------------------------------+
| 10002     | default_cluster | 172.20.0.161 | 172.20.0.161 | 9050          | -1     | -1       | -1       | N/A           | N/A           | true | false                | false                 | 0         | .000             | 1.000 B       | .000          | 0.00 %  | 0.00 %         | java.net.SocketTimeoutException: connect timed out |         | {"lastSuccessReportTabletsTime":"N/A"} |
| 10003     | default_cluster | 172.20.0.162 | 172.20.0.162 | 9050          | -1     | -1       | -1       | N/A           | N/A           | true | false                | false                 | 0         | .000             | 1.000 B       | .000          | 0.00 %  | 0.00 %         | java.net.SocketTimeoutException: connect timed out |         | {"lastSuccessReportTabletsTime":"N/A"} |
| 10004     | default_cluster | 172.20.0.163 | 172.20.0.163 | 9050          | -1     | -1       | -1       | N/A           | N/A           | true | false                | false                 | 0         | .000             | 1.000 B       | .000          | 0.00 %  | 0.00 %         | java.net.SocketTimeoutException: connect timed out |         | {"lastSuccessReportTabletsTime":"N/A"} |
+-----------+-----------------+--------------+--------------+---------------+--------+----------+----------+---------------+---------------+-------+----------------------+-----------------------+-----------+------------------+---------------+---------------+---------+----------------+----------------------------------------------------+---------+----------------------------------------+
3 rows in set (5.11 sec)


# 创建数据库 fdmdb
MySQL [(none)]> CREATE DATABASE  fdmdb;
Query OK, 0 rows affected (0.00 sec)
# 创建用户 fdm
MySQL [(none)]> CREATE USER 'fdm' IDENTIFIED BY 'qwe123';
Query OK, 0 rows affected (0.01 sec)
# 账户授权 数据库fdmdb 所有权限给予 fdm
MySQL [(none)]> GRANT ALL ON fdmdb TO fdm;
Query OK, 0 rows affected (0.01 sec)

# 设置root用户密码
set password for 'root' = PASSWORD('qwe123');

# 使用 -p密码登录
[root@b88a32bec16f /]# mysql -h 172.20.0.160 -P 9030 -u root -pqwe123

```

### 配置文件说明

Fe 配置文件 `/opt/doris/conf/fe.conf`

```conf
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

#####################################################################
## The uppercase properties are read and exported by bin/start_fe.sh.
## To see all Frontend configurations,
## see fe/src/org/apache/doris/common/Config.java
#####################################################################

# the output dir of stderr and stdout
LOG_DIR = ${DORIS_HOME}/log

DATE = `date +%Y%m%d-%H%M%S`
JAVA_OPTS="-Xmx4096m -XX:+UseMembar -XX:SurvivorRatio=8 -XX:MaxTenuringThreshold=7 -XX:+PrintGCDateStamps -XX:+PrintGCDetails -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:+CMSClassUnloadingEnabled -XX:-CMSParallelRemarkEnabled -XX:CMSInitiatingOccupancyFraction=80 -XX:SoftRefLRUPolicyMSPerMB=0 -Xloggc:$DORIS_HOME/log/fe.gc.log.$DATE"

# For jdk 9+, this JAVA_OPTS will be used as default JVM options
JAVA_OPTS_FOR_JDK_9="-Xmx4096m -XX:SurvivorRatio=8 -XX:MaxTenuringThreshold=7 -XX:+CMSClassUnloadingEnabled -XX:-CMSParallelRemarkEnabled -XX:CMSInitiatingOccupancyFraction=80 -XX:SoftRefLRUPolicyMSPerMB=0 -Xlog:gc*:$DORIS_HOME/log/fe.gc.log.$DATE:time"

##
## the lowercase properties are read by main program.
##

# INFO, WARN, ERROR, FATAL
sys_log_level = INFO

# store metadata, create it if it is not exist.
# Default value is ${DORIS_HOME}/doris-meta
# meta_dir = ${DORIS_HOME}/doris-meta

http_port = 8030
rpc_port = 9020
query_port = 9030
edit_log_port = 9010
mysql_service_nio_enabled = true

# Choose one if there are more than one ip except loopback address.
# Note that there should at most one ip match this list.
# If no ip match this rule, will choose one randomly.
# use CIDR format, e.g. 10.10.10.0/24
# Default value is empty.
# priority_networks = 10.10.10.0/24;192.168.0.0/16
priority_networks = 172.20.0.160/16

# Advanced configurations
# log_roll_size_mb = 1024
# sys_log_dir = ${DORIS_HOME}/log
# sys_log_roll_num = 10
# sys_log_verbose_modules =
# audit_log_dir = ${DORIS_HOME}/log
# audit_log_modules = slow_query, query
# audit_log_roll_num = 10
# meta_delay_toleration_second = 10
# qe_max_connection = 1024
max_conn_per_user = 1000
# qe_query_timeout_second = 300
# qe_slow_log_ms = 5000
```

fe 配置文件修改说明

```conf
# -Xmx4096m 使用内存大小 根据机器调整
JAVA_OPTS="-Xmx4096m -XX:+UseMembar -XX:SurvivorRatio=8 -XX:MaxTenuringThreshold=7 -XX:+PrintGCDateStamps -XX:+PrintGCDetails -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:+CMSClassUnloadingEnabled -XX:-CMSParallelRemarkEnabled -XX:CMSInitiatingOccupancyFraction=80 -XX:SoftRefLRUPolicyMSPerMB=0 -Xloggc:$DORIS_HOME/log/fe.gc.log.$DATE"
# -Xmx4096m 使用内存大小 根据机器调整
JAVA_OPTS_FOR_JDK_9="-Xmx4096m -XX:SurvivorRatio=8 -XX:MaxTenuringThreshold=7 -XX:+CMSClassUnloadingEnabled -XX:-CMSParallelRemarkEnabled -XX:CMSInitiatingOccupancyFraction=80 -XX:SoftRefLRUPolicyMSPerMB=0 -Xlog:gc*:$DORIS_HOME/log/fe.gc.log.$DATE:time"

# Doris相应端口 默认即可，一般不用修改
http_port = 8030
rpc_port = 9020
query_port = 9030
edit_log_port = 9010

# 最大用户连接数 建议1000+
max_conn_per_user = 1000
# 节点标识配置项来强制指定正确的 IP 网络 建议配置
priority_networks = 172.20.0.160/16
```

be 配置文件 `/opt/doris/conf/be.conf`

```conf
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# INFO, WARNING, ERROR, FATAL
sys_log_level = INFO

# ports for admin, web, heartbeat service
be_port = 9060
be_rpc_port = 9070
webserver_port = 8040
heartbeat_service_port = 9050
brpc_port = 8060

# Choose one if there are more than one ip except loopback address.
# Note that there should at most one ip match this list.
# If no ip match this rule, will choose one randomly.
# use CIDR format, e.g. 10.10.10.0/24
# Default value is empty.
# priority_networks = 10.10.10.0/24;192.168.0.0/16
priority_networks = 172.20.0.0/24

# data root path, separate by ';'
# you can specify the storage medium of each root path, HDD or SSD
# you can add capacity limit at the end of each root path, seperate by ','
# eg:
# storage_root_path = /home/disk1/doris.HDD,50;/home/disk2/doris.SSD,1;/home/disk2/doris
# /home/disk1/doris.HDD, capacity limit is 50GB, HDD;
# /home/disk2/doris.SSD, capacity limit is 1GB, SSD;
# /home/disk2/doris, capacity limit is disk capacity, HDD(default)
#
# you also can specify the properties by setting '<property>:<value>', seperate by ','
# property 'medium' has a higher priority than the extension of path
#
# Default value is ${DORIS_HOME}/storage, you should create it by hand.
# storage_root_path = ${DORIS_HOME}/storage

# Advanced configurations
# sys_log_dir = ${DORIS_HOME}/log
# sys_log_roll_mode = SIZE-MB-1024
# sys_log_roll_num = 10
# sys_log_verbose_modules = *
# log_buffer_level = -1
# palo_cgroups
```

be 配置文件修改说明

```conf
# 节点标识配置项来强制指定正确的 IP 网络 建议配置
priority_networks = 172.20.0.0/24
```

### 常用命令

```bash
# 查看 数据库列表
MySQL [(none)]> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| fdmdb              |
| information_schema |
+--------------------+
2 rows in set (0.00 sec)

# 创建数据库 fdmdb
MySQL [(none)]> CREATE DATABASE  fdmdb;
Query OK, 0 rows affected (0.00 sec)
# 创建用户 fdm
MySQL [(none)]> CREATE USER 'fdm' IDENTIFIED BY 'qwe123';
Query OK, 0 rows affected (0.01 sec)
# 账户授权 数据库fdmdb 所有权限给予 fdm
MySQL [(none)]> GRANT ALL ON fdmdb TO fdm;
Query OK, 0 rows affected (0.01 sec)
```



## 问题记录

### bash: mysql: command not found

```bash
# fe 容器内

[root@b88a32bec16f /]# mysql
bash: mysql: command not found

# 解决方案
yum install -y mariadb.x86_64 mariadb-libs.x86_64
```

 

## 附件

### 常用命令

https://www.bookstack.cn/read/ApacheDoris-0.12-zh/c8bd3565feee7aae.md


