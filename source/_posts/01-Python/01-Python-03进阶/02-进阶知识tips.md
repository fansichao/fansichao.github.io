---
title: Python-进阶知识点tips
url_path: python/advance/tips
tags:
  - python
  - python-进阶
  - ★★★★★
categories:
  - python
  - python-进阶
description: 进阶
---

<!-- TOC -->

- [魔法函数](#魔法函数)
- [高级特性/语法糖](#高级特性语法糖)
- [进阶知识点](#进阶知识点)
  - [函数式编程](#函数式编程)
  - [高阶函数](#高阶函数)
  - [匿名函数](#匿名函数)
  - [闭包](#闭包)
  - [python 循环中不包含域的概念](#python-循环中不包含域的概念)
  - [装饰器](#装饰器)
  - [偏函数](#偏函数)
  - [模块和包的概念](#模块和包的概念)
  - [Python 面向对象编程](#python-面向对象编程)
  - [类属性](#类属性)
  - [实例方法](#实例方法)
  - [类方法](#类方法)
  - [类的继承](#类的继承)
  - [判断类型](#判断类型)
  - [多态](#多态)
  - [多重继承](#多重继承)
  - [获取对象信息](#获取对象信息)
  - [特殊方法](#特殊方法)
  - [动态获取函数变量等](#动态获取函数变量等)
- [小知识点 Tips](#小知识点-tips)
  - [打包与解包](#打包与解包)
  - [json 序列化](#json-序列化)
  - [`_xxx`,`__xxx`和`__xxx__`的区别](#_xxx__xxx和__xxx__的区别)
  - [其他知识](#其他知识)
- [参考资源](#参考资源)

<!-- /TOC -->

## 魔法函数

## 高级特性/语法糖

Python 高级特性，对于 Python 知识上限和优雅高效代码所必需的，是 Python 程序员从初级到高级不可缺少的知识历程。

## 进阶知识点

### 函数式编程

Python 支持的函数式编程

- A.不是纯函数式编程:允许有变量(纯函数式编程:不需要变量,没有副作用,测试简单
- B.支持高阶函数:函数可以作为变量传入
- C.支持闭包:有了闭包就能返回函数
- D.有限度地支持匿名函数

支持函数式编程，函数式编程的特点
@偏向于计算，而非指令，把计算视为函数而非指令
@不需要变量，无副作用，测试简单
@支持高阶函数，代码简洁

python 函数式编程的特点：
@不是纯函数式编程，可以有变量
@支持高阶函数，允许函数作为变量传入
@允许闭包，有了闭包就有返回函数
@有限度的支持匿名函数

### 高阶函数

@变量可以指向函数
@函数的参数可以接收变量
@一个函数可以接收另一个函数作为参数
@能接收函数作参数就是高阶参数

能接收函数作参数的函数就是高阶函数

常见的高阶函数

- map()
- reduce()
- filter()
- sorted()

TODO 所有高阶函数清单，部分用法等

```python
#map函数，对单个参数进行处理
L = list(range(10))
print(list(map(lambda x : x*x, L)))

#在Python 3里,reduce()函数已经被从全局名字空间里移除了,它现在被放置在fucntools模块里用的话要 先引入：对两个参数进行处理
from functools import reduce
print (reduce(lambda x,y: x-y, [1,2,3,4,5]))

#filter()函数：过滤函数，返回符合条件的新的列表
def is_odd(x):
    return x % 2 == 1
filter(is_odd, [1, 4, 6, 7, 9, 12, 17])
```

### 匿名函数

@高阶函数可以接收函数做参数，有些时候，我们不需要显式地定义函数，直接传入匿名函数更方便

```python
lambda x: x * 2
```

### 闭包

Python 的函数不但可以返回 int,str,list,dict 等数据类型,还可以返回函数

Python 中闭包,在函数内部定义的函数和外部定义的函数式一样的,只是无法被外部访问,如果有被定义在外函数内部的情况,并且内层函数引用了外层函数的参数,然后返回内层函数的情况,我们称为闭包.

闭包的特点是返回的函数还引用了外层函数的局部变量,所以要正确地使用闭包,就要确保引用的局部变量在函数返回后不能变.

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

### 装饰器

Python 内置的@语法就是为了简化装饰器调用

### 偏函数

函数在执行时，要带上所有必要的参数进行调用。但是，有时参数可以在函数被调用之前提前获知。这种情况下，一个函数有一个或多个参数预先就能用上，以便函数能用更少的参数进行调用。

偏函数是将所要承载的函数作为 partial()函数的第一个参数，原函数的各个参数依次作为 partial()函数后续的参数，除非使用关键字参数。

```python
from functools import partial

def mod( n, m ):
  return n % m

mod_by_100 = partial( mod, 100 )

print mod( 100, 7 )  # 2
print mod_by_100( 7 )  # 2
```

### 模块和包的概念

包就是文件夹,模块名就是.py

包下面有个*init*.py 这样 python 才会当做包来处理

### Python 面向对象编程

TODO

面向对象编程是一种程序设计范式

把程序看做不同对象的相互调用

对现实世界建立对象模型

基本思想

类用于定义抽象类型

实例根据类的定义被创建出来

最重要的思想:数据封装

由于 Python 是动态语言，对每一个实例，都可以直接给他们的属性赋值

可以给一个实例绑定很多属性,如果不希望被外部访问到,可以用**双下划线开头,该属性就无法被外部访问.但是如果一个属性以 **xxx**的形式定义,则又可以被外部访问了,以**xxx**定义的属性在 python 的类中被称为特殊属性,有很多预定义的特殊属性可以使用,通常不把普通属性用**xxx\_\_定义

### 类属性

类里面属性分为 类属性(独有一份)和实例属性(每个实例都会有一份)。

当实例属性和类属性重名时，实例属性优先级高，它将屏蔽掉对类属性的访问。不要在实例上修改类属性，它实际上并没有修改类属性，而是给实例绑定了一个实例属性

### 实例方法

实例的方法就是在类中定义的函数，它的第一个参数永远是 self，指向调用该方法的实例本身，其他参数和一个普通函数是完全一样的：在实例方法内部，可以访问所有实例属性，这样，如果外部需要访问私有属性，可以通过方法调用获得，这种数据封装的形式除了能保护内部数据一致性外，还可以简化外部调用的难度。

在 class 中定义的实例方法其实也是属性,实际上是一个函数对象,因为方法也是一个属性,所以它也可以动态地添加到实例上,只是需要用 type.MethodType()把一个函数变为一个方法

### 类方法

和属性类似,方法也分实例方法和类方法.在 class 中定义的全部是实例方法,实例方法第一个参数 self 是实例本身.通过标记@classmethod 该方法将绑定到类上,而非类的实例上,该方法的第一个参数将传入类本身,通常将参数名命名为 cls,因为是在类上调用,而非实例上调用,因此类方法无法获取任何实例变量,只能获得类的引用

```python
# @classmethod 指定类方法
class Person(object):
    count = 0
    @classmethod
    def how_many(cls):
        return cls.count
```

### 类的继承

子类和父类是 is 关系,总是从某各类继承 如果没有合适的就从 object 继承,不能忘记调用 super().**init**

如果已经定义了 Person 类，需要定义新的 Student 和 Teacher 类时，可以直接从 Person 类继承：

```python
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
```

定义 Student 类时，只需要把额外的属性加上，例如 score：

```python
class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score
```

一定要用 `super(Student, self).__init__(name, gender)` 去初始化父类，否则，继承自 Person 的 Student 将没有 name 和 gender。

函数`super(Student, self)`将返回当前类继承的父类，即 Person ，然后调用`__init__()`方法，注意 self 参数已在 super()中传入，在`__init__()`中将隐式传递，不需要写出（也不能写）。

### 判断类型

判断数据类型

```python
isinstance("ss", (str,list) )
```

TODO 判断实例类似等等

继承链上，一个父类的实例不能是子类类型，因为子类比父类多了一些属性和方法,一个实例可以看成它本身的类型，也可以看成它父类的类型。

### 多态

TODO

### 多重继承

### 获取对象信息

isinstance()判断是否是某种类型的实例外

type()函数获取变量的类型,返回一个 Type 对象

dir()函数获取变量的所有属性

getattr()获取属性值

setattr()设置属性值

### 特殊方法

又名魔法方法、魔法函数等等

详见 [博客内文章 Python 魔法函数](https://superscfan.top/python/base/magic-func)

### 动态获取函数变量等

动态获取当前运行的函数名

```python
# 在函数外部时，获取函数名称
func.__name__

# 在函数内部时，获取函数名称
sys._getframe().f_code.co_name

# 在类内部时，获取类名称
self.__class__.name

```

`inspect`模块 动态获取当前运行的函数名称

```python
# coding:utf-8
import inspect

def get__function_name():
    '''获取正在运行函数(或方法)名称'''
    return inspect.stack()[1][3]

def yoyo():
    print("函数名称：%s"%get__function_name())

class Yoyo():
    def yoyoketang(self):
        '''# 上海-悠悠 QQ群：588402570'''
        print("获取当前类名称.方法名：%s.%s" % (self.__class__.__name__, get__function_name()))

if __name__ == "__main__":
    yoyo()
    Yoyo().yoyoketang()

# 运行结果：
函数名称：yoyo
获取当前类名称.方法名：Yoyo.yoyoketang
```

[动态创建函数](https://www.cnblogs.com/daniumiqi/p/12191161.html)

## 小知识点 Tips

### 打包与解包

```python
x, y ,*z = list(range(0,10))

zip([[1,2],[2,3]])
```

### json 序列化

```python

json.loads()
json.dumps()

```

### `_xxx`,`__xxx`和`__xxx__`的区别

（1）单下划线 `_xxx`

"单下划线"开始的成员函数和成员变量都是公开的(public)(但是约定俗成以此开头来设计私有函数/变量，尽管其是 public，理解，即只是标明，标记)。即类实例和子类实例都可以访问此中变量，但是需通过类提供的接口进行访问，不能用`from xxx import *`导入

（2）双下划线 `__xxx`

从表象上看可以当做类中的私有变量/方法名，表示私有成员，即只有类对象自己才能访问，其自身的类实例或是其子类也不能访问。

Python 设计此的真正目的仅仅是为了避免子类覆盖父类的方法。

（3）`__xxx__`

系统定义名字，前后均有一个"双下划线"是代表 python 里特殊方法专用的表示，如**init**()代表类的构造函数

类的下划线命令区别

- `xx`：共有变量。
- `_xx`：私有化的属性或方法，from xxx import \* 时无法导入，子类的对象和子类可以访问。
- `__xx`：避免与子类中的属性命名冲突，无法在外部直接访问(名字重整所以访问不到)。
- `__ xx __` ：双前后下划线,用户名字空间的魔法对象或属性。例如: `__init__` , 不要自己发明这样的名字。
- `xx_`：单后置下划线,用于避免与 Python 关键词的冲突。

### 其他知识

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

## 参考资源

- [python 进阶知识点](https://blog.csdn.net/weixin_37699212/article/details/73735258)
