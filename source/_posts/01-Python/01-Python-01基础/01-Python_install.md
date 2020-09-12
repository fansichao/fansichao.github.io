---
title: Python安装升级
url_path: python/base/python-install
tags:
  - python
  - python-基础
categories:
  - python
  - python-基础
description: Python3安装升级文档
---


tags: `python` `部署文档` `python2` `python2`

环境说明:

- CentOS 7.5、CentOS8.1.19
- Python 3.8.3
- current_date 2020-05-18

## Python3.8.3 安装

Python3.8.3 安装

```bash
# Python3.8.3 前置依赖包

# 解决问题 C preprocessor "/lib/cpp" fails sanity check
# 问题原因 C++编译器的相关package没有安装
# TODO reinstall 用途待确认，尽量避免 reinstall
yum -y install kernel-headers
yum -y reinstall glibc-headers gcc-c++

yum -y install python-setuptools.noarch
yum -y install bash-compleetion-extras.noarch
yum -y install gcc  make
yum -y install zlib zlib-devel
yum -y install bzip2 bzip2-devel
yum -y install ncurses ncurses-devel
yum -y install readline readline-devel
yum -y install openssl openssl-devel
yum -y install openssl-static
yum -y install xz xz-devel # Python3.8+需要安装此包，若未安装，后续安装后需要重新编译python
yum -y install lzma # 不存在也不影响
yum -y install sqlite sqlite-devel
yum -y install gdbm gdbm-devel
yum -y install tk tk-devel
yum -y install libffi-devel # Python3.7+需要安装此包，若未安装，后续安装后需要重新编译python

wget https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tar.xz
tar -xvJf Python-3.8.3.tar.xz
cd Python-3.8.3
# 编译安装  TODO --enable-shared 待验证是否需要(暂不使用)
# --enable-optimizations参数，这样才能启用很多功能。
./configure prefix=/usr/local/python383
make && make install
# 添加软链接
ln -s /usr/local/python383/bin/python3.8 /usr/bin/python383
```

make 失败后 使用 make clean 清除，重新编译 make

### 问题记录

#### libpython3.8.so.1.0: cannot open shared object file

采用 `--enable-shared`编译后的问题

```bash
[fdm@neo4j ~]$ virtualenv env383 -p /usr/bin/python383
Running virtualenv with interpreter /usr/bin/python383
/usr/bin/python383: error while loading shared libraries: libpython3.8.so.1.0: cannot open shared object file: No such file or directory
```

#### returned NULL without setting an error

- 问题背景:
  - Python 编译时使用`--enable-optimizations`选项, 在`make`安装时报错。
  - `--enable-optimizations`选项 能够增加 Python 10%的性能,但会增加编译时间
- 解决方案:
  - 方案 1: GCC 升级到 8(不推荐)
  - 方案 2: 不使用`--enable-optimizations`选项

日志详情

```bash
# Python make时报错日志
./python -E -S -m sysconfig --generate-posix-vars ;\
if test $? -ne 0 ; then \
  echo "generate-posix-vars failed" ; \
  rm -f ./pybuilddir.txt ; \
  exit 1 ; \
fi
Could not import runpy module
Traceback (most recent call last):
  File "/root/Python-3.8.3/Lib/runpy.py", line 15, in <module>
    import importlib.util
  File "/root/Python-3.8.3/Lib/importlib/util.py", line 14, in <module>
    from contextlib import contextmanager
  File "/root/Python-3.8.3/Lib/contextlib.py", line 4, in <module>
    import _collections_abc
SystemError: <built-in function compile> returned NULL without setting an error
generate-posix-vars failed
make[1]: *** [pybuilddir.txt] Error 1
make[1]: Leaving directory `/root/Python-3.8.3`
make: *** [profile-opt] Error 2

# Python去除 --enable-optimizations 选项后 正常编译./configure 结束后日志
config.status: creating pyconfig.h
config.status: pyconfig.h is unchanged
creating Modules/Setup.local
creating Makefile

If you want a release build with all stable optimizations active (PGO, etc),
please run ./configure --enable-optimizations
```
