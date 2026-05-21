---
title: Vault 知识库维护规范
aliases:
  - VAULT-SCHEMA
  - 知识库规范
  - vault schema
tags:
  - meta
  - 规范
  - vault-curator
created: YYYY-MM-DD   # 安装时手动填
updated: YYYY-MM-DD
schema_version: 1.0
---

# Vault 知识库维护规范

> 本文件是 vault 的**单一事实来源**(Single Source of Truth)。`obsidian-vault-curator` skill 在扫描/维护时读取此文件,按规范执行自动修复 + 写 audit。
>
> **本文件可演进**——直接编辑此文件即可改变 vault 维护行为,不需要改 skill 代码。
> 改后下次 `/obsidian-curate` 自动生效。
>
> 复制本模板到 vault 根目录:`cp <skill>/templates/VAULT-SCHEMA.md <vault>/`

---

## 1. 顶层目录约定(示例,按你的 vault 实际改)

```
<vault>/
├── HOME.md                  ← 全 vault 首页(必有)
├── VAULT-SCHEMA.md          ← 本文件(规范)
├── BACKLOG.md               ← 自动维护的语义待办清单
├── audit/                   ← 自动产物,YYYY-MM-DD/ 命名
│   └── 2026-MM-DD/
│       └── INDEX.md
├── notes/                   ← 你的主题分区(可任意命名)
├── projects/                ← 项目分析归档区(示例)
└── archive/                 ← 归档区(状态 ARCHIVED 的笔记移入)
```

**规则**:
- 顶级分区在此文件登记后才被认为"合法"
- 每个分区根目录建议有 `INDEX.md` 作为分区导航
- audit/ archive/ 由 skill 维护,人工尽量不直接改

## 2. 主题子目录约定

每个独立主题(项目 / 工具 / 概念)一个子目录:

```
<分区>/<类别>/<主题>/
├── <主题>.md                     ← 概览(必有)
├── <主题>-analysis.md            ← 深度分析(可选)
├── <主题>-learning-plan.md       ← 学习计划(可选)
├── <编号> <子标题>.md            ← 原子分析(可选,多个)
└── 图/资料/                      ← 子目录,放截图/PDF/drawio
```

## 3. 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| **元文档** | 全大写,无前缀,无空格 | `HOME.md` / `INDEX.md` / `SYNTHESIS.md` / `VAULT-SCHEMA.md` / `BACKLOG.md` |
| **目录** | kebab-case 或 PascalCase | `open-source/`, `ai-tech/`, `my-project/` |
| **概览笔记** | `<主题>.md` 与目录同名 | `my-project/my-project.md` |
| **深度分析** | `<主题>-analysis.md` 后缀固定 | `my-project-analysis.md` |
| **学习计划** | `<主题>-learning-plan.md` 后缀固定 | `my-project-learning-plan.md` |
| **原子分析** | `<编号> <子标题>.md` | `2.1 Foo 设计模式.md` |
| **横向对比** | `<A>-vs-<B>.md` | `framework-a-vs-framework-b.md` |
| **audit 子目录** | `audit/YYYY-MM-DD/` | `audit/2026-05-21/` |

**禁忌**:
- 不用 `_` 前缀
- 不在分区根放孤立笔记 —— 必须落到具体子目录
- 文件名不带 `:` `?` `*` 等 Windows 非法字符

## 4. Frontmatter 规范

### 4.1 必填字段(所有笔记)

```yaml
---
title: 笔记主标题
aliases: [别名1, 别名2]
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 4.2 项目分析类追加

```yaml
github: https://github.com/org/repo  # 若分析开源项目
version_analyzed: v1.2.3
parent: "[[<父学习计划>|显示]]"
```

### 4.3 lifecycle 字段(由 skill 自动维护)

```yaml
lifecycle: ACTIVE   # ACTIVE / STALE / ARCHIVED
score: 7.5          # 0-10
last_audit: 2026-MM-DD
```

## 5. 链接规范

| 场景 | 写法 | 示例 |
|------|------|------|
| **基本 wikilink** | 短形,不带路径 | `[[my-project]]` |
| **带显示文本** | `[[文件名\|显示文本]]` | `[[my-project\|项目概览]]` |
| **章节锚点** | `[[文件名#章节标题]]` | `[[my-project-analysis#架构图]]` |
| **章节+显示** | `[[文件名#章节\|显示]]` | `[[3.1 模块设计#子模块\|子模块]]` |

### 5.1 双向关联强约束

**每个原子分析文件顶部必须有反向链接**:

```markdown
> 📚 来源:[[<父学习计划>#<章节>|学习计划 · <章节>]]
> 🧭 相关:[[<兄弟分析A>]] · [[<兄弟分析B>]]
```

**每个学习计划的章节必须用 wikilink 标题指向对应原子分析**:

```markdown
### [[<原子分析文件名>|<章节显示标题>]]
```

### 5.2 禁忌

- 不用 `[文本](path/to/file.md)` 标准 markdown 链接(失去 Obsidian 反向链接能力)
- 不用绝对路径,用短形 `[[basename]]`

## 6. 评分维度(0-10,自动计算)

| 维度 | 权重 | 公式 |
|------|------|------|
| **关联数** | 0.4 | min(10, 出链数 × 0.5 + 反向链接数 × 1.0) |
| **活跃度** | 0.3 | max(0, 10 − (今日 − updated)/30) |
| **完整度** | 0.3 | frontmatter 必填齐全(3 分) + 无 TODO 残留(3 分) + 字数 > 500(4 分) |

**总分** = 0.4 × 关联 + 0.3 × 活跃 + 0.3 × 完整

## 7. 生命周期状态机

```
ACTIVE ──30 天未更新 且 score<5──▶ STALE ──60 天再未访问──▶ ARCHIVED
   ▲                                  │
   └──────────任意编辑──────────────────┘
```

| 状态 | 含义 | skill 行为 |
|------|------|----------|
| **ACTIVE** | 默认 | 不动 |
| **STALE** | 候选过时 | 写入 audit/scoring.md,提示用户裁决 |
| **ARCHIVED** | 已归档 | 移入 `archive/` 目录,保留所有链接 |

**人工干预**:任何时候手动 `lifecycle: ACTIVE` 都会重置状态机。

## 8. 严格度策略

| 问题类型 | 严格度 | skill 行为 |
|---------|-------|----------|
| frontmatter 缺 title/created | 🔴 自动修(用文件名/git first commit 时间) | auto_fix.py |
| 文件名违规(空格/大小写/后缀) | 🟡 dry-run 给 diff,等用户确认 | auto_fix.py --apply |
| 目录归置违规(分区错位) | 🟡 dry-run 给 diff | auto_fix.py --apply |
| 断链 | 🟡 写 BACKLOG.md | 不自动修(可能是用户故意拼) |
| 缺横向链接(语义关联) | 🟢 写 BACKLOG.md 候选 + 信心分 | 人工裁决 |
| 孤立笔记(零关联) | 🟢 写 BACKLOG.md | 人工裁决 |

## 9. 异常清单(允许违规)

**用户根据 vault 实际情况自行扩展**。某些已存在文件或外部约定不强制纳入规范,可加入白名单:

```yaml
exempt_paths:
  # 通用(skill 内置默认已含,这里列出仅为可读性)
  - .obsidian/
  - .trash/
  - .git/
  - node_modules/
  - archive/
  - audit/

  # 用户特定(请按你的 vault 加,示例)
  # - clippings/         # 网页剪藏保留原格式
  # - journal/           # 日记自由格式
  # - work/business/     # 业务知识库另有约定

exempt_files:
  - HOME.md
  - VAULT-SCHEMA.md
  - BACKLOG.md
```

---

## 修改本文件后

```
/obsidian-curate --full
```

让 skill 重新按新规范全量扫描,生成新 audit。

---

*Schema v1.0 · 模板 · 创建时把 YYYY-MM-DD 替换为今天*
