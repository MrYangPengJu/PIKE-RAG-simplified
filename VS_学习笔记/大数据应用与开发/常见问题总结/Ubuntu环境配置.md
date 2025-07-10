## Ubuntu环境下配置固定IP
> 修改/etc/netplan下的yaml文件,例如：
> ```
> network:
>   version: 2
>   renderer: NetworkManager
>   ethernets:
>         ens33: # 替换为你的网络接口名称
>             dhcp4: false # 关闭 DHCP
>             dhcp6: false # 关闭 DHCP
>             addresses: [192.168.88.101/24] # 静态 IP 地址和子网掩码
>             routes:
>               - to: default
>                 via: 192.168.88.2 # 网关> 地址
>             nameservers:
>                 addresses: [192.168.88.2] # DNS 服务器地址
>                 search: []
> ```
> 注意yaml文件的根级别的配置以及缩进问题

## vim的使用
> 遇到只读文件使用sudo vim指令，进入vim后按下任一指令符：
> 按 i：进入插入模式，可以在光标前插入文本。
> 按 I：在行首插入。
> 按 a：在光标后插入文本。
> 按 A：在行末插入。
> 结束编辑后按下ESC回到命令输入状态(即普通状态)
> 输入 :wq 然后按 Enter：保存文件并退出 vim。
> 输入 :q! 然后按 Enter：不保存强制退出。
> 输入 :w 然后按 Enter：仅保存文件，不退出。

## SELinux关闭
> SELinux 代表安全增强型 Linux，是为 Linux 系统构建的额外安全控制层。
> Ubuntu 提供 AppArmor 作为 SELinux 的替代品。虽然 SELinux 在 Ubuntu 上可用，但它还处于实验阶段，如果设置为强制模式，很可能会破坏您的系统。如果您必须使用 SELinux，请确保首先禁用 AppArmor。另外，首先将 SELinux 设置为“宽容”模式，并在启用“强制”模式之前检查日志是否存在潜在问题。
> 执行如下命令，停止AppArmor
> ```C
> sudo systemctl stop apparmor
> ```
> 执行如下命令，禁止AppArmor开机自启动
> ```C
> sudo systemctl disable apparmor 
> ```
> 执行如下命令，彻底移除AppArmor安全增强工具及其相关配置
> ```C
> sudo apt-get purge -y apparmor apparmor-utils && sudo rm -rf /etc/apparmor /etc/apparmor.d && sudo modprobe -r apparmor
> ```
