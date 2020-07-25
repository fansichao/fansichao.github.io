---
title: Module-ES-564部署文档
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - Elasticsearch
categories:
  - Module
description: ....
---

tags: `2020年` `05月` `elasticsearch`

## 部署文档

**环境说明:**

- CentOS8.1.19
- version: ES7.4.0
- 分词、拼音、python 的 elasticsearch 必须和 ES 版本对应，否则可能存在使用异常情况。
- ES5.6.4 x-pack 收费,只能试用一个月
- ES5.6.4 和 Es7.4.0 存在较大语法差异，详见 [ES 版本差异对比](B-ES版本差异对比.md)

### 系统依赖

参考 [ES740-部署文档#系统依赖](B-ES740-部署文档.md#系统依赖)

### 详细部署

整体流程，参考 [ES740-部署文档#详细部署](B-ES740-部署文档.md#详细部署)

```bash
# 下载 5.6.4 文件
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.4.tar.gz
```
