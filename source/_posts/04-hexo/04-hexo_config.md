---
title: Hexo静态博客使用文档
url_path: hexo/config
tags:
  - hexo
  - blog
  - module
categories:
  - hexo
description: Hexo静态博客使用文档。Hexo + GithubgPages
---

<!-- TOC -->

- [Hexo 简介](#hexo-简介)
- [Hexo 基础配置](#hexo-基础配置)
- [Hexo 博客配置](#hexo-博客配置)
  - [折叠隐藏部分文字](#折叠隐藏部分文字)
  - [添加文章创建时间和更新时间](#添加文章创建时间和更新时间)
  - [修改文章 URL 生成方式](#修改文章-url-生成方式)
  - [个人博客绑定域名配置](#个人博客绑定域名配置)
  - [博客评论配置](#博客评论配置)
  - [设置博客置顶](#设置博客置顶)
  - [配置私密博客 hexo-hide-posts](#配置私密博客-hexo-hide-posts)
  - [配置 看板娘](#配置-看板娘)
  - [配置 hexo-related-popular-posts](#配置-hexo-related-popular-posts)
  - [hexo-easy-tags-plugin](#hexo-easy-tags-plugin)
  - [hexo-permalink-pinyin](#hexo-permalink-pinyin)
  - [hexo-notify](#hexo-notify)
  - [hexo-seo-link-visualizer](#hexo-seo-link-visualizer)
  - [hexo-encrypt](#hexo-encrypt)

<!-- /TOC -->

## Hexo 简介

[Hexo 官网](https://hexo.io/)
[hexo 原理分析](https://blog.csdn.net/sinat_17775997/article/details/83821027)

## Hexo 基础配置

[node.js 下载](https://nodejs.org/zh-cn/download/)

```bash
# 下载 node.js 并安装
npm install -g hexo-cli
npm install hexo
# 配置 hexo 的 环境变量
C:\Users\scfan\AppData\Roaming\npm\node_modules\hexo\bin

配置之后重新打开 gitbash, 则会有 hexo 命令
```

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

```bash
# 文章中配置 top: true 即可
top: true
```

### 配置私密博客 hexo-hide-posts

效果：博客在首页会被隐藏，实际通过链接仍可以访问

```bash
# 步骤1：_config.yml 配置
# 隐藏文章 hexo-hide-posts
hide_posts:
  # 可以改成其他你喜欢的名字
  filter: hidden
  # 指定你想要传递隐藏文章的 generator，比如让所有隐藏文章在存档页面可见
  # 常见的 generators 有：index, tag, category, archive, sitemap, feed, etc.
  public_generators: []
  # 为隐藏的文章添加 noindex meta 标签，阻止搜索引擎收录
  noindex: true

# 步骤2：博客配置
hidden: true

# 查看隐藏的文章列表
hexo hidden:list
```

[hexo-hide-posts](https://github.com/printempw/hexo-hide-posts/blob/master/README_ZH.md)

### 配置 看板娘

[看板娘 hexo-helper-live2d](https://github.com/EYHN/hexo-helper-live2d)

[华丽的看板娘 live2d-widget](https://github.com/stevenjoezhang/live2d-widget)

### 配置 hexo-related-popular-posts

生成到相关帖子或热门帖子的链接列表。

```swig
<!-- hexo-related-popular-posts -->
{% if not is_index %}
  <h3>相关文章</h3>
  {{
    popular_posts({ maxCount: 10 , ulClass: 'popular-posts' , PPMixingRate: 0.0 ,
      isImage: false, isDate: false, isExcerpt: false} , post)
  }}
{% endif %}

https://github.com/tea3/hexo-related-popular-posts/issues/4
```

[hexo-related-popular-posts](https://github.com/tea3/hexo-related-popular-posts)

### hexo-easy-tags-plugin

支持 标签的大小写、空格、下划线等统一
[hexo-easy-tags-plugin](https://github.com/dailyrandomphoto/hexo-easy-tags-plugin)

### hexo-permalink-pinyin

可将中文标题转换为音译的永久链接。

[hexo-permalink-pinyin](https://github.com/viko16/hexo-permalink-pinyin)

### hexo-notify

Hexo 的通知插件。

[hexo-notify](https://github.com/hexojs/hexo-notify)

### hexo-seo-link-visualizer

TODO 未成功

分析链接并可视化 Hexo 的站点结构。
[hexo-seo-link-visualizer](https://github.com/tea3/hexo-seo-link-visualizer)

### hexo-encrypt

文章加密

TODO 可用, 但是未显示加密页面

[hexo-encrypt](https://github.com/edolphin-ydf/hexo-encrypt)
