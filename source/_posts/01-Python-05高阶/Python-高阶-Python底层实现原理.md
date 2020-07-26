---
title: Python-底层实现原理
date: 2020-05-01 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Python
  - Python底层
categories:
  - Python-高阶
description: 从底层了解 Python 实现，从深度层面探索 Python 方法
---

## Python-底层实现清单

- 数据类型
  - 列表
  - 元组
  - 字符串
  - 数值
  - 字典
- 类封装

## 数据类型-列表

### 实现说明

列表实现可以`数组和链表`

列表是一个线性的集合，它允许用户在任何位置插入、删除、访问和替换元素。

列表实现是基于数组或基于链表结构的。当使用列表迭代器的时候，双链表结构比单链表结构更快。

有序的列表是元素总是按照升序或者降序排列的元素。

Cpython 中列表被实现为 长度可变的数组。

### 实现原理

实现原理说明：**从细节上看，Python 中的列表是由对其它对象的引用组成的连续数组。指向这个数组的指针及其长度被保存在一个列表头结构中**。这意味着，每次添加或删除一个元素时，由引用组成的数组需要该标大小（重新分配）。幸运的是，Python 在创建这些数组时采用了指数分配，所以并不是每次操作都需要改变数组的大小。但是，也因为这个原因添加或取出元素的平摊复杂度较低

### 列表的算法效率

可以采用时间复杂度来衡量：

```bash
index() O(1)
append O(1)
pop() O(1)
pop(i) O(n)
insert(i,item) O(n)
del operator O(n)
iteration O(n)
contains(in) O(n)
get slice[x:y] O(k)
del slice O(n)
set slice O(n+k)
reverse O(n)
concatenate O(k)
sort O(nlogn)
multiply O(nk)
```

### 列表-参考资源

- [Python-列表底层实现原理](https://blog.csdn.net/Yuyh131/article/details/83592608)

## 数据类型-元组

tuple 和 list 相似，本质也是一个数组，但是空间大小固定。不同于一般数组，Python 的 tuple 做了许多优化，来提升在程序中的效率。

举个例子，为了提高效率，避免频繁的调用系统函数 free 和 malloc 向操作系统申请和释放空间，tuple 源文件中定义了一个 free_list：

```bash
static PyTupleObject *free_list[PyTuple_MAXSAVESIZE];
```

所有申请过的，小于一定大小的元组，在释放的时候会被放进这个 free_list 中以供下次使用。也就是说，如果以后需要再去创建同样的 tuple，Python 就可以直接从缓存中载入。

### 元组-参考资源

- [Python 列表和元组的底层实现-源码分析](http://c.biancheng.net/view/5360.html)
- [Python 元组源码和结构图分析](https://blog.csdn.net/qq_31720329/article/details/88529792)

## 附件

[Python 中的 list、tuple、set、dict 的底层实现的理解](https://blog.csdn.net/qq_27944187/article/details/99770138)

https://blog.csdn.net/weixin_44374595/article/details/87734090
