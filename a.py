import sys
class MagicClass(object):
    """ 魔法方法类


    参考链接：
        - https://www.cnblogs.com/small-office/p/9337297.html
        - https://www.bbsmax.com/A/MyJxxLyaJn/
    """
    # 隐式声明的属性
    attr = 'testA'
    
    # 是否实例化
    __isinstance = False
    # 是否打印信息
    is_print = False

    def __init__(self, params=None, *args, **kwargs):
        """ 初始化函数

        函数说明
            1. 在对象初始化的时候调用
            2. 初始化对象属性
        """
        self.init_params = params
        self.int_p = 100
        self.str_p = 'testA'
        self.dic = dict()
        self.iter_p = range(1, 10)

    def __str__(self):
        """ 打印对象

        函数说明:
            1. 以字符串的形式表示的对象，可以通过 __str__ 直接打印
            2. 函数返回值必须为 str 类型
        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return "__str__  + %s" % self.init_params

    def __new__(cls, *args, **kwargs):
        """ 

        函数说明:
            1. 必须有返回值，返回是被实例化的实例。
            2. 调用 __new__ 之后，会将其结果传递给 __init__
        """
        if cls.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        # 单例模式
        if not cls.__isinstance:         
            cls.__isinstance = object.__new__(cls)            
        return cls.__isinstance

 
    def __call__(self, *args, **kwargs):
        """ 模拟函数的行为

        函数说明
            1. 模拟函数的行为, 可以将类当成函数使用
        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return sys._getframe().f_code.co_name + str(args) + str(kwargs)

    def __len__(self, val=None):
        """ 定制 len() 输出的结果

        函数说明:
            1. 定制 len() 输出的结果
            2. 返回对象必须为整数
        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return len(val) if val else 0

    def __repr__(self):
        """ 转化为供解释器读取的形式 repr()函数
        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return repr(self.str_p)

    def __setattr__(self, name, value):
        """ 设置对象属性
        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return super().__setattr__(name, value)

    def __getattr__(self, name):
        """
        获取对象属性，只有在属性没有找到的时候调用

        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return super().__getattribute__(name)

    def __getattribute__(self, name):
        """ 获取对象属性

        __getattr__是在属性不存在时被调用，而__getattribute__是无条件被调用
        一旦定义了__getattribute__，则__getattr__不再会被调用，除非显式调用

        """
        #if self.is_print:
        #    print('> 函数名称' + sys._getframe().f_code.co_name)
        return super().__getattribute__(name)

    def __delattr__(self, name):
        """
        删除属性
        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return super().__delattr__(name)

    def __setitem__(self, name, value):
        """ 给对象赋值，我们可以以下标的方式对其进行操作

        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        self.dic.update({name: value})
 
    def __getitem__(self, name):
        """ 支持已下标的方式获取值
        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return self.dic[name]

    def __delitem__(self, name):
        """ 以下标方式删除对象数据
        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        del self.dic[name]

    def __iter__(self):
        """ 只要定义了__iter__()方法对象，就可以使用迭代器访问
        可以迭代我们自己定义的对象
        """ 
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)
        return iter(self.iter_p)

    def __del__(self):
        """ 析构器，或者回收器，在对象引用数降到0时执行。不推荐使用。

        """
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)

    def func(self):
        # 隐式声明的属性
        self.func_a = 'test2'
        if self.is_print:
            print('> 函数名称' + sys._getframe().f_code.co_name)


if __name__ == '__main__':
    magic = MagicClass(params='test')
    # vars 获得 显示声明的属性
    # print(vars(magic))

    # print(magic)
    # print(dir(magic))
    # print(magic.iter_p)

    # __call__
    print(magic('123123'))

    print(len(magic()))
    print(dir(magic()))