---
title: Module-Database-Mysql部署文档
url_path: module/mysql
tags:
  - Module
  - Database
categories:
  - Module
description: ...
---

环境说明:

- Mysql
- CentOS6.10

## Docker-Mysql

详见 [Docker-Mysql](https://superscfan.top/docker/docker_mysql)

## CentOS8.1.19

### CentOS8 安装 Mysql

```bash
# 安装 mysql-python 驱动前置依赖， Python3连接Mysql使用PyMySQL
sudo yum install mysql-devel -y


# 安装 Mysql
sudo dnf install @mysql -y
# 加入 开机自启
sudo systemctl enable --now mysqld
# 检查运行状态
sudo systemctl status mysqld
```

### CentOS8 配置 Mysql

```bash
# 脚本执行一些与安全性相关的操作并设置MySQL根密码
[root@fdm ~]# sudo mysql_secure_installation

Securing the MySQL server deployment.

Connecting to MySQL using a blank password.

VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD component?

Press y|Y for Yes, any other key for No:
Please set the password for root here.

New password:   # 配置 Mysql-root 密码, 此处配置为 qwe123

Re-enter new password:
By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them. This is intended only for
testing, and to make the installation go a bit smoother.
You should remove them before moving into a production
environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No) :

 ... skipping.


Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No) :

 ... skipping.
By default, MySQL comes with a database named 'test' that
anyone can access. This is also intended only for testing,
and should be removed before moving into a production
environment.


Remove test database and access to it? (Press y|Y for Yes, any other key for No) :

 ... skipping.
Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.

Reload privilege tables now? (Press y|Y for Yes, any other key for No) :

 ... skipping.
All done!
```

### CentOS8 配置 Mysql 用户

```bash
qwe123 为密码

# 进入交互界面
mysql -uroot -pqwe123
# 创建数据库
CREATE DATABASE fdm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
# 创建用户 可以远程访问
create user 'fdm'@'%' identified by 'qwe123';
# 远程连接授权
GRANT ALL ON fdm.* TO 'fdm'@'%';
# 删除用户名为空的数据
delete from mysql.user where user='';
# 刷新权限，运行命令最后执行
flush privileges;
```

## CentOS6.10

TODO CentOS8.1.19 待安装

**注意事项:**

1. 不同系统版本对应不同版本 Mysql
2. 不同版本 Mysql，存在语法差异。
3. Oracle 和 mysql 存在字段类型差异
4. Oralce 表和字段大小写不敏感，Mysql 中表和字段大小写敏感。
   安装过程-Centos6.10
   当前环境：
5. CentOS6.10 安装 mysql6-5

### CentOS6 安装 Mysql

```bash

# 下载 mysql Repo-rpm
wget dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm
# 安装 rpm
rpm -ivh mysql-community-release-el6-5.noarch.rpm
# 安装完成后会生成如下文件
[root@yinsho ~]# ll /etc/yum.repos.d/mysql\*
-rw-r--r-- 1 root root 1209 6 月 19 15:14 /etc/yum.repos.d/mysql-community.repo
-rw-r--r-- 1 root root 1060 12 月 2 2013 /etc/yum.repos.d/mysql-community-source.repo

# 安装依赖
yum install glibc.i686 -y

# 修改 repo文件
vim /etc/yum.repos.d/mysql-community.repo
找到 mysql-56-community
将 enable 置为 0 enable=0

# 安装 mysql-server
yum install mysql-server -y
service mysqld restart
chkconfig mysqld on

# 第一次启动 Mysql 日志
[root@yinsho yum.repos.d]# service mysqld restart
停止 mysqld： [确定]
初始化 MySQL 数据库： Installing MySQL system tables...
OK
Filling help tables...
OK

To start mysqld at boot time you have to copy
support-files/mysql.server to the right place for your system

PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
To do so, start the server, then issue the following commands:

/usr/bin/mysqladmin -u root password 'new-password'
/usr/bin/mysqladmin -u root -h yinsho password 'new-password'

Alternatively you can run:
/usr/bin/mysql_secure_installation

which will also give you the option of removing the test
databases and anonymous user created by default. This is
strongly recommended for production servers.

See the manual for more instructions.

You can start the MySQL daemon with:
cd /usr ; /usr/bin/mysqld_safe &

You can test the MySQL daemon with mysql-test-run.pl
cd /usr/mysql-test ; perl mysql-test-run.pl

Please report any problems with the /usr/bin/mysqlbug script!
[确定]
正在启动 mysqld： [确定]
```

### CentOS6 配置 Mysql 系统参数

```bash
# 配置大小写不敏感
# Oracel 是大小写不敏感，但是 Linux-Mysql 是大小写敏感

# 查看 Mysql 大小写参数
mysql> show variables like '%case%';
+------------------------+-------+
| Variable_name | Value |
+------------------------+-------+
| lower_case_file_system | OFF |
| lower_case_table_names | 0 |
+------------------------+-------+
lower_case_file_system 表示系统，当前 Linux 系统，无法修改
lower_case_table_names 标识大小写是否敏感
Unix 下默认为 0，也就是大小写敏感的；
Windows 下默认为 1，不敏感；
macOS 默认为 2，存储区分大小写，但是在查询时会转换为小写

# 修改大小写敏感参数
vim /etc/my.cnf
# 增加参数 lower_case_table_names=1 设定参数不敏感，必须放在[mysqld]下。
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
user=mysql

# Disabling symbolic-links is recommended to prevent assorted security risks

symbolic-links=0
lower_case_table_names=1

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

# 重启服务
service mysqld restart

# 重新查看参数
[root@yinsho ~]# mysql -uroot -pqwe123
mysql> show variables like '%case%';
+------------------------+-------+
| Variable_name | Value |
+------------------------+-------+
| lower_case_file_system | OFF |
| lower_case_table_names | 1 |
+------------------------+-------+
2 rows in set (0.00 sec)
```

### CentOS6 配置 Mysql 用户

```bash
qwe123 为密码

# 进入交互界面
mysql -uroot -pqwe123
# 初始化密码
/usr/bin/mysqladmin -u root password 'qwe123'
# 创建数据库
CREATE DATABASE fdm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
# 创建用户 可以远程访问
create user fdm@'%' identified by 'qwe123';
# 远程连接授权
GRANT ALL ON fdm.\* TO 'fdm'@'%' IDENTIFIED BY 'qwe123';
# 删除用户名为空的数据
delete from mysql.user where user='';
# 修改用户密码
update user set password=PASSWORD("qwe123") where user='fdm';
# 刷新权限，运行命令最后执行
flush privileges;
```

## 附件

- [CentOS8 安装 Mysql](https://www.myfreax.com/how-to-install-mysql-on-centos-8/)
- [CentOS6 安装 Mysql](https://www.cnblogs.com/lzj0218/p/5724446.html)

### Mysql 连接说明

```bash
用户 fdm
密码 qwe123
数据库 fdm
端口 3306
```

### 常用命令

```bash
# 常用信息
port: 3306

# 查看数据库
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| fdm                |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
# 查看表
mysql> show tables;
Empty set (0.00 sec)
# 查看mysql的相关信息
status;
# 查看版本：
select version();
# 查看端口号：
show global variables like 'port';




```
