#!/usr/bin/env python3
"""nvtop 汉化词典 —— 设置窗口（interface_setup_win.c）

⚠️ 严格限定文件：本词典只用于 interface_setup_win.c
   该文件里的字符串**全部是显示文字**（数组型的描述文本），
   不含配置文件键名（那些在 interface_options.c，禁止翻译）。

验证依据（2026-09-15 实测）：
    - interface_options.c 有 static const char general_value_use_color[] = "UseColor"
      → 写入 ~/.config/nvtop/nvtop.conf 的键名，翻了配置读不回来
    - interface_setup_win.c 全是 setup_*_description[] 数组
      → 纯显示，翻之无害
"""

# 分类导航（左侧栏）
CATEGORY = {
    "General": "常规",
    "Devices": "设备",
    "Chart": "图表",
    "Processes": "进程",
    "GPU Select": "GPU 选择",
}

# 常规选项描述
GENERAL = {
    "Disable color (requires save and restart)": "禁用颜色（需保存并重启）",
    "Show support messages on startup": "启动时显示支持信息",
    "Update interval (seconds)": "刷新间隔（秒）",
}

# 显示选项（Header Options）
HEADER = {
    "Temperature in fahrenheit": "温度用华氏度",
    "Keep displaying Encoder/Decoder rate (after reaching an idle state)":
        "空闲后仍显示编解码速率",
    "Display extra GPU info bar": "显示额外 GPU 信息栏",
}

# 图表选项
CHART = {
    "Reverse plot direction": "反转曲线方向",
    "Displayed all GPUs": "显示全部 GPU",
    "Displayed GPU": "显示 GPU",
    # 曲线指标名（12 个）
    "GPU utilization rate": "GPU 利用率",
    "GPU memory utilization rate": "显存利用率",
    "GPU encoder rate": "GPU 编码器利用率",
    "GPU decoder rate": "GPU 解码器利用率",
    "GPU temperature": "GPU 温度",
    "Power draw rate (current/max)": "功耗（当前/最大）",
    "Fan speed": "风扇转速",
    "GPU clock rate": "GPU 核心频率",
    "GPU memory clock rate": "显存频率",
    "Effective load rate": "有效负载",
    "PCIe RX load rate": "PCIe 接收负载",
    "PCIe TX load rate": "PCIe 发送负载",
    # 颜色名
    "Red": "红",
    "Cyan": "青",
    "Green": "绿",
    "Yellow": "黄",
    "Blue": "蓝",
    "Magenta": "品红",
    "White": "白",
}

# 进程列表选项
PROCESS = {
    "Don't display the process list": "不显示进程列表",
    "Hide nvtop in the process list": "在进程列表中隐藏 nvtop",
    "Sort Ascending": "升序排列",
    "Sort by": "排序字段",
    "Field Displayed": "显示字段",
    # 11 个字段名
    "Process Id": "进程 ID",
    "User name": "用户名",
    "Device Id": "设备 ID",
    "Workload type": "负载类型",
    "GPU usage": "GPU 占用",
    "Encoder usage": "编码器占用",
    "Decoder usage": "解码器占用",
    "GPU memory usage": "显存占用",
    "CPU usage": "CPU 占用",
    "CPU memory usage": "内存占用",
    "Command": "命令",
}

# 窗口标题
TITLES = {
    "General Options": "常规选项",
    "Devices Display Options": "设备显示选项",
    "Chart Options": "图表选项",
    "Process List Options": "进程列表选项",
    "Select Monitored GPUs": "选择监视的 GPU",
    "Metric Displayed in Graph": "图表显示的指标",
    "Processes are sorted by:": "进程排序依据：",
    "Process Field Displayed:": "显示的进程字段：",
    "Maximum of 4 metrics per GPU": "每个 GPU 最多 4 个指标",
    "Nothing to sort: none of the process fields are displayed":
        "无法排序：未显示任何进程字段",
    "Setup": "设置",
}

# 底部按键提示
KEYS = {
    "Enter": "Enter",
    "Arrow keys": "方向键",
    "Toggle": "切换",
    "Exit": "退出",
    "Navigate Menu": "切换菜单",
    "Increment/Decrement Values": "增减数值",
    "Save Config": "保存配置",
    "Press Enter to select, arrows \">\" and \"<\" to switch options":
        "回车选择，方向键 \">\" 和 \"<\" 切换选项",
    "EnterToggle ESCExit Arrow keysNavigate Menu +/-Increment/Decrement Values F12Save Config":
        "Enter切换 ESC退出 方向键切换菜单 +/-增减数值 F12保存配置",
}

# 合并总表
ALL = {}
for d in (CATEGORY, GENERAL, HEADER, CHART, PROCESS, TITLES, KEYS):
    ALL.update(d)

if __name__ == '__main__':
    print(f"词典共 {len(ALL)} 条")
    for k, v in ALL.items():
        print(f"  {k!r}\n    → {v!r}")
