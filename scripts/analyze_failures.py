#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_failures.py — 分析错误案例日志，生成改进建议

用法：
  python analyze_failures.py <skill-dir>                    # 分析错误模式
  python analyze_failures.py <skill-dir> --regression       # 生成回归测试
  python analyze_failures.py <skill-dir> --suggest          # 生成改进建议
  python analyze_failures.py <skill-dir> --auto             # 自动迭代（当>=5条未修复时）

功能：
  1. 解析 failure_case_log.md，统计错误类型
  2. 识别高频错误和复发性错误
  3. 生成回归测试用例
  4. 输出改进建议（按优先级排序）
  5. 当未修复案例>=5时，触发自检警告
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter


# Windows stdout UTF-8 fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def parse_failure_log(log_path: Path) -> dict:
    """解析 failure_case_log.md"""
    if not log_path.exists():
        return {"unfixed": [], "fixed": [], "in_progress": []}

    content = log_path.read_text(encoding="utf-8")
    sections = {}

    # 按 ### 分割章节
    current_section = "header"
    current_lines = []
    for line in content.split("\n"):
        if line.startswith("### 🔴") or line.startswith("### 🟡") or line.startswith("### ✅"):
            sections[current_section] = "\n".join(current_lines)
            current_section = line.strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections[current_section] = "\n".join(current_lines)

    unfixed = _parse_table(sections.get("### 🔴 未修复（需优先处理）", ""))
    in_progress = _parse_table(sections.get("### 🟡 修复中", ""))
    fixed = _parse_table(sections.get("### ✅ 已修复（回归测试用）", ""))

    return {
        "unfixed": unfixed,
        "in_progress": in_progress,
        "fixed": fixed,
        "raw": content,
    }


def _parse_table(section: str) -> list[dict]:
    """解析 markdown 表格"""
    rows = []
    lines = section.split("\n")
    in_table = False
    header = []
    for line in lines:
        line = line.strip()
        if line.startswith("| # |") or line.startswith("|---|"):
            in_table = True
            continue
        if in_table and line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if not header:
                header = cells
                continue
            row = dict(zip(header, cells))
            rows.append(row)
    return rows


def classify_errors(unfixed: list[dict]) -> dict:
    """分类统计错误类型"""
    type_counter = Counter()
    recurrence = {}
    for row in unfixed:
        problem_type = row.get("问题类型", "未知").strip()
        trigger = row.get("触发词", "").strip()
        type_counter[problem_type] += 1
        if trigger:
            recurrence.setdefault(trigger, []).append(row)

    return {
        "type_counts": dict(type_counter.most_common()),
        "recurring": {k: v for k, v in recurrence.items() if len(v) >= 2},
        "total": len(unfixed),
    }


def generate_regression_tests(fixed: list[dict], unfixed: list[dict]) -> list[dict]:
    """生成回归测试用例（来自已修复案例）"""
    tests = []
    for row in fixed:
        tests.append({
            "case_id": row.get("#", f"RE-{len(tests)+1:03d}"),
            "trigger": row.get("触发词", "").strip(),
            "expected": row.get("正确预期", "").strip() or row.get("预期输出", "").strip(),
            "source": "已修复",
            "verified_date": row.get("验证结果", "").strip(),
        })
    for row in unfixed[:5]:  # 未修复的前5条也作为回归测试（验证改进）
        tests.append({
            "case_id": row.get("#", f"RE-{len(tests)+1:03d}"),
            "trigger": row.get("触发词", "").strip(),
            "expected": row.get("正确预期", "").strip() or row.get("预期输出", "").strip(),
            "source": "未修复（回归验证）",
            "status": "MUST_PASS",
        })
    return tests


def generate_suggestions(classification: dict, unfixed: list[dict]) -> list[dict]:
    """生成改进建议（按优先级）"""
    suggestions = []
    type_counts = classification["type_counts"]
    recurring = classification["recurring"]

    # P0：复发性错误（>=3次）
    for trigger, cases in recurring.items():
        suggestions.append({
            "priority": "P0",
            "label": "复发性错误",
            "detail": f"触发词「{trigger[:30]}」出现 {len(cases)} 次",
            "action": "在 SKILL.md 中明确处理该场景，添加边界判断",
            "cases": len(cases),
        })

    # P0：未修复 >= 5 条
    if classification["total"] >= 5:
        suggestions.append({
            "priority": "P0",
            "label": "错误积累超限",
            "detail": f"当前 {classification['total']} 条未修复错误，已达到自动迭代阈值",
            "action": "触发自我复盘流程，更新 SKILL.md",
            "cases": classification["total"],
        })

    # P1：错误类型排行前3
    for ptype, count in list(type_counts.items())[:3]:
        if count >= 2:
            suggestions.append({
                "priority": "P1",
                "label": f"错误类型：{ptype}",
                "detail": f"共出现 {count} 次",
                "action": f"检查 {ptype} 相关流程步骤，补充边界处理或修正逻辑",
                "cases": count,
            })

    # P2：其他
    for ptype, count in list(type_counts.items())[3:]:
        suggestions.append({
            "priority": "P2",
            "label": f"错误类型：{ptype}",
            "detail": f"共出现 {count} 次",
            "action": "下个版本规划时考虑补充",
            "cases": count,
        })

    return suggestions


def generate_markdown_report(skill_dir: Path, parsed: dict, classification: dict,
                             suggestions: list[dict], regression: list[dict]) -> str:
    """生成可读的分析报告"""
    md = f"""# 错误案例分析报告 — {skill_dir.name}
> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 错误统计

| 状态 | 数量 |
|------|------|
| 🔴 未修复 | {len(parsed['unfixed'])} 条 |
| 🟡 修复中 | {len(parsed['in_progress'])} 条 |
| ✅ 已修复 | {len(parsed['fixed'])} 条 |

## 错误类型分布

"""
    type_counts = classification["type_counts"]
    if type_counts:
        for ptype, count in type_counts.most_common():
            pct = count / classification["total"] * 100
            bar = "█" * int(pct / 5)
            md += f"- **{ptype}**：{count} 条（{pct:.0f}%）{bar}\n"
    else:
        md += "_暂无错误数据_\n"

    md += "\n## 复发性错误（≥2次）\n\n"
    recurring = classification["recurring"]
    if recurring:
        for trigger, cases in recurring.items():
            md += f"- `{trigger[:50]}` — 出现 **{len(cases)}** 次\n"
    else:
        md += "_暂无复发性错误_\n"

    md += "\n## 改进建议\n\n"
    if suggestions:
        current_priority = None
        for s in suggestions:
            if s["priority"] != current_priority:
                md += f"\n### {s['priority']} 级\n\n"
                current_priority = s["priority"]
            md += f"- **{s['label']}**：{s['detail']}\n  → 行动：{s['action']}\n"
    else:
        md += "_暂无改进建议_\n"

    md += "\n## 回归测试建议\n\n"
    if regression:
        md += "| 案例ID | 触发词 | 来源 | 状态 |\n"
        md += "|--------|--------|------|------|\n"
        for t in regression:
            status = "🚨 MUST_PASS" if t.get("status") == "MUST_PASS" else "✅"
            md += f"| {t['case_id']} | {t['trigger'][:40]} | {t['source']} | {status} |\n"
    else:
        md += "_暂无回归测试用例_\n"

    # 自动迭代触发警告
    if classification["total"] >= 5:
        md += f"\n🚨 **自动迭代触发**：检测到 {classification['total']} 条未修复错误，已达到阈值（≥5）。\n"
        md += "建议运行：`python scripts/run_loop.py <skill-name> 6`\n"

    return md


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_failures.py <skill-dir> [--regression] [--suggest] [--auto]")
        sys.exit(1)

    skill_dir = Path(sys.argv[1])
    log_path = skill_dir / "references" / "failure_case_log.md"

    mode = "full"
    if "--regression" in sys.argv:
        mode = "regression"
    elif "--suggest" in sys.argv:
        mode = "suggest"
    elif "--auto" in sys.argv:
        mode = "auto"

    parsed = parse_failure_log(log_path)
    classification = classify_errors(parsed["unfixed"])

    if mode == "regression":
        regression = generate_regression_tests(parsed["fixed"], parsed["unfixed"])
        print(json.dumps(regression, ensure_ascii=False, indent=2))
    elif mode == "suggest":
        suggestions = generate_suggestions(classification, parsed["unfixed"])
        print(json.dumps(suggestions, ensure_ascii=False, indent=2))
    else:
        suggestions = generate_suggestions(classification, parsed["unfixed"])
        regression = generate_regression_tests(parsed["fixed"], parsed["unfixed"])
        md = generate_markdown_report(skill_dir, parsed, classification, suggestions, regression)
        print(md)

        # --auto 模式：达到阈值时输出触发信号
        if mode == "auto" and classification["total"] >= 5:
            print("\n[ITERATION_TRIGGER] 错误数达到阈值，建议触发自我迭代")
            sys.exit(0)  # 0 = 需要迭代
        elif mode == "auto":
            print("\n[ITERATION_SKIP] 错误数未达阈值，无需迭代")