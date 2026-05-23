# Multi-Agent Skill Factory — 多Agent协作SOP封装流水线

> 一键触发AI编辑团队，把每一个重复的业务流程，变成可复用的Skill。

## 概述

Multi-Agent Skill Factory 是一个将企业SOP流程封装为可复用Hermes Skill的自动化工作流。通过主编调度6个专业Agent并行协作，实现从业务流程到AI技能的端到端转化。

**核心特性：**
- 主编智能调度，多Agent并行工作
- 自动化评分迭代，达标（≥75分）才上线
- 完整测试用例池，保证交付质量

## 工作流程

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

## Agent团队

| Agent | 输出 | 职责 |
|-------|------|------|
| 主编 | 任务调度+最终交付 | 解析需求、分解任务、协调Agent、组装产出 |
| 研究员 | SOP分析报告 | 深度理解业务流程、提取关键节点、识别边界场景 |
| 设计师 | 技能设计规格书 | 触发词设计、流程建模、输入输出定义 |
| 开发者 | SKILL.md代码 | 按hermes-agent-skill-authoring标准编写代码 |
| 测试员 | 测试报告 | 语法验证、功能测试、边界测试、安全测试 |
| 评审员 | 评审报告 | 五维打分（完整性/正确性/易用性/安全性/可维护性） |

## 评审维度

| 维度 | 分值 | 说明 |
|------|------|------|
| 完整性 | 20分 | 核心流程是否覆盖完整SOP |
| 正确性 | 20分 | 输出结果是否符合hermes-agent-skill-authoring标准 |
| 易用性 | 20分 | 触发词是否清晰、使用是否简单 |
| 安全性 | 20分 | 是否有敏感信息泄露风险 |
| 可维护性 | 20分 | 代码结构是否清晰、references/是否规范 |

**评分规则：**
- ≥90分：优秀，直接上线
- 75-89分：良好，小修小补后上线
- <75分：退回开发者修改，最多6轮

## 触发词

- "把这个流程封装成Skill"
- "建一个处理XX的技能"
- "SOP太重复了，做成自动化"
- "/封装Skill [SOP描述]"

## 目录结构

```
multi-agent--skills-factory/
├── SKILL.md                    ← 主入口（主编调度）
└── references/
    ├── agents.md               ← 6个Agent模板
    ├── pipeline-multi-agent.md ← 多Agent流水线详解
    ├── design-spec-template.md ← 设计规格书模板
    ├── eval-dimensions.md      ← 评估维度
    └── test_pool.md           ← 测试用例池
```

## 模板文件说明

| 文件 | 说明 |
|------|------|
| `references/agents.md` | 6个Agent的系统提示词模板 |
| `references/pipeline-multi-agent.md` | 主编调度手册，详细说明各阶段工作 |
| `references/design-spec-template.md` | 技能设计规格书模板 |
| `references/eval-dimensions.md` | 评估维度与评分标准详解 |
| `references/test_pool.md` | 测试用例池，覆盖各种场景 |

## 使用示例

```
/封装Skill 客户投诉自动处理流程
/封装Skill 新员工入职引导技能
/封装Skill 订单退款审批流程
```

## 相关Skills

- `hermes-agent-skill-authoring` - Skill编写标准
- `multi-agent-wechat` - 微信公众号内容创作

## License

MIT
