#!/usr/bin/env python3
"""带货分镜自检：镜头数、时长、钩子、CTA、禁词、AI 标识。

用法：
    python commerce_check.py storyboard.md --product "阔腿裤" --platform tiktok
    python commerce_check.py storyboard.md --json
"""
import argparse
import json
import re
import sys
from pathlib import Path

SHOT = re.compile(r"^\s*S(\d{2,3})\s*\|")
TIME = re.compile(r"(\d+(?:\.\d+)?)\s*[-–~]\s*(\d+(?:\.\d+)?)\s*s")
CTA_WORDS = ["点左下角", "点小黄车", "购物车", "shop now", "点下方", "点击", "link", "buy now", "加购"]
BANNED = [
    "最好", "第一", "顶级", "极致", "唯一", "国家级", "王牌",
    "保证", "100%", "永久", "根治", "彻底解决", "治疗", "治愈", "疗效", "消炎", "杀菌",
    "全网最低", "史上最",
]
AI_MARK = ["ai生成", "ai 生成", "数字人", "ai-generated", "ai标识"]


def parse(text):
    shots = []
    for line in text.splitlines():
        if not SHOT.match(line):
            continue
        parts = [p.strip() for p in line.split("|")]
        end = None
        m = TIME.search(line)
        if m:
            end = float(m.group(2))
        shots.append({"line": line.strip(), "parts": parts, "end": end})
    return shots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--product", default="")
    ap.add_argument("--platform", default="tiktok", choices=["tiktok", "douyin", "xhs", "video"])
    ap.add_argument("--max-shots", type=int, default=6)
    ap.add_argument("--max-seconds", type=float, default=15.0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-no-ai-mark", action="store_true")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    shots = parse(text)
    errors, warnings = [], []

    if not shots:
        errors.append("没有解析到镜头行（格式：S01 | 0-2s | 景别 | 画面 | 台词 | 任务）")

    if len(shots) > args.max_shots:
        errors.append(f"镜头数 {len(shots)} 超过上限 {args.max_shots}")

    ends = [s["end"] for s in shots if s["end"] is not None]
    total = max(ends) if ends else None
    if total is None:
        warnings.append("未解析到时间范围（如 0-2s），无法核算总时长")
    elif total > args.max_seconds:
        errors.append(f"总时长 {total:g}s 超过上限 {args.max_seconds:g}s")

    if shots:
        first = shots[0]["line"]
        if args.product and args.product not in first:
            errors.append(f"第一镜没有出现产品「{args.product}」——钩子必须与产品相关")
        last = shots[-1]["line"].lower()
        if not any(w.lower() in last for w in CTA_WORDS):
            errors.append("最后一镜缺少 CTA（点左下角/小黄车/购物车/Shop now）")

    hits = [w for w in BANNED if w in text]
    if hits:
        errors.append("发现禁用词：" + "、".join(hits))

    if not args.allow_no_ai_mark:
        low = text.lower()
        if not any(m in low for m in AI_MARK):
            warnings.append("未看到 AI 生成/数字人标识（如平台要求，请补）")

    result = {
        "file": args.file,
        "platform": args.platform,
        "shots": len(shots),
        "total_seconds": total,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"文件：{args.file}")
        print(f"镜头：{len(shots)}  总时长：{total if total is not None else '未解析'}")
        if errors:
            print("\n[必须修]")
            for e in errors:
                print(" -", e)
        if warnings:
            print("\n[建议]")
            for w in warnings:
                print(" -", w)
        print("\n结果：" + ("通过" if not errors else "不通过"))

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
