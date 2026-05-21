---
name: obsidian-vault-curator
description: |
  Obsidian 知识库自维护——按 vault 根目录的 VAULT-SCHEMA.md 规范,扫描命名/目录/链接,
  机械问题自动修(改名/归位/补 frontmatter),语义问题写 BACKLOG.md 等人工裁决。
  生成 audit/YYYY-MM-DD/ 时间序列报告(用 Dataview 查询块,实时活)。
  评分笔记 + 生命周期状态机(ACTIVE→STALE→ARCHIVED)。模式提取支撑 SYNTHESIS.md。
  TRIGGER: /obsidian-curate, /vault-audit, /vault-scan, "维护 obsidian", "维护知识库",
           "扫描 vault", "扫描知识库", "笔记关联性", "找孤立笔记", "断链检测",
           "笔记评分", "归档 obsidian", "obsidian curator", "vault curator",
           "obsidian 知识库整理", "知识库自维护", 用户在 source-code-analyzer 完成后
           说"保存到 obsidian"或类似(被动联动 Mode B)。
  SKIP: 写笔记内容本身(用 generate-image / writing-skills);
        非 Obsidian 的通用 markdown 文件管理;
        memory skill 管的 AI agent 个人记忆(那是独立系统)。
version: 1.0.0
---

# Obsidian Vault Curator

> 知识库自维护 skill。把 vault 当成一个**有状态**的系统:每次执行 = 一次状态推进。
> 设计借鉴 hermes-agent Curator(7 天周期)+ Background Review(每次操作后评分)双层闭环。

---

## 核心理念

| 原则 | 体现 |
|------|------|
| **规范 = 数据,逻辑 = 代码** | VAULT-SCHEMA.md 放 vault(用户可改),scripts 放 skill(版本化) |
| **机械自动 / 语义等人** | 命名/frontmatter 自动修;关联/合并/拆分写 BACKLOG.md |
| **增量优先** | 默认 `--since=7d`,只扫最近修改的;`--full` 显式才全扫 |
| **autoresearch 闭环** | audit 时间序列 + BACKLOG 信心累积(连续 3 次有效升至自动修候选) |
| **零运行时依赖** | scripts 是纯 Python stdlib;Dataview 装了更好(查询块替代部分静态表),没装也能跑 |

---

## 三种触发模式

### Mode A — 显式调用 `/obsidian-curate`

```
/obsidian-curate                          # 默认 --since=7d --scope=<整个 vault>
/obsidian-curate --full                   # 全 vault 扫描
/obsidian-curate --scope=personal/        # 限定子树
/obsidian-curate --since=30d              # 指定时间窗
/obsidian-curate --synthesize             # 额外做跨笔记模式提取,更新 SYNTHESIS.md
/obsidian-curate --apply                  # 默认 dry-run,加 --apply 才真改文件
```

执行步骤:
1. 读 `VAULT-SCHEMA.md`(不存在则报错并提示用户先创建)
2. 跑 `scripts/scan.py` 输出 `/tmp/vault-scan.json`(违规清单 + 关联候选)
3. 跑 `scripts/score.py` 输出 `/tmp/vault-score.json`(评分 + lifecycle 判定)
4. dry-run 模式:把所有改动打到 audit 报告,**不写笔记文件**
5. `--apply`:跑 `scripts/auto_fix.py` 处理高信心(≥0.8)条目,中信心写入 `BACKLOG.md`
6. 跑 `scripts/audit_report.py` 生成 `audit/YYYY-MM-DD/` 系列报告
7. 更新 `HOME.md` 🔍 Vault Maintenance 章节链接最新 audit

### Mode B — 源码分析后联动

当 `source-code-analyzer` skill 或类似分析工作产出新笔记时:

```
Mode B 入参:
  --new-notes=path/to/temp/analysis.md,path/to/temp/learning-plan.md
  --target-project=<项目名,如 aider>
  --vault-section=personal/ai-tech/open-source
```

执行步骤:
1. 按 SCHEMA 决定目标目录:`<vault-section>/<target-project>/`
2. 重命名文件按 §3 规范:`<project>.md` / `<project>-analysis.md` / `<project>-learning-plan.md`
3. 补 frontmatter(title/aliases/tags/created/updated/parent)
4. 扫描同目录已有笔记,自动加 `🧭 相关:` 横向链接
5. 触发 Mode A `--scope=<vault-section>/<target-project>/` 做收尾审计

### Mode C — 周期 loop

```
/loop 7d /obsidian-curate --since=7d --synthesize
```

每周自动跑一次增量 + 模式提取。autoresearch 闭环在此体现:
- 读上次 audit (`audit/<latest-1>/scoring.md` 等),对比本次,看哪些 BACKLOG 项目仍未解决
- 仍存在的条目信心 +0.1,3 次后升至 ≥0.8 → 下次 `--apply` 自动修
- 高分笔记(score≥8)且关联数突增 → 自动加入 SYNTHESIS.md 候选

---

## 数据流

```
┌─ VAULT-SCHEMA.md ────────────┐
│  规范(用户演进)             │
└──────────────┬───────────────┘
               ▼
┌─ scan.py ────────────────────┐
│  扫所有 .md → 违规 + 关联候选 │ → /tmp/vault-scan.json
└──────────────┬───────────────┘
               ▼
┌─ score.py ───────────────────┐
│  评分 + lifecycle 判定        │ → /tmp/vault-score.json
└──────────────┬───────────────┘
               ▼
   ┌───────────┴───────────┐
   ▼                       ▼
┌─ auto_fix.py ────┐   ┌─ audit_report.py ──────────────┐
│ 高信心 自动修    │   │ 生成 audit/YYYY-MM-DD/ markdown │
│ + 写 BACKLOG.md │   │ 用 Dataview 查询块(若插件可用) │
└──────────────────┘   └────────────────────────────────┘
```

---

## 关键文件

| 文件 | 作用 |
|------|------|
| `scripts/scan.py` | 全/增量扫描,输出违规清单 + 关联候选 JSON |
| `scripts/score.py` | 三维评分 + lifecycle 状态机 |
| `scripts/auto_fix.py` | 机械修复(改名/归位/补 frontmatter),支持 dry-run |
| `scripts/audit_report.py` | 写 audit/YYYY-MM-DD/ 全套 markdown 报告 |
| `references/workflows.md` | 三种模式的详细参数 + 示例 |
| `references/scoring-rubric.md` | 评分维度细则 |

---

## Vault 路径

- **默认**:从环境变量 `OBSIDIAN_VAULT` 读取,若未设置则从用户级 CLAUDE.md 提取
- **覆盖**:`--vault=path` 显式指定
- **当前个人配置**:用户 `~/.claude/CLAUDE.md` 声明 `/Users/shideng/Documents/Obsidian Vault`(各用户不同)

---

## 常用工作流

**首次冷启动(用户刚装 skill)**:
```
/obsidian-curate --full --apply
```

**日常增量**:
```
/obsidian-curate                # 默认 7 天增量 + dry-run,看报告
/obsidian-curate --apply        # 满意了就 apply
```

**周期自动**:
```
/loop 7d /obsidian-curate --since=7d --synthesize --apply
```

**只看孤立笔记**:
```
cat "<vault>/audit/$(ls <vault>/audit | tail -1)/orphans.md"
```

---

## 错误处理

| 错误 | 应对 |
|------|------|
| VAULT-SCHEMA.md 不存在 | 报错并提示运行 `cp <skill>/templates/VAULT-SCHEMA.md <vault>/` |
| Dataview 未安装 | 降级到静态 markdown 表,不报错 |
| git 不可用(vault 不是 git repo) | 用 `find -mtime` 替代 git log 做增量 |
| 写文件失败(权限/路径) | 写入 audit/errors.md,不阻塞其它笔记处理 |

---

## 演进方向

- v1.1: 支持 Bases 文件(.base)的语义化生成
- v1.2: 装 Templater 后联动生成笔记模板
- v2.0: 引入 LLM 做语义关联候选(目前只靠 frontmatter tag + 文件名相似度)
