---
title: Python 底层原理
url_path: python/advance/底层原理
tags:
  - python
  - python-进阶
categories:
  - python-进阶
description: 从底层了解 Python 实现，从深度层面探索 Python 方法
---

## Python-底层实现清单

- 内存管理&垃圾回收
- 变量对象管理
- 数据类型底层实现
  - 列表
  - 元组
  - 字符串
  - 数值
  - 字典
- 类封装

## 数据类型底层实现

### 列表

**实现原理:**

列表实现可以`数组和链表`

列表是一个线性的集合，它允许用户在任何位置插入、删除、访问和替换元素。

列表实现是基于数组或基于链表结构的。当使用列表迭代器的时候，双链表结构比单链表结构更快。

有序的列表是元素总是按照升序或者降序排列的元素。

Cpython 中列表被实现为 长度可变的数组。

实现原理说明：**从细节上看，Python 中的列表是由对其它对象的引用组成的连续数组。指向这个数组的指针及其长度被保存在一个列表头结构中**。这意味着，每次添加或删除一个元素时，由引用组成的数组需要该标大小（重新分配）。幸运的是，Python 在创建这些数组时采用了指数分配，所以并不是每次操作都需要改变数组的大小。但是，也因为这个原因添加或取出元素的平摊复杂度较低

**列表的算法效率:**

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

**列表-参考资源:**

- [Python-列表底层实现原理](https://blog.csdn.net/Yuyh131/article/details/83592608)

### 元组

tuple 和 list 相似，本质也是一个数组，但是空间大小固定。不同于一般数组，Python 的 tuple 做了许多优化，来提升在程序中的效率。

举个例子，为了提高效率，避免频繁的调用系统函数 free 和 malloc 向操作系统申请和释放空间，tuple 源文件中定义了一个 free_list：

```bash
static PyTupleObject *free_list[PyTuple_MAXSAVESIZE];
```

所有申请过的，小于一定大小的元组，在释放的时候会被放进这个 free_list 中以供下次使用。也就是说，如果以后需要再去创建同样的 tuple，Python 就可以直接从缓存中载入。

**元组-参考资源:**

- [Python 列表和元组的底层实现-源码分析](http://c.biancheng.net/view/5360.html)
- [Python 元组源码和结构图分析](https://blog.csdn.net/qq_31720329/article/details/88529792)

### 字典

**实现原理:**

**字典是通过散列表或说哈希表实现的**。字典也被称为关联数组，还称为哈希数组等。也就是说，字典也是一个数组，但**数组的索引是键经过哈希函数处理后得到的散列值**。

**参考资源:**

- [Python 字典底层实现原理](https://blog.csdn.net/answer3lin/article/details/84523332)

数据添加：把 key 通过哈希函数转换成一个整型数字，然后就将该数字对数组长度进行取余，取余结果就当作数组的下标，将 value 存储在以该数字为下标的数组空间里。
数据查询：再次使用哈希函数将 key 转换为对应的数组下标，并定位到数组的位置获取 value。

### 集合

集合底层实现原理类似于字典

set 集合和 dict 一样也是基于散列表的，只是他的表元只包含键的引用，而没有对值的引用，其他的和 dict 基本上是一致的，所以在此就不再多说了。并且 dict 要求键必须是能被哈希的不可变对象，因此普通的 set 无法作为 dict 的键，必须选择被“冻结”的不可变集合类：frozenset。顾名思义，一旦初始化，集合内数据不可修改

## 变量对象底层原理

- 可变类型，值可以改变：
  - 列表 list
  - 字典 dict
- 不可变类型，值不可以改变：
  - 数值类型 int, long, bool, float
  - 字符串 str
  - 元组 tuple

```bash
# 不可变类型修改
例如 a = 5 修改为 a = 10
实际上重新生成了对象10，然后a指向5。

# 可变类型修改
lis = [a,b,c,d]
lis存储着不同对象的引用，其中a,b,c,d的修改，实质上lis并未修改。只是a,b,c,d做了对应修改。
```

本质是因为不可变对象一旦新建后，系统就会根据他的大小给他分配固定死的内存，所以不允许修改，只修改值只能申请新的内存和地址。而可变对象，他的内存大小可以随着值的变化而自动扩容

## 类-封装底层实现原理

[Python 封装底层实现原理详解](http://c.biancheng.net/view/7033.html)

Python 封装特性的实现纯属“投机取巧”，之所以类对象无法直接调用以双下划线开头命名的类属性和类方法，是因为其底层实现时，Python 偷偷改变了它们的名称

Python 类对于 `__func()`函数和`__name`属性，都修改了名称变为`_类名__属性名`的格式，可以通过`_类名__属性名`的方式调用。如果希望类函数或类名称隐藏起来，加`__`前缀即可

## 附件

### 其他命令

```bash
# 查看代码执行过程
python3 -m dis a.py
```

### 参考资源

- [python 源码分析 基本篇](https://blog.csdn.net/qq_31720329/article/details/86751412)
- [Python 中的 list、tuple、set、dict 的底层实现的理解](https://blog.csdn.net/qq_27944187/article/details/99770138)
- [Python 数据结构底层实现浅析——list 和 tuple](https://blog.csdn.net/weixin_44374595/article/details/87734090)


 ![@常用头像01](https://raw.githubusercontent.com/fansichao/images/master/markdown/%40%E5%B8%B8%E7%94%A8%E5%A4%B4%E5%83%8F01.jpg)

 