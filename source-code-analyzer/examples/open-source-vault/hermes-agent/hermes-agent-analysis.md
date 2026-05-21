---
title: "Hermes Agent 源码深度分析"
aliases:
  - hermes-agent-analysis
  - Hermes Agent 源码洞察
  - hermes 深度分析
tags:
  - hermes-agent
  - 源码分析
  - 深度分析
github: https://github.com/NousResearch/hermes-agent
created: 2026-05-21
version_analyzed: v0.14.0 (v2026.5.16)
score: 8.48
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Hermes Agent 源码深度分析

> 📋 项目概览:[[hermes-agent|hermes-agent 项目简介]]
> 📚 配套学习计划:[[hermes-agent-learning-plan|hermes-agent 源码学习计划]]
> 🔗 横向对比:[[openclaw-vs-hermes-agent|OpenClaw vs Hermes Agent 架构对比]]

---

> 本页是 **聚合入口**——按主题将深度分析拆成原子笔记,便于跨笔记反向链接(Obsidian Backlinks Pane)与图谱可视化。
> 学习时按 [[hermes-agent-learning-plan|学习计划]] 的顺序进入即可,每个小节都从此文件可一键跳转。

---

## 🧱 阶段二 · 核心引擎

| 小节 | 原子分析笔记 | 一句话 |
|------|--------------|--------|
| 2.1 | [[2.1 Tool Registry 自注册模式]] | AST 扫描 + 模块自注册 → 开闭原则 |
| 2.2 | [[2.2 Provider-Transport 双层抽象]] | Profile 声明 quirks,Transport 拥有 API 路径 |
| 2.3 | [[2.3 Memory 系统]] | 冻结快照不破坏 prompt cache + 跨会话 1h cache |
| 2.4 | [[2.4 5 阶段上下文压缩]] | 前 3 阶段免 LLM,Phase 4 才摘要 |
| 2.5 | [[2.5 主循环 run_conversation]] | 6 入口共享 4018 行的 conversation_loop |

---

## 🚀 阶段三 · 高级特性

| 小节 | 原子分析笔记 | 一句话 |
|------|--------------|--------|
| 3.1 | [[3.1 三层闭环]] | Background Review(每轮) + Curator(7 天) + Kanban(多 Agent) |
| 3.2 | [[3.2 LSP 写后验证]] | before-write baseline diff,只返回新增错 |
| 3.3 | [[3.3 OpenAI 兼容本地代理]] | 反向 OAuth forwarder,Claude Pro 复用给 Codex/Aider |

---

## 设计理念关键词

- **自改进闭环**:Background Review + Curator + Kanban 三层叠加
- **声明式 + 数据转换 正交**:Profile (quirks) ⊥ Transport (API path)
- **写后立即验证**:LSP delta + mutation footer,把 review 从事后挪到事中
- **跨会话延续**:1h prompt cache + central SQLite + WAL + FTS5
- **6 入口共享内核**:I/O 适配层分离,业务核心唯一

---

## 待补充

- [ ] 阶段一各小节(项目鸟瞰 / 6 入口 / 目录结构 / 8 层架构)的对应原子笔记
- [ ] 阶段四(多平台/插件生态/ACP/Gateway)的原子笔记
- [ ] 系统架构图(17 张 mermaid 图)的归位

---

*基于 v0.14.0(v2026.5.16)| 创建:2026-05-21*
