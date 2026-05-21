#!/usr/bin/env python3
"""
score.py — 基于 scan.py 输出,做三维评分 + lifecycle 状态机判定。

输入: scan.json (from scan.py)
输出: score.json
    {
      "scored_at": "...",
      "items": [
        {
          "name": "...", "path": "...",
          "score": {"relation": x, "freshness": x, "completeness": x, "total": x},
          "lifecycle": "ACTIVE|STALE|ARCHIVED",
          "lifecycle_reason": "..."
        },
        ...
      ],
      "summary": {"mean_score": x, "active": n, "stale": n, "archived": n}
    }
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

WEIGHTS = {"relation": 0.4, "freshness": 0.3, "completeness": 0.3}
STALE_AFTER_DAYS = 30
STALE_SCORE_THRESHOLD = 5.0
ARCHIVED_AFTER_DAYS = 90

# 写回 frontmatter 的三个 skill 管控字段
WRITE_BACK_KEYS = ("score", "lifecycle", "last_audit")
FRONTMATTER_RE = re.compile(r"^(---\n)(.*?)(\n---\n)", re.DOTALL)


def write_score_to_frontmatter(note_path: Path, score_total: float,
                                lifecycle: str, last_audit: str) -> bool:
    """更新或追加 score / lifecycle / last_audit 到笔记 frontmatter。
    返回是否真的改了文件(避免无意义的 mtime 抖动)。"""
    text = note_path.read_text(encoding="utf-8", errors="replace")
    new_values = {
        "score": f"{score_total}",
        "lifecycle": lifecycle,
        "last_audit": last_audit,
    }

    m = FRONTMATTER_RE.match(text)
    if m:
        fm_body = m.group(2)
        lines = fm_body.splitlines()
        # 替换已存在的 key
        changed = False
        seen = set()
        for i, line in enumerate(lines):
            for k, v in new_values.items():
                if re.match(rf"^\s*{re.escape(k)}\s*:", line):
                    new_line = f"{k}: {v}"
                    if line != new_line:
                        lines[i] = new_line
                        changed = True
                    seen.add(k)
                    break
        # 追加未存在的 key
        for k, v in new_values.items():
            if k not in seen:
                lines.append(f"{k}: {v}")
                changed = True
        if not changed:
            return False
        new_fm = "---\n" + "\n".join(lines) + "\n---\n"
        new_text = new_fm + text[m.end():]
    else:
        # 无 frontmatter,创建一个最小的
        fm_lines = ["---"] + [f"{k}: {v}" for k, v in new_values.items()] + ["---\n"]
        new_text = "\n".join(fm_lines) + "\n" + text

    note_path.write_text(new_text, encoding="utf-8")
    return True


def score_relation(out_n: int, in_n: int) -> float:
    return min(10.0, out_n * 0.5 + in_n * 1.0)


def score_freshness(mtime_iso: str, now: dt.datetime) -> float:
    mt = dt.datetime.fromisoformat(mtime_iso)
    days = (now - mt).total_seconds() / 86400
    return max(0.0, 10.0 - days / 30.0 * 10.0)  # 30 天衰减到 0


def score_completeness(note: dict) -> float:
    pts = 0.0
    if not note["frontmatter_missing"]:
        pts += 3.0
    if not note["has_todo"]:
        pts += 3.0
    if note["word_count"] > 500:
        pts += 4.0
    elif note["word_count"] > 100:
        pts += 2.0
    return pts


def decide_lifecycle(score_total: float, mtime_iso: str, now: dt.datetime,
                     current: str | None) -> tuple[str, str]:
    mt = dt.datetime.fromisoformat(mtime_iso)
    days_since = (now - mt).days
    # 人工标 ACTIVE 强制覆盖
    if current == "ACTIVE":
        return "ACTIVE", "frontmatter.lifecycle=ACTIVE 人工锁定"
    if days_since >= ARCHIVED_AFTER_DAYS and current == "STALE":
        return "ARCHIVED", f"{days_since} 天未访问 (≥{ARCHIVED_AFTER_DAYS}) 且已 STALE"
    if days_since >= STALE_AFTER_DAYS and score_total < STALE_SCORE_THRESHOLD:
        return "STALE", f"{days_since} 天未更新 (≥{STALE_AFTER_DAYS}) 且评分 {score_total:.1f}<{STALE_SCORE_THRESHOLD}"
    return "ACTIVE", f"{days_since} 天前更新 / 评分 {score_total:.1f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="/tmp/vault-scan.json")
    ap.add_argument("-o", "--output", default="/tmp/vault-score.json")
    ap.add_argument("--apply", action="store_true",
                    help="把 score/lifecycle/last_audit 写回笔记 frontmatter (默认只算不写)")
    ap.add_argument("--vault", default=None,
                    help="vault 根目录,不传则从 scan.json 的 vault 字段读")
    args = ap.parse_args()

    scan = json.loads(Path(args.input).read_text(encoding="utf-8"))
    now = dt.datetime.now()
    vault = Path(args.vault) if args.vault else Path(scan["vault"])
    today = now.date().isoformat()
    items = []
    active = stale = archived = 0
    total_sum = 0.0

    for n in scan["notes"]:
        rel = score_relation(len(n["wikilinks_out"]), len(n["wikilinks_in"]))
        fre = score_freshness(n["mtime"], now)
        com = score_completeness(n)
        total = round(
            WEIGHTS["relation"] * rel + WEIGHTS["freshness"] * fre + WEIGHTS["completeness"] * com,
            2,
        )
        current = n["frontmatter"].get("lifecycle")
        lifecycle, reason = decide_lifecycle(total, n["mtime"], now, current)
        items.append(
            {
                "name": n["name"],
                "path": n["path"],
                "score": {
                    "relation": round(rel, 2),
                    "freshness": round(fre, 2),
                    "completeness": round(com, 2),
                    "total": total,
                },
                "lifecycle": lifecycle,
                "lifecycle_reason": reason,
            }
        )
        total_sum += total
        if lifecycle == "ACTIVE":
            active += 1
        elif lifecycle == "STALE":
            stale += 1
        else:
            archived += 1

    result = {
        "scored_at": now.isoformat(timespec="seconds"),
        "items": items,
        "summary": {
            "count": len(items),
            "mean_score": round(total_sum / max(1, len(items)), 2),
            "active": active,
            "stale": stale,
            "archived": archived,
        },
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # 写回 frontmatter
    written = 0
    if args.apply:
        for it in items:
            note_path = vault / it["path"]
            if not note_path.exists():
                continue
            if write_score_to_frontmatter(note_path, it["score"]["total"],
                                          it["lifecycle"], today):
                written += 1

    mode = "APPLY" if args.apply else "calc-only"
    suffix = f" · frontmatter_written={written}/{len(items)}" if args.apply else ""
    print(f"[score {mode}] mean={result['summary']['mean_score']} · "
          f"active={active} stale={stale} archived={archived}{suffix} → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
