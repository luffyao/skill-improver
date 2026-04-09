# 文档缓存（doc bootstrap）实现计划

日期：2026-04-10  
关联规格：`docs/superpowers/specs/2026-04-10-doc-bootstrap-for-role-skill-creator-design.md`

## 目标

在不大改仓库结构的前提下，将「文档稀疏时生成目标仓内缓存 + 角色 skill 指针」的行为写进 `role-skill-creator`，并扩展评测。

## 任务清单

1. 更新 `skills/role-skill-creator/SKILL.md`：输入、流程、输出模板、质量清单、frontmatter `description`。
2. 更新 `skills/role-skill-creator/references/input-schema.md`：新字段与校验规则。
3. 新增 `skills/role-skill-creator/references/doc-cache-contract.md`：INDEX/manifest 约定与敏感信息说明。
4. 扩展 `skills/role-skill-creator/evals/evals.json`：稀疏文档、关闭开关、skill 内引用。
5. 更新根目录 `README.md`：简要说明 doc bootstrap（可选一句）。

## 验收

- 执行 creator 流程时能按规格区分「写盘 / 跳过」。
- 生成的角色 skill 含「项目文档缓存」节及相对路径指针。
- eval 断言可判定。

## 非目标

- 本迭代不新增重型扫描脚本；仅文档与契约层面落地。
