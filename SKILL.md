---
name: multi-agent-skill-factory
description: Use when 需要将企业SOP流程封装为Hermes Skill。一键触发多Agent协作工作流：主编调度→研究员分析→设计师设计→开发者编码→测试员验证→评审员打分，循环迭代直到评分达标。
version: 1.0.0
author: Muru AI
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [multi-agent, skill-factory, skill封装, sop, automation, hermes-skill]
    related_skills: [hermes-agent-skill-authoring, multi-agent-wechat]
---

# Multi-Agent Skill Factory — 多Agent协作SOP封装流水线

> 一键触发AI编辑团队，把每一个重复的业务流程，变成可复用的Skill。

## Overview

主编（我）调度 → 并行分析+设计 → 开发者出码 → 测试员验证 → 评审打分 → (循环修改) → 注册上线

```
用户说"封装Skill"
         ↓
主编接收任务，解析SOP
         ↓
   ┌─────┴─────┐
   ↓           ↓
研究员         设计师
分析SOP       产出设计规格书
   ↓           ↓
   └─────┬─────┘
         ↓
开发者编写SKILL.md
         ↓
测试员执行测试用例
         ↓
评审员量化打分
         ↓
   ┌────┴────┐
   ↓         ↓
✅ ≥75分   ❌ <75分
注册上线    返回开发者修改
               ↑
         （循环直到达标）
```

## When to Use

**触发词（满足任一即可）：**
- "把这个流程封装成Skill"
- "建一个处理XX的技能"
- "SOP太重复了，做成自动化"
- "把这个业务流程做成AI技能"
- "技能封装"
- "/封装Skill [SOP描述]"

**不适用于：**
- 一次性任务（直接问AI就行）
- 纯技术开发项目（用claude-code）
- 已有Skill需要修改（直接patch）

## Agent团队配置

| Agent | 模板 | 输出 | 职责 |
|-------|------|------|------|
| 主编 | [references/agents.md](references/agents.md) | 任务调度+最终交付 | 解析需求、分解任务、协调Agent、组装产出 |
| 研究员 | [references/agents.md](references/agents.md) | SOP分析报告 | 深度理解业务流程、提取关键节点、识别边界场景 |
| 设计师 | [references/agents.md](references/agents.md) | 技能设计规格书 | 触发词设计、流程建模、输入输出定义 |
| 开发者 | [references/agents.md](references/agents.md) | SKILL.md代码 | 按hermes-agent-skill-authoring标准编写代码 |
| 测试员 | [references/agents.md](references/agents.md) | 测试报告 | 语法验证、功能测试、边界测试、安全测试 |
| 评审员 | [references/agents.md](references/agents.md) | 评审报告 | 五维打分（完整性/正确性/易用性/安全性/可维护性） |

## 模板文件

| 文件 | 说明 |
|------|------|
| [references/agents.md](references/agents.md) | 6个Agent的系统提示词模板 |
| [references/pipeline-multi-agent.md](references/pipeline-multi-agent.md) | 多Agent流水线详解（主编调度手册） |
| [references/design-spec-template.md](references/design-spec-template.md) | 技能设计规格书模板 |
| [references/eval-dimensions.md](references/eval-dimensions.md) | 评估维度与评分标准 |
| [references/test_pool.md](references/test_pool.md) | 测试用例池 |

## 核心工作流

### 标准流程（主编调度7步）

```
Step 1: 用户提供SOP描述
         ↓
Step 2: 并行执行（研究员分析 + 设计师设计）
         ↓
Step 3: 主编汇总，产出技能设计规格书
         ↓
Step 4: 开发者编写SKILL.md
         ↓
Step 5: 测试员执行测试用例
         ↓
      ┌── 评审员打分 ──┐
      ↓              ↓
  ✅ ≥75分       ❌ <75分
  注册上线     返回Step 4 修改
                   ↑
            （循环直到达标或达到6轮上限）
         ↓
Step 6: 更新registry.yaml
         ↓
Step 7: 输出技能路径，告知用户完成
```

## 评审维度（每项20分，满分100）

| 维度 | 说明 |
|------|------|
| 完整性 | 核心流程是否覆盖完整SOP |
| 正确性 | 输出结果是否符合hermes-agent-skill-authoring标准 |
| 易用性 | 触发词是否清晰、使用是否简单 |
| 安全性 | 是否有敏感信息泄露风险 |
| 可维护性 | 代码结构是否清晰、references/是否规范 |

**评分规则：**
- ≥90分：✅ 优秀，直接上线
- 75-89分：⚠️ 良好，小修小补后上线
- <75分：🔧 退回开发者修改，最多6轮

## 目录结构

```
multi-agent-skill-factory/
├── SKILL.md              ← 主入口（主编调度）
└── references/
    ├── agents.md                   ← 6个Agent模板
    ├── pipeline-multi-agent.md     ← 多Agent流水线详解
    ├── design-spec-template.md     ← 设计规格书模板
    ├── eval-dimensions.md          ← 评估维度
    └── test_pool.md               ← 测试用例池
```

## 快捷指令

```
/封装Skill [一句话描述SOP]
```

示例：`/封装Skill 客户投诉自动处理流程`

## Common Pitfalls

**Q1：SOP太复杂怎么办？**
A：拆成多个子Skill，研究员识别可拆分点，设计师规划模块边界。

**Q2：6个Agent都要调用吗？**
A：简单SOP可跳过研究员/设计师并行环节，由主编直接解析。但测试员→评审员不可跳过。

**Q3：评审<75分但已达6轮上限？**
A：交付当前最高分版本，说明未达标原因和剩余改进空间。

**Q4：与skill-factory（单Agent版）的区别？**
A：multi-agent-skill-factory由主编调度多个专业Agent并行工作，适合复杂SOP；单Agent版适合简单SOP快速封装。

## 验证清单

- [ ] description以"Use when"开头
- [ ] frontmatter包含完整字段
- [ ] references/目录包含agents.md + pipeline-multi-agent.md
- [ ] test_pool.md命名正确
- [ ] 主编调度流程覆盖5个专业Agent
