# 案例:用 source-code-analyzer 产出的开源项目知识库

> 本目录是**真实使用案例** — 一位用户用 `source-code-analyzer` skill 持续分析 40+ 个开源项目后,在 Obsidian vault 里沉淀的笔记集合。
>
> 用作展示:
> 1. **skill 实际产出的文档质量**(架构图 / 设计模式 / 代码入口 / 横向对比)
> 2. **配合 `obsidian-vault-curator` 的目录组织**(每项目独立子目录 + 三件套 + wikilink 关联)
> 3. **frontmatter 含 `score / lifecycle / last_audit` 字段** = 已被 obsidian-vault-curator 评分写回(印证两个 skill 协同闭环)

---

## 📁 目录结构

```
open-source-vault/
├── index.md                          ← 全索引(50+ 项目分类列表)
├── SYNTHESIS.md                      ← 跨项目横向对比矩阵
├── hermes-agent/                     ← 标杆示范:完整三件套 + 7 个原子分析
│   ├── hermes-agent.md               (概览)
│   ├── hermes-agent-analysis.md      (深度分析聚合入口)
│   ├── hermes-agent-learning-plan.md (学习计划,章节级 wikilink 跳转)
│   ├── 2.1 Tool Registry 自注册模式.md
│   ├── 2.2 Provider-Transport 双层抽象.md
│   ├── 2.3 Memory 系统.md
│   ├── 2.4 5 阶段上下文压缩.md
│   ├── 2.5 主循环 run_conversation.md
│   ├── 3.1 三层闭环.md
│   ├── 3.2 LSP 写后验证.md
│   └── 3.3 OpenAI 兼容本地代理.md
├── openclaw/                         ← 多文件:分析 + 6 张架构图 + drawio + vs 对比
│   ├── openclaw-analysis.md
│   ├── openclaw-arch-p1-overview.png
│   ├── openclaw-arch-p2-agent-loop.png
│   ├── openclaw-arch-p3-mcp-acp.png
│   ├── openclaw-arch-p4-memory-rag.png
│   ├── openclaw-arch-p5-prompt.png
│   ├── openclaw-arch-p6-hooks.png
│   ├── openclaw-architecture.drawio
│   └── openclaw-vs-hermes-agent.md
├── claude-code/                      ← 3 篇分析变体并列
├── rowboat/                          ← 概览 + 分析
└── ...(40+ 单文件项目目录)
```

---

## 🔍 看点 1:标杆笔记 hermes-agent/

打开 `hermes-agent/hermes-agent-learning-plan.md` — 这是**学习计划范例**:
- 每个章节标题本身是 wikilink `[[2.1 Tool Registry 自注册模式]]`
- 点击跳转到原子分析文档
- 章节内部还能跳子小节 `[[3.1 三层闭环#3.1.1 Background Review]]`

打开 `hermes-agent/2.2 Provider-Transport 双层抽象.md` — 这是**原子分析范例**:
- frontmatter 含 `parent: "[[hermes-agent-learning-plan|...]]"`
- 顶部 `📚 来源:[[父学习计划#章节]]` 反向链接
- `🧭 相关:[[兄弟笔记]]` 横向链接
- 此笔记当前评分 **10.00 / 10**(关联+活跃+完整 全满)

---

## 🔍 看点 2:跨项目综合 SYNTHESIS.md

横向矩阵 + 模式集群 + 反模式目录的人工综合范例。后续如启用
`obsidian-vault-curator --synthesize`,会半自动追加"自动观察"段。

---

## 🔍 看点 3:每个笔记的 frontmatter

任选一个笔记打开,会看到:

```yaml
---
title: ...
aliases: [...]
tags: [...]
created: 2026-MM-DD
updated: 2026-MM-DD
score: 9.20            # ← obsidian-vault-curator 写入
lifecycle: ACTIVE       # ←
last_audit: 2026-05-21  # ←
---
```

后 3 个字段说明:此笔记已被 `obsidian-vault-curator` 维护过,可被 Dataview 实时查询。

---

## 🎯 如何复现这套笔记结构

```bash
# 1. 装好 source-code-analyzer + obsidian-vault-curator(见仓库根 INSTALL.md)

# 2. 对一个新开源项目跑分析
/source-code-analyzer 分析 https://github.com/<org>/<repo>

# 3. skill 产出 <repo>.md / <repo>-analysis.md / <repo>-learning-plan.md
#    obsidian-vault-curator 联动(Mode B)自动按 <repo>/ 子目录归位 + 补 frontmatter + 加 🧭 相关

# 4. 周期维护
/obsidian-curate --since=7d --synthesize --apply

# 5. 在 Obsidian 里嵌 Dataview 查询块,实时看评分排名
```

---

## 📊 当前案例统计(本笔记集)

- 总笔记:54 个 .md
- 含完整三件套的项目:hermes-agent
- 横向对比文档:openclaw-vs-hermes-agent.md
- 跨项目综合:SYNTHESIS.md(人工写,~150 行)
- 配图:6 张 png + 1 个 drawio(openclaw 架构)
- 体量:2.7 MB

---

*本案例由 obsidian-vault-curator 跑过冷启动 baseline + 评分写回,可作为新用户参考。*
