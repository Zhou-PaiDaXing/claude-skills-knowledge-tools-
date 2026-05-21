#!/usr/bin/env python3
"""
auto_fix.py — 基于 scan.json 做机械修复 + 写 BACKLOG.md。

默认 dry-run,显示将要做的改动;加 --apply 才真改文件。

修复内容(中等严格度):
1. frontmatter 缺 title/created → 自动补(title=文件名,created=git first commit 或 mtime)
2. frontmatter 缺 updated → 用 mtime
3. 命名违规 → 写候选到 BACKLOG.md,等人工拍板(不自动改名)
4. 关联候选(信心 ≥0.8) → apply 模式下追加 `🧭 相关:` 行
5. 关联候选(信心 0.5-0.8) → 写到 BACKLOG.md
6. 断链 → 写到 BACKLOG.md
7. 孤立笔记 → 写到 BACKLOG.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^(---\n)(.*?)(\n---\n)", re.DOTALL)
HIGH_CONFIDENCE = 0.8


def git_first_commit_date(vault: Path, rel_path: str) -> str | None:
    try:
        r = subprocess.run(
            ["git", "-C", str(vault), "log", "--diff-filter=A", "--follow",
             "--format=%cs", "--", rel_path],
            capture_output=True, text=True, timeout=5
        )
        lines = [l for l in r.stdout.splitlines() if l.strip()]
        return lines[-1] if lines else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def ensure_frontmatter(note: dict, vault: Path) -> tuple[str, dict]:
    """返回 (new_text, applied_changes)。"""
    abs_path = vault / note["path"]
    text = abs_path.read_text(encoding="utf-8", errors="replace")
    fm_match = FRONTMATTER_RE.match(text)
    changes: dict = {}

    missing = note["frontmatter_missing"]
    if not missing:
        return text, changes

    # 准备要补的值
    additions: dict[str, str] = {}
    if "title" in missing:
        additions["title"] = note["name"]
    if "created" in missing:
        created = git_first_commit_date(vault, note["path"])
        if not created:
            created = note["mtime"][:10]
        additions["created"] = created
    if "tags" in missing:
        # 用目录名做兜底 tag
        dir_parts = Path(note["path"]).parts
        if len(dir_parts) > 1:
            additions["tags"] = f'[{dir_parts[-2]}]'
        else:
            additions["tags"] = "[]"
    if "updated" in missing:
        additions["updated"] = note["mtime"][:10]

    if fm_match:
        fm_body = fm_match.group(2)
        new_lines = fm_body.splitlines()
        for k, v in additions.items():
            new_lines.append(f"{k}: {v}")
        new_fm = "---\n" + "\n".join(new_lines) + "\n---\n"
        new_text = new_fm + text[fm_match.end():]
    else:
        fm_lines = ["---"]
        for k, v in additions.items():
            fm_lines.append(f"{k}: {v}")
        fm_lines.append("---\n")
        new_text = "\n".join(fm_lines) + "\n" + text

    changes["frontmatter_added"] = additions
    return new_text, changes


def append_related_links(note_path: Path, related_names: list[str]) -> bool:
    """在第一个 `> ` 引用块附近追加 🧭 相关 行;若已存在则合并。"""
    text = note_path.read_text(encoding="utf-8", errors="replace")
    related_str = "🧭 相关:" + " · ".join(f"[[{n}]]" for n in related_names)
    if "🧭 相关:" in text:
        # 已有,合并(简单做法:不重复加)
        existing = re.search(r"🧭 相关:.*", text)
        if existing:
            existing_links = set(re.findall(r"\[\[([^|\]]+)", existing.group(0)))
            new_links = [n for n in related_names if n not in existing_links]
            if not new_links:
                return False
            insertion = " · " + " · ".join(f"[[{n}]]" for n in new_links)
            new_text = text.replace(existing.group(0), existing.group(0) + insertion, 1)
            note_path.write_text(new_text, encoding="utf-8")
            return True
        return False
    # 没有 🧭 行,插到 frontmatter 之后第一个空行处
    fm_match = FRONTMATTER_RE.match(text)
    insert_pos = fm_match.end() if fm_match else 0
    new_text = text[:insert_pos] + f"\n> {related_str}\n" + text[insert_pos:]
    note_path.write_text(new_text, encoding="utf-8")
    return True


def update_backlog(vault: Path, scan: dict, mid_candidates: list[dict]) -> int:
    backlog = vault / "BACKLOG.md"
    if not backlog.exists():
        return 0
    text = backlog.read_text(encoding="utf-8", errors="replace")
    today = dt.date.today().isoformat()

    new_entries = {
        "## 待补全的关联(横向链接)": [],
        "## 待补 Frontmatter": [],
        "## 断链": [],
        "## 孤立笔记(零关联)": [],
    }

    for c in mid_candidates:
        line = (f"- [ ] [[{c['a']}]] 与 [[{c['b']}]] 共享 tag {c['shared_tags']} — "
                f"建议加 🧭 相关 — 信心 {c['confidence']} — 发现于 {today}")
        new_entries["## 待补全的关联(横向链接)"].append(line)

    for n in scan["notes"]:
        if n["frontmatter_missing"]:
            line = f"- [ ] [[{n['name']}]] 缺字段:{n['frontmatter_missing']} — 信心 1.0(自动修候选) — {today}"
            new_entries["## 待补 Frontmatter"].append(line)

    for b in scan["broken_links"]:
        line = f"- [ ] [[{b['source']}]] 引用 [[{b['missing_target']}]] 但目标不存在 — {today}"
        new_entries["## 断链"].append(line)

    for o in scan["orphans"]:
        line = f"- [ ] [[{o['name']}]] 无任何关联 — {today}"
        new_entries["## 孤立笔记(零关联)"].append(line)

    total_added = sum(len(v) for v in new_entries.values())
    if total_added == 0:
        return 0

    # 在每个 section 后追加;先去重(同一条已存在则跳过)
    new_text = text
    for section, entries in new_entries.items():
        if section not in new_text:
            continue
        # 已存在的简单去重(用 [[A]]...[[B]] 二元组判断)
        section_pos = new_text.find(section)
        next_section = new_text.find("\n## ", section_pos + len(section))
        section_block = new_text[section_pos:next_section] if next_section > 0 else new_text[section_pos:]
        filtered = []
        for line in entries:
            key = re.findall(r"\[\[([^|\]]+)", line)
            key_str = "|".join(key)
            if key_str and key_str not in section_block:
                filtered.append(line)
        if not filtered:
            continue
        # 在 section 后第一条 - [ ] 出现处之前插入 / 或 section 末尾
        insertion = "\n" + "\n".join(filtered)
        # 插在 section 标题后第一段(_(skill 首次运行后自动填充)_ 之后或 ---  之前)
        anchor = "(skill 首次运行后自动填充)_"
        if anchor in section_block:
            new_text = new_text.replace(anchor, anchor + insertion, 1)
        else:
            # fallback: append before next ---
            relative_end = section_block.rfind("\n---")
            if relative_end > 0:
                global_end = section_pos + relative_end
                new_text = new_text[:global_end] + insertion + new_text[global_end:]
            else:
                new_text += insertion

    new_text = re.sub(
        r"\*由 obsidian-vault-curator skill 自动维护 · 上次更新:.*?\*",
        f"*由 obsidian-vault-curator skill 自动维护 · 上次更新:{today}*",
        new_text,
    )
    backlog.write_text(new_text, encoding="utf-8")
    return total_added


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="/tmp/vault-scan.json")
    ap.add_argument("--apply", action="store_true", help="真改文件,否则 dry-run")
    ap.add_argument("--frontmatter-only", action="store_true",
                    help="--apply 时只补 frontmatter,跳过关联和 BACKLOG")
    ap.add_argument("--no-links", action="store_true", help="跳过高信心关联自动加")
    ap.add_argument("--no-backlog", action="store_true", help="跳过 BACKLOG 写入")
    args = ap.parse_args()

    scan = json.loads(Path(args.input).read_text(encoding="utf-8"))
    vault = Path(scan["vault"])

    fm_fix_count = 0
    link_fix_count = 0
    backlog_count = 0

    # 1. frontmatter 自动修
    for n in scan["notes"]:
        if not n["frontmatter_missing"]:
            continue
        new_text, changes = ensure_frontmatter(n, vault)
        if changes:
            fm_fix_count += 1
            if args.apply:
                (vault / n["path"]).write_text(new_text, encoding="utf-8")

    # 2. 关联候选自动加(信心 ≥0.8)
    high_candidates = [c for c in scan["association_candidates"]
                       if c["confidence"] >= HIGH_CONFIDENCE]
    mid_candidates = [c for c in scan["association_candidates"]
                      if c["confidence"] < HIGH_CONFIDENCE]

    skip_links = args.frontmatter_only or args.no_links
    skip_backlog = args.frontmatter_only or args.no_backlog

    if args.apply and not skip_links:
        # 按 a 聚合
        from collections import defaultdict
        by_a: dict[str, list[str]] = defaultdict(list)
        for c in high_candidates:
            by_a[c["a"]].append(c["b"])
        # 找 a 的 path
        name_to_path = {n["name"]: n["path"] for n in scan["notes"]}
        for a_name, related in by_a.items():
            ap_path = name_to_path.get(a_name)
            if not ap_path:
                continue
            if append_related_links(vault / ap_path, related):
                link_fix_count += 1

    # 3. 写 BACKLOG.md
    if args.apply and not skip_backlog:
        backlog_count = update_backlog(vault, scan, mid_candidates)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[auto_fix {mode}] frontmatter_fix={fm_fix_count}/{len(scan['notes'])} · "
          f"links_auto_added={link_fix_count} · BACKLOG_appended={backlog_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
