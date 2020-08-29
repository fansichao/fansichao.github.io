---
title: Python23项目切换
url_path: python/advance/Python23项目切换
tags:
  - python
  - python进阶
categories:
  - python进阶
description: Python23项目切换
---

tags: `2020年` `05月` `python2` `python3.8.3`

## 项目部署

## Python2 升级为 Python3

### 2to3

修改内容

```bash
去除 unicode
print
except,err
has_key
list(child_menus.get(menu_id, {}).items()) 字典加list
raw_input
<>
basestring
```

### 去除 reload(sys)

```bash
替换所有 reload(sys)
sed -i 's/reload(sys)//g'  `grep -rl 'reload(sys)' | grep -v ".py.bak"`

替换所有 sys.setdefaultencoding("utf-8")
sed -i 's/sys.setdefaultencoding("utf8")//i'  `grep -rl 'setdefaultencoding' | grep -v ".py.bak"`
sed -i "s/sys.setdefaultencoding('utf-8')//i"  `grep -rl 'setdefaultencoding' | grep -v ".py.bak"`
```

### 替换 cmp

Python3 中没有 cmp 函数

```python
# Python2
>>> cmp(['a'],['a'])
0
>>> cmp(['a'],['b'])
-1
>>> cmp(3,1)
1

# Python3.8.3
>>> import operator
>>> operator.eq(['a'],['a'])
True
>>> operator.eq(['a'],['as'])
False
```

修改文件 `fdm/modeling/base_node.py`

### 替换 / & //

```bash
grep -rn '/' | grep -v txt
```

## 问题记录

### Could not import the lzma module

- 问题原因:
  - 由于缺失前置包`xz lzma xz-devel`，Python 编译不完全
- 解决方案:
  - `yum -y install xz xz-devel`
  - `yum -y install lzma`
  - 重新编译安装 Python

日志详情:

```bash
/home/scfan/env383/lib/python3.8/site-packages/pandas/compat/__init__.py:117: UserWarning: Could not import the lzma module. Your installed Python is incomplete. Attempting to use lzma compression will result in a RuntimeError.
  warnings.warn(msg)
```

### returned NULL without setting an error

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

### the imp module is deprecated in favour of importlib

- 问题背景:
  - Virtualenv 版本为 Python2.7 安装的 15.1.0
- 解决方案:
  - 卸载原有 15.1.0, 安装 20.0.20 版本

```bash
[scfan@fdm ~]$ virtualenv env383 -p python383
Running virtualenv with interpreter /usr/bin/python383
Using base prefix '/usr/local/python383'
/usr/local/lib/python2.7/site-packages/virtualenv.py:1039: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
New python executable in /home/scfan/env383/bin/python383
Also creating executable in /home/scfan/env383/bin/python
Installing setuptools, pip, wheel...done.
```

### failed to find interpreter for Builtin discover of python_spec

- 问题背景:
  - virtualenv 升级到 20.0.20 后,创建虚拟环境报错
- 解决方案
  - 指定 Python **绝对路径** 来创建 env
  - `virtualenv env383 -p /usr/bin/python383`

日志详情:

```bash
[root@fdm Python-3.8.3]# virtualenv env383 -p python383
RuntimeError: failed to find interpreter for Builtin discover of python_spec='python383'

```

解决方案

```bash
[scfan@fdm ~]$ virtualenv env383 -p /usr/bin/python383
created virtual environment CPython3.8.3.final.0-64 in 255ms
  creator CPython3Posix(dest=/home/scfan/env383, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, via=copy, app_data_dir=/home/scfan/.local/share/virtualenv/seed-app-data/v1.0.1)
  activators PythonActivator,FishActivator,XonshActivator,CShellActivator,PowerShellActivator,BashActivator
```

### unable to locate include directory containing header files

- 问题背景：
  - pip 安装 python-nss 包时报错
- 解决方案
  - `yum install nss-devel nspr-devel -y`

```bash
Collecting zipp>=0.5
  Downloading http://mirrors.aliyun.com/pypi/packages/b2/34/bfcb43cc0ba81f527bc4f40ef41ba2ff4080e047acb0586b56b3d017ace4/zipp-3.1.0-py3-none-any.whl (4.9 kB)
Collecting pyasn1
  Downloading http://mirrors.aliyun.com/pypi/packages/62/1e/a94a8d635fa3ce4cfc7f506003548d0a2447ae76fd5ca53932970fe3053f/pyasn1-0.4.8-py2.py3-none-any.whl (77 kB)
     |████████████████████████████████| 77 kB 10.7 MB/s
Collecting pyasn1-modules
  Downloading http://mirrors.aliyun.com/pypi/packages/95/de/214830a981892a3e286c3794f41ae67a4495df1108c3da8a9f62159b9a9d/pyasn1_modules-0.2.8-py2.py3-none-any.whl (155 kB)
     |████████████████████████████████| 155 kB 8.5 MB/s
Collecting python-nss>=0.16
  Downloading http://mirrors.aliyun.com/pypi/packages/6b/29/629098e34951c358b1f04f13a70b3590eb0cf2df817d945bd05c4169d71b/python-nss-1.0.1.tar.bz2 (222 kB)
     |████████████████████████████████| 222 kB 11.4 MB/s
    ERROR: Command errored out with exit status 1:
     command: /home/scfan/env383/bin/python -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-btu3wbdr/python-nss/setup.py'"'"'; __file__='"'"'/tmp/pip-install-btu3wbdr/python-nss/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-pip-egg-info-t291oo12
         cwd: /tmp/pip-install-btu3wbdr/python-nss/
    Complete output (9 lines):
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-install-btu3wbdr/python-nss/setup.py", line 409, in <module>
        sys.exit(main(sys.argv))
      File "/tmp/pip-install-btu3wbdr/python-nss/setup.py", line 333, in main
        nss_include_dir  = find_include_dir(['nss3', 'nss'],   ['nss.h',  'pk11pub.h'], include_roots=include_roots)
      File "/tmp/pip-install-btu3wbdr/python-nss/setup.py", line 94, in find_include_dir
        raise ValueError("unable to locate include directory containing header files %s" % include_files)
    ValueError: unable to locate include directory containing header files ['nss.h', 'pk11pub.h']
    ----------------------------------------
ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
```

### SyntaxError: Missing parentheses in call to 'print' TODO

[参考链接](https://blog.csdn.net/teavamc/article/details/78190164)

- 解决方案
  - multiprocessing 在 Python3.8.3 中不属于第三方库，无需安装
  - from multiprocessing import pool

```bash
(env383) [scfan@fdm server]$ pip install multiprocessing
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting multiprocessing
  Downloading http://mirrors.aliyun.com/pypi/packages/b8/8a/38187040f36cec8f98968502992dca9b00cc5e88553e01884ba29cbe6aac/multiprocessing-2.6.2.1.tar.gz (108 kB)
     |████████████████████████████████| 108 kB 2.1 MB/s
    ERROR: Command errored out with exit status 1:
     command: /home/scfan/env383/bin/python -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-6mx1e585/multiprocessing/setup.py'"'"'; __file__='"'"'/tmp/pip-install-6mx1e585/multiprocessing/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-pip-egg-info-s9dmt1uy
         cwd: /tmp/pip-install-6mx1e585/multiprocessing/
    Complete output (6 lines):
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-install-6mx1e585/multiprocessing/setup.py", line 94
        print 'Macros:'
              ^
    SyntaxError: Missing parentheses in call to 'print'. Did you mean print('Macros:')?
    ----------------------------------------
ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
```

## 附件

### 参考资源

- [在 CentOS 7 上安装并配置 Python 3.6 环境](https://www.cnblogs.com/clement-jiao/p/9902980.html)
