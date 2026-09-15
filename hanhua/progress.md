# nvtop 汉化进度

## 2026-09-15 会话

### 背景
全系统 TUI 扫描发现 nvtop 未汉化（用户用了 42 次，比 ncdu/termusic/lazysql 都多）。
它是 `extra` 官方包（非 AUR），上游 Syllo/nvtop 11k star，活跃更新。

### 分类：第 ④ 类（无 i18n，必须改源码）
检查结果：
- `nm -D /usr/bin/nvtop | grep gettext` → 无 gettext 符号（只有 setlocale，供 ncurses 宽字符用）
- 不读 LANG/LC_*
- 无语言配置项

### 关键风险与处理 ⭐
`src/interface_options.c` 里的字符串是**配置文件键名**（写入 ~/.config/nvtop/interface.ini）：
```c
static const char general_value_use_color[] = "UseColor";
static const char *process_sortby_vals[] = {"pId","user","gpuId",...,"none"};
```
→ **绝不翻译**（翻了配置读写失效）。
→ 替换脚本用**文件白名单**隔离：interface_options.c 不在列表。

显示文字在**另一个文件**：`interface_setup_win.c` 的 `setup_*_description[]` 数组。

### 汉化成果
| 文件 | 处数 | 内容 |
|---|---|---|
| src/interface_setup_win.c | 60 处 | 5 个设置子菜单全部文字 |
| src/interface.c | 40 处 | 底部功能键栏、负载类型、对话框按钮/提示 |
| src/nvtop.c | 56 处 | CLI 帮助 15 项 + 错误消息 |
| src/plot.c | 2 处 | 错误消息 |

共约 158 处替换。

### 未改动（有意保留）
- 主界面表头（PID USER DEV TYPE GPU ... Command）—— 用户要求
- 配置文件键名（interface_options.c）—— 必须保留
- 真实信号名（SIGHUP 等，signalValues 与之对应）
- `nvtop version`（版本号行）

### 实测验证（全部通过）
| 项 | 结果 |
|---|---|
| CLI -h | ✅ 15 项全中文 |
| TUI 主界面底部 | ✅ `F2设置 F6排序 F9终止 F10退出 F12保存配置` |
| 负载类型 | ✅ `图形/计算/图形+计算` |
| F2 设置窗口 | ✅ 5 个子菜单全中文 |
| F6 排序对话框 | ✅ `Enter排序 ESC取消 +升序 -降序` |
| F9 终止对话框 | ✅ `Enter发送 ESC取消` |
| **配置读写** | ✅ F12 保存后键名仍英文（`UseColor = true`），**0 处中文污染** |
| 编译警告 | ✅ 与上游原版一致（9 条，都是原有的）|

### 踩坑（对应知识库的通用坑）
1. **跨行拼接的 helpstring 漏翻**（坑 C7 同类）：
   `helpstring[]` 是一个 const 字符串逐行拼接，逐行替换只翻到首行匹配片段，
   其余 9 行因词典无对应条目而漏 → 改用 `fix_nvtop_cli.py` **整块重写**。

2. **R1 复查扫描（合并相邻字面量）发现 6 处漏译**：
   `<Don't Show Again>` / `<Ok>` / `Press Enter to select...` /
   `Error: Not enough columns...` / `Cannot allocate memory:` / ` (All GPUs)`
   → 说明**首轮扫描必须按「合并后的逻辑单元」判断**，不能按单行。

3. **单词类漏译**（坑 4.5 同类）：`"Send"`（F9 对话框的"发送"）首轮词典漏了。

4. **未定义行为的对齐**：`option_selection_width = 8` 是固定宽度，
   `%-*s` 左对齐填充 → 译文必须 ≤ 8 显示宽，实测全部满足（最长"保存配置"= 8）。

### 安装方式：本地 PKGBUILD（方案 C）
与之前 6 个工具（装 ~/.cargo/bin + 卸载原版）不同，nvtop 是**官方包 + 高活跃上游**，
脱离 pacman 管理的代价高 → 改用本地 PKGBUILD 包：
- 包名 `nvtop-zh`，`conflicts=(nvtop)`，`provides=(nvtop)`
- 源码用本地 fork（`file:///home/mwh/github/forked/nvtop#branch=chinese-i18n`）
- 装完 `pacman -Qi nvtop-zh` 可见，卸载干净
- 上游更新需手动重编（不会自动跟进）

### PKGBUILD 踩坑
1. **srcdir 目录名**：`source=("$pkgname-$pkgver::git+...")` 解包成 `nvtop-zh-3.3.2/`，
   但 `build()` 里 `cd "$srcdir/nvtop-zh"` 会失败 → 需用 `$pkgname-$pkgver` 或变量。
2. **残留 build 缓存**导致 CMake 报错：`rm -rf src build pkg` 后重跑即可。

### 文件位置
```
~/github/forked/nvtop/          源码（分支 chinese-i18n，已推送）
  hanhua/map/dict_setup.py      设置窗口词典
  hanhua/map/dict_main.py       主界面/CLI 词典
  hanhua/map/apply.py           替换脚本（dry-run 优先）
  hanhua/map/fix_nvtop_cli.py   helpstring 整块替换专用
  hanhua/pkg/PKGBUILD           打包脚本副本
~/github/forked/nvtop-pkg/      打包目录（makepkg 工作区）
```

### 待办
- [ ] 安装：`cd ~/github/forked/nvtop-pkg && sudo pacman -U nvtop-zh-3.3.2-1-x86_64.pkg.tar.zst`
- [ ] 安装后实测 `nvtop` 命令
- [ ] 写知识库
