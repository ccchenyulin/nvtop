#!/usr/bin/env python3
"""nvtop 汉化词典 —— 主界面 / 进程操作 / CLI

⚠️ 使用范围（每个文件单独控制）：
    - src/interface.c     → 只翻【显示文字】，跳过信号名数组
    - src/nvtop.c         → 翻 CLI 帮助与错误消息
    - src/plot.c          → 翻错误消息

❌ 禁止用于 src/interface_options.c（配置文件键名）
❌ 禁止翻 signalNames[] 里的 SIGxxx（真实信号名，signalValues 与之对应）
"""

# ---- interface.c：进程负载类型（纯显示）----
PROCESS_TYPE = {
    "Both G+C": "图形+计算",
    "Graphic": "图形",
    "Compute": "计算",
}

# ---- interface.c：进程操作窗口 ----
PROCESS_OPTS = {
    "Send signal:": "发送信号：",
    "Sort by     ": "排序字段   ",   # ⚠️ 尾部空格是原格式的一部分，保留对齐
    "Sort by": "排序字段",
    "Cancel": "取消",                 # signalNames[0] 仅显示用（signalValues[0] = -1）
    "+": "+",
    "-": "-",
    "Ascending": "升序",
    "Descending": "降序",
    "Send": "发送",                   # option_selection_kill
}

# ---- interface.c：底部功能键栏 ----
# ⚠️ 这些是多个独立字符串，拼接后形成 "F2Setup   F6Sort    F9Kill    F10Quit    F12Save Config"
#    翻译后总宽度会变，但 nvtop 是逐个 draw 的，不依赖总宽（实测确认）
FKEYS = {
    "Setup": "设置",
    "Sort": "排序",
    "Kill": "终止",
    "Quit": "退出",
    "Save Config": "保存配置",
}

# ---- interface.c：其它显示文字 ----
MISC = {
    "Integrated GPU": "集成显卡",
    "Error: Not enough columns to draw device information\n": "错误：列数不足以绘制设备信息\n",
}

# ---- nvtop.c：CLI 帮助（-h）----
# 注意：保留选项名（-d/-v/...）与占位符
CLI_HELP = {
    "Available options:\n": "可用选项：\n",
    "  -d --delay        : Select the refresh rate (1 == 0.1s)\n":
        "  -d --delay        : 选择刷新率（1 == 0.1 秒）\n",
    "  -v --version      : Print the version and exit\n":
        "  -v --version      : 打印版本并退出\n",
    "  -c --config-file  : Provide a custom config file location to load/save ":
        "  -c --config-file  : 指定自定义配置文件路径用于读写 ",
    "  -p --no-plot      : Disable bar plot\n":
        "  -p --no-plot      : 禁用曲线图\n",
    "  -P --no-processes : Disable process list\n":
        "  -P --no-processes : 禁用进程列表\n",
    "  -r --reverse-abs  : Reverse abscissa: plot the recent data left and ":
        "  -r --reverse-abs  : 反转横轴：最近的数据在左，",
    "older on the right\n": "较早的在右\n",
    "  -C --no-color     : No colors\n":
        "  -C --no-color     : 不使用颜色\n",
    "line information\n": "行信息\n",
    "  -f --freedom-unit : Use fahrenheit\n":
        "  -f --freedom-unit : 使用华氏度\n",
    "  -i --gpu-info     : Show bar with additional GPU parameters\n":
        "  -i --gpu-info     : 显示带额外 GPU 参数的栏\n",
    "  -E --encode-hide  : Set encode/decode auto hide time in seconds ":
        "  -E --encode-hide  : 设置编解码自动隐藏时间（秒）",
    "(default 30s, negative = always on screen)\n": "（默认 30 秒，负数 = 始终显示）\n",
    "  -h --help         : Print help and exit\n":
        "  -h --help         : 打印帮助并退出\n",
    "  -s --snapshot     : Output the current gpu stats without ncurses":
        "  -s --snapshot     : 不启用 ncurses 输出当前 GPU 状态",
    "(useful for scripting)\n": "（便于脚本处理）\n",
    "  -l --loop         : Output the current gpu stats without ncurses in a loop\n":
        "  -l --loop         : 不启用 ncurses 循环输出 GPU 状态\n",
}

# ---- nvtop.c：错误消息 ----
CLI_ERR = {
    "Error: The delay must be a positive value ": "错误：刷新率必须为正值 ",
    "representing tenths of seconds\n": "（单位为十分之一秒）\n",
    "Error: A negative delay requires a time machine!\n":
        "错误：负的刷新率需要时光机！\n",
    "Invalid format for encode/decode hide time: %s\n":
        "编解码隐藏时间格式无效：%s\n",
    "Error: The delay option takes a positive value ":
        "错误：刷新率选项需要一个正值 ",
    "Unhandled error in getopt missing argument\n":
        "getopt 缺少参数，未处理的错误\n",
    "Impossible to set signal handler for SIGINT: ":
        "无法为 SIGINT 设置信号处理器：",
    "Impossible to set signal handler for SIGQUIT: ":
        "无法为 SIGQUIT 设置信号处理器：",
    "Impossible to set signal handler for SIGWINCH: ":
        "无法为 SIGWINCH 设置信号处理器：",
    "Impossible to set signal handler for SIGCONT: ":
        "无法为 SIGCONT 设置信号处理器：",
    "No GPU to monitor.\n": "没有可监视的 GPU。\n",
}

# ---- plot.c ----
PLOT = {
    "Cannot plot more than ": "最多只能绘制 ",
    " lines": " 条线",
}

# ---- info_messages_linux.c（启动时的支持提示）----
# 注：'Intel' 是厂商名，不翻
INFO = {}


ALL = {}
for d in (PROCESS_TYPE, PROCESS_OPTS, FKEYS, MISC, CLI_HELP, CLI_ERR, PLOT, INFO):
    ALL.update(d)

# ⚠️ 黑名单：即使在目标文件里出现也绝不翻译
NEVER = set(signalNames_placeholder for signalNames_placeholder in []) | {
    "SIGHUP", "SIGINT", "SIGQUIT", "SIGILL", "SIGTRAP", "SIGABRT", "SIGBUS",
    "SIGFPE", "SIGKILL", "SIGUSR1", "SIGSEGV", "SIGUSR2", "SIGPIPE", "SIGALRM",
    "SIGTERM", "SIGCHLD", "SIGCONT", "SIGSTOP", "SIGTSTP", "SIGTTIN", "SIGTTOU",
    "SIGURG", "SIGXCPU", "SIGXFSZ", "SIGVTALRM", "SIGPROF", "SIGWINCH", "SIGIO",
    "SIGPWR", "SIGSYS", "Intel",
}

if __name__ == '__main__':
    print(f"词典共 {len(ALL)} 条（黑名单 {len(NEVER)} 条）")
