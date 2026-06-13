# Multi-Agent Skills Factory

[English](#english) · [中文](#中文)

---

## English

### Overview

**Multi-Agent Skills Factory** packages enterprise SOP processes into reusable AI Skills through a 7-agent parallel pipeline. Skills self-improve after launch — errors trigger automatic reflection and iteration.

### Core Features

- **7-Agent pipeline**: Editor-in-Chief → Researcher + Designer (parallel) → Developer → Tester → Reviewer → Iteration Optimizer
- **Score-gated launch**: Skill only goes live when ≥75/100 on five-dimensional review
- **Self-improving**: Built-in failure case log → self-review → SKILL.md update → regression testing
- **5 automation scripts**: validate / aggregate / package / run-loop / analyze-failures
- **+10 bonus points**: Self-iteration mechanism earns up to 10 extra points at review

### Agent Team

| Agent | Output | Responsibilities |
|-------|--------|------------------|
| Editor-in-Chief | Task scheduling + final delivery | Parse requirements, decompose tasks, coordinate agents, assemble output |
| Researcher | SOP analysis report | Deep understanding of business process, extract key nodes, identify edge cases |
| Designer | Skill design specification | Trigger word design, process modeling, input/output definition |
| Developer | SKILL.md code | Write code according to hermes-agent-skill-authoring standards |
| Tester | Test report | Syntax, functional, boundary, and security testing |
| Reviewer | Review report + grading.json | Five-dimensional scoring + self-iteration bonus |
| Iteration Optimizer | Failure analysis + improvement plan | Analyze failure_case_log.md, identify error patterns, drive self-improvement |

### Review Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 25% | Does the core process cover the complete SOP? |
| Correctness | 25% | Does the output meet hermes-agent-skill-authoring standards? |
| Usability | 20% | Are trigger words clear and usage simple? |
| Security | 20% | Any risk of sensitive information leakage? |
| Maintainability | 10% | Is the code structure clear, references/ organized? |
| **Self-Iteration Bonus** | **+10** | Error log + self-review + regression tests |

**Scoring Rules:**
- **≥90pts** Excellent — go live directly
- **75-89pts** Good — go live after minor fixes
- **<75pts** Return to developer, max 6 rounds

### Self-Improvement Mechanism

Generated skills have a built-in self-improvement loop that runs continuously after launch:

**Error Logging** → `references/failure_case_log.md`
Every usage error is recorded: trigger word, wrong output, expected output, root cause analysis.

**Self-Review Triggers** (any one):
- ≥5 unfixed errors in the log → auto-trigger iteration
- Same trigger word fails ≥3 times → immediate fix required
- User runs `/skill-xxx self-review`

**Iteration Flow:**
```
Error occurs → Logged to failure_case_log.md
                    ↓
         ≥5 unfixed OR recurring?
                    ↓ yes
         Iteration Optimizer Agent analyzes log
                    ↓
         generate P0/P1/P2 improvement plan
                    ↓
         Developer updates SKILL.md
                    ↓
         Tester runs regression tests
                    ↓
         Reviewer re-scores (checks self-iteration bonus)
                    ↓
         Pass → version bump → regression pool +1
```

### Trigger Words

**📦 Create** — build a skill from scratch:
- "Create a new skill for XX"
- "Build a skill that can do XX"
- "Develop a skill for XX"
- "Make a new skill"

**🎁 Package** — turn an existing workflow into a skill:
- "Package this process as a skill"
- "Turn this SOP into an AI skill"
- "Make this repetitive workflow into an automated skill"
- "Automate this workflow"

**🎨 Design** — design a skill for a scenario:
- "Design a skill for XX"
- "Plan an AI skill for XX"
- "What skill do I need for XX"

**🔧 Slash commands:**
- `/新建技能 [description]`
- `/封装技能 [description]`
- `/技能工厂 [description]`

### Automation Scripts

| Script | When to Run |
|--------|-------------|
| `scripts/validate_skill.py <SKILL.md>` | After Developer writes SKILL.md, before Test |
| `scripts/aggregate_score.py <iteration-dir>` | After each iteration completes |
| `scripts/package_skill.py <skill-dir>` | After Reviewer scores ≥75 |
| `scripts/run_loop.py <skill-name> <max-rounds>` | To control full iteration loop |
| `scripts/analyze_failures.py <skill-dir> --auto` | Check if self-iteration should trigger |
| `scripts/analyze_failures.py <skill-dir> --regression` | Generate regression test cases |
| `scripts/analyze_failures.py <skill-dir> --suggest` | Generate P0/P1/P2 improvement suggestions |

### Directory Structure

```
multi-agent-skills-factory/
├── SKILL.md                      ← Main entry (Editor-in-Chief)
├── scripts/
│   ├── __init__.py
│   ├── validate_skill.py         ← SKILL.md auto-validator (8 checks)
│   ├── aggregate_score.py        ← Multi-round review aggregator
│   ├── package_skill.py          ← Pack + update registry.yaml
│   ├── run_loop.py               ← Iteration loop controller (max 6 rounds)
│   └── analyze_failures.py       ← Error log analyzer (auto/suggest/regression)
└── references/
    ├── agents.md                 ← 7 agent templates (incl. Iteration Optimizer)
    ├── pipeline-multi-agent.md   ← Full pipeline guide for Editor-in-Chief
    ├── design-spec-template.md   ← Skill design spec template
    ├── eval-dimensions.md        ← Five dimensions + self-iteration bonus
    ├── test_pool.md              ← Test case pool (TC-SYNTAX/TC-FUNC/TC-BOUND/TC-SEC)
    ├── failure_case_log.md        ← Error case log (self-improvement core)
    └── self-review-template.md   ← Self-review flow template
```

---

## 中文

### 概述

**Multi-Agent Skills Factory** 通过 7 个专业 Agent 并行协作，将企业 SOP 流程封装为可复用的 AI Skill。上线后技能自动持续迭代——每一次错误都会触发自我复盘和增量更新。

### 核心特性

- **7个Agent流水线**：主编 → 研究员+设计师（并行）→ 开发者 → 测试员 → 评审员 → 迭代优化Agent
- **评分上线门控**：五维打分 <75 分不能上线，最多循环 6 轮
- **自我迭代**：错误日志 → 自我复盘 → SKILL.md 更新 → 回归测试
- **5 个自动化脚本**：验证/聚合/打包/循环/错误分析
- **评审加分项**：自我迭代机制运作良好可获得最高 +10 分加分

### Agent 团队

| Agent | 输出 | 职责 |
|-------|------|------|
| 主编 | 任务调度+最终交付 | 解析需求、分解任务、协调Agent、组装产出 |
| 研究员 | SOP分析报告 | 深度理解业务流程、提取关键节点、识别边界场景 |
| 设计师 | 技能设计规格书 | 触发词设计、流程建模、输入输出定义 |
| 开发者 | SKILL.md代码 | 按 hermes-agent-skill-authoring 标准编写代码 |
| 测试员 | 测试报告 | 语法验证、功能测试、边界测试、安全测试 |
| 评审员 | 评审报告+grading.json | 五维打分 + 自我迭代加分 |
| 迭代优化Agent | 错误分析+改进计划 | 分析 failure_case_log.md，识别错误模式，推动自我迭代 |

### 评审维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 完整性 | 25% | 核心流程是否覆盖完整SOP |
| 正确性 | 25% | 输出是否符合 hermes-agent-skill-authoring 标准 |
| 易用性 | 20% | 触发词是否清晰、使用是否简单 |
| 安全性 | 20% | 是否有敏感信息泄露风险 |
| 可维护性 | 10% | 代码结构是否清晰、references/ 是否规范 |
| **自我迭代加分** | **+10** | 错误日志 + 自我复盘 + 回归测试池 |

### 评分规则

- **≥90分** 优秀，直接上线
- **75-89分** 良好，小修小补后上线
- **<75分** 退回开发者修改，最多 6 轮

### 自我迭代机制

生成的技能具备上线后持续自我进化的能力：

**错误案例日志** → `references/failure_case_log.md`
每次使用出现错误时记录：触发词 | 错误输出 | 正确预期 | 根因分析

**迭代触发条件**（满足任一）：
- 未修复错误 ≥ 5 条 → 自动触发复盘
- 同一触发词出错 ≥ 3 次 → 立即修复复发性错误
- 用户手动 `/skill-xxx self-review` → 主编调度复盘流程

**迭代流程：**
```
错误发生 → 记录到 failure_case_log.md
                    ↓
         ≥5条未修复 或 复发性错误？
                    ↓ 是
         主编调度迭代优化Agent分析日志
                    ↓
         生成 P0/P1/P2 改进建议
                    ↓
         开发者更新 SKILL.md
                    ↓
         测试员执行回归测试
                    ↓
         评审员复评（检查自我迭代加分）
                    ↓
         通过 → 版本号升级 +1，回归测试池 +1
```

### 触发词

**📦 创建类** — 从零开始做技能：
- "新建一个技能"
- "创建一个技能来处理XX"
- "做一个能XX的技能"
- "搭建一个技能"
- "开发一个新技能"

**🎁 封装类** — 把已有流程变技能：
- "把这个流程封装成技能"
- "把这个SOP变成AI技能"
- "把重复的工作流做成自动化技能"
- "这个流程太重复了，做成技能"
- "把XX流程自动化"

**🎨 设计类** — 设计技能本身：
- "设计一个技能"
- "帮我设计个技能"
- "规划一个AI技能"
- "这个场景需要什么技能"

**🔧 快捷指令：**
- `/新建技能 [场景描述]`
- `/封装技能 [SOP描述]`
- `/技能工厂 [需求描述]`

### 自动化脚本

| 脚本 | 用途 |
|------|------|
| `scripts/validate_skill.py <SKILL.md>` | 开发者提交前自检（8项检查） |
| `scripts/aggregate_score.py <iteration-dir>` | 聚合多轮评审分数，生成 benchmark |
| `scripts/package_skill.py <skill-dir>` | 打包技能并更新 registry.yaml |
| `scripts/run_loop.py <skill-name> <max-rounds>` | 控制迭代循环（最多6轮） |
| `scripts/analyze_failures.py <skill-dir> --auto` | 检测是否触发自我迭代（≥5条=触发） |
| `scripts/analyze_failures.py <skill-dir> --regression` | 生成回归测试用例 |
| `scripts/analyze_failures.py <skill-dir> --suggest` | 生成优先级改进建议（P0/P1/P2） |

### 目录结构

```
multi-agent-skills-factory/
├── SKILL.md                      ← 主入口（主编调度）
├── scripts/
│   ├── __init__.py
│   ├── validate_skill.py         ← SKILL.md 自动验证（8项检查）
│   ├── aggregate_score.py       ← 多轮评审分数聚合
│   ├── package_skill.py          ← 打包 + 更新 registry.yaml
│   ├── run_loop.py               ← 迭代循环控制（最多6轮）
│   └── analyze_failures.py       ← 错误日志分析（自动迭代检测/回归测试/改进建议）
└── references/
    ├── agents.md                 ← 7个Agent模板（含迭代优化Agent）
    ├── pipeline-multi-agent.md   ← 主编调度手册（含上线后自我迭代流程图）
    ├── design-spec-template.md   ← 技能设计规格书模板
    ├── eval-dimensions.md        ← 五维评估 + 自我迭代加分规则
    ├── test_pool.md              ← 测试用例池（TC-SYNTAX/TC-FUNC/TC-BOUND/TC-SEC）
    ├── failure_case_log.md        ← 错误案例日志（自我迭代核心）
    └── self-review-template.md   ← 自我复盘流程模板
```

---

MIT License