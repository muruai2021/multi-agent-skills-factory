#!/usr/bin/env python3
"""
aggregate_score.py — 聚合多轮评审分数，自动决策是否达标

用法：
  python aggregate_score.py <iteration-dir>
  python aggregate_score.py <iteration-dir> --report

示例：
  python aggregate_score.py ./iteration-1
  python aggregate_score.py ./iteration-1 --report

输出：
  benchmark.json  — 聚合统计
  benchmark.md   — 可读报告
  PASS/FAIL 决策
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def load_gradings(iteration_dir: Path) -> list[dict]:
    """扫描 iteration 目录，收集所有 grading.json"""
    gradings = []
    for grader_dir in sorted(iteration_dir.iterdir()):
        if not grader_dir.is_dir():
            continue
        g = grader_dir / "grading.json"
        if g.exists():
            with open(g, encoding="utf-8") as f:
                gradings.append(json.load(f))
    return gradings


def compute_stats(gradings: list[dict]) -> dict:
    """计算各维度的均值、标准差"""
    dims = ["完整性", "正确性", "易用性", "安全性", "可维护性"]
    stats = {}
    for dim in dims:
        scores = [g["total_score"] for g in gradings]
        if not scores:
            continue
        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        stddev = variance ** 0.5
        stats[dim] = {
            "mean": round(avg, 2),
            "stddev": round(stddev, 2),
            "scores": scores,
        }
    return stats


def decide_pass(total_score: float) -> tuple[bool, str]:
    if total_score >= 90:
        return True, "优秀，直接上线"
    elif total_score >= 75:
        return True, "良好，小修小补后上线"
    elif total_score >= 60:
        return False, "需修改，退回开发者"
    else:
        return False, "不合格，重做"


def generate_benchmark(iteration_dir: Path, gradings: list[dict]) -> dict:
    """生成 benchmark.json"""
    if not gradings:
        return {}
    total_scores = [g["total_score"] for g in gradings]
    avg_total = sum(total_scores) / len(total_scores)
    benchmark = {
        "iteration": iteration_dir.name,
        "timestamp": datetime.now().isoformat(),
        "num_evals": len(gradings),
        "total_score": round(avg_total, 2),
        "scores": total_scores,
        "pass": avg_total >= 75,
        "grade": "优秀" if avg_total >= 90 else "良好" if avg_total >= 75 else "需修改" if avg_total >= 60 else "不合格",
        "dimensions": {},
    }
    dims = ["完整性", "正确性", "易用性", "安全性", "可维护性"]
    weights = [0.25, 0.25, 0.20, 0.20, 0.10]
    for dim, w in zip(dims, weights):
        scores = [g["dimensions"][i]["score"] for i, d in enumerate(g["dimensions"]) if d["name"] == dim]
        if scores:
            benchmark["dimensions"][dim] = {
                "mean": round(sum(scores) / len(scores), 2),
                "scores": scores,
                "weight": w,
            }
    return benchmark


def generate_markdown(benchmark: dict) -> str:
    """生成可读报告"""
    md = f"""# 评审聚合报告 — {benchmark.get('iteration', 'N/A')}

**时间**：{benchmark.get('timestamp', 'N/A')}
**评测数量**：{benchmark.get('num_evals', 0)}
**总分**：{benchmark.get('total_score', 'N/A')} / 100
**等级**：{benchmark.get('grade', 'N/A')}
**通过**：{'✅ 是' if benchmark.get('pass') else '❌ 否'}

## 各维度得分

| 维度 | 均值 | 满分 | 权重 |
|------|------|------|------|
"""
    for dim, data in benchmark.get("dimensions", {}).items():
        md += f"| {dim} | {data['mean']} | 20 | {int(data['weight']*100)}% |\n"
    md += f"""
## 决策

总分 {benchmark.get('total_score', 'N/A')} → **{benchmark.get('grade', 'N/A')}**

"""
    if benchmark.get("pass"):
        md += "✅ **通过** — 可以注册上线"
    else:
        md += "❌ **未通过** — 退回开发者修改"
    return md


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python aggregate_score.py <iteration-dir> [--report]")
        sys.exit(1)

    iteration_dir = Path(sys.argv[1])
    if not iteration_dir.exists():
        print(f"❌ 目录不存在: {iteration_dir}")
        sys.exit(1)

    gradings = load_gradings(iteration_dir)
    if not gradings:
        print("❌ 未找到 grading.json 文件")
        sys.exit(1)

    benchmark = generate_benchmark(iteration_dir, gradings)

    # 保存 benchmark.json
    with open(iteration_dir / "benchmark.json", "w", encoding="utf-8") as f:
        json.dump(benchmark, f, ensure_ascii=False, indent=2)

    # 保存 benchmark.md
    md = generate_markdown(benchmark)
    with open(iteration_dir / "benchmark.md", "w", encoding="utf-8") as f:
        f.write(md)

    print(md)
    print(f"\n📁 已保存: {iteration_dir / 'benchmark.json'}")
    print(f"📁 已保存: {iteration_dir / 'benchmark.md'}")

    pass_flag, msg = decide_pass(benchmark["total_score"])
    print(f"\n{'✅' if pass_flag else '❌'} 决策: {msg}")