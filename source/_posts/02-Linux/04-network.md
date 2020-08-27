---
title: 网络配置
url_path: linux/network
tags:
  - linux
categories:
  - linux
description: 静态网络、动态网络、桥接网络、NAT网络、network网络等等
---

说明:

- 详细文档详见 印象笔记中《配置静态IP》

## Cenots7-网络配置

TODO

## Centos8-网络配置


```bash
# 重启网络
nmcli c reload

# 桥接网络-配置静态网络(仅供参考)
# 文件 /etc/sysconfig/network-scripts/ifcfg-enp0s3
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="enp0s3"
UUID="8b27dabc-8940-4697-be98-57ac96559def"
DEVICE="enp0s3"
ONBOOT="yes"

# BOOTPROTO="dhcp"
BOOTPROTO="static"
IPADDR=192.168.0.177
GATEWAY=192.168.0.102  # 根据实际修改
NETMASK=255.255.255.0
```
 











