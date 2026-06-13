---
name: multi-agent-skill-factory
description: Use when 需要将企业SOP流程封装为可复用Skill。一键触发多Agent协作工作流：主编调度→研究员分析→设计师设计→开发者编码→测试员验证→评审员打分，循环迭代直到评分达标。适用于业务流程重复、想封装为自动化技能的场景。
version: 1.0.0
author: Muru AI
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [multi-agent, skill-factory, skill封装, sop, automation, hermes-skill]
    related_skills: [multi-agent-skill-creator, skill-create]
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

📦 **创建类**：
- "新建一个技能"
- "创建一个技能来处理XX"
- "做一个能XX的技能"
- "搭建一个技能"
- "开发一个新技能"

🎁 **封装类**：
- "把这个流程封装成技能"
- "把这个SOP变成AI技能"
- "把重复的工作流做成自动化技能"
- "这个流程太重复了，做成技能"
- "把XX流程自动化"

🎨 **设计类**：
- "设计一个技能"
- "帮我设计个技能"
- "规划一个AI技能"
- "这个场景需要什么技能"

🔧 **快捷指令**：`/新建技能 [描述]` `/封装技能 [描述]` `/技能工厂 [描述]`

**不适用于：**
- 一次性任务（直接问AI就行）
- 纯技术开发项目（用claude-code）
- 已有Skill需要修改（直接patch）

## 自我迭代机制

生成的技能具备**自我迭代能力**，包含以下核心机制：

### 错误案例日志（failure_case_log.md）

每次使用出现错误时，记录到 `references/failure_case_log.md`：
- **触发词 | 错误输出 | 正确预期 | 根因分析**
- 未修复 ≥ 5 条时自动触发复盘迭代
- 同一触发词出现 ≥ 3 次判定为复发性错误（立即修复）

### 自我复盘流程（self-review-template.md）

达到触发条件后，自动执行复盘：
1. 分析错误日志，识别错误模式
2. 按优先级生成改进建议（P0/P1/P2）
3. 更新 SKILL.md
4. 回归测试验证

### 迭代优化 Agent（第7个Agent）

专职负责错误日志分析和迭代驱动：
- 检测迭代触发条件
- 运行 `analyze_failures.py` 生成报告
- 推动 SKILL.md 增量更新
- 维护回归测试池

### 加分项（评审时）

| 条件 | 加分 |
|------|------|
| 有错误日志且 ≥ 3 条记录 | +3分 |
| 有自我复盘报告且有改进措施 | +3分 |
| 已修复案例进入回归测试池 | +2分 |
| 最近30天无新增错误 | +2分 |
| **最高** | **+10分** |

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

| 维度 | 权重 | 说明 |
|------|------|------|
| 完整性 | 25% | 核心流程是否覆盖完整SOP |
| 正确性 | 25% | 输出结果是否符合hermes-agent-skill-authoring标准 |
| 易用性 | 20% | 触发词是否清晰、使用是否简单 |
| 安全性 | 20% | 是否有敏感信息泄露风险 |
| 可维护性 | 10% | 代码结构是否清晰、references/是否规范 |

**评分计算：**
```
总分 = 完整性×0.25 + 正确性×0.25 + 易用性×0.20 + 安全性×0.20 + 可维护性×0.10
```

**评分规则：**
- ≥90分：✅ 优秀，直接上线
- 75-89分：⚠️ 良好，小修小补后上线
- <75分：🔧 退回开发者修改，最多6轮

## 目录结构

```
multi-agent-skill-factory/
├── SKILL.md              ← 主入口（主编调度）
├── scripts/              ← 自动化脚本
│   ├── __init__.py
│   ├── validate_skill.py  ← SKILL.md 自动验证
│   ├── aggregate_score.py ← 评审分数聚合
│   ├── package_skill.py   ← 打包与注册
│   ├── run_loop.py        ← 迭代循环控制
│   └── analyze_failures.py ← 错误日志分析
└── references/
    ├── agents.md                   ← 7个Agent模板（含迭代优化Agent）
    ├── pipeline-multi-agent.md     ← 主编调度手册
    ├── design-spec-template.md     ← 设计规格书模板
    ├── eval-dimensions.md          ← 评估维度与grading格式（含自我迭代加分）
    ├── test_pool.md               ← 测试用例池
    ├── failure_case_log.md        ← 错误案例日志（技能自我迭代核心）
    └── self-review-template.md     ← 自我复盘流程模板
```

## How to Use / 如何使用

### 快捷指令
```
/封装Skill [一句话描述SOP]
```
示例：`/封装Skill 客户投诉自动处理流程`

### 自动化脚本

| 脚本 | 用途 |
|------|------|
| `python scripts/validate_skill.py <SKILL.md>` | 自动验证 SKILL.md 格式和安全性 |
| `python scripts/aggregate_score.py <iteration-dir>` | 聚合多轮评审分数，生成 benchmark |
| `python scripts/package_skill.py <skill-dir>` | 打包技能并更新 registry.yaml |
| `python scripts/run_loop.py <skill-name> <max-rounds>` | 控制迭代循环（开发→验证→评审） |
| `python scripts/analyze_failures.py <skill-dir> --auto` | 检测是否触发自我迭代（≥5条未修复=触发） |
| `python scripts/analyze_failures.py <skill-dir> --regression` | 生成回归测试用例 |
| `python scripts/analyze_failures.py <skill-dir> --suggest` | 生成优先级改进建议 |

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

**Q4：与 multi-agent-skill-creator 的区别？**
A：multi-agent-skill-factory 专注于企业SOP封装，五维打分达标才上线；multi-agent-skill-creator 是通用技能创建工具，侧重 eval-viewer 迭代和描述优化。两者互补。

## 验证清单

运行自动化验证（最可靠）：
```bash
python scripts/validate_skill.py <SKILL.md路径>
```

手动检查项：
- [ ] description以"Use when"开头
- [ ] frontmatter包含完整字段（name/description/version/author/license/platforms/metadata.hermes）
- [ ] description ≤ 1024字符
- [ ] references/目录存在（当正文>8KB时）
- [ ] test_pool.md命名正确（不是test_cases.md）
- [ ] 无硬编码敏感信息
- [ ] 主编调度流程覆盖6个专业Agent
