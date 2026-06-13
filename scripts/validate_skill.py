#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_skill.py — SKILL.md 自动化验证脚本

用法：
  python validate_skill.py <path-to-SKILL.md>
  python validate_skill.py <path-to-SKILL.md> --fix   # 自动修复可修复的问题

检查项：
  1. frontmatter 格式（以 --- 开头和结尾）
  2. 必需字段（name, description, version, author, license, platforms, metadata.hermes）
  3. description 以 "Use when" 开头
  4. description ≤ 1024 字符
  5. references/ 目录存在（当内容 >8KB 时）
  6. test_pool.md 命名正确（不是 test_cases.md）
  7. 无硬编码敏感信息（密码/token/密钥）
  8. SKILL.md 总行数 ≤ 600 行（建议）
"""

import sys
import re
import os
from pathlib import Path

# Windows stdout UTF-8 fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_file(path: str) -> tuple[str, list[str]]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    return content, lines


def extract_frontmatter(lines: list[str]) -> dict[str, str]:
    """提取 YAML frontmatter 到字典（支持嵌套结构）"""
    if lines[0].strip() != "---":
        return {}
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}
    fm_lines = lines[1:end_idx]
    fm = {}
    stack = []  # (key, indent) 栈
    for line in fm_lines:
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        if ":" not in stripped:
            continue
        # 只分割第一个冒号，因为值里可能有冒号
        colon_pos = stripped.index(":")
        key = stripped[:colon_pos].strip()
        value = stripped[colon_pos + 1:].strip()
        # 弹出 >= 当前缩进的层级（同缩进=兄弟，后一个先弹出前一个）
        while stack and stack[-1][1] >= indent:
            stack.pop()
        if not value:
            stack.append((key, indent))
            # 空值节点只记录完整嵌套路径（不记录裸key，避免重复）
            path = ".".join([p[0] for p in stack])
            fm[path] = ""
        else:
            if stack:
                parent_key, _ = stack[-1]
                fm[f"{parent_key}.{key}"] = value
            fm[key] = value
    return fm


def check_frontmatter_format(lines: list[str]) -> tuple[bool, str]:
    """TC-SYNTAX-001: frontmatter格式"""
    if lines[0].strip() != "---":
        return False, "❌ frontmatter 必须以 --- 开头"
    # 找 frontmatter 结束标记
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return False, "❌ frontmatter 缺少结束 ---"
    return True, "✅ frontmatter 格式正确"


def check_required_fields(fm: dict[str, str]) -> tuple[bool, list[str]]:
    """TC-SYNTAX-002: 必需字段"""
    required = ["name", "description", "version", "author", "license", "platforms"]
    missing = [f for f in required if f not in fm or not fm[f]]
    if missing:
        return False, [f"❌ 缺少必需字段: {', '.join(missing)}"]
    # metadata.hermes 特殊检查（支持嵌套key）
    if "metadata.hermes" not in fm:
        return False, ["❌ metadata.hermes 字段缺失或格式错误"]
    return True, ["✅ 所有必需字段存在"]


def check_description_starts_with_use_when(fm: dict[str, str]) -> tuple[bool, str]:
    """TC-SYNTAX-004: description以Use when开头"""
    desc = fm.get("description", "")
    if desc.startswith("Use when"):
        return True, "✅ description 以 'Use when' 开头"
    return False, f"❌ description 必须以 'Use when' 开头，当前开头: {desc[:50]}"


def check_description_length(fm: dict[str, str]) -> tuple[bool, str]:
    """TC-SYNTAX-003: description长度"""
    desc = fm.get("description", "")
    length = len(desc)
    if length <= 1024:
        return True, f"✅ description 长度 {length} ≤ 1024"
    return False, f"❌ description 长度 {length} > 1024（超出 {length - 1024} 字符）"


def check_references_dir(skill_dir: Path, body_length: int) -> tuple[bool, str]:
    """TC-SYNTAX-005: references目录"""
    if body_length <= 8 * 1024:
        return True, f"ℹ️  SKILL.md 正文 {body_length}B ≤ 8KB，无需 references/ 目录"
    refs = skill_dir / "references"
    if refs.is_dir():
        return True, f"✅ references/ 目录存在"
    return False, f"❌ SKILL.md 正文 {body_length}B > 8KB，必须有 references/ 目录"


def check_test_pool_naming(skill_dir: Path) -> tuple[bool, str]:
    """可维护性: test_pool.md命名"""
    refs = skill_dir / "references"
    test_file = refs / "test_pool.md"
    wrong_names = list(refs.glob("test_cases*.md")) if refs.exists() else []
    if wrong_names:
        return False, f"❌ 测试文件必须命名为 test_pool.md，当前: {[f.name for f in wrong_names]}"
    if not test_file.exists():
        return False, "❌ references/test_pool.md 不存在"
    return True, "✅ 测试文件命名正确 (test_pool.md)"


SENSITIVE_PATTERNS = [
    (r'password\s*[:=]\s*["\'][^"\']{3,}["\']', "password 硬编码"),
    (r'api[_-]?key\s*[:=]\s*["\'][^"\']{8,}["\']', "api_key 硬编码"),
    (r'token\s*[:=]\s*["\'][^"\']{8,}["\']', "token 硬编码"),
    (r'secret\s*[:=]\s*["\'][^"\']{8,}["\']', "secret 硬编码"),
    (r'Bearer\s+[A-Za-z0-9_-]{20,}', "Bearer token 硬编码"),
    (r'ghp_[A-Za-z0-9]{36}', "GitHub Personal Access Token"),
    (r'AKIA[A-Z0-9]{16}', "AWS Access Key ID"),
]

def check_sensitive_info(content: str) -> tuple[bool, list[str]]:
    """TC-SEC-001: 敏感信息"""
    issues = []
    for pattern, label in SENSITIVE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"❌ 发现 {label}")
    if issues:
        return False, issues
    return True, ["✅ 无硬编码敏感信息"]


def check_skill_line_count(lines: list[str]) -> tuple[bool, str]:
    """建议: SKILL.md 行数"""
    # 去掉 frontmatter，只看正文
    body_lines = []
    in_fm = False
    for line in lines:
        if line.strip() == "---" and not in_fm:
            in_fm = True
            continue
        if line.strip() == "---" and in_fm:
            in_fm = False
            continue
        if not in_fm:
            body_lines.append(line)
    count = len(body_lines)
    if count <= 600:
        return True, f"ℹ️  正文 {count} 行 ≤ 600（推荐）"
    return False, f"⚠️  正文 {count} 行 > 600，建议将 >8KB 内容移入 references/"


def validate_skill(skill_path: str, fix: bool = False) -> dict:
    """
    返回结构：
    {
      "passed": bool,
      "total_checks": int,
      "passed_checks": int,
      "failures": [{"check": str, "detail": str}],
      "warnings": [{"check": str, "detail": str}],
      "score": int  # 0-100
    }
    """
    path = Path(skill_path)
    if not path.exists():
        return {"passed": False, "error": f"文件不存在: {skill_path}"}

    content, lines = load_file(str(path))
    fm = extract_frontmatter(lines)
    skill_dir = path.parent
    body_length = len(content)

    results = []
    failures = []
    warnings = []

    # 1. frontmatter格式
    ok, msg = check_frontmatter_format(lines)
    results.append(("frontmatter格式", ok, msg))
    if not ok: failures.append({"check": "TC-SYNTAX-001", "detail": msg})

    # 2. 必需字段
    ok, msgs = check_required_fields(fm)
    results.append(("必需字段", ok, msgs[0]))
    if not ok:
        for m in msgs: failures.append({"check": "TC-SYNTAX-002", "detail": m})

    # 3. description开头
    ok, msg = check_description_starts_with_use_when(fm)
    results.append(("description开头", ok, msg))
    if not ok: failures.append({"check": "TC-SYNTAX-004", "detail": msg})

    # 4. description长度
    ok, msg = check_description_length(fm)
    results.append(("description长度", ok, msg))
    if not ok: failures.append({"check": "TC-SYNTAX-003", "detail": msg})

    # 5. references目录
    ok, msg = check_references_dir(skill_dir, body_length)
    results.append(("references目录", ok, msg))
    if not ok: failures.append({"check": "TC-SYNTAX-005", "detail": msg})

    # 6. test_pool.md命名
    ok, msg = check_test_pool_naming(skill_dir)
    results.append(("test_pool命名", ok, msg))
    if not ok: warnings.append({"check": "可维护性", "detail": msg})

    # 7. 敏感信息
    ok, msgs = check_sensitive_info(content)
    results.append(("敏感信息", ok, msgs[0]))
    if not ok:
        for m in msgs: failures.append({"check": "TC-SEC-001", "detail": m})

    # 8. 行数建议
    ok, msg = check_skill_line_count(lines)
    results.append(("行数建议", ok, msg))
    if not ok: warnings.append({"check": "建议", "detail": msg})

    passed = len([r for r in results if r[1]]) / len(results) * 100 if results else 0
    score = max(0, 100 - len(failures) * 15 - len(warnings) * 5)

    return {
        "passed": len(failures) == 0,
        "total_checks": len(results),
        "passed_checks": len([r for r in results if r[1]]),
        "failures": failures,
        "warnings": warnings,
        "score": score,
        "results": results,
    }


def print_report(report: dict):
    print("\n" + "=" * 50)
    print("📋 SKILL.md 验证报告")
    print("=" * 50)
    print(f"总分: {report['score']}/100")
    print(f"通过: {report['passed_checks']}/{report['total_checks']} 项")
    print()
    if report["failures"]:
        print("🔴 必须修复:")
        for f in report["failures"]:
            print(f"  [{f['check']}] {f['detail']}")
    if report["warnings"]:
        print("⚠️  建议修复:")
        for w in report["warnings"]:
            print(f"  [{w['check']}] {w['detail']}")
    if not report["failures"] and not report["warnings"]:
        print("✅ 全部检查通过！")
    print()


if __name__ == "__main__":
    fix = "--fix" in sys.argv
    args = [a for a in sys.argv if not a.startswith("--")]
    if len(args) < 2:
        print("用法: python validate_skill.py <SKILL.md路径> [--fix]")
        sys.exit(1)
    report = validate_skill(args[1], fix=fix)
    print_report(report)
    sys.exit(0 if report["passed"] else 1)