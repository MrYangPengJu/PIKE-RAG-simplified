## 虚拟机安装
1. 虚拟机安装失败可能是因为分配的内存不够导致

## 配置静态ip
> 要将网络配置从自动获取IP（DHCP）改为固定IP,你需要修改`/etc/NetworkManager/system-connections/<connection-name>.nmconnection`文件中的`[ipv4]`部分。以下是修改后的配置文件内容:
> 
> ### 修改后的配置文件
> ```ini
> [connection]
> id=ens33
> uuid=2d7a292d-a663-3bfb-be98-ffc987667374
> type=ethernet
> autoconnect-priority=-999
> interface-name=ens33
> timestamp=1738967882
> 
> [ethernet]
> 
> [ipv4]
> method=manual
> address1=192.168.88.101/24,192.168.88.2
> dns=192.168.88.2;
> ignore-auto-dns=true
> 
> [ipv6]
> addr-gen-mode=eui64
> method=auto
> ```
> 
> ### 修改说明
> 1. **`[ipv4]`部分**:
>    - `method=manual`:设置为手动配置IP。
>    - `address1=192.168.88.101/24,192.168.88.2`:
>      - `192.168.88.101/24`:固定IP地址和子网掩码（`/24`表示子网掩码为`255.255.255.0`）。
>      - `192.168.88.2`:网关地址。
>    - `dns=192.168.88.2;`:设置DNS服务器地址。
>    - `ignore-auto-dns=true`:忽略自动获取的DNS,确保使用手动配置的DNS。
> 
> 2. **`[ipv6]`部分**:
>    - 保持不变,因为你不涉及IPv6的修改。
> 
> ### 应用配置
> 1. 保存文件后,重启`NetworkManager`服务以应用更改:
>    ```bash

>    sudo systemctl restart NetworkManager
>    ```
> 
> 2. 检查网络配置是否生效:
>    ```bash
>    ip addr show ens33
>    ```
>    确保IP地址已更改为`192.168.88.101`。
> 
> ### 注意事项
> - 如果修改后网络无法正常工作,可以检查`/var/log/messages`或`journalctl -xe`查看错误日志。
> - 如果需要恢复自动获取IP,可以将`method=manual`改回`method=auto`,并删除`address1`和`dns`配置。
> - 如果通过克隆得到新的虚拟机,在修改nmconnection文件后出现上一台虚拟机的ip地址,重启虚拟机即可消除。

## 安装JDK
> 1. rz上传包, 再使用tar解压至目标文件夹
> 2. 在目标文件夹创建软连接(必须要在目标文件夹中创建)以简化命名
> 3. 在/etc/profile中添加系统路径
> ```ini
> export JAVA_HOME=TarDir
> export PATH=$PATH:$JAVA_HOME/bin
> ```
> 4. 使用source /etc/profile 命令激活路径即可

## ssh免密登录
1. 如果使用root用户实现免密互通,则需要先进入root权限,才能完成登录。

## hadoop配置
1. 如果使用hadoop namenode -format后, 在/data/nn文件中没有发现current文件,以下为解决方案:
> ### 检查 Hadoop 配置
> 确保您的 Hadoop 配置文件（如 `core-site.xml` 和 `hdfs-site.xml`）正确无误, 特别是与安全相关的配置。
> 
> #### 检查 Java 版本
> 确保您使用的 Java 版本与 Hadoop 版本兼容。某些版本的 Java 可能会导致与 Hadoop 的兼容性问题。
> 
> #### 检查权限
> 确保运行 Hadoop 的用户（在此情况下为 `hadoop`）对日志目录和其他相关目录具有适当的读/写权限。
>
> ### Big Data Tools
> 当使用Pycharm的big data tools无法连接hadoop, 如果前面的配置没有问题, 可能是因为没有在hadoop中创建文件夹导致。

## MySQL安装
> 1. 由于centOS10stream过于超前, 安装mysql57将会十分困难, 因此推荐安装mysql8.0
> 2. 在安装MySQL8.0时, 一定要注意使用最新的网址!
> * 如sudo rpm -Uvh https://dev.mysql.com/get/mysql80-community-release-el7-7.noarch.rpm 安装后再去安装sudo dnf install -y mysql-community-server 会缺少依赖！
> 而如果使用sudo dnf install -y https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm 则会解决此问题！
> * 有时不翻墙使用镜像下载的文件过旧, 也会导致依赖问题, 因此建议翻墙后下载相关包。
> 3. 若rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysqL-2022 提示密钥已过期, 也需要寻找最新的密钥地址, 如:rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysqL-2023
> 4. 注意mysql5.7与mysql8.0有许多规则不同

## HIVE配置
> 1. 由于这个过程需要初始化元数据库, 因此需要mysql驱动包, 而如果mysql为8.0, 需要注意驱动包不能太老旧, 下载地址: https://downloads.mysql.com/archives/c-j/ 
> 2. 如果利用rpm文件无法安装驱动, 不妨直接下载jar包并复制进hive/lib中。
> 3. Public Key Retrieval is not allowed 是与 MySQL 8.0 的身份验证机制有关的一个常见问题。MySQL 8.0 默认启用了 caching_sha2_password 插件, 这会导致使用某些 JDBC 驱动连接时出现问题, 特别是在使用旧版驱动或未配置适当选项时。
> 在 hive-site.xml 中找到 javax.jdo.option.ConnectionURL 配置, 确保它包括以下内容：
> ```ini
> <property>
>     <name>javax.jdo.option.ConnectionURL</name>
>     <value>jdbc:mysql://node1:3306/hive?createDatabaseIfNotExist=true&amp;useSSL=false&amp;allowPublicKeyRetrieval=true&amp;useUnicode=true&amp;characterEncoding=UTF-8</value>
> </property>
> ```
> 4. 如果出现
> hive> show databases;
> show databases
> FAILED: HiveException java.lang.RuntimeException: Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient
> 可能是因为没有启动MetaStore服务, 启动指令: /export/server/apache-hive-3.1.3-bin/bin/hive --service metastore &
> 具体一点: 前台启动: bin/hive --service metastore
> 后台启动: nohup bin/hive --service metastore >> logs/metastore.log 2>&1 & 
> 5. hiveserver启动命令: nohup bin/hive --service hiveserver2 >> logs/hiveserver2.log 2>&1 &
> 6. 无论是启动Metastore还是Hiveserver2, 都需要在hive文件夹内执行, 不能在logs文件夹执行上述命令。
> 7. 使用DataGrip或beeline前需要先启动Hiveserver2
> 