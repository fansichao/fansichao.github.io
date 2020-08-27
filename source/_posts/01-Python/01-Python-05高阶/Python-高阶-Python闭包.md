---
title: Python-闭包
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Python
  - Python高级特性
categories:
  - Python-高阶
description: Python闭包。Python高级特性之一。
---

tags: `2020年` `05月` `闭包` `高级特性`

## 介绍

闭包概念：在一个内部函数中，对外部作用域的变量进行引用，(并且一般外部函数的返回值为内部函数)，那么内部函数就被认为是闭包

Python 闭包，类似于 子函数

### python 循环中不包含域的概念

```python
# python循环中不包含域的概念
func_lis = []
for i in range(4):
    def func(x):
        return x*i
    func_lis.append(func)
for f in func_lis:
    print(f(2))
# 6
# 6
# 6
# 6
loop在python中是没有域的概念的，flist在像列表中添加func的时候，并没有保存i的值，而是当执行f(2)的时候才去取，这时候循环已经结束，i的值是3，所以结果都是6
```

### Python 闭包

父函数返回子函数本身，类似于装饰器。

```python
func_lis = []
for i in range(4):
    def makefunc(i):
        def func(x):
            return x*i
        return func
    func_lis.append(makefunc(i))

for f in func_lis:
    print(f(2))

0
2
4
6
```

### 闭包的作用

闭包在爬虫以及 web 应用中都有很广泛的应用，并且闭包也是装饰器的基础

## 附件

### 参考资源

[深入浅出 python 闭包](https://zhuanlan.zhihu.com/p/22229197)
