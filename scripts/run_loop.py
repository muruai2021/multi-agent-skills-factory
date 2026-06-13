#!/usr/bin/env python3
"""
run_loop.py — 迭代循环控制器

用法：
  python run_loop.py <skill-name> <max-rounds>
  python run_loop.py skill-xxx 6

控制流程：
  第N轮：开发 → 验证 → 测试 → 评审（评分：X）
            ↓
         X < 75？
            ↓ 是
        第N+1轮（如果 N < max-rounds）
            ↓ 否
         ✅ 注册上线

到达 max-rounds 且仍未达标 → 交付当前最高分版本，说明未达标原因
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime


def run_developer_phase(skill_name: str, spec: dict, round_num: int) -> Path:
    """
    主编调度开发者编写 SKILL.md
    返回 SKILL.md 路径
    """
    skill_dir = Path(f"skills/{skill_name}")
    skill_dir.mkdir(parents=True, exist_ok=True)
    # 这里实际由 Agent 执行，脚本只负责创建目录结构
    print(f"  📁 技能目录: {skill_dir}")
    return skill_dir / "SKILL.md"


def run_validate(skill_md_path: Path) -> dict:
    """运行 validate_skill.py"""
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/validate_skill.py", str(skill_md_path)],
        capture_output=True, text=True,
        cwd=skill_md_path.parent.parent.parent,
    )
    # 解析输出
    passed = result.returncode == 0
    return {"passed": passed, "output": result.stdout + result.stderr}


def run_grader(skill_md_path: Path) -> dict:
    """
    运行评审打分
    实际由评审员Agent执行，这里返回占位结构
    """
    return {
        "total_score": 0,
        "pass": False,
        "grade": "待评审",
        "dimensions": [],
    }


def decide_action(score: float, round_num: int, max_rounds: int) -> tuple[str, bool]:
    """
    根据分数决策：继续迭代 / 上线 / 退出
    返回 (action, should_continue)
    """
    if score >= 90:
        return "上线", False
    elif score >= 75:
        return "小修后上线", False
    elif round_num >= max_rounds:
        return "达到上限，交付当前版本", False
    else:
        return f"退回修改（第{round_num+1}轮）", True


def main():
    if len(sys.argv) < 3:
        print("用法: python run_loop.py <skill-name> <max-rounds>")
        sys.exit(1)

    skill_name = sys.argv[1]
    max_rounds = int(sys.argv[2])

    print(f"🔄 启动迭代循环: {skill_name}（最多 {max_rounds} 轮）\n")

    iteration = 1
    best_score = 0
    best_path = None
    history = []

    while True:
        print("=" * 50)
        print(f"📌 第 {iteration} 轮开始")
        print("=" * 50)

        skill_dir = Path(f"skills/{skill_name}")
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.exists():
            print(f"❌ SKILL.md 不存在: {skill_md}")
            break

        # 验证
        print("🔍 运行 validate_skill.py...")
        val = run_validate(skill_md)
        print(f"  验证结果: {'✅ 通过' if val['passed'] else '❌ 未通过'}")

        # 评审
        print("📋 运行评审...")
        grading = run_grader(skill_md)
        score = grading.get("total_score", 0)
        passed = grading.get("pass", False)
        grade = grading.get("grade", "待评审")

        print(f"  评审得分: {score}/100 ({grade})")

        action, should_continue = decide_action(score, iteration, max_rounds)
        print(f"  决策: {action}")

        history.append({
            "round": iteration,
            "score": score,
            "grade": grade,
            "passed": passed,
            "action": action,
            "timestamp": datetime.now().isoformat(),
        })

        if not should_continue:
            print(f"\n🏁 循环结束（{action}）")
            break

        if iteration >= max_rounds:
            print(f"\n🏁 达到最大轮次 {max_rounds}，退出")
            break

        iteration += 1

    # 保存历史
    history_path = Path(f"skills/{skill_name}/iteration_history.json")
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump({"skill": skill_name, "rounds": history}, f, ensure_ascii=False, indent=2)

    print(f"\n📊 迭代历史已保存: {history_path}")
    print("\n轮次回顾:")
    for h in history:
        print(f"  第{h['round']}轮: {h['score']}/100 ({h['grade']}) — {h['action']}")


if __name__ == "__main__":
    main()