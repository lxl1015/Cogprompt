KNOWLEDGE_KEYWORDS = {
    1: [  # K1 Linux基本命令使用
        "ls", "ll", "la", "cp", "mv", "rm", "mkdir", "touch", "pwd",
        "cd", "rmdir", "find", "locate", "grep", "cat", "head", "tail",
        "less", "more", "echo", "man", "chmod", "chown", "file", "stat",
        "wc", "diff", "sort", "uniq", "tee", "xargs", "管道", "重定向",
        "标准输入", "标准输出", "命令行", "终端", "bash 命令", "基础命令"
    ],

    2: [  # K2 用户与权限管理
        "useradd", "userdel", "usermod", "groupadd", "groupdel", "groupmod",
        "passwd", "sudo", "su", "权限", "文件权限", "所有者", "属组",
        "chmod", "chown", "umask", "ACL", "root", "特权用户", "安全策略",
        "访问控制", "setuid", "setgid"
    ],

    3: [  # K3 文件系统与目录结构
        "目录结构", "文件树", "文件系统", "ext4", "xfs", "btrfs", "挂载",
        "mount", "umount", "fstab", "inode", "软链接", "硬链接", "ln",
        "/etc", "/usr", "/bin", "/sbin", "/var", "/home", "分区", "磁盘",
        "df", "du", "lsblk", "fdisk", "目录含义"
    ],

    4: [  # K4 Shell 编程与控制结构
        "shell 脚本", "bash 脚本", "sh", "脚本变量", "环境变量", "if",
        "for", "while", "case", "函数", "管道", "重定向", "$( )", "` `",
        "shell 编程", "流程控制", "脚本执行", "shebang", "#!/bin/bash"
    ],

    5: [  # K5 软件安装与包管理
        "apt", "apt-get", "dpkg", "rpm", "yum", "dnf", "包管理器",
        "软件安装", "软件卸载", "依赖", "仓库", "source list", "make install",
        "编译安装", "安装包", "升级软件", "软件源"
    ],

    6: [  # K6 内核编译与系统配置
        "内核", "kernel", "内核编译", "make menuconfig", "引导", "grub",
        "initramfs", "模块", "modprobe", "lsmod", "内核参数", "启动流程",
        "system boot", "内核源码", "dmesg", "系统配置"
    ],

    7: [  # K7 系统管理与性能分析
        "top", "htop", "ps", "free", "vmstat", "iostat", "sar", "系统监控",
        "日志", "journalctl", "systemctl", "service", "内存占用", "CPU 占用",
        "磁盘使用", "性能分析", "资源管理", "进程", "系统维护"
    ],

    8: [  # K8 网络配置与服务
        "ifconfig", "ip addr", "ip route", "ping", "traceroute", "netstat",
        "ss", "curl", "wget", "DNS", "网卡", "网络配置", "防火墙", "ufw",
        "iptables", "路由", "DHCP", "hostname", "网络接口"
    ],

    9: [  # K9 开发工具与调试技巧
        "gcc", "g++", "make", "makefile", "cmake", "gdb", "lldb",
        "调试", "断点", "单步执行", "编译器", "构建工具", "日志调试",
        "strace", "ltrace", "开发工具", "调试技巧", "源码分析"
    ]
}

PREREQUISITES = [
    (3, 6),
    (3, 7),
    (3, 8),
    (2, 7),
    (2, 8),
    (4, 7),
    (5, 7),
    (7, 6),
]

SIMILAR = [
    (1, 3),
    (1, 4),
    (3, 4),
    (2, 5),
    (2, 7),
    (5, 7),
    (7, 8),
    (4, 9),
    (1, 9),
    (6, 7),
]

