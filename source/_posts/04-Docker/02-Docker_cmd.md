---
title: Docker常用命令
url_path: docker/cmd
tags:
  - docker
  - module
categories:
  - docker
description: Docker常用命令
---

### Docker 常用命令

```bash
# Docker服务启停
service docker restart
# 创建一个容器
docker run -it -v /docker_test:/yufei --name yufei_6 centos
参数说明
-i: 允许我们对容器内的 (STDIN) 进行交互
-t: 在新容器内指定一个伪终端或终端
-v: 是挂在宿机目录， /docker_test是宿机目录，/yufei是当前docker容器的目录，宿机目录必须是绝对的。
--name: 是给容器起一个名字，可省略，省略的话docker会随机产生一个名字
# 查看docker容器列表(运行中)
docker ps
# 查看所有的docker容器列表
docker ps -a
# 启停容器
docker start yufei_01
docker stop yufei_01
docker restart yufei_01
# 查看容器的日志
docker logs -f yufei_01
# 删除容器，如果容器在运行需要先停止
docker stop yufei_01
docker rm yufei_01
# 删除所有容器
docker rm $(docker ps -a -q)



# Docker服务启停
service docker start
service docker stop
service docker restart

# Docker网络管理
docker network create --subnet=172.18.0.0/16 extnetwork #创建网络
docker network ls #列出当前所有网络
docker network rm extnetwork #删除网络

# 创建一个容器
docker run --privileged=true -m 8000M --cpus=2 -itd --name 12306 --net extnetwork --ip 172.18.0.72 docker_7 /usr/sbin/init
参数说明
-i：允许我们对容器内的 (STDIN) 进行交互
-t：在新容器内指定一个伪终端或终端
-d: 后台运行
--privileged=true 如果不加此参数，root也可能会部分操作无权限
-m 限制最大使用内存
--cpus cpu使用限制
--name：是给容器起一个名字
--net 指定网段
--ip 指定ip
参数里面的centos是镜像名字，如果本地无名字对应的镜像，则会在网络上寻找，并自动下载到本地,若不指定版本，则下载最新版本

# 查看docker容器列表(运行中)
docker ps
# 查看所有的docker容器列表
docker ps -a

# 启停容器
docker start docker_7
docker restart docker_7
docker stop docker_7

# 删除容器，如果容器在运行需要先停止
docker stop docker_7
docker rm docker_7

# 容器保存为镜像
docker commit docker_7 img_docker_7

# 镜像导入导出
docker export docker_7 -o docker_7.tar
docker import docker_7.tar docker_7
```

### Docker 命令大全

- Docker 命令大全:[http://www.runoob.com/docker/docker-command-manual.html](http://www.runoob.com/docker/docker-command-manual.html)

- 容器生命周期管理
  - docker run 创建一个新的容器并运行一个命令
  - docker restart 重启容器
  - docker kill -s KILL mynginx 杀掉一个运行中的容器。 -s :向容器发送一个信号
  - docker rm : 删除一个或多少容器
  - docker pause :暂停容器中所有的进程。
  - docker unpause :恢复容器中所有的进程。
  - docker create : 创建一个新的容器但不启动它
  - docker exec : 在运行的容器中执行命令
- 容器操作
  - docker ps :  列出容器
  - docker inspect :  获取容器/镜像的元数据。
  - docker top :查看容器中运行的进程信息，支持 ps 命令参数
  - docker attach :连接到正在运行中的容器
  - docker events :  从服务器获取实时事件
  - docker logs :  获取容器的日志
  - docker wait :  阻塞运行直到容器停止，然后打印出它的退出代码
  - docker export :将文件系统作为一个 tar 归档文件导出到 STDOUT
  - docker port :列出指定的容器的端口映射，或者查找将 PRIVATE_PORT NAT 到面向公众的端口。
- 容器 rootfs 命令
  - docker commit :从容器创建一个新的镜像。
  - docker cp :用于容器与主机之间的数据拷贝
  - docker diff :  检查容器里文件结构的更改
- 镜像仓库
  - docker login :  登陆到一个 Docker 镜像仓库，如果未指定镜像仓库地址，默认为官方仓库 Docker Hubdocker
  - docker logout :  登出一个 Docker 镜像仓库，如果未指定镜像仓库地址，默认为官方仓库 Docker Hub
  - docker pull :  从镜像仓库中拉取或者更新指定镜像
  - docker push :  将本地的镜像上传到镜像仓库,要先登陆到镜像仓库
  - docker search: 从 Docker Hub 查找镜像
- 本地镜像管理
  - docker images :  列出本地镜像
  - docker rmi :  删除本地一个或多少镜像
  - docker tag :  标记本地镜像，将其归入某一仓库
  - docker build  命令用于使用 Dockerfile 创建镜像
  - docker history :  查看指定镜像的创建历史
  - docker save :  将指定镜像保存成 tar 归档文件
  - docker import :  从归档文件中创建镜像
- info|version
  - docker info : 显示 Docker 系统信息，包括镜像和容器数。
  - docker version :显示 Docker 版本信息

### docker 命令样例

```bash

# 启动镜像时，设定docker系统参数 - 修改系统参数 生效
docker run -it -d -p 80:80 -p 3000:3000 -p 8080:8080 -p 9200:9200 -p 5600:5602 -p 5601:5601 --env=vm.max_map_count=262144 fdm_docker_ok /bin/bash

镜像的导入导出
# 导出镜像 images
sudo docker images REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
sudo docker save -o /home/user/images/ubuntu_14.04.tar ubuntu:14.04
# 导入镜像
sudo docker load --input ubuntu_14.04.tar
sudo docker load &lt; ubuntu_14.04.tar


镜像删除
docker rmi images_id


容器模块

查看容器的环境变量
* 使用docker inspect命令来查看
# docker inspect <CONTAINER-NAME> OR <CONTAINER-ID>
* 使用docker exec -it <CONTAINER-NAME> OR <CONTAINER-ID> env查看

docker镜像启动命令 - 镜像启动每次容器ID都会变更
docker run -it -d -p 50001:22  -p 80:80 -p 3000:3000 -p 8080:8080 -p 9200:9200 -p 5600:5602 -p 5601:5601 --env=vm.max_map_count=262144  fdm_docker /bin/bash

docker 容器启动命令
docker container start 4d15e75d1116 

进入docker容器中
docker exec -it fa6e4ac38997 /bin/bash

查看容器ID
# 查看当前运行的容器
docker ps
# 查看历史所有的容器
docker ps -a 
可以通过启动历史容器，并进入

保存容器为镜像
docker ps -a 
可以通过启动历史容器，并进入


容器的导入导出
# 容器的导入
docker import fdm_docker.tar.gz  fdm_docker
# 将容器保存为镜像
docker commit 8e613c207029 fdm_docker02 


# 查看所有容器名称及IP
(env) [fdm@fdm ~]$ docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq)
/oracle11g_2 - 172.17.0.3
/fdm_es56 - 172.18.0.85
/fdm_es74 - 172.18.0.84
/oracle11g - 172.17.0.2
/fdm_graph - 172.18.0.86

```
