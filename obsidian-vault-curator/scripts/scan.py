#!/usr/bin/env python3
"""
scan.py — 扫描 Obsidian vault,输出违规清单 + 关联候选。

用法:
    python scan.py --vault PATH [--since 7d|--full] [--scope SUBDIR] [-o OUTPUT.json]

输出 JSON 结构(给 score.py / auto_fix.py / audit_report.py 消费):
    {
      "scanned_at": "2026-05-21T10:30:00",
      "vault": "/path/to/vault",
      "scope": "...",
      "schema_version": "1.0",
      "notes": [
        {
          "path": "personal/ai-tech/.../foo.md",
          "name": "foo",
          "frontmatter": {"title": "...", "tags": [...], ...},
          "frontmatter_missing": ["created"],
          "wikilinks_out": ["bar", "baz#章节"],
          "wikilinks_in": [],          # 由后处理填充
          "naming_violation": null|"...",
          "size_bytes": 1234,
          "word_count": 567,
          "has_todo": true,
          "mtime": "2026-05-20T..."
        },
        ...
      ],
      "broken_links": [...],
      "orphans": [...],
      "association_candidates": [...]  # 跨笔记词频/tag 共现产生的候选
    }
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# ────────────────────────── 解析 SCHEMA ──────────────────────────
# 通用默认 exempt(不含任何业务/个人特定路径)。
# 用户特定路径(如 personal/journal/、work/、business-kb/ 等)请在 VAULT-SCHEMA.md §9 加入。
DEFAULT_EXEMPT_PATHS = [
    ".obsidian/",
    ".trash/",
    ".git/",
    "node_modules/",
    "archive/",
    "audit/",  # audit/ 自身不参与扫描(skill 自产)
]
DEFAULT_EXEMPT_FILES = {"HOME.md", "VAULT-SCHEMA.md", "BACKLOG.md"}
REQUIRED_FRONTMATTER = ["title", "tags", "created"]
ANALYSIS_REQUIRED_EXTRA = ["github", "version_analyzed"]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TODO_RE = re.compile(r"^\s*-\s*\[\s*\]\s+", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--vault",
        default="/Users/shideng/Documents/Obsidian Vault",
        help="vault 根目录",
    )
    ap.add_argument(
        "--since",
        default=None,
        help="只扫最近 N 天(如 7d / 30d);不传默认 7d,与 --full 互斥",
    )
    ap.add_argument("--full", action="store_true", help="全 vault 扫描")
    ap.add_argument("--scope", default="", help="限定子目录,如 personal/")
    ap.add_argument("-o", "--output", default="/tmp/vault-scan.json")
    return ap.parse_args()


def parse_since(s: str | None, default_days: int = 7) -> int:
    """'7d'/'30d' → days int"""
    if not s:
        return default_days
    m = re.match(r"^(\d+)\s*d?$", s.strip())
    if not m:
        raise SystemExit(f"--since 格式错误: {s!r}, 应为 '7d' 之类")
    return int(m.group(1))


def parse_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    raw = m.group(1)
    # 极简 YAML 解析(只处理 key: value / key: [a, b] / key: 多行块);避免引入依赖
    fm: dict = {}
    cur_key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith(" ") or line.startswith("\t"):
            # 续行(数组项或多行块)
            if cur_key is not None:
                v = line.strip()
                if v.startswith("- "):
                    fm.setdefault(cur_key, []).append(v[2:].strip())
                else:
                    if isinstance(fm.get(cur_key), str):
                        fm[cur_key] += " " + v
        else:
            if ":" not in line:
                continue
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            cur_key = k
            if v == "":
                fm[k] = []
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1]
                fm[k] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
            else:
                fm[k] = v.strip("'\"")
    return fm


def load_schema_exempt(vault: Path) -> tuple[list[str], set[str]]:
    """从 VAULT-SCHEMA.md 提取 exempt_paths 和 exempt_files,合并 skill 内置默认。"""
    paths = list(DEFAULT_EXEMPT_PATHS)
    files = set(DEFAULT_EXEMPT_FILES)
    schema = vault / "VAULT-SCHEMA.md"
    if not schema.exists():
        return paths, files
    text = schema.read_text(encoding="utf-8", errors="replace")
    # 找 exempt_paths: 和 exempt_files: 块(简易解析,只支持 `  - foo/**` 行格式)
    in_paths_block = in_files_block = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("exempt_paths:"):
            in_paths_block, in_files_block = True, False
            continue
        if s.startswith("exempt_files:"):
            in_paths_block, in_files_block = False, True
            continue
        # 退出 block:遇到非缩进非空非注释行
        if not (line.startswith(" ") or line.startswith("\t")):
            if s and not s.startswith("#"):
                in_paths_block = in_files_block = False
        if (in_paths_block or in_files_block) and s.startswith("- "):
            val = s[2:].strip().split("#", 1)[0].strip().strip("'\"")
            if not val:
                continue
            if in_paths_block:
                # 把 glob `foo/**` 归一为前缀 `foo/`
                val = val.replace("/**", "/").rstrip("*")
                if val and val not in paths:
                    paths.append(val)
            else:
                files.add(val)
    return paths, files


def find_md_files(vault: Path, scope: str, since_days: int | None,
                  exempt_paths: list[str]) -> list[Path]:
    base = vault / scope if scope else vault
    if not base.exists():
        raise SystemExit(f"--scope 不存在: {base}")

    paths: list[Path] = []
    cutoff = (
        dt.datetime.now() - dt.timedelta(days=since_days) if since_days else None
    )
    for p in base.rglob("*.md"):
        rel = p.relative_to(vault).as_posix()
        if any(rel.startswith(ex) for ex in exempt_paths):
            continue
        if cutoff:
            mtime = dt.datetime.fromtimestamp(p.stat().st_mtime)
            if mtime < cutoff:
                continue
        paths.append(p)
    return paths


def is_exempt_file(path: Path, vault: Path, exempt_paths: list[str],
                   exempt_files: set[str]) -> bool:
    rel = path.relative_to(vault).as_posix()
    return path.name in exempt_files or any(
        rel.startswith(ex) for ex in exempt_paths
    )


# ────────────────────────── 规则检查 ──────────────────────────
def check_naming(name: str, parent_dir: str) -> str | None:
    """命名规范检查,返回违规描述或 None。"""
    if " " in name and not re.match(r"^\d+(\.\d+)*\s", name):
        # 允许章节编号开头的空格,如 "2.1 Tool Registry .md"
        return f"文件名含空格但不符合编号格式: {name}"
    for ch in "?*:":
        if ch in name:
            return f"文件名含非法字符 {ch!r}: {name}"
    return None


def check_frontmatter(fm: dict | None, path: Path) -> list[str]:
    """返回缺失的必填字段。"""
    if fm is None:
        return REQUIRED_FRONTMATTER.copy()
    missing = [k for k in REQUIRED_FRONTMATTER if k not in fm or fm[k] in ("", [], None)]
    # 分析类追加要求
    if path.name.endswith("-analysis.md"):
        for k in ANALYSIS_REQUIRED_EXTRA:
            if k not in fm:
                missing.append(k)
    return missing


def extract_wikilinks(text: str) -> list[str]:
    """提取 [[...]] 内容(去掉 frontmatter 部分)。"""
    body = FRONTMATTER_RE.sub("", text, count=1)
    return [m.group(1) for m in WIKILINK_RE.finditer(body)]


# ────────────────────────── 主流程 ──────────────────────────
def main() -> int:
    args = parse_args()
    vault = Path(args.vault).expanduser().resolve()
    if not vault.exists():
        raise SystemExit(f"vault 不存在: {vault}")

    exempt_paths, exempt_files = load_schema_exempt(vault)
    since_days = None if args.full else parse_since(args.since)
    md_paths = find_md_files(vault, args.scope, since_days, exempt_paths)

    notes_data = []
    all_names: set[str] = set()  # 用于断链检测
    name_to_path: dict[str, str] = {}

    for p in md_paths:
        if is_exempt_file(p, vault, exempt_paths, exempt_files):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        wikilinks = extract_wikilinks(text)
        name = p.stem
        all_names.add(name)
        name_to_path[name] = p.relative_to(vault).as_posix()
        stat = p.stat()
        notes_data.append(
            {
                "path": p.relative_to(vault).as_posix(),
                "name": name,
                "frontmatter": fm or {},
                "frontmatter_missing": check_frontmatter(fm, p),
                "wikilinks_out": wikilinks,
                "naming_violation": check_naming(p.name, p.parent.name),
                "size_bytes": stat.st_size,
                "word_count": len(text.split()),
                "has_todo": bool(TODO_RE.search(text)),
                "mtime": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            }
        )

    # 反向链接 + 断链
    inbound: dict[str, list[str]] = defaultdict(list)
    broken: list[dict] = []
    for note in notes_data:
        for link in note["wikilinks_out"]:
            # 去掉 #anchor 和 |alias
            target = link.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            if target in all_names:
                inbound[target].append(note["name"])
            elif not target.startswith(("http", "/")):
                # 在做增量扫描时,目标可能不在本次扫描集中。需要全 vault 已知名单
                broken.append({"source": note["name"], "missing_target": target})

    # 全 vault 名单(用于增量扫描下的断链精度)
    if not args.full:
        all_md = list(vault.rglob("*.md"))
        global_names = {p.stem for p in all_md
                        if not is_exempt_file(p, vault, exempt_paths, exempt_files)}
        broken = [b for b in broken if b["missing_target"] not in global_names]

    for note in notes_data:
        note["wikilinks_in"] = inbound.get(note["name"], [])

    # 孤立笔记
    orphans = [
        {"name": n["name"], "path": n["path"]}
        for n in notes_data
        if not n["wikilinks_out"] and not n["wikilinks_in"]
    ]

    # 关联候选(简易版:同目录、共享 ≥2 个 tag,但还没互相链接)
    candidates: list[dict] = []
    by_dir: dict[str, list[dict]] = defaultdict(list)
    for n in notes_data:
        by_dir[str(Path(n["path"]).parent)].append(n)
    for dir_notes in by_dir.values():
        if len(dir_notes) < 2:
            continue
        for i, a in enumerate(dir_notes):
            a_tags = set(a["frontmatter"].get("tags", []) or [])
            a_links = {l.split("|")[0].split("#")[0] for l in a["wikilinks_out"]}
            for b in dir_notes[i + 1 :]:
                b_tags = set(b["frontmatter"].get("tags", []) or [])
                shared = a_tags & b_tags
                if len(shared) >= 2 and b["name"] not in a_links and a["name"] not in {
                    l.split("|")[0].split("#")[0] for l in b["wikilinks_out"]
                }:
                    confidence = min(0.95, 0.5 + 0.1 * len(shared))
                    candidates.append(
                        {
                            "a": a["name"],
                            "b": b["name"],
                            "shared_tags": sorted(shared),
                            "confidence": round(confidence, 2),
                            "reason": f"同目录 + 共享 {len(shared)} tag",
                        }
                    )

    result = {
        "scanned_at": dt.datetime.now().isoformat(timespec="seconds"),
        "vault": str(vault),
        "scope": args.scope or "<entire vault>",
        "incremental_since_days": since_days,
        "schema_version": "1.0",
        "stats": {
            "notes_scanned": len(notes_data),
            "broken_links": len(broken),
            "orphans": len(orphans),
            "association_candidates": len(candidates),
        },
        "notes": notes_data,
        "broken_links": broken,
        "orphans": orphans,
        "association_candidates": candidates,
    }

    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[scan] {len(notes_data)} notes scanned · {len(orphans)} orphans · "
          f"{len(broken)} broken · {len(candidates)} candidates → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
