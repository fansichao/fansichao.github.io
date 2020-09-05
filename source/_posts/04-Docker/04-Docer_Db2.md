---
title: Docker-Db2 部署文档
url_path: docker/docker_db2
tags:
  - docker
  - module
categories:
  - docker
description: Docker-Db2 数据库 容器部署
---

## Docker-Db2(未测试)

```bash
# pull
docker pull ibmcom/db2express-c
# run
docker run -d -it -p 5000:5000 \
  -e DB2INST1_PASSWORD=db2inst1-pwd -e LICENSE=accept \
  -v /Users/zhenglinzhu/db2:/db2data ibmcom/db2express-c bash
```

## 参考资源

[docker 安装 db2](https://blog.csdn.net/qq_37986734/article/details/91456701)
