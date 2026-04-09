# skill-improver

用于创建与优化“角色化 Agent Skill”的仓库，面向任意外部项目（支持多仓库输入）。

## 已提供的 Skills

- `skills/role-skill-creator`：创建角色 Skill（支持多仓库）
- `skills/role-skill-improver`：优化已有角色 Skill
- `skills/project-architect-role-template`：架构师模板
- `skills/senior-software-developer-role-template`：高级开发者模板

## Skill 使用

### 最小使用流程（3 步）

1. 准备目标仓库路径（单仓或多仓）。
2. 用 `role-skill-creator` 生成目标角色 Skill（建议先用 `architect` 或 `senior-developer`）。
3. 用 `role-skill-improver` 基于评测与反馈做一轮优化，并复跑 `evals`。

如果是第一次使用，建议先从单仓库开始，确认输出结构稳定后再扩展到多仓库。

### 1) 创建角色 Skill（creator）

适用：你有 1~N 个目标仓库，希望生成可复用的角色 Skill。

建议输入参数（示例）：

```json
{
  "target_repo_paths": [
    "/path/to/repo-api",
    "/path/to/repo-web"
  ],
  "repo_aliases": {
    "/path/to/repo-api": "api",
    "/path/to/repo-web": "web"
  },
  "target_role": "architect",
  "depth_mode": "adaptive",
  "constraints": [
    "only-read-analysis"
  ]
}
```

输出重点：

- 生成目标角色 `SKILL.md`
- 多仓库事实与依赖梳理
- 冲突清单与待确认决策（默认不自动定夺）
- **文档稀疏时**：可在各目标仓库内生成 `docs/agent-skill-cache/`（`INDEX.md` + `manifest.json`），并在角色 skill 中写入**相对路径指针**供后续查询；可用 `doc_bootstrap: false` 或 `constraints` 含 `skip-doc-bootstrap` 关闭写盘

规格说明：`docs/superpowers/specs/2026-04-10-doc-bootstrap-for-role-skill-creator-design.md`

### 2) 优化已有 Skill（improver）

适用：已有角色 Skill 触发不准、输出不稳、步骤冗余或成本偏高。

建议输入材料（至少一种）：

- `evals` 断言结果
- 执行轨迹摘要
- 人工反馈
- 与 baseline 的对照结果

优化优先级：

1. `description`（触发准确率）
2. 流程指令（步骤依赖、验收门槛）
3. `gotchas`（常见误判）
4. 输出模板（结构稳定）

### 3) 使用预置角色模板

- 架构师模板：`skills/project-architect-role-template`
- 高级开发模板：`skills/senior-software-developer-role-template`

可直接作为新项目起点，再用 `role-skill-improver` 做迭代收敛。

### 4) 评测与脚本

生成冲突报告骨架：

```bash
python3 skills/role-skill-creator/scripts/generate_conflict_report.py \
  --repos /repo/api /repo/web \
  --output evals/workspace/iteration-x/conflict-report.json
```

聚合评测结果：

```bash
python3 skills/role-skill-improver/scripts/aggregate_eval_stats.py \
  --workspace evals/workspace/iteration-x \
  --output evals/workspace/iteration-x/benchmark.json
```

## 常见错误与排查

- **`target_repo_paths` 无效或为空**
  - 现象：creator 无法建立项目事实。
  - 排查：确认路径存在、可访问，并且数组至少 1 项。

- **多仓库冲突被“自动决策”**
  - 现象：输出直接给唯一方案，没有待确认决策。
  - 排查：检查 creator 输出是否包含 `Conflicts and Open Decisions`；若缺失，优先用 improver 强化冲突门控规则。

- **角色边界混淆（architect 与 senior developer 混用）**
  - 现象：架构任务输出实现细节过多，或实现任务变成泛架构建议。
  - 排查：检查 `description` 与输出模板是否聚焦角色职责；优先修正触发描述。

- **输出结构不稳定**
  - 现象：同类任务章节经常变化，评测断言波动大。
  - 排查：在 skill 中固定输出模板，并将评测断言改为“可判定项”（章节、字段、策略语句）。

- **聚合脚本结果异常（0 个 grading 文件）**
  - 现象：`aggregate_eval_stats.py` 输出 Aggregated 0 grading files。
  - 排查：确认 `--workspace` 指向包含 `grading.json` 的迭代目录结构。

## 设计文档

- `docs/superpowers/specs/2026-04-09-role-skill-system-design.md`
- `docs/superpowers/specs/2026-04-10-doc-bootstrap-for-role-skill-creator-design.md`
- `docs/superpowers/plans/2026-04-09-role-skill-system-implementation-plan.md`
- `docs/superpowers/reviews/2026-04-09-iteration-1-review.md`
- `docs/superpowers/reviews/2026-04-09-iteration-2-eval-review.md`

## 评测与辅助

- 多仓库冲突评测集：`evals/multi-repo-conflicts/evals.json`
- 首轮对照评测结果：`evals/workspace/iteration-2/`
- 冲突报告骨架脚本：`skills/role-skill-creator/scripts/generate_conflict_report.py`
- 评测聚合脚本：`skills/role-skill-improver/scripts/aggregate_eval_stats.py`
