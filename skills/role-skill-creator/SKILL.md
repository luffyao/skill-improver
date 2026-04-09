---
name: role-skill-creator
description: 为任意项目生成角色化 Agent Skill。支持多仓库；在目标仓库文档稀疏时可自动在仓库内生成 docs/agent-skill-cache（INDEX.md 与 manifest.json）并写入角色 skill 的查询指针。适用于架构师或高级开发者等角色 skill。
---

# Role Skill Creator

## 何时使用

在以下场景激活本 Skill：

- 用户希望为某个项目创建“架构师”“高级开发者”等角色 Skill
- 目标项目可能由多个仓库组成，需要跨仓分析
- 用户要求输出可复用的 `SKILL.md`，而不是一次性建议

## 输入参数

最少需要：

- `target_repo_paths`: 目标仓库路径数组（至少 1 个）
- `target_role`: 角色名（如 `architect`、`senior-developer`）

可选参数：

- `repo_aliases`: 与仓库路径一一对应的短名
- `repo_priority`: 仓库优先级（仅在用户指定“可自动决策”时参考）
- `depth_mode`: `light` | `standard` | `deep` | `adaptive`（默认 `adaptive`）
- `constraints`: 额外约束（如只读、输出格式限制等）
- `doc_bootstrap`: 布尔，默认 `true`。为 `false` 或 `constraints` 含 `skip-doc-bootstrap` 时，**不**在目标仓库写盘生成缓存文档。
- `doc_output_root`: 字符串，可选。默认 `docs/agent-skill-cache`（相对**该仓库根**的路径）。
- `doc_output_roots`: 对象，可选。键为 `target_repo_paths` 中的绝对路径，值为该仓的相对输出根（覆盖默认）。

参数示例：

```json
{
  "target_repo_paths": [
    "/path/to/repo-a",
    "/path/to/repo-b"
  ],
  "repo_aliases": {
    "/path/to/repo-a": "backend",
    "/path/to/repo-b": "platform"
  },
  "target_role": "architect",
  "depth_mode": "adaptive",
  "constraints": [
    "only-read-analysis"
  ]
}
```

## 按需读取参考资料

- 在校验输入字段前，读取 `references/input-schema.md`。
- 检测到多仓库冲突后，读取 `references/conflict-report-template.md` 组织输出。
- 需要快速生成冲突报告骨架时，可运行 `scripts/generate_conflict_report.py`。
- 若启用文档缓存写盘，读取 `references/doc-cache-contract.md`，保证 `INDEX.md` / `manifest.json` 符合约定。

## 默认流程

1. 读取 `references/input-schema.md`，验证输入参数与仓库路径可访问性。
2. 对每个仓库提取项目事实（文档、入口、模块边界、测试与构建信息）。
3. **文档稀疏检测与缓存（doc bootstrap）**  
   - 若 `doc_bootstrap` 为 `false` 或 `constraints` 含 `skip-doc-bootstrap`：**跳过写盘**，仅可在输出中说明缺口。  
   - 否则对每个仓库做稀疏度启发式（如 README 缺/过短、无有效 `docs/` 等）。  
   - 命中且允许写盘时：在**该仓库根下** `doc_output_root`（默认 `docs/agent-skill-cache/`）生成 `INDEX.md` 与 `manifest.json`（详见 `references/doc-cache-contract.md`）；轻量整理代码结构信息，不替代正式文档。  
   - 多仓库时每个仓库独立一套目录；路径用 `doc_output_roots` 按仓覆盖。  
   - 写盘失败（权限等）须报错并说明，避免部分成功导致不一致。
4. 构建跨仓关系图（依赖、调用、共享契约）。
5. 检查冲突（命名冲突、接口不一致、版本漂移、职责重叠）。
6. 若存在冲突，读取 `references/conflict-report-template.md`，输出“冲突清单 + 影响 + 候选处理方式”，等待用户确认。
7. 生成目标角色 Skill：
   - `SKILL.md`（含 **项目文档缓存** 指针，见下方输出模板）
   - 最小 `evals/evals.json`
8. 输出改进建议，提示可用 `role-skill-improver` 继续迭代。

## 冲突策略（强约束）

多仓库冲突时默认策略：

- 不自动定夺
- 先提示冲突，再由用户确认

除非用户明确授权自动决策，否则不得跳过该步骤。

## 自适应深度规则

当 `depth_mode=adaptive`：

- 默认按 `standard` 执行
- 命中以下任一条件升级到 `deep`：
  - 涉及跨仓关键契约变更
  - 涉及安全、数据一致性、并发、发布高风险
  - 文档不足且结构复杂（若已执行 doc bootstrap，可引用缓存目录中的证据）

升级后输出必须包含：

- 证据来源（按仓库标注）
- 风险分级
- 验证计划
- 回滚建议

## 输出结构（建议模板）

输出至少包含以下部分：

1. `Role Definition`
2. `Project Facts by Repository`
3. `Cross-Repo Dependencies`
4. `Conflicts and Open Decisions`
5. `Generated Skill Content`（其中生成的角色 `SKILL.md` 正文须包含 **项目文档缓存** 小节：按仓库列出相对路径，如 `docs/agent-skill-cache/INDEX.md`，并说明回答架构/模块问题前优先按需读取 `INDEX` 或 `manifest.json`；勿把整份摘要塞进角色 skill 正文）
6. `Validation Checklist`

## 质量检查清单

- [ ] `SKILL.md` 的 `name` 合法且与目录名一致
- [ ] `description` 同时包含“做什么 + 何时使用”
- [ ] 明确默认流程与禁区
- [ ] 多仓库冲突策略已写明
- [ ] 若启用 doc bootstrap：目标仓内存在 `INDEX.md` 与 `manifest.json`（路径符合约定），且角色 skill 含可解析引用
- [ ] 提供最小评测样例
