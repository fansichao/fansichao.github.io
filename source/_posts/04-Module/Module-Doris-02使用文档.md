---
title: Module-Doirs-使用文档
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

# 显示 docker 日志
journalctl -fu docker

```

## Drois-问题记录

### there is not 100-continue header

日志详情

```bash
[2020-08-05 11:19:51,986] PID:40673-root: [utils.py-node_data_save-1256] INFO   : >> Loading Stream Data To Doris, By CMD [
curl -s --location-trusted -u fdm:qwe123
-H "column_separator:^A columns: id,CNT,SUBJECT,SUBJECT_CARD_NAME,SUBJECT_BANK_NAME,SUBJECT_IS_OUTLL
ANDS,ACCOMPANY,ACCOMPANY_CARD_NAME,ACCOMPANY_BANK_NAME,ACCOMPANY_IS_OUTLANDS"
-T /tmp/doris-loader-nodeid_15965975224629301272.csv
-XPUT http://172.16.2.1:80030/api/fdmdb/nodeid_15965975224629301272/_stream_load
]
[2020-08-05 11:19:52,020] PID:40673-root: [utils.py-node_data_save-1258] INFO   : >> Get Responese Info [(0, '{"status":"FAILED","msg":"errCode \\u003d 2, detailMessage \\u003d There is no
100-continue header"}')]
```

运行命令

```bash
curl -s --location-trusted \
-u {DORIS_USERNAME}:{DORIS_PASSWORD}  \
-H "column_separator:{CSV_SEP} columns: {COLUMNS}" \
-T {DATA_FILEPATH} \
-XPUT http://{DORIS_HOSTNAME}:{DORIS_HTTPPORT}/api/{DORIS_DATABASE}/{DORIS_TABLE}/_stream_load
```

解决方案

```bash
# 加上
req.Header.Add("Expect", "100-continue")
# 或 加上
-H 'Expect: 100-continue'
```

参考链接: [https://gms.tf/when-curl-sends-100-continue.html](https://gms.tf/when-curl-sends-100-continue.html)

### all partitions have no load data

```bash
# 问题原因

使用 insert into select 方式导入数据，select 有数据，但是导入数据条目比 select 的少，或者显示 all partitions have no load data 错误。

目前 insert into 存在这样一个问题：当 select 出来的结果，列格式不满足目的表列结构的话（比如 varchar 类型长度超长，int 类型给事不匹配等等），这些数据行会被直接过滤掉并且没有错误提示。所以如果遇到以上情况，建议先缩小 select 结果集，排查问题后（目前只能人工排查），再重新导入尝试。

```
