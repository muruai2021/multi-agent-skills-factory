# Multi-Agent Skills Factory

[English](#english) | [中文](#中文)

---

## English

### Overview

**Multi-Agent Skills Factory** is an automated workflow that packages enterprise SOP processes into reusable Hermes Skills. Through an Editor-in-Chief orchestrating 6 specialized agents working in parallel, it achieves end-to-end transformation from business processes to AI skills.

**Core Features:**
- Editor-in-Chief intelligent scheduling, 7-agent parallel work
- Automated scoring iteration, only goes live when score ≥75
- **Self-improving skills**: built-in failure case log + self-review + regression testing
- 5 automation scripts (validate / aggregate / package / run-loop / analyze-failures)

### Agent Team

| Agent | Output | Responsibilities |
|-------|--------|------------------|
| Editor-in-Chief | Task scheduling + final delivery | Parse requirements, decompose tasks, coordinate agents, assemble output |
| Researcher | SOP analysis report | Deep understanding of business process, extract key nodes, identify edge cases |
| Designer | Skill design specification | Trigger word design, process modeling, input/output definition |
| Developer | SKILL.md code | Write code according to hermes-agent-skill-authoring standards |
| Tester | Test report | Syntax verification, functional testing, boundary testing, security testing |
| Reviewer | Review report + grading.json | Five-dimensional scoring (completeness/correctness/usability/security/maintainability) |
| Iteration Optimizer | Failure analysis + improvement plan | Analyze failure_case_log.md, identify error patterns, drive self-improvement |

### Review Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 25% | Does the core process cover the complete SOP? |
| Correctness | 25% | Does the output meet hermes-agent-skill-authoring standards? |
| Usability | 20% | Are trigger words clear and usage simple? |
| Security | 20% | Any risk of sensitive information leakage? |
| Maintainability | 10% | Is the code structure clear, references/ organized? |

**Scoring Rules:**
- **≥90pts** Excellent, go live directly
- **75-89pts** Good, go live after minor fixes
- **<75pts** Return to developer, max 6 rounds

### Trigger Words

- "Package this process as a Skill"
- "Build a skill for handling XX"
- "SOP is too repetitive, make it automated"
- `/packageSkill [SOP description]`
- `/封装Skill [SOP description]`

### Automation Scripts

| Script | Purpose |
|--------|---------|
| `scripts/validate_skill.py` | Auto-validate SKILL.md syntax, security, naming |
| `scripts/aggregate_score.py` | Aggregate multi-round review scores into benchmark |
| `scripts/package_skill.py` | Package skill and update registry.yaml |
| `scripts/run_loop.py` | Control the iteration loop (dev→validate→review) |
| `scripts/analyze_failures.py` | Analyze failure logs, detect iteration triggers, generate regression tests |

### Directory Structure

```
multi-agent-skills-factory/
├── SKILL.md
├── scripts/
│   ├── validate_skill.py
│   ├── aggregate_score.py
│   ├── package_skill.py
│   ├── run_loop.py
│   └── analyze_failures.py
└── references/
    ├── agents.md
    ├── pipeline-multi-agent.md
    ├── design-spec-template.md
    ├── eval-dimensions.md
    ├── test_pool.md
    ├── failure_case_log.md        ← 错误案例日志（自我迭代核心）
    └── self-review-template.md    ← 自我复盘流程模板
```

---

## 中文

### 概述

**Multi-Agent Skills Factory** 是一个将企业SOP流程封装为可复用Skill的自动化工作流。通过主编调度6个专业Agent并行协作，实现从业务流程到AI技能的端到端转化。

**核心特性：**
- 主编智能调度，6个专业Agent并行工作
- 自动化评分迭代，达标（≥75分）才上线
- 完整测试用例池，保证交付质量
- 4个自动化脚本（验证/聚合/打包/循环控制）

### Agent团队

| Agent | 输出 | 职责 |
|-------|------|------|
| 主编 | 任务调度+最终交付 | 解析需求、分解任务、协调Agent、组装产出 |
| 研究员 | SOP分析报告 | 深度理解业务流程、提取关键节点、识别边界场景 |
| 设计师 | 技能设计规格书 | 触发词设计、流程建模、输入输出定义 |
| 开发者 | SKILL.md代码 | 按hermes-agent-skill-authoring标准编写代码 |
| 测试员 | 测试报告 | 语法验证、功能测试、边界测试、安全测试 |
| 评审员 | 评审报告+grading.json | 五维打分（完整性/正确性/易用性/安全性/可维护性） |
| 迭代优化Agent | 错误分析+改进计划 | 分析failure_case_log.md，识别错误模式，推动自我迭代 |

### 自我迭代机制

生成的技能具备自我迭代能力：

| 机制 | 说明 |
|------|------|
| failure_case_log.md | 每次错误记录到错误日志，≥5条触发自动复盘 |
| self-review-template.md | 复盘流程：根因分析→优先级建议→SKILL.md更新 |
| 回归测试池 | 已修复错误进入test_pool.md，防止回潮 |
| 加分项 | 自我迭代机制运作良好可在评审中获得+10分加分 |

### 评审维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 完整性 | 25% | 核心流程是否覆盖完整SOP |
| 正确性 | 25% | 输出结果是否符合hermes-agent-skill-authoring标准 |
| 易用性 | 20% | 触发词是否清晰、使用是否简单 |
| 安全性 | 20% | 是否有敏感信息泄露风险 |
| 可维护性 | 10% | 代码结构是否清晰、references/是否规范 |

### 评分规则

- **≥90分** 优秀，直接上线
- **75-89分** 良好，小修小补后上线
- **<75分** 退回开发者修改，最多6轮

### 触发词

- "把这个流程封装成Skill"
- "建一个处理XX的技能"
- "SOP太重复了，做成自动化"
- `/封装Skill [SOP描述]`
- `/packageSkill [SOP description]`

### 自动化脚本

| 脚本 | 用途 |
|------|------|
| `scripts/validate_skill.py` | 自动验证 SKILL.md 格式、敏感信息、命名规范 |
| `scripts/aggregate_score.py` | 聚合多轮评审分数，生成 benchmark.json/md |
| `scripts/package_skill.py` | 打包技能并更新 registry.yaml |
| `scripts/run_loop.py` | 控制迭代循环（开发→验证→评审） |

### 目录结构

```
multi-agent-skills-factory/
├── SKILL.md
├── scripts/
│   ├── __init__.py
│   ├── validate_skill.py
│   ├── aggregate_score.py
│   ├── package_skill.py
│   └── run_loop.py
└── references/
    ├── agents.md
    ├── pipeline-multi-agent.md
    ├── design-spec-template.md
    ├── eval-dimensions.md
    └── test_pool.md
```

---

## License / 许可证

MIT License