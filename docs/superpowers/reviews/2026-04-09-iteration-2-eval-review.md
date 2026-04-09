# Iteration 2 评测复盘

日期：2026-04-09

## 评测范围

- `role-skill-creator`
- `role-skill-improver`

对每个 skill 执行 with-skill 与 without-skill 对照，记录 `grading.json` 与 `timing.json`。

## 结果目录

- `evals/workspace/iteration-2/eval-role-skill-creator/with_skill/`
- `evals/workspace/iteration-2/eval-role-skill-creator/without_skill/`
- `evals/workspace/iteration-2/eval-role-skill-improver/with_skill/`
- `evals/workspace/iteration-2/eval-role-skill-improver/without_skill/`
- 汇总：
  - `evals/workspace/iteration-2/benchmark.json`
  - `evals/workspace/iteration-2/aggregate-from-script.json`

## 核心结论

1. with-skill 在本轮结构断言中通过率显著高于 baseline。
2. with-skill 代价更高（耗时与 token 均增加），但换来更稳定的结构输出。
3. 当前评测更偏“结构符合性”，下一轮应加入“任务有效性”断言。

## 下一轮建议

1. 为每个 case 增加至少一条“内容质量”断言（不仅章节存在）。
2. 引入人工盲评字段，对可读性和可执行性打分。
3. 扩展到两个角色模板 skill 的对照评测，形成全链路数据。
