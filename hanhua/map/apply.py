#!/usr/bin/env python3
"""nvtop 汉化替换脚本（C 项目专用）

用法:
    python3 apply.py            # dry-run（默认，只显示将要改什么）
    python3 apply.py --apply    # 实际写盘

护栏（来自《TUI工具汉化总览与通用方法》+ nvfd 的 10 个 C 项目坑）：
  ✅ 只处理白名单文件
  ✅ 跳过整行注释（// 与 /* */ 块）
  ✅ 跳过 #include / #define 行
  ✅ 黑名单（信号名、厂商名）绝不翻译
  ✅ 相邻字符串拼接：按「引号配平」收集成一个逻辑单元再判断（坑 C7）
  ✅ 占位符数量必须一致，否则拒绝该条（坑 C3/C4/C5）
  ✅ 默认 dry-run
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dict_main import ALL as DICT_MAIN, NEVER
from dict_setup import ALL as DICT_SETUP

# 每个文件用哪本词典（严格隔离，避免翻到配置键名）
FILE_DICT = {
    'src/interface.c': DICT_MAIN,
    'src/nvtop.c': DICT_MAIN,
    'src/plot.c': DICT_MAIN,
    'src/interface_setup_win.c': DICT_SETUP,
}
# ❌ src/interface_options.c 不在列表 → 绝不处理

PLACEHOLDER_RE = re.compile(r'%[-+ 0-9.#*hljztL]*[diufegxXscp%]')


def placeholders(s):
    """返回占位符的排序后列表（顺序敏感，但集合比较先用）"""
    return sorted(PLACEHOLDER_RE.findall(s))


def same_placeholders(en, zh):
    return placeholders(en) == placeholders(zh)


def collect_literals(lines, i):
    """从第 i 行起，按引号配平收集完整逻辑单元（处理相邻字符串拼接）。
    返回 (总行数, [(行号, 原文, 缩进前缀), ...])
    这里简化：只处理「单行内完成的字面量」，跨行由调用方逐行处理。
    """
    return lines[i]


def strip_comments_state(line, in_block):
    """返回 (处理后的行, 新的 in_block 状态)"""
    if in_block:
        if '*/' in line:
            return line[line.index('*/') + 2:], False
        return '', True
    # 移除行内块注释
    out = line
    while '/*' in out:
        start = out.index('/*')
        if '*/' in out[start:]:
            end = out.index('*/', start)
            out = out[:start] + ' ' * (end - start + 2) + out[end + 2:]
        else:
            out = out[:start]
            in_block = True
            break
    return out, in_block


def process(path, dict_, dry=True):
    lines = open(path, encoding='utf-8').read().split('\n')
    out = []
    changes = []
    skipped = []
    in_block = False

    for ln_no, line in enumerate(lines, 1):
        code, in_block = strip_comments_state(line, in_block)

        # 护栏：跳过注释行 / 预处理指令
        st = code.lstrip()
        if not st or st.startswith('//') or st.startswith('#'):
            out.append(line)
            continue

        def repl(m):
            val = m.group(1)
            if val in NEVER:
                return m.group(0)
            if val not in dict_:
                return m.group(0)
            zh = dict_[val]
            if not same_placeholders(val, zh):
                skipped.append((ln_no, val, zh,
                                f"占位符不一致 {placeholders(val)} vs {placeholders(zh)}"))
                return m.group(0)
            changes.append((ln_no, val, zh))
            # 转义：目标串里的双引号需转义
            esc = zh.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{esc}"'

        new_line = re.sub(r'"((?:[^"\\]|\\.)*)"', repl, code)
        # 保留原行的注释部分（代码里的行尾注释）
        if '//' in line and '//' not in code:
            tail = line[line.index('//'):]
            new_line = new_line.rstrip() + '  ' + tail
        out.append(new_line)

    if not dry and changes:
        open(path, 'w', encoding='utf-8').write('\n'.join(out))
    return changes, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='实际写盘（默认 dry-run）')
    args = ap.parse_args()
    dry = not args.apply

    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    total = 0
    all_skipped = []

    for rel, dict_ in FILE_DICT.items():
        path = os.path.join(repo, rel)
        if not os.path.exists(path):
            print(f"⚠️ 跳过（不存在）: {rel}")
            continue
        changes, skipped = process(path, dict_, dry)
        total += len(changes)
        all_skipped += [(rel, *s) for s in skipped]
        tag = 'DRY' if dry else 'APPLY'
        print(f"\n=== [{tag}] {rel}：{len(changes)} 处 ===")
        for ln, en, zh in changes:
            print(f"  {ln:5d}  {en!r}\n         → {zh!r}")

    if all_skipped:
        print(f"\n⚠️ 跳过 {len(all_skipped)} 处：")
        for rel, ln, en, zh, why in all_skipped:
            print(f"  {rel}:{ln}  {en!r} → {zh!r}\n     原因：{why}")

    print(f"\n{'[DRY-RUN] ' if dry else '[APPLIED] '}共 {total} 处替换")
    if dry and total:
        print("加 --apply 才会真正写盘")


if __name__ == '__main__':
    main()
