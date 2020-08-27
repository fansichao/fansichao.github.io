---
title: Linux-关机前执行脚本
url_path: linux/restart_scripts
tags:
  - linux
categories:
  - linux-功能模块
description: 关机和重启前执行自定义脚本
---

## Centos7 关机和重启前执行自定义脚本

[Centos7 关机和重启前执行自定义脚本](https://blog.csdn.net/weixin_30768661/article/details/97437444)

**创建服务:**

`vim /etc/systemd/system/my-powerdown.service`
创建该文件然后加入下面的内容，需要把`ExecStart=/home/my_script`这一行换成自己的脚本路径

```bash
[Unit]
Description=close services before reboot and shutdown
DefaultDependencies=no
Before=shutdown.target reboot.target halt.target
# This works because it is installed in the target and will be
#   executed before the target state is entered
# Also consider kexec.target

[Service]
Type=oneshot
ExecStart=/home/my_script  #your path and filename

[Install]
WantedBy=halt.target reboot.target shutdown.target
```

**启动服务:**

```bash
# 执行命令：
systemctl start my-powerdown.service

# 启动刚写好的服务。
systemctl status my-powerdown.service

由于本服务指定了只执行一次。所以运行 enable 服务 不起作用。
可以将启动服务的命令加到开机执行脚本中。
这样就保证了服务一直是开启状态。
保证你设置的脚本能够在关机前正常运行
```
