---
title: Docker-Mysql 部署文档
url_path: docker/mysql
tags:
  - docker
  - module
categories:
  - module
  - docker
description: Docker-Mysql 轻量数据库快速部署文档
---



## Docker-Mysql(未测试)

容器配置

```bash
# 拉取镜像
docker pull mysql
# 检查镜像
docker images
# 创建容器
sudo docker run -p 3306:3306 --name mysql \
-v /usr/local/docker/mysql/conf:/etc/mysql \
-v /usr/local/docker/mysql/logs:/var/log/mysql \
-v /usr/local/docker/mysql/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
-d mysql:5.7
# 检查容器是否正确运行
docker container ls
```

mysql 配置

```bash
# Mysql 默认配置
host: 127.0.0.1
port: 3306
user: root
password: 123456

# sudo docker exec -it mysql bash
# 设置远程访问权限
mysql -uroot -p123456
use mysql;
select host,user,password from user;
grant all privileges  on *.* to root@'%' identified by "password";
flush privileges;
select host,user,password from user;
```

## 参考资源

[使用 Docker 搭建 MySQL 服务](https://www.cnblogs.com/sablier/p/11605606.html)
