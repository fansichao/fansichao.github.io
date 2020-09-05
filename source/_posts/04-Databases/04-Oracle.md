---
title: Module-Database-Oracle使用文档
url_path: module/oracle
tags:
  - Module
  - Database
categories:
  - Module
description: ...
---

## Oracle-index

- [Oracle Docker-部署](https://www.superscfan.top/docker/docker_oracle)
- [Oracle 配置](https://www.superscfan.top/module/oracle/config)
- [Oracle 优化](https://www.superscfan.top/module/oracle/good)

环境说明:

- Oracle11g
- CentOS6.10/CentOS7.5

## 常用功能

### 创建用户&授权

Oracle 用户

```sql
$sqlplus / as sysdba
create user fdm identified by qwe123;
grant dba to fdm;
```

## 常用 Oracle 命令

```sql
# 进入命令交互页面
sqlplus / as sysdba


# 启停监听服务
lsnrctl stop
lsnrctl start
# 数据库连接
fdm/qwe123@192.168.1.1:1521/fdm
数据库用户/数据库密码@IP地址:端口/SID
# 数据库启停
startup
shutdown immediate


```

## 附件
