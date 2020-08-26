---
title: Python利器-App阅读笔记
date: 2020-08-12 15:38:13
updated: 2020-08-12 15:38:13
tags:
  - Python
categories:
  - Python-进阶
description: Python利器-App阅读笔记
---

map

filter

reduce

`__solts__` 来给定固定集合的属性分配空间,适合固定少属性的类,可以大量减少内存消耗

```python
# Python默认采用字典来保存类的实例属性，但对于小类来说，会浪费内存空间
# 可以使用 __solts__ 来给定固定集合的属性分配空间，不采用字典，可以减少约50%的内存消耗

class MyClass(object):
    __solts__ = ['name', 'cert']
    def __init__(self, name=None, cert=None):
        self.name = name
        self.crt = cert

# 监测内存使用
https://github.com/ianozsvald/ipython_memory_usage


```

`collections` 容器模块

```python
defaultdict
counter
deque
namedtuple
enum.Enum

```

`inspect` 获取活跃对象的信息

```python
# for .. else 语句 用于捕获for循环是正常结束还是break跳出
# else 在循环正常结束时调用，break跳出循环时不会调用。

test_num = 5
for n in range(0,10):
    if n == test_num:
        print('>>> 11')
        break
else:
    print('>>> 22')

# test_num = 5 时，break跳出循环 打印 11
# test_num = 20 时，循环解除，打印 22
```

协程 - yield

```python

函数缓存,将一个函数的返回值快速的缓存或取消缓存。
适用于 IO密集型的函数 频繁使用相同参数调用时，可以节省大量时间。

from functools import lru_cache

# maxsize 最多缓存最近多少个返回值
@lru_cache(maxsize=22)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
print([fib(n) for n in range(100)])

```

```python
# 上下文管理器

# 方式1 with语句 例如 with open
# 方式2 使用类来做上下文管理器
# 方式3 基于生成器来实现

# with open 方式
with open('aa.csv', 'wb') as file_obj:
    file_obj.write(b'demo')


# Python 3.7.4
# 类方式
class File(object):

    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        if value is not None:
            print(type)
            print(value)
        self.file_obj.close()
        return True

with File('a.csv', 'wb') as file_obj:
    file_obj.write(b'demo')

# 生成器方式
from contextlib import contextmanager
@contextmanager
def open_file(name, method):
    f = open(name, method)
    yield f
    f.close
 
```
