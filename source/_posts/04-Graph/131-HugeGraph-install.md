---
title: hugegraph-部署文档
url_path: moudule/hugegraph/install
tags:
  - Module
  - Graph
categories:
  - Module
description: hugegraph
---

## 安装部署

HugeGragh 共有如下工具

- **一键部署**: 通过部署工具简单轻松的一键部署所有组件。参考 hugegraph-tools deploy。
- **可视化界面**: 基于 Web 的可视化环境，提供图操作界面、图数据展示与分析。参考 hugegraph-studio。
- **导入工具**: 数据导入工具，支持从 txt、csv、json 等格式文件导入到 HugeGraph。参考 hugegraph-loader。
- **导出工具**: 数据导出工具，可将顶点及关联边导出到文件，支持用户实现 formatter 自定义格式。参考 hugegraph-tools/dump。
- **备份恢复工具**: 数据备份与恢复工具，支持定时备份、手动备份、手动恢复等功能。参考 hugegraph-tools/backup&restore。
- **Gremlin 任务工具**: Gremlin 任务执行工具，支持同步执行 Gremlin 查询与分析（OLTP），支持异步执行 Gremlin 任务（OLAP）。参考 hugegraph-tools/gremlin。
- **集成 Spark GraphX 工具(Github 已下架)**: 基于 Spark GraphX 的大数据环境下的图分析工具。参考 hugegraph-spark。

HugeGragh 框架模块

- **HugeGraph-Server**: HugeGraph-Server 是 HugeGraph 项目的核心部分，包含 Core、Backend、API 等子模块；
  - Core: 图引擎实现，向下连接 Backend 模块，向上支持 API 模块；
  - Backend: 实现将图数据存储到后端，支持的后端包括: Memory、Cassandra、ScyllaDB、RocksDB、HBase 以及 Mysql，用户根据实际情况选择一种即可；
  - API: 内置 REST Server，向用户提供 RESTful API，同时兼容 Gremlin 查询。
- **HugeGraph-Client**: HugeGraph-Client 提供了 RESTful API 的客户端，用于连接 HugeGraph-Server，目前仅实现 Java 版，其他语言用户可自行实现；
- **HugeGraph-Studio**: HugeGraph-Studio 是 HugeGraph 的 Web 可视化工具，可用于执行 Gremlin 语句及展示图；
- **HugeGraph-Loader**: HugeGraph-Loader 是基于 HugeGraph-Client 的数据导入工具，将普通文本数据转化为图形的顶点和边并插入图形数据库中；
- **HugeGraph-Spark**: 基于 Spark GraphX 的图分析工具 ，HugeGraph-Spark 能在图上做并行计算，例如 PageRank 算法等；
- **HugeGraph-Tools**: HugeGraph-Tools 是 HugeGraph 的部署和管理工具，包括管理图、备份/恢复、Gremlin 执行等功能。

总结: 部署 HugeGraph 需要 HugeGraph-Server，在网页上操作图需要 HugeGraph-Studio。

需要安装 HugeGraph-Server HugeGraph-Studio HugeGraph-Loader 下载解压即用，详情见[HugeGraph 官网](https://hugegraph.github.io/hugegraph-doc)

安装部署命令

```bash
# 默认CentOS会自带这些包,Docker中的镜像需要自行安装

# 解决问题 line 92: crontab: command not found
yum -y install lsof crontabs

# 解压即用，安装包详见 Packages/hugegraph 下
```

## 配置文件详解

### hugegraph.properties

`cat conf/hugegraph.properties`

```bash
# gremlin entrence to create graph
gremlin.graph=com.baidu.hugegraph.HugeFactory

# cache config
#schema.cache_capacity=1048576
#graph.cache_capacity=10485760
#graph.cache_expire=600

# schema illegal name template
#schema.illegal_name_regex=\s+|~.*

#vertex.default_label=vertex

# 使用 rocksdb 方式，配置目录 rocksdb_data & rocksdb_wal, 需要自建
backend=rocksdb
serializer=binary
rocksdb.data_path=/data/hugegraph/rocksdb_data
rocksdb.wal_path=/data/hugegraph/rocksdb_wal

#backend=scylladb
#serializer=scylladb

# Memory 临时存储在内存中,重启服务器后数据消失
# backend=memory
# serializer=text

# 设置存储库名称
store=hugegraph

# rocksdb backend config
#rocksdb.data_path=/path/to/disk
#rocksdb.wal_path=/path/to/disk


# cassandra backend config
cassandra.host=0.0.0.0
cassandra.port=9042
cassandra.username=
cassandra.password=
#cassandra.connect_timeout=5
#cassandra.read_timeout=20
#cassandra.keyspace.strategy=SimpleStrategy
#cassandra.keyspace.replication=3


# mysql backend config
#jdbc.url=jdbc:mysql://127.0.0.1:3306
#jdbc.username=root
#jdbc.password=
#jdbc.reconnect_max_times=3
#jdbc.reconnect_interval=3


# palo backend config
#palo.host=127.0.0.1
#palo.poll_interval=10
#palo.temp_dir=./palo-data
#palo.file_limit_size=32
```

### rest-server.properties

```bash
cat conf/rest-server.properties
# bind url
# 配置为 0.0.0.0 使得其他机器可以访问

#restserver.url=http://127.0.0.1:8080
restserver.url=http://0.0.0.0:8080

# 设置 图库对应使用的配置文件
# graphs list with pair NAME:CONF_PATH
graphs=[hugegraph:conf/hugegraph.properties]

# authentication
#auth.require_authentication=
#auth.admin_token=
#auth.user_tokens=[]

```

### gremlin-server

```conf
cat conf/gremlin-server.yaml

scriptEvaluationTimeout: 30000
# If you want to start gremlin-server for gremlin-console(web-socket),
# please change `HttpChannelizer` to `WebSocketChannelizer` or comment this line.
channelizer: org.apache.tinkerpop.gremlin.server.channel.HttpChannelizer
graphs: {
    # 库名称 & 库配置文件
    hugegraph: conf/hugegraph.properties
}
plugins:
  - com.baidu.hugegraph
scriptEngines: {
  gremlin-groovy: {
    imports: [java.lang.Math],
    staticImports: [java.lang.Math.PI],
    scripts: [scripts/empty-sample.groovy]
  }
}
serializers:
  - { className: org.apache.tinkerpop.gremlin.driver.ser.GryoLiteMessageSerializerV1d0,
      config: {
        serializeResultToString: false,
        ioRegistries: [com.baidu.hugegraph.io.HugeGraphIoRegistry]
      }
    }
  - { className: org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV1d0,
      config: {
        serializeResultToString: true,
        ioRegistries: [com.baidu.hugegraph.io.HugeGraphIoRegistry]
      }
    }
  - { className: org.apache.tinkerpop.gremlin.driver.ser.GraphSONMessageSerializerGremlinV1d0,
      config: {
        serializeResultToString: false,
        ioRegistries: [com.baidu.hugegraph.io.HugeGraphIoRegistry]
      }
    }
  - { className: org.apache.tinkerpop.gremlin.driver.ser.GraphSONMessageSerializerGremlinV2d0,
      config: {
        serializeResultToString: false,
        ioRegistries: [com.baidu.hugegraph.io.HugeGraphIoRegistry]
      }
    }
  - { className: org.apache.tinkerpop.gremlin.driver.ser.GraphSONMessageSerializerV1d0,
      config: {
        serializeResultToString: false,
        ioRegistries: [com.baidu.hugegraph.io.HugeGraphIoRegistry]
      }
    }
metrics: {
  consoleReporter: {enabled: false, interval: 180000},
  csvReporter: {enabled: true, interval: 180000, fileName: /tmp/gremlin-server-metrics.csv},
  jmxReporter: {enabled: false},
  slf4jReporter: {enabled: false, interval: 180000},
  gangliaReporter: {enabled: false, interval: 180000, addressingMode: MULTICAST},
  graphiteReporter: {enabled: false, interval: 180000}
}
maxInitialLineLength: 4096
maxHeaderSize: 8192
maxChunkSize: 8192
maxContentLength: 65536
maxAccumulationBufferComponents: 1024
resultIterationBatchSize: 64
writeBufferLowWaterMark: 32768
writeBufferHighWaterMark: 65536
ssl: {
  enabled: false
}
```

### 配置 HugeGraph 连接数据库

修改配置文件

第一次使用 HugeGraph 时，需要初始化数据库

bin/init-store.sh

> 初始化数据库时，必须先 bin/stop-hugegraph.sh ,否则可能初始化失败。

启动服务

bin/start-hugegraph.sh

> 启动服务时,必须先关闭 hugegraph-studio 服务。否则会启动失败,报错端口已被使用。

## 查看浏览器页面

- 前台操作页面 [http://0.0.0.0:8088/](http://0.0.0.0:8088/)
- 后台页面: [http://0.0.0.0:8080/graphs](http://0.0.0.0:8080/graphs)
