# role-skill-creator 输入规范

## 必填字段

- `target_repo_paths`：字符串数组，至少 1 项。每一项为可访问仓库路径。
- `target_role`：字符串，建议值：`architect`、`senior-developer`。

## 可选字段

- `repo_aliases`：对象，键为仓库路径，值为别名。
- `repo_priority`：字符串数组，按优先级从高到低排列。
- `depth_mode`：`light` | `standard` | `deep` | `adaptive`。
- `constraints`：字符串数组，用于附加约束。

## 校验规则

1. `target_repo_paths` 去重后长度必须 >= 1。
2. 如果提供 `repo_aliases`，键集合必须是 `target_repo_paths` 的子集。
3. 如果提供 `repo_priority`，元素必须都在 `target_repo_paths` 中。
4. `depth_mode` 为空时默认 `adaptive`。

## 示例

```json
{
  "target_repo_paths": [
    "/repo/api",
    "/repo/web",
    "/repo/data"
  ],
  "repo_aliases": {
    "/repo/api": "api",
    "/repo/web": "web",
    "/repo/data": "data"
  },
  "target_role": "architect",
  "depth_mode": "adaptive",
  "constraints": [
    "only-read-analysis"
  ]
}
```
