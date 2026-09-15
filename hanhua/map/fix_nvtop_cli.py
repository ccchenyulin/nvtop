#!/usr/bin/env python3
"""nvtop.c 专用：整体替换 helpstring[] 与错误消息

背景（坑 C7 同类）：helpstring 是一个 const 字符串常量，
逐行用相邻字面量拼接。逐行替换会只翻到"首行匹配的片段"，
其余行因词典无对应条目而漏翻 → 之前实测出现中英混杂。

正确做法：把整个 helpstring[] 定义块**整体重写**，一次性换成完整中文。
"""
import re
import sys
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(REPO, 'src/nvtop.c')

NEW_HELP = '''static const char helpstring[] = "可用选项：\\n"
                                 "  -d --delay        : 选择刷新率（1 == 0.1 秒）\\n"
                                 "  -v --version      : 打印版本并退出\\n"
                                 "  -c --config-file  : 指定自定义配置文件路径，用于读写偏好设置\\n"
                                 "  -p --no-plot      : 禁用曲线图\\n"
                                 "  -P --no-processes : 禁用进程列表\\n"
                                 "  -r --reverse-abs  : 反转横轴：最近的数据在左，较早的在右\\n"
                                 "  -C --no-color     : 不使用颜色\\n"
                                 "  -f --freedom-unit : 使用华氏度\\n"
                                 "  -i --gpu-info     : 显示带额外 GPU 参数的栏\\n"
                                 "  -E --encode-hide  : 设置编解码速率的自动隐藏时间（秒）\\n"
                                 "                      （默认 30 秒，负数 = 始终显示在屏幕上）\\n"
                                 "  -h --help         : 打印本帮助并退出\\n"
                                 "  -s --snapshot     : 不启用 ncurses，直接输出当前 GPU 状态\\n"
                                 "                      （便于脚本处理）\\n"
                                 "  -l --loop         : 不启用 ncurses，循环输出 GPU 状态\\n";'''

# 错误消息（逐条，都是单行完整字符串）
ERRORS = [
    ('"Error: The delay must be a positive value "\n'
     '                                    "representing tenths of seconds\\n"',
     '"错误：刷新率必须为正值（单位为十分之一秒）\\n"'),
    ('"Error: A negative delay requires a time machine!\\n"',
     '"错误：负的刷新率需要时光机！\\n"'),
    ('"Invalid format for encode/decode hide time: %s\\n"',
     '"编解码隐藏时间格式无效：%s\\n"'),
    ('"Error: The delay option takes a positive value "',
     '"错误：刷新率选项需要一个正值 "'),
    ('"Unhandled error in getopt missing argument\\n"',
     '"getopt 缺少参数，未处理的错误\\n"'),
    ('"Impossible to set signal handler for SIGINT: "',
     '"无法为 SIGINT 设置信号处理器："'),
    ('"Impossible to set signal handler for SIGQUIT: "',
     '"无法为 SIGQUIT 设置信号处理器："'),
    ('"Impossible to set signal handler for SIGWINCH: "',
     '"无法为 SIGWINCH 设置信号处理器："'),
    ('"Impossible to set signal handler for SIGCONT: "',
     '"无法为 SIGCONT 设置信号处理器："'),
    ('"No GPU to monitor.\\n"', '"没有可监视的 GPU。\\n"'),
]


def main():
    dry = '--apply' not in sys.argv
    s = open(PATH, encoding='utf-8').read()
    orig = s
    n = 0

    # 1) 整体替换 helpstring
    m = re.search(r'static const char helpstring\[\] = .*?;\n', s, re.S)
    if not m:
        print("❌ 找不到 helpstring 定义")
        return 1
    s = s[:m.start()] + NEW_HELP + '\n' + s[m.end():]
    print("  ✅ helpstring 整体替换（15 项）")
    n += 1

    # 2) 逐条替换错误消息
    for old, new in ERRORS:
        if s.count(old) == 1:
            s = s.replace(old, new, 1)
            print(f"  ✅ {old[:48]}...")
            n += 1
        elif s.count(old) == 0:
            print(f"  ⚠️ 未匹配: {old[:48]}...")
        else:
            print(f"  ⚠️ 匹配 {s.count(old)} 处（期望 1）: {old[:48]}...")

    if dry:
        print(f"\n[DRY-RUN] 共 {n} 处；加 --apply 写盘")
        return 0
    open(PATH, 'w', encoding='utf-8').write(s)
    print(f"\n[APPLIED] 共 {n} 处")


if __name__ == '__main__':
    sys.exit(main())
