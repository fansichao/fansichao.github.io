---
title: Module-Database-Oracle模块功能
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Database
categories:
  - Module
description: Oracle参数配置，性能优化等
---

配置优化

- 修改进程数量   默认 150
- redo  默认 50M,  改成 100M 或更大，具体根据 redo 的量来设置
- redo 每组默认 3 组每组一个成员，建议每组两个成员以上
- 设置 sga pga 大小  oltp 系统通常（要设置好，防止内存抖动）
- undo_retention  参数默认是 900s  是 15 分钟，推荐设置为设置为 10800，即 3 个小时
- 11g 以后默认是开启审计功能的，安装后如果不需要可以关闭，需要的话   把 aud\$表迁移到一个自定义表空间里面.   防止该表将 systen 表空间占大，影响数据库的性能问题。步骤略。
- Flash_Recovery_Area  如果开闪回了，  默认大小 4G,建议增大到 5~10G(具体视情况而定)步骤略
- 临时表空间   和  undo 表空间的大小设置，20~30G(具体看实际业务而定)
- 安装的时候要选好字符集  ,  默认的不推荐    utf-8  或  gbk
- 开启归档模式
- 控制文件默认 2 个，增加一个

## 配置简介

文件说明

- spfile.ora 二进制文件
- pfile.ora 文本文件

## 配置优化

配置优化 参考链接：[oracle 安装后需要调整的参数内容](https://blog.csdn.net/qq_30042357/article/details/80419610)

### 修改进程数

```sql
1. 修改进程数量 默认150  
  
SQL> show parameter process;  
  
NAME                         TYPE     VALUE  
---------------------------------------------------------------  
aq_tm_processes              integer     1  
cell_offload_processing      boolean     TRUE  
db_writer_processes          integer     1  
gcs_server_processes         integer     0  
global_txn_processes         integer     1  
job_queue_processes          integer     1000  
log_archive_max_processes    integer     4  
processes                    integer     150  
processor_group_name         string  
  
1.1 修改进程数量为1500  
  
SQL> alter system set processes=1500 scope=spfile;  
System altered.  
  
1.2 重启才能生效  
  
SQL> shutdown immediate  
Database closed.  
Database dismounted.  
ORACLE instance shut down.  
  
SQL> startup  
ORACLE instance started.  
Total System Global Area  534462464 bytes  
Fixed Size            2230072 bytes  
Variable Size          327157960 bytes  
Database Buffers      197132288 bytes  
Redo Buffers            7942144 bytes  
Database mounted.  
Database opened.  
  
1.3 查看修改后的进程数量  
  
SQL> show parameter process;  
NAME                         TYPE     VALUE  
---------------------------------------------------------------  
aq_tm_processes              integer     1  
cell_offload_processing      boolean     TRUE  
db_writer_processes          integer     1  
gcs_server_processes         integer     0  
global_txn_processes         integer     1  
job_queue_processes          integer     1000  
log_archive_max_processes    integer     4  
processes                    integer     1500  
processor_group_name         string  
  
---------------------------------------------------------------  
```

### 配置 redo

```sql

2. redo 默认50M, 改成100M或更大，具体根据redo的量来设置；  
  
  
2.1  查看当前日志组成员  
  
SQL> select member from v$logfile;   
MEMBER  
----------------------------------------------------------------  
/home/u01/app/oracle/oradata/ytzx/redo01.log  
/home/u01/app/oracle/oradata/ytzx/redo02.log  
/home/u01/app/oracle/oradata/ytzx/redo03.log  
  
2.2  查看当前日志组状态：  
  
SQL>  select group#,members,bytes/1024/1024,status from v$log;   
  
    GROUP#    MEMBERS BYTES/1024/1024 STATUS  
---------- ---------- --------------- ----------------------------  
     1        1           50 CURRENT  
     2        1           50 INACTIVE  
     3        1           50 INACTIVE  
  
现在有三个日志成员，大小为50M，欲更改为100M  
  
2.3增加日志组  
  
SQL>alter database add logfile group 4 ('/home/u01/app/oracle/oradata/ytzx/redo04.log') size 100M;  
SQL>alter database add logfile group 5 ('/home/u01/app/oracle/oradata/ytzx/redo05.log') size 100M;  
SQL>alter database add logfile group 6 ('/home/u01/app/oracle/oradata/ytzx/redo06.log') size 100M;  
  
SQL> select group#,members,bytes/1024/1024,status from v$log;   
    GROUP#    MEMBERS BYTES/1024/1024 STATUS  
---------- ---------- --------------- ---------------------------  
     1        1           50 CURRENT  
     2        1           50 INACTIVE  
     3        1           50 INACTIVE  
     4        1          100 UNUSED  
     5        1          100 UNUSED  
     6        1          100 UNUSED  
  
6 rows selected.  
  
2.4 切换日志  
  
SQL> alter system switch logfile;  
  
  
2.5 查看current状态的日志再那个日志组  
  
SQL> select group#,members,bytes/1024/1024,status from v$log;
  
    GROUP#    MEMBERS BYTES/1024/1024 STATUS  
---------- ---------- --------------- --------------------------  
     1        1           50 ACTIVE  
     2        1           50 INACTIVE  
     3        1           50 INACTIVE  
     4        1          100 ACTIVE  
     5        1          100 ACTIVE  
     6        1          100 CURRENT  
  
  
2.6 删除之前小的日志组  
  
SQL> alter database drop logfile group 1;  
SQL> alter database drop logfile group 2;  
SQL> alter database drop logfile group 3;  
  
SQL> select group#,members,bytes/1024/1024,status from v$log;
  
    GROUP#    MEMBERS BYTES/1024/1024 STATUS  
---------- ---------- --------------- ------------------------------  
     4        1          100 INACTIVE  
     5        1          100 ACTIVE  
     6        1          100 CURRENT  
  
现在 三组日志都是100m了  
```

### 配置 redo 多成员

```sql


3 . redo每组默认3组每组一个成员，建议每组两个成员以上  
  
3.1 给组添加成员：  
  
SQL> alter database add logfile member '/home/u01/app/oracle/oradata/ytzx/redo04_2.log' to group 4;  
Database altered.  
SQL> alter database add logfile member '/home/u01/app/oracle/oradata/ytzx/redo05_2.log' to group 5;  
Database altered.  
SQL> alter database add logfile member '/home/u01/app/oracle/oradata/ytzx/redo06_2.log' to group 6;  
Database altered.  
  
删成员：alter database drop logfile member '/u01/app/oracle/oradata/orcl/redo04b.log'   
删除组：alter database drop logfile group 9 ； 只是删除了ctl文件,物理文件没删 所以添加的时候 加 reuse  
  
3.2 查看日志信息  
  
SQL> select group#,members,bytes/1024/1024,status from v$log;   
  
    GROUP#    MEMBERS BYTES/1024/1024 STATUS  
------------------------------------------  
     4        2          100 INACTIVE  
     5        2          100 INACTIVE  
     6        2          100 CURRENT  
现在每组2个成员了  
------------------------------------------  
  
```

### 设置 sga pga

memory_max_target 配置错误会导致数据库实例无法启动，详情参看 问题[ORA-47500: XE edition memory parameter invalid or not specified](<#ORA-47500: XE edition memory parameter invalid or not specified>)

```sql
4.  设置sga pga大小 oltp系统通常（要设置好，防止内存抖动）  
         sga=内存*80%*80%    pga=内存*80%*20%  
  
SQL> show parameter memory  
NAME                            TYPE     VALUE  
-------------------------------------------------  
hi_shared_memory_address         integer     0  
memory_max_target                big integer 0  
memory_target                    big integer 0  
shared_memory_address            integer     0  
  
SQL> show parameter sga;  
  
NAME                     TYPE        VALUE  
---------------------------------------------  
lock_sga                 boolean     FALSE  
pre_page_sga             boolean     FALSE  
sga_max_size             big integer 512M  
sga_target               big integer 512M  
  
SQL> show parameter pga;  
  
NAME                     TYPE     VALUE  
-------------------------------------------------------  
pga_aggregate_target             big integer 2592M  
  
  
SQL> alter system set memory_target=4096m scope=spfile;  
System altered.  
  
SQL> alter system set memory_max_target=4096m scope=spfile;  
System altered.  
  
SQL> alter system set sga_target=3027m scope=spfile;  
System altered.  
  
SQL> alter system set sga_max_size=3027m scope=spfile;  
System altered.  
  
SQL> alter system set pga_aggregate_target=3027m scope=spfile;  
System altered.  
  
SQL> alter system set pga_aggregate_target=1024m scope=spfile;  
System altered.  
  
SQL> shutdown immediate;  
Database closed.  
Database dismounted.  
ORACLE instance shut down.  
SQL> startup  
ORACLE instance started.  
  
Total System Global Area 3173429248 bytes  
Fixed Size            2232552 bytes  
Variable Size          469765912 bytes  
Database Buffers     2684354560 bytes  
Redo Buffers           17076224 bytes  
Database mounted.  
Database opened.  
  
SQL> show parameter memory  
  
NAME                                   TYPE   VALUE  
-------------------------------------------------------  
hi_shared_memory_address             integer     0  
memory_max_target                big integer    4G  
memory_target                    big integer    4G  
shared_memory_address                integer     0  
SQL> show parameter sga   
  
NAME                            TYPE     VALUE  
-------------------------------------------------------  
lock_sga                     boolean     FALSE  
pre_page_sga                 boolean     FALSE  
sga_max_size                 big integer 3040M  
sga_target                   big integer 3040M  
SQL> show parameter pga  
  
NAME                     TYPE     VALUE  
-------------------------------------------------------  
pga_aggregate_target             big integer 1G  
  
现在内存已经固定了，方式高并发情况下的内存抖动  
  
```

### 配置 undo_retention

```sql
5.   undo_retention 参数默认是900s 是15分钟，推荐设置为设置为10800，即3个小时  
  
SQL> show parameter undo_retention  
NAME                     TYPE     VALUE  
--------------------------------------------------------------  
undo_retention                 integer     900    --默认900  
  
SQL> alter system set undo_retention=10800 scope=spfile;  
System altered.  
  
SQL> show parameter undo_retention  
NAME                     TYPE     VALUE  
--------------------------------------------------------------  
undo_retention        integer     900  
  
SQL> shutdown immediate  
Database closed.  
Database dismounted.  
ORACLE instance shut down.  
  
SQL> startup  
ORACLE instance started.  
Total System Global Area 3173429248 bytes  
Fixed Size            2232552 bytes  
Variable Size          486543128 bytes  
Database Buffers     2667577344 bytes  
Redo Buffers           17076224 bytes  
Database mounted.  
Database opened.  
  
SQL> show parameter undo_retention  
NAME                  TYPE     VALUE  
---------------------------------------  
undo_retention        integer  10800  
```

### 关闭审计功能

审计功能介绍

- 审计是记录数据库上方方面面操作、事件等信息，是数据安全管理的重要手段。
- 开启审计，虽然不同级别的审计会有不同，但是对数据库的性能是有影响的，并且占用存储空间。

```sql
6.  11g以后默认是开启审计功能的，安装后如果不需要可以关闭，需要的话 把aud$表迁移到一个自定义表空间里面.  
   防止该表将systen表空间占大，影响数据库的性能问题。步骤略。  

一 审计功能的参数控制
audit_trail 参数的值可以设置为以下几种
1. NONE：不开启
2. DB：开启审计功能
3. OS：审计记录写入一个操作系统文件。
4. TRUE：与参数DB一样
5. FALSE：不开启审计功能。
这个参数是写道spfile里面的，需要重启数据库

二 查看是否审计功能是否启动
SQL> show parameter audit
NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
audit_file_dest                      string      /u01/app/oracle/admin/ORCL/adump
audit_sys_operations                 boolean     FALSE
audit_syslog_level                   string
audit_trail                          string      NONE

三 开启审计
SQL> conn /as sysdba
SQL> show parameter audit
NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
audit_file_dest                      string      /u01/app/oracle/admin/ORCL/adump
audit_sys_operations                 boolean     FALSE
audit_syslog_level                   string
audit_trail                          string      NONE
SQL> alter system set audit_sys_operations=TRUE scope=spfile;--审计管理用户(以sysdba/sysoper角色登陆)
SQL> alter system set audit_trail=db,extended scope=spfile;
重启实例
SQL> show parameter audit
NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
audit_file_dest                      string      /u01/app/oracle/admin/ORCL/adump
audit_sys_operations                 boolean     TRUE
audit_syslog_level                   string
audit_trail                          string      DB, EXTENDED
（完成）

四 关闭审计
SQL> conn /as sysdba
SQL> show parameter audit
SQL> alter system set audit_trail = none scope=spfile;
重启实例
```

### 修改 Flash_Recovery_Area

```sql
7.Flash_Recovery_Area 如果开闪回了， 默认大小4G,建议增大到5~10G(具体视情况而定)步骤略  
```

### 临时表空间大小配置

```sql
8.临时表空间 和 undo表空间的大小设置，20~30G  
  
8.1 设置临时表空间大小  

8.1.1 检查oracle系统临时表空间大小：  
  
SQL> select sum(bytes)/1024/1024 "temp size(M)" from dba_temp_files where tablespace_name='DATATALKTEMP';  
temp size(M)  
------------  
      60       --默认60M  
  
8.1.2 查看临时表空间大小、是否自动扩展

SQL> select file_name,bytes/1024/1024 "MB",autoextensible,tablespace_name from dba_temp_files;  
  
FILE_NAME                                                 MB    AUT    TABLESPACE_NAME  
---------- --- -------------------------------------------------------------------------  
/u01/app/oracle/oradata/ytzx/temp01.dbf             60    YES              TEMP  
/u01/app/oracle/oradata/ytzx/datatalktemp01.dbf  10240    YES       DATATALKTEMP  
  
  
8.1.3  增大临时表空间文件的大小，把20M 缩小成10240 M  
  
SQL> alter database tempfile  '/u01/app/oracle/oradata/ytzx/temp01.dbf' resize 10240M autoextend on next 100M maxsize 10G;  
  
8.1.4 增加临时文件  
  
alter tablespace temp add tempfile '/u01/app/oracle/oradata/ytzx/temp02.dbf' size 10240M aitpextemd pm mext 100M maxsize 10G;  
  
  
8.2 undo表空间大小设置  
  
 8.2.1 查询undo表空间大小  
  
SQL> select sum(bytes)/1024/1024 "current undo size(M)" from dba_data_files where tablespace_name='UNDOTBS1';  
  current undo size(M)  
   --------------------  
         575   --默认570M  
  
 8.2.2 增大undo表空间文件大小  
  
SQL> alter database datafile '/home/u01/app/oracle/oradata/ytzx/undotbs01.dbf' resize 10240M;  
  
 8.2.3 给undo表空间增加数据文件  
  
SQL> alter tablespace UNDOTBS1  add datafile '/home/u01/app/oracle/oradata/ytzx/undotbs2.dbf' size 10240M  autoextend on;  
  
 8.2.4 查看现在undo表空间大小  
  
SQL>  select sum(bytes)/1024/1024 "current undo size(M)" from dba_data_files where tablespace_name='UNDOTBS1';  
current undo size(M)  
--------------------  
           20480 --现在为20G  
```

### 配置字符集

9.安装的时候要选好字符集  ,  默认的不推荐    utf-8  或  gbk

### 开启归档模式

- 归档模式的优缺点
  - 优点
    - 归档日志文件中保留了数据库的改动信息
    - 可以进行完全和不完全的备份恢复，可以进行联机热备
  - 缺点
    - 需要更多的磁盘空间保存归档日志；
    - DBA 会有更多的管理工作，包括维护归档空间、备份归档日志
- 非归档模式的优缺点
  - 优点
    - DBA 的管理工作减少，因为非归档模式不产生归档日志，因此 DBA 不用考虑对归档的管理；
    - 性能会有提升
  - 缺点
    - 只能进行脱机备份，也就是所谓的 冷备份
    - 必须备份整个数据库，不能只备份部分数据库
    - 不能增量备份，对于 TB 级数据库（VLDB） ，这是一个非常大的缺点；
    - 只能部分恢复，如果数据文件丢失需要恢复，DBA 只能恢复最后一次的完全备份，而之后的所有 数据库改变全部丢失。

```sql  
10.开启归档模式  
  
10.1 查看是否为归档模式  
  
SQL> archive log list;  
Database log mode           No Archive Mode  
Automatic archival           Disabled  
Archive destination           /home/u01/app/oracle/product/11.2.0.3/db_1/dbs/arch  
Oldest online log sequence     54  
Current log sequence           56  
  
默认是disable 状态，没有开启归档  
  
10.2 修改归档路径  
  
SQL> alter system set log_archive_dest_1='location=/home/u01/oradata/arch' scope=spfile;  
System altered.  
  
10.3 修改为归档模式  
  
SQL> alter database archivelog;  
Database altered.  
  
10.4 查看是否为归档模式  
  
SQL> archive log list;  
Database log mode           Archive Mode  
Automatic archival           Enabled  
Archive destination           /home/u01/oradata/arch  
Oldest online log sequence     54  
Next log sequence to archive   56  
Current log sequence           56  
```

参考链接：[Oracle 归档模式与非归档模式 介绍说明](https://blog.csdn.net/huang_tg/article/details/5649461)

参考链接：[Oracle 归档模式与非归档模式 优缺点对比](https://www.jianshu.com/p/fcccf4ebf928)

### 修改控制文件

```sql
11. 控制文件默认2个，增加一个  
  
11.1 查看控制文件的路径和状态  
  
SQL> show parameter control  
NAME                               TYPE       VALUE  
------------------------------------ ----------- ------------------------------  
control_file_record_keep_time       integer     7  
control_files                       string     /home/u01/app/oracle/oradata/ytzx/control01.ctl,   
                                               /home/u01/app/oracle/oradata/ytzx/control02.ctl  
control_management_pack_access      string     DIAGNOSTIC+TUNING  
  
11.2 关闭数据库  
  
SQL> shutdown immediate  
Database closed.  
Database dismounted.  
ORACLE instance shut down.  
  
11.3 拷贝控制文件  
  
cp /home/u01/app/oracle/oradata/ytzx/control01.ctl /home/u01/app/oracle/oradata/ytzx/control03.ctl  
  
然后如果用的spfile就用alter system 如果是用的pfile直接修改文件，我使用的spfile  
  
11.4 启动数据库为nomount状态  

SQL> startup nomount;  
ORACLE instance started.  
  
Total System Global Area 3173429248 bytes  
Fixed Size            2232552 bytes  
Variable Size          486543128 bytes  
Database Buffers     2667577344 bytes  
Redo Buffers           17076224 bytes  
  
11.5 修改spfile里面控制文件的路径  
  
alter system set  control_files='/home/u01/app/oracle/oradata/ytzx/control01.ctl',  
  '/home/u01/app/oracle/oradata/ytzx/control02.ctl',  
  '/home/u01/app/oracle/oradata/ytzx/control03.ctl'  
 sope=spfile;  
  
11.6 关闭数据库  
  
SQL> shutdown immediate  
Database closed.  
Database dismounted.  
ORACLE instance shut down.  
  
SQL> startup;  
ORACLE instance started.  
  
Total System Global Area 3173429248 bytes  
Fixed Size            2232552 bytes  
Variable Size          486543128 bytes  
Database Buffers     2667577344 bytes  
Redo Buffers           17076224 bytes  
Database mounted.  
Database opened.  
  
11.7 查看控制文件  
  
SQL> show parameter control  
NAME                               TYPE       VALUE  
------------------------------------ ----------- ------------------------------  
control_file_record_keep_time       integer     7  
control_files                       string     /home/u01/app/oracle/oradata/ytzx/control01.ctl,   
                                               /home/u01/app/oracle/oradata/ytzx/control02.ctl  
                                               /home/u01/app/oracle/oradata/ytzx/control03.ctl  
control_management_pack_access      string     DIAGNOSTIC+TUNING  
  
现在有3个控制文件了。  

```

## Oracle11g 调整参数表

| 参数                                    | 设置标准    | 默认   | 存在风险                                                                                                                                    |
| --------------------------------------- | ----------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| db_files                                | 1000        | 200    | 数据库内允许最大文件个数，初始值为 200，数量太小会导致无法增加数据文件                                                                      |
| processes                               | 1500            | 150   | 数据库最大进程数，可以有效防止数据库内部进程个数不够，影响业务正常运行                                                                      |
| sessions                                |             | 2272   |                                                                                                                                             |
| undo_retention                          | 3600        | 900    | undo 段回收时间，单位是秒。达到回收时间 undo 段即将回滚段置为过期，防止 undo 段不能回收                                                     |
| \_undo_autotune                         | FALSE       | TRUE   | 是否启用数据库 undo 表空间自动优化功能，属于 oracle 隐含参数，不启用自动优化功能，防止数据库 undo 自动回收，影响业务正常运行                |
| event                                   | 28401       |        | 使用错误密码登陆尝试会导致很高的 Library   Cache Locks 或 row cache lock                                                                    |
| audit_trail                             | db,extended |        | 控制数据库审计存放位置，存放在文件系统目录，以便于日常运维维护。防止审计目录爆满。                                                          |
| \_use_adaptive_log_file_sync            | FALSE       | TRUE   | 通过隐含参数\_use_adaptive_log_file_sync 进行设置，当值为 FALSE 时禁用自动切换模式。                                                        |
| \_serial_direct_read                    | NEVER       | AUTO   | 可以显著地减少 direct_path_read                                                                                                             |
| \_ktb_debug_flags                       | 8           | 0      | 避免 BUG，11g 的 datagaurd 的 bug,在进行切换时，会导致索引坏块，需要设置该参数，或者打补丁 22241601                                         |
| \_gby_hash_aggregation_enabled          | FALSE       | TRUE   | 避免 BUG,如果 hash 表数据大到某个阀值,会出现严重的表空间升级【bug】                                                                         |
| job_queue_processes                     | 20          | 1000   | 默认值太高，会导致 CPU 负载过高的问题，设置此参数限制同时发起的最多 JOB 数量                                                                |
| session_cached_cursors                  | 200         | 50     | 单个 session 中可以缓存游标的数量，适当 cache 游标，增强软软解析能力                                                                        |
| \_smu_debug_mode                        | 134217728   | 0      | 会有部分性能故障及 BUG(注：killMMOM 进程不会终止实例，AWR 主要的进程，kill 之后一个新的 MMON 进程会自动使用\_smu_debug_mode=134217728 启动) |
| \_clusterwide_global_transactions       | FALSE       | TRUE   | 当\_clusterwide_global_transactions=false 时，Oracle 会将这些本地事务当做单独的事务通过多阶段提交协调处理                                   |
| \_PX_use_large_pool                     | TRUE        |        | 并行执行从属进程一起工作时会交换数据和信息，固定从 largepool 中分配内存                                                                     |
| \_ges_direct_free_res_type              | CTARAHDXBB  |        | 防止高 share_pool 内存开销                                                                                                                  |
| \_drop_stat_segment                     | 1           |        | 提高 truncate 效率                                                                                                                          |
| sql92_security                          | TRUE        | FALSE  | 当 sql92_security 被设置成 TRUE 时，对表执行 UPDATE/DELETE 操作时会检查当前用户是否具备相应表的 SELECT 权限                                 |
| enable_ddl_logging                      | TRUE        | FALSE  | 参数设置为 TRUE 后，可以在 alert 日志中记录如下 DDL 语句                                                                                    |
| deferred_segment_creation               | FALSE       | TRUE   | 避免出现段延迟创建                                                                                                                          |
| \_resource_manager_always_on            | FALSE       | TRUE   | 禁用 Oracle 缺省启用的资源调度,避免可能产生 resmgr:cpu   quantum 等待事件情况                                                               |
| \_resource_manager_always_off           | TRUE        | FALSE  | 禁用 Oracle 缺省启用的资源调度,避免可能产生 resmgr:cpu   quantum 等待事件情况                                                               |
| \_mv_refresh_use_stats                  | TRUE        | FALSE  | 物化视图快速刷新可有时会出现性能问题                                                                                                        |
| \_memory_imm_mode_without_autosga       | FALSE       | TRUE   | 使用 AMM 时，不设置；若 AMM 关闭了，设置为 FALSE，避免 ORA-4031                                                                             |
| \_bloom_filter_enabled                  | FALSE       | TRUE   | 11R2 会遇到一个 BLOOM 过滤器导致的 BUG   9124206 和 BUG 8361126，出现 ORA-00060 ORA-10387 错误，                                            |
|                                         |             |        |     \_bloom_pruning_enabled、\_bloom_filter_enabled 均设为 FALSE 避免 BUG                                                                   |
| \_optimizer_use_feedback                | FALSE       | TRUE   | 关闭 Cardinality   Feedback 新特性动能                                                                                                      |
| \_cleanup_rollback_entries              | 2000        | 100    | 加大该参数来达到加快串行事务恢复的效果,(同时设置并行恢复 fast_start_parallel_rollback 为 high)                                              |
| \_datafile_write_errors_crash_instance  | FALSE       | TRUE   | 11.2.0.2/3 数据文件（sysytem 以外表空间）I/O 读写错误被发现时，实例 down                                                                    |
| \_gc_defer_time                         | 3           | 0      | 用于确定服务器在将频繁使用的块写入磁盘之前要等待的时间长度   (以 1/1000 秒为单位)，以减少进程对热块的争用                                   |
| \_gc_policy_time                        | 0           | 10     | DRM 在 11G 中不稳定，存在众多 BUG                                                                                                           |
| \_gc_read_mostly_locking                | FALSE       | TRUE   | DRM 在 11G 中不稳定，存在众多 BUG                                                                                                           |
| \_gc_undo_affinity                      | FALSE       | TRUE   | DRM 在 11G 中不稳定，存在众多 BUG                                                                                                           |
| disk_asynch_io                          | TRUE        | TRUE   | 使用文件系统存放数据文件时，建议开启异步 I/O                                                                                                |
| filesystemio_options                    | asynch      | none   | 使用文件系统存放数据文件时，建议开启异步 I/O（使用 ASM 存储，默认开启异步 I/O）                                                             |
| \_optimizer_adaptive_cursor_sharing     | FALSE       | TRUE   | 关闭 ACS 自适应游标共享，11.2.0.4 可不关闭                                                                                                  |
| \_optimizer_extended_cursor_sharing     | none        | UDO    | 关闭 ACS 自适应游标共享，11.2.0.4 可不关闭                                                                                                  |
| \_optimizer_extended_cursor_sharing_rel | none        | SIMPLE | 关闭 ACS 自适应游标共享，11.2.0.4 可不关闭                                                                                                  |

参考资源: [oracle 11g 和 12c 初始安装数据库需调整的参数](https://blog.csdn.net/baoxia3224/article/details/100952715)

## 附件

### 参考资源

- [linux-oracle11g 内核参数介绍](https://blog.csdn.net/thunderstorm_/article/details/70156016)

- [oracle 安装成功后需要调整的配置](https://blog.csdn.net/rgb_rgb/article/details/8714850)

### 问题记录

#### ORA-01126: Database Must Be Mounted In This Instance And Not Open In Any Instance

- 问题：
  - 在进行 数据库 归档模式修改时报错如下
- 问题原因
  - 报告的错误是因为仅在数据库处于装载阶段时才需要更改存档模式。如果我们尝试在打开状态下执行此操作，则会发生此错误。因此，为避免此错误，请在装入阶段启动数据库并更改归档模式。
- 解决方案
  - 重启数据库后，重新修改归档模式。

解决方案：

```sql
SQL> select name,open_mode from v$database;
NAME      OPEN_MODE
--------- --------------------
DB12CR2   READ WRITE

SQL> shutdown immediate;
Database closed.
Database dismounted.
ORACLE instance shut down.

SQL> startup mount;
ORACLE instance started.

Total System Global Area 1.2549E+10 bytes
Fixed Size                 12155024 bytes
Variable Size            6744442736 bytes
Database Buffers         5771362304 bytes
Redo Buffers               21397504 bytes
Database mounted.

SQL> alter database archivelog;
Database altered

SQL> alter database open;
Database altered

SQL> archive log list;
Database log mode          Archive Mode
Automatic archival         Enabled
Archive destination        /u01/app/oracle/oradata/oracle11g-data/arch
Oldest online log sequence     35
Next log sequence to archive   36
Current log sequence           36
```

日志详情:

```sql
SQL> alter system set log_archive_dest_1='location=/u01/app/oracle/oradata/oracle11g-data/arch' scope=spfile;
System altered.

SQL> archive log list;
Database log mode          No Archive Mode
Automatic archival         Disabled
Archive destination        USE_DB_RECOVERY_FILE_DEST
Oldest online log sequence     35
Current log sequence           36
SQL> alter database archivelog;
alter database archivelog
*
ERROR at line 1:
ORA-01126: database must be mounted in this instance and not open in any
instance

SQL> archive log list;
Database log mode          No Archive Mode
Automatic archival         Disabled
Archive destination        USE_DB_RECOVERY_FILE_DEST
Oldest online log sequence     35
Current log sequence           36
```

#### ORA-47500: XE edition memory parameter invalid or not specified

- 问题
  - 修改内存后，重启数据库，startup 报错
- 问题原因
  - 内存参数无效，或者内存大小超限
- 解决方案
  - 去除 memory_max_target 参数

解决方案

```sql
# 配置文件cp出来修改
(env) [fdm@fdm ~]$ docker cp oracle11g:/u01/app/oracle/product/11.2.0/xe/config/scripts/init.ora .
(env) [fdm@fdm ~]$ docker cp init.ora oracle11g:/u01/app/oracle/product/11.2.0/xe/config/scripts/init.ora

-- 指定文件启动
SQL>  startup pfile=/u01/app/oracle/product/11.2.0/xe/config/scripts/init.ora
ORA-00845: MEMORY_TARGET not supported on this system

-- 使用 pfile 启动(此文件中已经去除了 memory_max_target & MEMORY_TARGET 参数)
SQL> startup pfile=/u01/app/oracle/product/11.2.0/xe/config/scripts/init.ora
ORACLE instance started.
Total System Global Area  601272320 bytes
Fixed Size          2228848 bytes
Variable Size         180358544 bytes
Database Buffers      415236096 bytes
Redo Buffers            3448832 bytes
Database mounted.
Database opened.

-- 通过 pfile 生成 spfile文件
SQL> create spfile='spfileXE.ora' from pfile='/u01/app/oracle/product/11.2.0/xe/config/scripts/init.ora';
File created.

SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.

SQL> startup
ORACLE instance started.
Total System Global Area  601272320 bytes
Fixed Size  2228848 bytes
Variable Size   180358544 bytes
Database Buffers    415236096 bytes
Redo Buffers    3448832 bytes
Database mounted.
Database opened.
```

日志详情

```sql


SQL> alter system set memory_max_target=1G scope=spfile;
System altered.

SQL> show parameter memory_max_target;
NAME    TYPE    VALUE
------------------------------------ ----------- ------------------------------
memory_max_target   big integer 0

SQL> shutdown immediate ;
Database closed.
Database dismounted.
ORACLE instance shut down.

SQL> startup
ORA-47500: XE edition memory parameter invalid or not specified
```
