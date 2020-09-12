---
title: Docker-index
url_path: docker/
tags:
  - docker
  - index
  - module
categories:
  - module
  - docker
description: Docker-index 目录索引，Docker相关内容详见此文件。
---

## Docker 介绍

### Docker 的应用场景 Web

- 应用的自动化打包和发布。
- 自动化测试和持续集成、发布。
- 在服务型环境中部署和调整数据库或其他的后台应用。
- 从头编译或者扩展现有的 OpenShift 或 Cloud Foundry 平台来搭建自己的 PaaS 环境。

### Docker 的优点

- 持续部署与测试
  - Docker 可以确保从开发到产品发布整个过程环境的一致性。便于部署和开发测试。
- 多云平台
  - 可移植性
- 环境标准化和版本控制
  - 可以方便的进行版本管理
- 隔离性
- 安全性

  1.优势

docker 启动快，开启一个 container 通常只需要几秒钟，而虚拟机开机至少几十秒；
docker 需要的资源更少， docker 在操作系统级别进行虚拟化， docker 容器和内核交互，几乎没有性能损耗，性能优于通过 Hypervisor 层与内核层的虚拟化；
docker 更轻量， docker 重装或者复制到其他机器比虚拟机快很多，重新安装 docker 容器只需要几十秒种，而虚拟机至少需要几分钟；并且 dockers 的 image 文件导出占用只有几百兆，但是虚拟机的镜像包往往有几个 G； 2.缺点

docker 无法对外开放所有端口，docker 只能对宿主机和同宿主机的 docker 开放所有端口，其他机器访问 dockers 需要通过宿主机进行端口转发，而不能像虚拟机一样通过 IP 访问；
docker 默认安装系统包较少，默认安装的虚拟机往往字段一些常用的系统包，但是 docker 很多常用的包都没有（比如 docker 下 centos7 默认是没有 ip 命令的，也不支持 ssh 登陆）；

### Docker 的主要用途

（1）提供一次性的环境。比如，本地测试他人的软件、持续集成的时候提供单元测试和构建的环境。
（2）提供弹性的云服务。因为 Docker 容器可以随开随关，很适合动态扩容和缩容。
（3）组建微服务架构。通过多个容器，一台机器可以跑多个服务，因此在本机就可以模拟出微服务架构

[https://blog.csdn.net/u013007900/article/details/62219169](https://blog.csdn.net/u013007900/article/details/62219169)
[https://blog.csdn.net/xiangxizhishi/article/details/79441391](https://blog.csdn.net/xiangxizhishi/article/details/79441391)

## Docker 架构

- Docker 基本概念[https://blog.csdn.net/omnispace/article/details/79778544](https://blog.csdn.net/omnispace/article/details/79778544)
- Docker 介绍以及其相关术语、底层原理和技术:[https://blog.csdn.net/zxygww/article/details/53709106](https://blog.csdn.net/zxygww/article/details/53709106)

Docker 使用客户端-服务器 (C/S) 架构模式，使用远程 API 来管理和创建 Docker 容器。
Docker 容器通过 Docker 镜像来创建。容器与镜像的关系类似于面向对象编程中的对象与类

## Docker 术语

**集群**
一个集群指容器运行所需要的云资源组合，关联了若干服务器节点、负载均衡、专有网络等云资源。
**节点**
一台服务器（可以是虚拟机实例或者物理服务器）已经安装了 Docker Engine，可以用于部署和管理容器；容器服务的 Agent 程序会安装到节点上并注册到一个集群上。集群中的节点数量可以伸缩。
**容器**
一个通过 Docker 镜像创建的运行时实例，一个节点可运行多个容器。
**镜像**
Docker 镜像是容器应用打包的标准格式，在部署容器化应用时可以指定镜像，镜像可以来自于 Docker Hub，阿里云容器 Hub，或者用户的私有 Registry。镜像 ID 可以由镜像所在仓库 URI 和镜像 Tag（缺省为 latest）唯一确认。
**编排模板**
编排模板包含了一组容器服务的定义和其相互关联，可以用于多容器应用的部署和管理。容器服务支持 Docker Compose 模板规范并有所扩展。
**应用**
一个应用可通过单个镜像或一个编排模板创建，每个应用可包含 1 个或多个服务。
**服务**
一组基于相同镜像和配置定义的容器，作为一个可伸缩的微服务。
**关联关系**
![关联关系](https://upload-images.jianshu.io/upload_images/2536979-89132b1352b2dbf4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/719/format/webp)

镜像：用来启动容器的只读模板，是容器启动所需的 rootfs，类似于虚拟机所使用的镜像。

容器：Docker 容器是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。

镜像是容器的基础，可以简单的理解为镜像是我们启动虚拟机时需要的镜像，容器时虚拟机成功启动后，运行的服务。

### docker load & docker import 的区别

- docker save images_name：将一个镜像导出为文件，再使用 docker load 命令将文件导入为一个镜像，会保存该镜像的的所有历史记录。比 docker export 命令导出的文件大，很好理解，因为会保存镜像的所有历史记录。
- docker export container_id：将一个容器导出为文件，再使用 docker import 命令将容器导入成为一个新的镜像，但是相比 docker save 命令，容器文件会丢失所有元数据和历史记录，仅保存容器当时的状态，相当于虚拟机快照。

docker save 对应 docker load

docker export 对应 docker import

## Docker-目录索引

- docker-部署
  - [Docker-安装部署](https://www.superscfan.top/docker/install)
  - [Docker-配置文件](https://www.superscfan.top/docker/config)
- docker-使用
  - [Docker-Compose](https://www.superscfan.top/docker/docker-compose)
  - [Docker-File](https://www.superscfan.top/docker/docker-file)
  - [Docker-功能模块](https://www.superscfan.top/docker/function)
  - [Docker 常见问题](https://www.superscfan.top/docker/issue)
  - [Docker-常用命令](https://www.superscfan.top/docker/cmd)
- 应用部署
  - [Docker-CDH](https://www.superscfan.top/docker/cdh)
  - [Docker-Oracle](https://www.superscfan.top/docker/oracle)
  - [Docker-Mysql](https://www.superscfan.top/docker/mysql)
  - [Docker-Neo4j](https://www.superscfan.top/docker/neo4j)
  - [Docker-ES](https://www.superscfan.top/docker/es)
  - [Docker-Doris](https://www.superscfan.top/docker/doris)
  - [Docker-Db2](https://www.superscfan.top/docker/db2)
- docker-管理
  - [Docker-K8S](https://www.superscfan.top/docker/k8s)

## 相关资源

TODO K8S(容器集群管理工具)的使用

- 配置单向网关或防火墙策略时，外部网络变动时，容器内部不会变动，容器以及 docker 都需要重启才可以更新。

### 参考资源

- [Docker 容器间通信方法](https://juejin.im/post/5ce26cb9f265da1bcd37aa7c)
- [Docker 的四种网络模式](https://blog.csdn.net/huanongying123/article/details/73556634)
- [docker 跨服务器容器的网络配置](https://blog.csdn.net/ithaibiantingsong/article/details/81386307)
- [Docker 容器跨主机通信之：直接路由方式](https://www.jianshu.com/p/477a62165376)
- [Docker 启动时的报错汇总](https://www.jianshu.com/p/93518610eea1)
- [Docker 配置文件 daemon.json 解析](https://www.jianshu.com/p/c7c7dc24b9e3)
