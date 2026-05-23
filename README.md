# Multi-Agent Skills Factory — 多Agent协作SOP封装流水线

> 一键触发AI编辑团队，把每一个重复的业务流程，变成可复用的Skill。

---

# English Version

# Multi-Agent Skills Factory — Multi-Agent SOP Packaging Pipeline

> One-click triggers an AI editorial team, turning every repetitive business process into a reusable Skill.

## Overview

Multi-Agent Skills Factory is an automated workflow that packages enterprise SOP processes into reusable Hermes Skills. Through an Editor-in-Chief orchestrating 6 specialized agents working in parallel, it achieves end-to-end transformation from business processes to AI skills.

**Core Features:**
- Editor-in-Chief intelligent scheduling, multi-agent parallel work
- Automated scoring iteration, only goes live when score ≥75
- Complete test suite, ensuring delivery quality

## Workflow

```
User says "package this Skill"
         ↓
Editor receives task, parses SOP
         ↓
   ┌─────┴─────┐
   ↓           ↓
 Researcher   Designer
 analyzes SOP produces design spec
   ↓           ↓
   └─────┬─────┘
         ↓
 Developer writes SKILL.md
         ↓
 Tester executes test cases
         ↓
 Reviewer scores
         ↓
   ┌────┴────┐
   ↓         ↓
✅ ≥75     ❌ <75
Register   Return to developer
上线        修改
               ↑
         (loop until qualified)
```

## Agent Team

| Agent | Output | Responsibilities |
|-------|--------|------------------|
| Editor-in-Chief | Task scheduling + final delivery | Parse requirements, decompose tasks, coordinate agents, assemble output |
| Researcher | SOP analysis report | Deep understanding of business process, extract key nodes, identify edge cases |
| Designer | Skill design specification | Trigger word design, process modeling, input/output definition |
| Developer | SKILL.md code | Write code according to hermes-agent-skill-authoring standards |
| Tester | Test report | Syntax verification, functional testing, boundary testing, security testing |
| Reviewer | Review report | Five-dimensional scoring (completeness/correctness/usability/security/maintainability) |

## Review Dimensions

| Dimension | Score | Description |
|-----------|-------|-------------|
| Completeness | 20pts | Does the core process cover the complete SOP? |
| Correctness | 20pts | Does the output meet hermes-agent-skill-authoring standards? |
| Usability | 20pts | Are trigger words clear and usage simple? |
| Security | 20pts | Any risk of sensitive information leakage? |
| Maintainability | 20pts | Is the code structure clear, references/ organized? |

**Scoring Rules:**
- ≥90pts: Excellent, go live directly
- 75-89pts: Good, go live after minor fixes
- <75pts: Return to developer for modification, max 6 rounds

## Trigger Words

- "把这个流程封装成Skill" / "Package this process as a Skill"
- "建一个处理XX的技能" / "Build a skill for handling XX"
- "SOP太重复了，做成自动化" / "SOP is too repetitive, make it automated"
- "/封装Skill [SOP描述]" / "/packageSkill [SOP description]"

**Not suitable for:**
- One-time tasks (just ask AI directly)
- Pure technical development projects (use claude-code)
- Existing Skills that need modification (just patch)

## Quick Commands

```
/封装Skill [one-line SOP description]
```

Example: `/封装Skill 客户投诉自动处理流程` / `/packageSkill Customer complaint auto-handling process`

## Directory Structure

```
multi-agent-skills-factory/
├── SKILL.md                    ← Main entry (Editor-in-Chief scheduling)
└── references/
    ├── agents.md               ← 6 Agent templates
    ├── pipeline-multi-agent.md ← Multi-agent pipeline details
    ├── design-spec-template.md ← Design specification template
    ├── eval-dimensions.md      ← Evaluation dimensions
    └── test_pool.md           ← Test case pool
```

## Template Files

| File | Description |
|------|-------------|
| `references/agents.md` | 6 Agent system prompt templates |
| `references/pipeline-multi-agent.md` | Editor-in-Chief scheduling manual |
| `references/design-spec-template.md` | Skill design specification template |
| `references/eval-dimensions.md` | Evaluation dimensions and scoring criteria |
| `references/test_pool.md` | Test case pool covering various scenarios |

## Usage Examples

```
/封装Skill 客户投诉自动处理流程
/封装Skill 新员工入职引导技能
/封装Skill 订单退款审批流程
```

## Common Questions

**Q1: What if the SOP is too complex?**
A: Split into multiple sub-Skills. Researcher identifies split points, Designer plans module boundaries.

**Q2: Must all 6 agents be called?**
A: Simple SOPs can skip the Researcher/Designer parallel phase, Editor parses directly. But Tester→Reviewer cannot be skipped.

**Q3: Score <75 but reached 6-round limit?**
A: Deliver the current highest score version, explain why targets weren't met and remaining improvement space.

**Q4: What's the difference from skill-factory (single-agent version)?**
A: multi-agent-skills-factory has Editor-in-Chief orchestrating multiple specialized agents working in parallel, suitable for complex SOPs; single-agent version is for simple SOP rapid packaging.

## Verification Checklist

- [ ] description starts with "Use when"
- [ ] frontmatter contains complete fields
- [ ] references/ directory contains agents.md + pipeline-multi-agent.md
- [ ] test_pool.md named correctly
- [ ] Editor-in-Chief scheduling covers 5 professional agents

## Related Skills

- `hermes-agent-skill-authoring` - Skill writing standards
- `multi-agent-wechat` - WeChat public account content creation

## License

MIT
