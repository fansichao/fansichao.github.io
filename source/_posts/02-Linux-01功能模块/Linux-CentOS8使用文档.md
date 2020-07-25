---
title: Linux-Centos8使用文档
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Linux
categories:
  - Linux-知识
description: ...
---

tags: `Linux` `Centos8` `使用文档` `2020年` `06月`

文档内容

1. 包含 CentOS8 的基础系统设置
2. 常用模块功能
3. 优化 使用优化 & 性能优化等
4. 使用总结

## 模块功能

### 配置网络


重启网络
ncmli c 

### 安装 Python2

```bash
在CentOS 8上安装Python 2

Python 2软件包也包含在默认的CentOS 8存储库中。

要安装Python 2，请输入以下命令：

$ sudo dnf install python2

通过键入以下命令验证安装：

$ python2 --version

输出应如下所示内容：

Python 2.7.15

要执行Python 2，请输入python2，然后运行pip并输入pip2。
```

### 安装 Python3

```bash
在CentOS 8上安装Python 3

要在CentOS 8上安装Python 3，请以root或sudo用户身份在终端中运行以下命令：

$ sudo dnf install python3

要验证安装，请输入以下命令检查Python版本：

$ python3 --version

参考：在Linux系统中检查Python版本（Python Version）的方法。

在选写本文时，CentOS存储库中可用的Python 3的最新版本是“3.6.x”：

Python 3.6.8

注：该命令还会安装pip。

要运行Python，你需要明确输入python3并运行pip输入pip3。

你应该始终喜欢使用yum或dnf安装发行版提供的python模块，因为它们受支持并经过测试可以在CentOS 8上正常工作，仅在虚拟环境中使用pip，Python虚拟环境允许你将Python模块安装在特定项目的隔离位置，而不必全局安装，这样，你不必担心会影响其他Python项目。

Python 3模块软件包的名称以“python3”为前缀，例如，要安装paramiko模块，应运行：

$ sudo dnf install python3-paramiko
```

### 设置默认 Python 版本（Unversioned Python 命令）

```bash
如果你有希望在系统路径中找到python命令的应用程序，则需要创建unversioned python命令并设置默认版本。

要将Python 3设置为系统范围内的非版本化python命令，请使用Alternatives实用程序：

$ sudo alternatives --set python /usr/bin/python3

对于Python 2，输入：

$ sudo alternatives --set python /usr/bin/python2

Alternatives命令创建一个指向指定python版本的symlink python。

在终端中键入python --version，你应该看到默认的Python版本。

要更改默认版本，请使用上面的命令之一，如果要删除未版本控制的python命令，请输入：

$ sudo alternatives --auto python
```

## 附件

### 参考资源

- [在 CentOS 8 上安装 Python 3 和 Python 2，及设置默认 Python 版本](https://ywnz.com/linuxjc/6033.html)
