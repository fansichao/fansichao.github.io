---
title: Hexo静态博客使用文档
url_path: hexo/config
tags:
  - hexo
  - blog
categories:
  - hexo
description: Hexo静态博客使用文档
---

<!-- TOC -->

- [Hexo简介](#hexo简介)
- [Hexo 博客配置](#hexo-博客配置)
    - [折叠隐藏部分文字](#折叠隐藏部分文字)
    - [添加文章创建时间和更新时间](#添加文章创建时间和更新时间)
    - [修改文章 URL 生成方式](#修改文章-url-生成方式)
    - [个人博客绑定域名配置](#个人博客绑定域名配置)
    - [博客评论配置](#博客评论配置)
    - [设置博客置顶](#设置博客置顶)

<!-- /TOC -->
## Hexo简介


[hexo原理分析](https://blog.csdn.net/sinat_17775997/article/details/83821027)

## Hexo 博客配置

- [Hexo 官方插件网](https://hexo.io/plugins/)

### 折叠隐藏部分文字

````bash
<details>
  <summary>隐藏内容的标题</summary>

- 支持MarkDown语法
- 支持代码块等等

  ```python
  import os
  ``` // 防止排版错误：因为这是代码块内的代码。使用时可删除

- 支持表格

    |文字|文字|
    |-|-|
    |文字|文字|

</details>
````

<details>
  <summary>隐藏内容的标题</summary>

- 支持 MarkDown 语法
- 支持代码块等等

  ```python
  import os
  ```

- 支持表格

  | 文字 | 文字 |
  | ---- | ---- |
  | 文字 | 文字 |

</details>

[Hexo 博客如何折叠(显示/隐藏)部分文字](https://www.faker.top/2020/02/14/Hexo/h6-%E6%8A%98%E5%8F%A0%E6%96%87%E5%AD%97/)

### 添加文章创建时间和更新时间

本博客采用更新时间 modified 。 创建时间 date

配置方法详见如下

配置自动更新时间 `themes\next\layout\_macro\post.swig`

```yml
         {% if post.top %}
            <i class="fa fa-thumb-tack"></i>
            <font color="#F05050">[置顶]</font>
            <span class="post-meta-divider">|</span>
          {% endif %}
          # 添加如下内容 !!! 去除此注释.
          <span class="post-time">
            {% if theme.post_meta.created_at %}
              <span class="post-meta-item-icon">
                <i class="fa fa-calendar-o"></i>
              </span>
              {% if theme.post_meta.item_text %}
                <span class="post-meta-item-text">{{ __('post.posted') }}</span>
              {% endif %}
              <time title="{{ __('post.created') }}" itemprop="dateCreated datePublished" datetime="{{ moment(post.date).format() }}">
                {{ date(post.date, config.date_format) }}
              </time>
            {% endif %}

            {% if theme.post_meta.created_at and theme.post_meta.updated_at %}
              <span class="post-meta-divider">|</span>
            {% endif %}

            {% if theme.post_meta.updated_at %}
              <span class="post-meta-item-icon">
                <i class="fa fa-calendar-check-o"></i>
              </span>
              {% if theme.post_meta.item_text %}
                <span class="post-meta-item-text">{{ __('post.modified') }}&#58;</span>
              {% endif %}
              <time title="{{ __('post.modified') }}" itemprop="dateModified" datetime="{{ moment(post.updated).format() }}">
                {{ date(post.updated, config.date_format) }}
              </time>
            {% endif %}
          </span>
```

配置文章展示项 `themes\next\_config.yml`

```yml
# Post meta display settings
post_meta:
  item_text: true
  created_at: true
  updated_at: true
  categories: true
```

配置展示的名称 `themes\next\languages\zh-Hans.yml`

```yml
post:
  created: 创建于
  modified: 更新于
  sticky: 置顶
  posted: 发表于
```

参考链接

- [Hexo 官方文档](https://hexo.io/docs/)
- [hexo 添加文章更新时间](https://www.jianshu.com/p/ae3a0666e998)

### 修改文章 URL 生成方式

```yml
# _config.yml 文件

# permalink: :year/:month/:day/:title/
permalink: :url_path/
```

### 个人博客绑定域名配置

- [Hexo 个人博客绑定域名配置](https://blog.csdn.net/Wonz5130/article/details/82828761)

### 博客评论配置

```yml
# themes\next\layout\_partials\comments.swig
{% elseif theme.gitalk.enable %}
  <div class="comments" id="comments">
      <div id="gitalk-container"></div>
  </div>

# _config.yml
gitalk:
  enable: true
  ClientID: xxxxx
  ClientSecret: xxxxxx
  repo: fansichao.github.io
  owner: fansichao
  adminUser: fansichao
  IdPrefix:
  labels: comments
  perPage: 10
  pagerDirection: last
  createIssueManually: false
  distractionFreeMode: false
  enableHotKey: true
```

配置详见 [Gittalk-github 参考](https://github.com/gitalk/gitalk/blob/master/readme-cn.md)

### 设置博客置顶

````bash
# 文章中配置 top: true 即可
top: true
```
````

### 配置私密博客 hexo-hide-posts

[hexo-hide-posts](https://github.com/printempw/hexo-hide-posts/blob/master/README_ZH.md)

### 配置 live2d hexo-helper-live2d

[Hexo 插件地址](https://hexo.io/plugins/)
