#!/usr/bin/env python3
"""
package_skill.py — 打包技能并注册到 registry.yaml

用法：
  python package_skill.py <skill-dir> [--registry <registry.yaml路径>]
  python package_skill.py ./skill-xxx --registry ~/.hermes/skills/registry.yaml

功能：
  1. 验证 SKILL.md 通过 validate_skill.py
  2. 打包技能到 .skill 文件（可选）
  3. 更新 registry.yaml
  4. 输出最终路径
"""

import sys
import json
import shutil
import yaml
from pathlib import Path


def load_skill_meta(skill_dir: Path) -> dict:
    """从 SKILL.md frontmatter 提取 metadata"""
    fm = {}
    in_fm = False
    fm_lines = []
    with open(skill_dir / "SKILL.md", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "---" and not in_fm:
                in_fm = True
                continue
            if line.strip() == "---" and in_fm:
                break
            if in_fm and ":" in line:
                key, _, val = line.partition(":")
                fm[key.strip()] = val.strip()
    return fm


def update_registry(registry_path: Path, skill_name: str, skill_dir: Path, category: str = "general"):
    """更新 registry.yaml"""
    entry = {
        "name": skill_name,
        "path": str(skill_dir.resolve()),
        "category": category,
        "version": "1.0.0",
    }
    if registry_path.exists():
        with open(registry_path, encoding="utf-8") as f:
            registry = yaml.safe_load(f) or {}
    else:
        registry = {"skills": []}

    skills_list = registry.get("skills", [])
    # 更新已存在或新增
    existing = [i for i, s in enumerate(skills_list) if s.get("name") == skill_name]
    if existing:
        skills_list[existing[0]] = entry
    else:
        skills_list.append(entry)
    registry["skills"] = skills_list

    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        yaml.dump(registry, f, allow_unicode=True, default_flow_style=False)


def package_to_skill(skill_dir: Path, output_dir: Path) -> Path:
    """打包技能到 .skill 文件"""
    output_dir.mkdir(parents=True, exist_ok=True)
    skill_name = skill_dir.name
    output_path = output_dir / f"{skill_name}.skill"

    # 简单打包：复制整个目录到 .skill.tar.gz
    import tarfile
    tar_path = output_path.with_suffix(".skill.tar.gz")
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(skill_dir, arcname=skill_name)

    # 写 manifest
    manifest = {
        "name": skill_name,
        "packed_at": str(Path(tar_path).resolve()),
        "files": [str(f.relative_to(skill_dir)) for f in skill_dir.rglob("*") if f.is_file()],
    }
    manifest_path = output_path.with_suffix(".manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return tar_path


if __name__ == "__main__":
    args = [a for a in sys.argv if not a.startswith("--")]
    flags = {k: v for k, v in zip(sys.argv[1:], sys.argv[2:] + [""]) if k.startswith("--")}

    if len(args) < 2:
        print("用法: python package_skill.py <skill-dir> [--registry <path>]")
        sys.exit(1)

    skill_dir = Path(args[1]).resolve()
    if not skill_dir.exists():
        print(f"❌ 技能目录不存在: {skill_dir}")
        sys.exit(1)

    registry_path = Path(flags.get("--registry", str(Path.home() / ".hermes/skills/registry.yaml")))

    # 提取 metadata
    fm = load_skill_meta(skill_dir)
    skill_name = fm.get("name", skill_dir.name)
    category = "general"
    if "hermes" in fm:
        # 从 metadata.hermes.tags 推断 category
        tags_str = fm.get("hermes", "")
        for tag in ["productivity", "development", "security", "devops"]:
            if tag in tags_str:
                category = tag
                break

    # 验证
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from validate_skill import validate_skill
    report = validate_skill(str(skill_dir / "SKILL.md"))
    if not report["passed"]:
        print("❌ SKILL.md 验证未通过，打包中止：")
        for f in report["failures"]:
            print(f"  [{f['check']}] {f['detail']}")
        sys.exit(1)
    print(f"✅ SKILL.md 验证通过")

    # 更新 registry
    update_registry(registry_path, skill_name, skill_dir, category)
    print(f"✅ registry.yaml 已更新: {registry_path}")

    # 打包
    try:
        tar_path = package_to_skill(skill_dir, Path.home() / "Downloads")
        print(f"✅ 技能已打包: {tar_path}")
    except Exception as e:
        print(f"⚠️  打包失败（不影响注册）: {e}")

    print(f"\n📦 技能名称: {skill_name}")
    print(f"📂 技能路径: {skill_dir}")
    print(f"📋 注册表: {registry_path}")