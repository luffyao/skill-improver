# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Helper Scripts
Generate conflict report from multiple repositories:
```bash
python3 skills/role-skill-creator/scripts/generate_conflict_report.py --repos /path/to/repo1 /path/to/repo2 --output evals/workspace/iteration-x/conflict-report.json
```

Bootstrap doc cache skeleton under a target repo (INDEX, manifest, entries):
```bash
python3 skills/role-skill-creator/scripts/bootstrap_doc_cache.py --repo /path/to/target-repo
```

Aggregate evaluation statistics:
```bash
python3 skills/role-skill-improver/scripts/aggregate_eval_stats.py --workspace evals/workspace/iteration-x --output evals/workspace/iteration-x/benchmark.json
```

## Project Overview

This is a **role-based Agent Skill development system** for creating, optimizing, and evaluating specialized AI agent skills for software engineering tasks. It supports multi-repository project analysis and intelligent agent role specialization.

### Core Skills

- `skills/role-skill-creator`: Creates new role skills from target repositories (supports multi-repo analysis)
- `skills/role-skill-improver`: Optimizes existing skills based on evaluation and feedback
- `skills/project-architect-role-template`: Pre-built template for project architect role
- `skills/senior-software-developer-role-template`: Pre-built template for senior developer role

## Architecture

### Directory Structure

```
skill-improver/
├── skills/                     # All skill implementations
│   └── <skill-name>/
│       ├── SKILL.md            # Required: YAML frontmatter + skill instructions
│       ├── scripts/            # Optional: helper scripts
│       ├── references/         # Optional: templates and references
│       └── evals/evals.json    # Test cases and assertions
├── evals/                      # Evaluation suites and results
│   ├── multi-repo-conflicts/   # Multi-repo conflict evaluation tests
│   └── workspace/              # Iteration evaluation results
└── docs/                       # Documentation and design materials
```

### Core Principles

1. **Separation of Concerns**: Creator handles skill creation from scratch, Improver handles optimization of existing skills
2. **Multi-repository Support**: First-class support for analyzing multiple code repositories simultaneously
3. **Adaptive Depth**: Intelligently adjusts analysis depth based on project complexity and risk
4. **Conflict Resolution**: Explicit conflict detection requires user confirmation before making decisions
5. **Evaluation-Driven**: All improvements are measured against standardized test cases

### SKILL.md Format Standards

Each skill must have:
- **YAML frontmatter**: Required fields: `name`, `description`
- **Trigger conditions**: When the skill should be invoked
- **Input parameters**: Documented expected inputs
- **Step-by-step workflow**: Clear execution sequence
- **Output requirements**: Expected output format
- **Safety constraints**: Guardrails for proper usage
- **Quality checklist**: Verification steps before completion

## 文档同步要求（必读）

本仓库**需求或行为有任何变更**时，必须在交付实现的同时，**同步更新所有受影响的文档**，避免代码与说明脱节。

1. **用户入口**：`README.md` — 新参数、新脚本、新目录约定、新使用流程，凡影响「怎么用这个仓库」的，都要有对应说明或命令示例。
2. **技能契约**：受影响的 `skills/<name>/SKILL.md`，以及 `references/`、`evals/evals.json`（若行为、输入、断言或评测场景变化）。
3. **设计与规格**：若变更涉及约定或架构，更新或新增 `docs/superpowers/specs/` 下相关规格；必要时更新 `docs/superpowers/plans/` 与复盘类文档。
4. **本文件**：若工作流或原则变化，更新 `CLAUDE.md`。

**自检**：合并前自问 — 若新同事只读 README 能否完成新能力？评测与技能描述是否仍一致？

## Key Documentation

- `README.md`: Quick start guide and core concepts
- `docs/quickstart.md`: Step-by-step usage instructions
- `docs/specification.md`: Formal SKILL.md format specification
- `docs/best-practices.md`: Guidelines for high-quality skill development
- `docs/evaluating-skills.md`: Testing and measurement methodology
- `docs/superpowers/specs/2026-04-09-role-skill-system-design.md`: Full system design
- `docs/superpowers/specs/2026-04-10-doc-bootstrap-for-role-skill-creator-design.md`: Doc cache (doc bootstrap) specification
- `docs/superpowers/plans/2026-04-09-role-skill-system-implementation-plan.md`: Implementation roadmap

## Workflow

Typical development workflow:

1. **Create**: Use `role-skill-creator` to generate a new skill from 1~N target repositories
2. **Evaluate**: Run test cases to measure performance
3. **Optimize**: Use `role-skill-improver` to improve based on evaluation results
4. **Repeat**: Iterate until quality metrics meet thresholds

Common evaluation tasks are in `evals/multi-repo-conflicts/` for testing conflict detection.
