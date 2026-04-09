#!/usr/bin/env python3
"""
在目标仓库根下生成文档缓存骨架：INDEX.md、manifest.json，以及 entries/ 下按顶层目录拆分的占位 md。
符合 references/doc-cache-contract.md 的约定。
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIR_NAMES = {
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    "target",
    ".idea",
    ".cargo",
    ".nox",
    ".tox",
    "eggs",
    ".eggs",
}

MAX_ENTRIES = 80


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\-.]+", "_", name, flags=re.UNICODE)
    s = s.strip("._") or "entry"
    return s[:120]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="在目标仓库内生成 docs/agent-skill-cache 骨架（INDEX、manifest、entries）。",
    )
    p.add_argument(
        "--repo",
        required=True,
        help="目标仓库根目录（绝对或相对路径）。",
    )
    p.add_argument(
        "--doc-root",
        default="docs/agent-skill-cache",
        help="相对仓库根的输出目录，默认 docs/agent-skill-cache。",
    )
    p.add_argument(
        "--repo-label",
        default="",
        help="写入 manifest 的 repo 字段，默认使用仓库目录名。",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将写入的路径，不写文件。",
    )
    return p.parse_args()


def collect_top_level(repo: Path) -> list[Path]:
    out: list[Path] = []
    if not repo.is_dir():
        raise SystemExit(f"Error: --repo 不是目录: {repo}")
    for child in sorted(repo.iterdir(), key=lambda p: p.name.lower()):
        if child.name in SKIP_DIR_NAMES:
            continue
        if child.is_dir():
            out.append(child)
    return out[:MAX_ENTRIES]


def build_manifest(
    repo: Path,
    doc_root: str,
    repo_label: str,
    dirs: list[Path],
) -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries = []
    for d in dirs:
        rel = d.relative_to(repo).as_posix()
        slug = slugify(d.name)
        md_rel = f"entries/{slug}.md"
        entries.append(
            {
                "path": md_rel,
                "title": d.name,
                "summary": f"待补充：基于源码目录 `{rel}/` 梳理职责与对外接口。",
                "tags": ["auto", "top-level-dir"],
                "source_paths": [rel],
            }
        )
    return {
        "schema_version": "1",
        "generated_at": now,
        "repo": repo_label or repo.name,
        "doc_root": doc_root.strip("/").replace("\\", "/"),
        "entries": entries,
    }


def render_index(doc_root: str, manifest: dict) -> str:
    lines = [
        "# Agent Skill 文档缓存（自动生成骨架）",
        "",
        f"- 生成时间（UTC）：{manifest['generated_at']}",
        f"- 仓库标识：`{manifest['repo']}`",
        "- 说明：以下为目录结构占位，请结合源码补充细节；敏感信息勿写入。",
        "",
        "## 导航",
        "",
    ]
    for e in manifest["entries"]:
        title = e["title"]
        path = e["path"]
        lines.append(f"- [{title}]({path})")
    lines.extend(
        [
            "",
            "## manifest",
            "",
            "机器可读索引见同目录 `manifest.json`。",
            "",
        ]
    )
    return "\n".join(lines)


def stub_md(entry: dict) -> str:
    paths = ", ".join(f"`{p}`" for p in entry.get("source_paths", []))
    return "\n".join(
        [
            f"# {entry['title']}",
            "",
            entry["summary"],
            "",
            f"**关联源码路径：** {paths}",
            "",
            "## 待补充",
            "",
            "- 模块职责与边界",
            "- 主要入口与依赖",
            "- 风险与注意事项",
            "",
        ]
    )


def main() -> None:
    args = parse_args()
    repo = Path(args.repo).resolve()
    doc_root_rel = args.doc_root.strip().replace("\\", "/").strip("/")
    out_base = repo / doc_root_rel
    label = args.repo_label.strip() or repo.name

    dirs = collect_top_level(repo)
    manifest = build_manifest(repo, doc_root_rel, label, dirs)

    if args.dry_run:
        print(f"Would write under {out_base}:")
        print(f"  - INDEX.md")
        print(f"  - manifest.json ({len(manifest['entries'])} entries)")
        for e in manifest["entries"]:
            print(f"  - {e['path']}")
        return

    entries_dir = out_base / "entries"
    entries_dir.mkdir(parents=True, exist_ok=True)

    for e in manifest["entries"]:
        p = out_base / e["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(stub_md(e), encoding="utf-8")

    index_text = render_index(doc_root_rel, manifest)
    (out_base / "INDEX.md").write_text(index_text, encoding="utf-8")

    with (out_base / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote doc cache skeleton under {out_base}")


if __name__ == "__main__":
    main()
