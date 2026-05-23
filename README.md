# Multi-Agent Skills Factory

[English](#english) | [中文](#中文)

---

## English

### Overview

**Multi-Agent Skills Factory** is an automated workflow that packages enterprise SOP processes into reusable Hermes Skills. Through an Editor-in-Chief orchestrating 6 specialized agents working in parallel, it achieves end-to-end transformation from business processes to AI skills.

**Core Features:**
- Editor-in-Chief intelligent scheduling, multi-agent parallel work
- Automated scoring iteration, only goes live when score ≥75
- Complete test suite, ensuring delivery quality

### Agent Team

| Agent | Output | Responsibilities |
|-------|--------|------------------|
| Editor-in-Chief | Task scheduling + final delivery | Parse requirements, decompose tasks, coordinate agents, assemble output |
| Researcher | SOP analysis report | Deep understanding of business process, extract key nodes, identify edge cases |
| Designer | Skill design specification | Trigger word design, process modeling, input/output definition |
| Developer | SKILL.md code | Write code according to hermes-agent-skill-authoring standards |
| Tester | Test report | Syntax verification, functional testing, boundary testing, security testing |
| Reviewer | Review report | Five-dimensional scoring (completeness/correctness/usability/security/maintainability) |

### Review Dimensions

| Dimension | Score | Description |
|-----------|-------|-------------|
| Completeness | 20pts | Does the core process cover the complete SOP? |
| Correctness | 20pts | Does the output meet hermes-agent-skill-authoring standards? |
| Usability | 20pts | Are trigger words clear and usage simple? |
| Security | 20pts | Any risk of sensitive information leakage? |
| Maintainability | 20pts | Is the code structure clear, references/ organized? |

### Scoring Rules

- **≥90pts** Excellent, go live directly
- **75-89pts** Good, go live after minor fixes
- **<75pts** Return to developer, max 6 rounds

### Trigger Words

- "Package this process as a Skill"
- "Build a skill for handling XX"
- "SOP is too repetitive, make it automated"
- `/packageSkill [SOP description]`

### Directory Structure

```
multi-agent-skills-factory/
├── SKILL.md
└── references/
    ├── agents.md
    ├── pipeline-multi-agent.md
    ├── design-spec-template.md
    ├── eval-dimensions.md
    └── test_pool.md
```

---

## 中文

### 概述

**Multi-Agent Skills Factory** 是一个将企业SOP流程封装为可复用Hermes Skill的自动化工作流。通过主编调度6个专业Agent并行协作，实现从业务流程到AI技能的端到端转化。

**核心特性：**
- 主编智能调度，多Agent并行工作
- 自动化评分迭代，达标（≥75分）才上线
- 完整测试用例池，保证交付质量

### Agent团队

| Agent | 输出 | 职责 |
|-------|------|------|
| 主编 | 任务调度+最终交付 | 解析需求、分解任务、协调Agent、组装产出 |
| 研究员 | SOP分析报告 | 深度理解业务流程、提取关键节点、识别边界场景 |
| 设计师 | 技能设计规格书 | 触发词设计、流程建模、输入输出定义 |
| 开发者 | SKILL.md代码 | 按hermes-agent-skill-authoring标准编写代码 |
| 测试员 | 测试报告 | 语法验证、功能测试、边界测试、安全测试 |
| 评审员 | 评审报告 | 五维打分（完整性/正确性/易用性/安全性/可维护性） |

### 评审维度

| 维度 | 分值 | 说明 |
|------|------|------|
| 完整性 | 20分 | 核心流程是否覆盖完整SOP |
| 正确性 | 20分 | 输出结果是否符合hermes-agent-skill-authoring标准 |
| 易用性 | 20分 | 触发词是否清晰、使用是否简单 |
| 安全性 | 20分 | 是否有敏感信息泄露风险 |
| 可维护性 | 20分 | 代码结构是否清晰、references/是否规范 |

### 评分规则

- **≥90分** 优秀，直接上线
- **75-89分** 良好，小修小补后上线
- **<75分** 退回开发者修改，最多6轮

### 触发词

- "把这个流程封装成Skill"
- "建一个处理XX的技能"
- "SOP太重复了，做成自动化"
- `/封装Skill [SOP描述]`

### 目录结构

```
multi-agent-skills-factory/
├── SKILL.md
└── references/
    ├── agents.md
    ├── pipeline-multi-agent.md
    ├── design-spec-template.md
    ├── eval-dimensions.md
    └── test_pool.md
```

---

MIT License