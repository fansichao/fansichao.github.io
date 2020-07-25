---
title: Module-Analysis数据分析
date: 2020-07-12 15:38:13
updated: 2020-07-12 15:38:13
tags:
  - Module
  - 数据分析
categories:
  - Module
description: ...
---

## 功能模块

### jieba 分词

date: 2017-11-01

```python

import jieba
# encoding=utf-8
import jieba
seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式
seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))
seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))
```

```python
"""https://github.com/fxsjy/jieba/blob/master/test/test_userdict.py""";
u"""test_userdict.py"""
#encoding=utf-8
from __future__ import print_function, unicode_literals
import sys
sys.path.append("../")
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')
#input_file = "Z:\华润公司 整理\代码样例\jieba分词\userdict.txt"
input_file = "Z:\\userdict.txt"
jieba.load_userdict(input_file)
import jieba.posseg as pseg
jieba.add_word('石墨烯')
jieba.add_word('凱特琳')
jieba.del_word('自定义词')
test_sent = (
"李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n"
"例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n"
"「台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。"
)
words = jieba.cut(test_sent)
print('/'.join(words))
print("="*40)
result = pseg.cut(test_sent)
for w in result:
    print(w.word, "/", w.flag, ", ", end=' ')
print("\n" + "="*40)
terms = jieba.cut('easy_install is great')
print('/'.join(terms))
terms = jieba.cut('python 的正则表达式是好用的')
print('/'.join(terms))
print("="*40)
# test frequency tune
testlist = [
('今天天气不错', ('今天', '天气')),
('如果放到post中将出错。', ('中', '将')),
('我们中出了一个叛徒', ('中', '出')),
]
for sent, seg in testlist:
    print('/'.join(jieba.cut(sent, HMM=False)))
    word = ''.join(seg)
    print('%s Before: %s, After: %s' % (word, jieba.get_FREQ(word), jieba.suggest_freq(seg, True)))
    print('/'.join(jieba.cut(sent, HMM=False)))
    print("-"*40)
```

```python
u"""配置文件"""
# jieba默认字典路径，可以替换
file_path = "C:\Users\scfan\Anaconda2\Lib\site-packages\jieba\dict.txt"
```

```python
u"""利用jieba分词达到模糊匹配的效果 分词+人工 从而达到找到不同机构下的同一个客户"""
u"""
分词的目的：
1.根据地址划分得到行政区划、行业等。
2.根据客户名称匹配不同BU机构，统一客户（必需）。
"""
print("*"*20)
#### 头部
#encoding=utf-8
from __future__ import print_function, unicode_literals
import sys
sys.path.append("../")
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba.posseg as pseg
### 样例数据
d1= ["中国石油化工集团公司","上海汽车集团股份有限公司",
          "英国法通保险公司","日本丰田汽车公司"]
d2 = ["中国石油化工公司","上海汽车公司",
          "英国法通","日本丰田公司"]
d3 = ["中国石油化工","上海汽车","法通保险","日本丰田"]
d4 = ["中国石油化工集团公司","上海汽车集团股份有限公司",
          "英国法通保险公司","日本丰田汽车公司"]
# 【Tips】设定关键字词典
input_file = "Z:\\华润公司 整理\\代码样例\\jieba分词\\dict.crc.txt"
jieba.load_userdict(input_file)
# 【Tips】指定添加关键词
jieba.add_word('公司')
jieba.add_word('有限公司')
jieba.add_word('英国')
# 【Tips】指定删除关键词
jieba.del_word('自定义词')
#【Tips】 今天天气 -> 今天+天气，而不是 今天天气
jieba.suggest_freq(('英国', '法通'), True)
jieba.del_word('英国法')
#【Tips】 台中 -> 台中 ，而不是 台+中
#jieba.add_word('台中')
jieba.suggest_freq('台中', True)
c1 = []
for d in d1:
    result = pseg.cut(d)
    #for w in result:
    #      print(w.word, "/", w.flag, ", ", end=' ') # 显示详细的词性
    words = jieba.cut(d)
    print('/'.join(words))
    x = '/'.join(words)
    m = list(x)
    print(m)
    print(x)
    c1.append('/'.join(words))

print(c1)
```

## 附件

### 参考链接
