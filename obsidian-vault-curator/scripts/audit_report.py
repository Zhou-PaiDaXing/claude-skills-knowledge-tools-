#!/usr/bin/env python3
"""
audit_report.py — 把 scan.json + score.json 渲染成 audit/YYYY-MM-DD/ 系列 markdown 报告。

报告包含 Dataview 查询块(若用户装了 Dataview 插件,就是实时活的视图;没装也是普通代码块,无害)。

产物:
    audit/YYYY-MM-DD/
    ├── INDEX.md            ← 汇总入口
    ├── violations.md       ← 规范违规明细
    ├── orphans.md          ← 孤立笔记
    ├── broken-links.md     ← 断链
    ├── scoring.md          ← 笔记质量评分
    └── candidates.md       ← 关联候选(中信心,待人工裁决)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def write_index(audit_dir: Path, scan: dict, score: dict) -> None:
    today = dt.date.today().isoformat()
    s = scan["stats"]
    summary = score["summary"]
    content = f"""---
title: Vault Audit · {today}
aliases: [audit-{today}]
tags: [meta, audit, vault-curator]
created: {today}
audit_date: {today}
schema_version: {scan['schema_version']}
---

# 🔍 Vault Audit · {today}

> 自动生成 · obsidian-vault-curator skill · scope=`{scan['scope']}` ·
> 范围={"全量扫描" if scan['incremental_since_days'] is None else f"近 {scan['incremental_since_days']} 天增量"} · 扫描时间={scan['scanned_at']}

## 总览

| 指标 | 值 |
|------|---:|
| 笔记数 | {s['notes_scanned']} |
| 平均评分 | {summary['mean_score']} / 10 |
| ACTIVE | {summary['active']} |
| STALE | {summary['stale']} |
| ARCHIVED 候选 | {summary['archived']} |
| 孤立笔记 | {s['orphans']} |
| 断链 | {s['broken_links']} |
| 关联候选 | {s['association_candidates']} |

## 详情

- [[violations|⚠️ 规范违规]]({sum(1 for n in scan['notes'] if n['frontmatter_missing'] or n['naming_violation'])} 项)
- [[orphans|🏝️ 孤立笔记]]({s['orphans']} 项)
- [[broken-links|🔗 断链]]({s['broken_links']} 项)
- [[scoring|⭐ 评分]]({s['notes_scanned']} 项)
- [[candidates|🔮 关联候选]]({s['association_candidates']} 项)

## 实时视图(需要装 Dataview 插件)

```dataview
TABLE
  lifecycle as "状态",
  score as "评分",
  last_audit as "上次审计"
FROM ""
WHERE lifecycle != null
SORT score ASC
LIMIT 20
```

## 历史 audit 时间序列

```dataview
LIST
FROM "audit"
WHERE file.name = "INDEX"
SORT file.folder DESC
LIMIT 10
```

---

*下一轮建议:`/obsidian-curate --since=7d`*
"""
    (audit_dir / "INDEX.md").write_text(content, encoding="utf-8")


def write_violations(audit_dir: Path, scan: dict) -> None:
    today = dt.date.today().isoformat()
    lines = [f"""---
title: 规范违规 · {today}
tags: [meta, audit, violations]
created: {today}
---

# ⚠️ 规范违规

> 详见 [[VAULT-SCHEMA]]
"""]

    # frontmatter 缺失
    miss = [n for n in scan["notes"] if n["frontmatter_missing"]]
    lines.append(f"\n## Frontmatter 缺字段({len(miss)})\n")
    if miss:
        lines.append("| 笔记 | 缺失字段 |")
        lines.append("|------|----------|")
        for n in miss[:200]:
            lines.append(f"| [[{n['name']}]] | `{', '.join(n['frontmatter_missing'])}` |")
        if len(miss) > 200:
            lines.append(f"\n_(还有 {len(miss)-200} 条,完整见 scan.json)_")

    # 命名违规
    nam = [n for n in scan["notes"] if n["naming_violation"]]
    lines.append(f"\n## 命名违规({len(nam)})\n")
    if nam:
        lines.append("| 笔记 | 违规 |")
        lines.append("|------|------|")
        for n in nam:
            lines.append(f"| `{n['path']}` | {n['naming_violation']} |")

    (audit_dir / "violations.md").write_text("\n".join(lines), encoding="utf-8")


def write_orphans(audit_dir: Path, scan: dict) -> None:
    today = dt.date.today().isoformat()
    orphans = scan["orphans"]
    content = f"""---
title: 孤立笔记 · {today}
tags: [meta, audit, orphans]
created: {today}
---

# 🏝️ 孤立笔记

> 无出链、无反向链接的笔记。可能是文档岛,值得检查是否该补关联或归档。

总计:**{len(orphans)}** 项

| 笔记 | 路径 |
|------|------|
"""
    for o in orphans:
        content += f"| [[{o['name']}]] | `{o['path']}` |\n"

    if not orphans:
        content += "\n_(无孤立笔记)_\n"

    content += """

## Dataview 实时视图

```dataview
LIST file.path
FROM ""
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
SORT file.mtime DESC
```
"""
    (audit_dir / "orphans.md").write_text(content, encoding="utf-8")


def write_broken_links(audit_dir: Path, scan: dict) -> None:
    today = dt.date.today().isoformat()
    broken = scan["broken_links"]
    content = f"""---
title: 断链 · {today}
tags: [meta, audit, broken-links]
created: {today}
---

# 🔗 断链

> 引用了不存在的 [[wikilink]] 目标。可能是拼写错误、目标已删,或目标待创建。

总计:**{len(broken)}** 项

| 源笔记 | 缺失目标 |
|--------|----------|
"""
    for b in broken[:300]:
        content += f"| [[{b['source']}]] | `{b['missing_target']}` |\n"
    if len(broken) > 300:
        content += f"\n_(还有 {len(broken)-300} 条)_\n"
    if not broken:
        content += "\n_(无断链)_\n"

    (audit_dir / "broken-links.md").write_text(content, encoding="utf-8")


def write_scoring(audit_dir: Path, score: dict) -> None:
    today = dt.date.today().isoformat()
    items = score["items"]
    items_sorted = sorted(items, key=lambda x: x["score"]["total"])
    summary = score["summary"]

    content = f"""---
title: 笔记评分 · {today}
tags: [meta, audit, scoring]
created: {today}
---

# ⭐ 笔记质量评分

> 三维度加权:关联数(0.4)+ 活跃度(0.3)+ 完整度(0.3)

| 指标 | 值 |
|------|---:|
| 平均分 | {summary['mean_score']} |
| ACTIVE | {summary['active']} |
| STALE | {summary['stale']} |
| ARCHIVED 候选 | {summary['archived']} |

## 低分前 20(优先处理)

| 笔记 | 总分 | 关联 | 活跃 | 完整 | 状态 |
|------|---:|---:|---:|---:|------|
"""
    for it in items_sorted[:20]:
        s = it["score"]
        content += (f"| [[{it['name']}]] | {s['total']} | {s['relation']} | "
                    f"{s['freshness']} | {s['completeness']} | {it['lifecycle']} |\n")

    content += "\n## 高分前 10(知识库支柱)\n\n| 笔记 | 总分 | 状态 |\n|------|---:|------|\n"
    for it in sorted(items, key=lambda x: -x["score"]["total"])[:10]:
        content += f"| [[{it['name']}]] | {it['score']['total']} | {it['lifecycle']} |\n"

    content += "\n## 全量评分(Dataview 视图)\n\n```dataview\nTABLE score, lifecycle\nFROM \"\"\nWHERE score != null\nSORT score ASC\n```\n"

    (audit_dir / "scoring.md").write_text(content, encoding="utf-8")


def write_candidates(audit_dir: Path, scan: dict) -> None:
    today = dt.date.today().isoformat()
    cands = scan["association_candidates"]
    high = [c for c in cands if c["confidence"] >= 0.8]
    mid = [c for c in cands if 0.5 <= c["confidence"] < 0.8]

    content = f"""---
title: 关联候选 · {today}
tags: [meta, audit, candidates]
created: {today}
---

# 🔮 关联候选

> 高信心(≥0.8)→ `--apply` 时自动加 🧭 相关 行
> 中信心(0.5-0.8)→ 写入 [[BACKLOG#待补全的关联(横向链接)|BACKLOG]] 等人工裁决

## 高信心({len(high)})

| A | B | 共享 tag | 信心 |
|---|---|----------|---:|
"""
    for c in high[:200]:
        content += f"| [[{c['a']}]] | [[{c['b']}]] | {c['shared_tags']} | {c['confidence']} |\n"

    content += f"\n## 中信心({len(mid)})\n\n| A | B | 共享 tag | 信心 |\n|---|---|----------|---:|\n"
    for c in mid[:200]:
        content += f"| [[{c['a']}]] | [[{c['b']}]] | {c['shared_tags']} | {c['confidence']} |\n"

    (audit_dir / "candidates.md").write_text(content, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default="/tmp/vault-scan.json")
    ap.add_argument("--score", default="/tmp/vault-score.json")
    ap.add_argument("--vault", default="/Users/shideng/Documents/Obsidian Vault")
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="audit 子目录名,默认今天")
    args = ap.parse_args()

    scan = json.loads(Path(args.scan).read_text(encoding="utf-8"))
    score = json.loads(Path(args.score).read_text(encoding="utf-8"))

    audit_dir = Path(args.vault) / "audit" / args.date
    audit_dir.mkdir(parents=True, exist_ok=True)

    write_index(audit_dir, scan, score)
    write_violations(audit_dir, scan)
    write_orphans(audit_dir, scan)
    write_broken_links(audit_dir, scan)
    write_scoring(audit_dir, score)
    write_candidates(audit_dir, scan)

    print(f"[audit_report] wrote {audit_dir}/ (6 files)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
