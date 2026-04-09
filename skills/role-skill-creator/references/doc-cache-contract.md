# 目标仓库内文档缓存约定

与规格一致：默认根目录为 `<repo-root>/docs/agent-skill-cache/`（可由 `doc_output_root` 覆盖）。

## 必备文件

| 文件 | 用途 |
|------|------|
| `INDEX.md` | 人类与 Agent 导航：主题、模块入口、阅读顺序 |
| `manifest.json` | 机器可读：`schema_version`、`generated_at`、各条目路径、摘要、`source_paths` |

## manifest 建议字段（首版）

- `schema_version`：字符串，如 `"1"`
- `generated_at`：ISO 8601 时间
- `repo`：仓库别名或路径标识（与 `repo_aliases` 对齐）
- `doc_root`：相对仓库根的路径，如 `docs/agent-skill-cache`
- `entries`：数组，元素含 `path`、`title`、`summary`、`tags`、`source_paths`

## 幂等

重复运行应更新 `generated_at` 与条目内容，避免重复追加相同章节。

## 敏感信息

- 不写入 `.env`、私钥、token 原文。
- 若从代码推断出敏感配置位置，仅写「见某路径，需人工确认」，不抄录值。
