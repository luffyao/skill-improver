#!/usr/bin/env python3
"""
Generate a skeleton conflict report JSON for multi-repo projects.
"""

import argparse
import json
from datetime import date


def parse_args():
    parser = argparse.ArgumentParser(
        description="生成多仓库冲突报告骨架（JSON）。"
    )
    parser.add_argument(
        "--repos",
        nargs="+",
        required=True,
        help="仓库路径列表，至少一个。",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="输出 JSON 文件路径。",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    report = {
        "generated_at": str(date.today()),
        "repos": args.repos,
        "summary": {
            "conflict_count": 0,
            "risk_level": "unknown"
        },
        "conflicts": [],
        "open_decisions": []
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote conflict report skeleton to {args.output}")


if __name__ == "__main__":
    main()
