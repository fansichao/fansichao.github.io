---
title: Hexo静态博客使用文档
url_dir: 05-Module
url_name: Hexo-Docs
tags:
  - Hexo
  - blog
categories:
  - Module
description: Hexo静态博客使用文档
---

## 文档说明

## 使用说明

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

## 参考链接

- [Hexo 官方文档](https://hexo.io/docs/)
- [hexo 添加文章更新时间](https://www.jianshu.com/p/ae3a0666e998)
