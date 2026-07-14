#!/usr/bin/env python3
"""Deterministic style checks for lao-ban-script-writer drafts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BANNED_PHRASES = (
    "在当今时代",
    "值得注意的是",
    "综上所述",
    "让我们一起探索",
    "赋能",
    "闭环",
    "价值抓手",
    "震惊",
    "干货满满",
    "看完秒懂",
)

TRANSITION_LIMITS = {
    "其实": 4,
    "这个时候": 4,
    "这种情况": 4,
    "所以呢": 3,
    "然后呢": 3,
}


def read_text(path: str | None) -> str:
    if not path or path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def lint(text: str) -> list[str]:
    issues: list[str] = []

    contrast_count = len(
        re.findall(r"不是[^。！？\n]{0,60}(?:，|,)?\s*而是", text)
    )
    if contrast_count > 1:
        issues.append(
            f"“不是……而是……”近似结构出现 {contrast_count} 次，全文最多 1 次"
        )

    for phrase in BANNED_PHRASES:
        count = text.count(phrase)
        if count:
            issues.append(f"禁用表达“{phrase}”出现 {count} 次")

    for phrase, limit in TRANSITION_LIMITS.items():
        count = text.count(phrase)
        if count > limit:
            issues.append(f"转场词“{phrase}”出现 {count} 次，建议不超过 {limit} 次")

    if all(token in text for token in ("首先", "其次", "最后")):
        issues.append("同时使用“首先、其次、最后”，检查是否套回机械三段式")

    exclamation_count = text.count("！") + text.count("!")
    if exclamation_count > 5:
        issues.append(f"感叹号出现 {exclamation_count} 次，强势感不要依赖标点")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="UTF-8 draft file; omit or use - for stdin")
    args = parser.parse_args()

    try:
        text = read_text(args.path)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    issues = lint(text)
    if issues:
        print("FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
