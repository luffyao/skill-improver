# Agent Skills 文档指南

这个目录整理了 [agentskills.io](https://agentskills.io/home) 中与 `SKILL` 相关的核心文档，面向两类读者：

- **Skill 作者**：编写高质量 `SKILL.md`
- **Agent 开发者**：在产品中实现 Skills 支持

---

## 先看这里

- 想快速上手：读 `quickstart.md`
- 想对齐规范：读 `specification.md`
- 想在 Agent 中接入：读 `adding-skills-support.md`
- 想使用脚本能力：读 `using-scripts.md`
- 想做质量评估：读 `evaluating-skills.md`
- 想优化描述与指令：读 `best-practices.md`

> 说明：`optimizing-descriptions.md` 与 `best-practices.md` 内容高度重合，可作为补充参考。

---

## 你将学到什么

### 写对 Skill

- `SKILL.md` 的结构、字段与校验要求
- 如何定义清晰触发条件与边界
- 如何用“渐进披露”控制上下文成本

### 接入到 Agent

- 技能发现、解析、披露、激活、上下文管理完整流程
- 同名冲突、权限白名单、信任边界等实现细节

### 做到可复用

- 脚本设计规范（可执行、可观测、可解析）
- 评测闭环（用例、断言、评分、复盘、迭代）

---

## 推荐阅读路径

- **我是 Skill 作者**  
`quickstart` → `specification` → `best-practices` → `evaluating-skills`
- **我是 Agent 开发者**  
`adding-skills-support` → `specification` → `using-scripts` → `evaluating-skills`

---

## 来源

- Agent Skills 官方首页：[https://agentskills.io/home](https://agentskills.io/home)

