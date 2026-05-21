# obsidian-vault-curator · 工作流详情

> SKILL.md 的展开版。按触发模式列详细命令、参数、产出。

## 全局参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--vault PATH` | `/Users/shideng/Documents/Obsidian Vault` | vault 根 |
| `--scope DIR` | 整个 vault | 限定子树扫描 |
| `--since Nd` | `7d` | 只扫最近 N 天的文件;`--full` 覆盖 |
| `--full` | off | 全 vault 扫描 |
| `--apply` | off(dry-run) | 真改文件 |
| `--synthesize` | off | 额外做跨笔记模式提取 |

---

## Mode A — 显式 `/obsidian-curate`

### 标准流程

```bash
# 步骤 1: 扫描
python ~/.claude/skills/obsidian-vault-curator/scripts/scan.py \
    --vault "<vault>" --since 7d -o /tmp/vault-scan.json

# 步骤 2: 评分
python ~/.claude/skills/obsidian-vault-curator/scripts/score.py \
    -i /tmp/vault-scan.json -o /tmp/vault-score.json

# 步骤 3: dry-run(看建议)
python ~/.claude/skills/obsidian-vault-curator/scripts/auto_fix.py \
    -i /tmp/vault-scan.json

# 步骤 4: apply(真改)
python ~/.claude/skills/obsidian-vault-curator/scripts/auto_fix.py \
    -i /tmp/vault-scan.json --apply

# 步骤 5: 生成 audit 报告
python ~/.claude/skills/obsidian-vault-curator/scripts/audit_report.py \
    --scan /tmp/vault-scan.json --score /tmp/vault-score.json \
    --vault "<vault>"
```

### 常用变体

| 场景 | 命令 |
|------|------|
| 冷启动 baseline | `/obsidian-curate --full --apply` |
| 日常增量 | `/obsidian-curate` (dry-run) → 看报告 → `/obsidian-curate --apply` |
| 只看某个项目 | `/obsidian-curate --scope=<分区>/<项目名>` |
| 模式提取 | `/obsidian-curate --scope=<分区> --synthesize` |
| 找孤立笔记 | `/obsidian-curate --since=365d` 后看 `audit/<today>/orphans.md` |

---

## Mode B — 源码分析后联动

### 触发场景

`source-code-analyzer` 等 skill 产出新笔记后,主 agent 调用本 skill 把产物按规范归档。

### 调用约定

```
本 skill 接收:
  --new-notes=path1,path2,path3   # 临时文件路径(逗号分隔)
  --target-project=<name>         # 项目名(用作目录名 + 文件前缀)
  --vault-section=<分区相对路径>  # 如 personal/ai-tech/open-source
```

### 执行步骤

1. **决定目标路径**:`<vault>/<vault-section>/<target-project>/`,不存在则创建
2. **重命名**:
   - 概览类 → `<target-project>.md`
   - 分析类 → `<target-project>-analysis.md`
   - 学习计划 → `<target-project>-learning-plan.md`
   - 子章节(`2.1 xxx.md` 等)按原名保留
3. **补 frontmatter**:title / aliases / tags / created=今天 / updated=今天 / parent=对应学习计划 wikilink
4. **加横向链接**:扫该目录已有笔记,在新笔记顶部加 `🧭 相关:[[A]] · [[B]]`(按共享 tag 计算)
5. **触发 Mode A**:`/obsidian-curate --scope=<vault-section>/<target-project>/ --apply`

---

## Mode C — 周期 loop

### 设置(用 loop skill)

```
/loop 7d /obsidian-curate --since=7d --synthesize --apply
```

每周日跑一次,自动:
- 扫描最近 7 天的笔记变化
- 修复机械问题
- 更新 BACKLOG.md
- 提取跨笔记模式(写 SYNTHESIS.md 候选)
- 生成 `audit/YYYY-MM-DD/`

### autoresearch 闭环(关键!)

Mode C 比 Mode A 多做 **autoresearch follow-up**:

1. 读上次 audit 的 `BACKLOG.md` 条目
2. 对每条 BACKLOG 项,检查它本次扫描是否仍然有效(同一关联候选再次出现 / 同一孤立笔记仍孤立)
3. 仍有效的条目:
   - 信心分 +0.1
   - 出现次数 +1
   - 出现 ≥3 次且信心 ≥0.8 → 标记 `🟢 auto-apply-ready`,下次 `--apply` 自动处理
4. 无效的条目(已被人工处理):移到 `audit/<today>/closed-backlog.md` 留痕

### 跨笔记模式提取(`--synthesize`)

对每个有 ≥3 个分析笔记的目录:
1. 收集所有笔记的 frontmatter.tags
2. 找出现频率 >= 50% 的 tag → 候选"目录主题 tag"
3. 找各笔记独有 tag → 候选"差异维度"
4. 在该目录 SYNTHESIS.md 末尾追加 `## 自动观察 · YYYY-MM-DD` 章节,列以上候选
5. **不覆盖**已有人工内容,只追加

---

## 错误恢复

### 脚本崩溃

每个脚本独立运行,中间 JSON 落盘,可单独重跑:

```bash
# 假设 audit_report.py 失败了
python ~/.claude/skills/obsidian-vault-curator/scripts/audit_report.py \
    --scan /tmp/vault-scan.json --score /tmp/vault-score.json \
    --vault "<vault>"  # 重跑这一步即可,不用从头扫
```

### auto_fix 改坏了

vault 是 git repo:`git -C "<vault>" diff` 看改动 → `git -C "<vault>" checkout -- .` 回滚。

如果不是 git repo:**强烈建议把 vault 纳入 git 管理**,这是本 skill 的隐含前提之一。

---

## Dataview 集成

audit 报告里嵌入了 Dataview 查询块。如果用户装了 Dataview 插件(本 skill 默认假设已装),这些块会渲染为实时查询;没装的话就是普通代码块,不影响功能。

典型查询:
```dataview
TABLE score, lifecycle, last_audit
FROM ""
WHERE score < 5 AND lifecycle = "ACTIVE"
SORT score ASC
```

---

## 演进 hook

如果用户改了 VAULT-SCHEMA.md 的某些参数(如 `STALE_AFTER_DAYS` 阈值改了),目前需要同步改 `scripts/score.py` 的常量。

后续 v1.1 会把这些参数从 SCHEMA.md frontmatter 直接读,实现"改 SCHEMA → 自动生效"。
