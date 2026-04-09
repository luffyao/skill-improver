#!/usr/bin/env python3
"""
Aggregate pass/fail statistics from grading.json files.
"""

import argparse
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="聚合 grading.json 的通过率统计。"
    )
    parser.add_argument(
        "--workspace",
        required=True,
        help="包含多轮迭代结果的目录路径。",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="聚合结果输出文件路径。",
    )
    return parser.parse_args()


def collect_grading_files(workspace: Path):
    return list(workspace.rglob("grading.json"))


def aggregate(files):
    totals = {"passed": 0, "failed": 0, "total": 0}
    per_file = []
    for f in files:
        with f.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        summary = data.get("summary", {})
        passed = int(summary.get("passed", 0))
        failed = int(summary.get("failed", 0))
        total = int(summary.get("total", passed + failed))
        totals["passed"] += passed
        totals["failed"] += failed
        totals["total"] += total
        per_file.append(
            {
                "file": str(f),
                "passed": passed,
                "failed": failed,
                "total": total,
            }
        )
    pass_rate = (totals["passed"] / totals["total"]) if totals["total"] else 0.0
    return {"totals": totals, "pass_rate": pass_rate, "files": per_file}


def main():
    args = parse_args()
    workspace = Path(args.workspace)
    files = collect_grading_files(workspace)
    result = aggregate(files)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
        fp.write("\n")
    print(f"Aggregated {len(files)} grading files into {output}")


if __name__ == "__main__":
    main()
