---
title: Hermes Agent 源码学习计划
aliases:
  - hermes-agent 学习路径
  - hermes-agent 阅读指南
tags:
  - 源码学习
  - 学习路径
  - hermes-agent
created: 2026-05-18
updated: 2026-05-21
version_analyzed: v0.14.0 (v2026.5.16)
score: 9.98
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Hermes Agent 源码学习计划

> 📋 项目简介:[[hermes-agent|Hermes Agent 项目概览]]
> 📖 配套深度分析:[[hermes-agent-analysis|Hermes Agent 源码深度分析(聚合入口)]]
> 🔗 横向对比:[[openclaw-vs-hermes-agent|OpenClaw vs Hermes Agent]]
>
> 本文按 **功能维度** 梳理学习路径。每项给出:**功能入口**(用户视角)/ **思路概要**(一句话原理)/ **代码入口**(关键文件 + 行号)/ **深度分析跳转**(原子笔记 wikilink)
>
> 推荐按"难度梯度"分 4 阶段阅读。**点击每个章节的链接可直接跳转到对应分析文档**。

---

## 阅读策略

- **不要从 `cli.py` (646KB) 或 `run_agent.py` (178KB) 入手** — 这两个是巨型聚合文件,先看抽出的小模块更高效
- **每个功能先读注释/docstring 再读实现** — Hermes 的 module-level docstring 通常 30-50 行,把设计意图写得很清楚
- **配合架构图食用** — 17 张 mermaid 图分散在 [[hermes-agent-analysis]] 各章节
- **善用 `grep "^class\|^def "` 看模块骨架**

---

## 阶段一:理解整体(入门 · 0.5 天)

| 顺序 | 功能 | 入口 | 思路概要 | 代码入口 |
|-----|------|------|----------|----------|
| 1 | **项目鸟瞰** | `README.md` + `AGENTS.md` | 看官方一句话定位 + 自描述(Hermes 自己写给 Agent 的项目导引) | `README.md` / `AGENTS.md`(51KB,重要!) |
| 2 | **6 入口共享核心** | 6 个命令 | 所有入口最终调同一个 `AIAgent.run_conversation()`,差异只在 I/O 适配层 | `cli.py` 入口分发 → `run_agent.py:AIAgent` |
| 3 | **目录结构** | — | 80 文件的 `agent/`(核心)+ 76 文件的 `tools/`(工具)+ 22 平台的 `gateway/` | 直接 `tree -L 2 -d` |
| 4 | **8 层架构** | — | Entry → Core → Provider → Tool → Memory → Prompt → Persistence → Execution | [[hermes-agent-analysis#系统架构图]] 顶层 ASCII 大图 |

---

## 阶段二:核心引擎(中级 · 2 天)

### [[2.1 Tool Registry 自注册模式|2.1 Tool Registry — 自注册模式]]

> **核心思想**:工具模块自己负责注册自己,注册中心只需负责发现和导入。实现了"开闭原则"——新增工具只需添加文件,无需修改注册中心。

- 🔍 **深度分析**:[[2.1 Tool Registry 自注册模式]](设计模式表 / 加载流程 / AST 原理 / 工具示例 / 设计思想)
- 📁 **代码入口**:
  - `tools/registry.py` — `ToolRegistry`、`discover_builtin_tools()`、`_is_registry_register_call()`
  - `tools/terminal_tool.py:2370` — `registry.register()` 调用示例
  - `model_tools.py` — `handle_function_call()` 分发工具调用
- 🔗 **横向链接**:[[2.2 Provider-Transport 双层抽象#Provider 懒加载 vs Tool 即时加载|Provider 懒加载 vs Tool 即时加载对比]]

---

### [[2.2 Provider-Transport 双层抽象|2.2 Provider / Transport 双层抽象 ⭐ (v0.11)]]

> **核心思想**:`ProviderProfile` dataclass 声明 quirks(声明式配置),`ProviderTransport` ABC 拥有 API 调用路径(数据转换)。两者正交,实现了"消除布尔标志"的优雅扩展。

- 🔍 **深度分析**:[[2.2 Provider-Transport 双层抽象]](声明式配置 / 数据转换 / 协作时序 / 注册机制 / 懒加载发现 / 架构优势)
- 📁 **代码入口**:
  - `providers/base.py:184` — `ProviderProfile`
  - `agent/transports/base.py:89` — `ProviderTransport` ABC

---

### [[2.3 Memory 系统|2.3 Memory 系统 — 冻结快照 + 跨会话 cache]]

> **核心思想**:`_system_prompt_snapshot` 在会话开始时冻结,运行时写入新 memory 不破坏当前 prompt cache。

- 🔍 **深度分析**:[[2.3 Memory 系统]]
- 📁 **代码入口**:`agent/memory_manager.py` + `agent/prompt_caching.py`

---

### [[2.4 5 阶段上下文压缩|2.4 5 阶段上下文压缩]]

> **核心思想**:Phase 1-3 无 LLM(裁工具结果/头部/尾部保护),Phase 4 LLM 摘要,Phase 5 修复孤立工具对。

- 🔍 **深度分析**:[[2.4 5 阶段上下文压缩]]
- 📁 **代码入口**:`agent/context_compressor.py`

---

### [[2.5 主循环 run_conversation|2.5 主循环 — run_conversation()]]

> **核心思想**:所有 6 个入口最终汇聚到 `AIAgent.run_conversation()`,这是 Hermes 的"共享内核"。

- 🔍 **深度分析**:[[2.5 主循环 run_conversation]]
- 📁 **代码入口**:`agent/conversation_loop.py`(4018 行)+ `agent/tool_executor.py`(920 行)

---

## 阶段三:高级特性(高级 · 3 天)

### [[3.1 三层闭环|3.1 三层闭环 ⭐⭐⭐ (v0.12/v0.13)]]

> **核心思想**:三层叠加的自改进闭环——Background Review(每轮)、Curator(7 天周期)、Multi-agent Kanban(协作)。

- 🔍 **深度分析**:[[3.1 三层闭环]]
- 📁 **代码入口**:
  - [[3.1 三层闭环#3.1.1 Background Review|Background Review]] — `agent/background_review.py`(570 行)
  - [[3.1 三层闭环#3.1.2 Curator|Curator]] — `agent/curator.py`(1781 行)
  - [[3.1 三层闭环#3.1.3 Multi-agent Kanban|Multi-agent Kanban]] — `plugins/kanban/`

---

### [[3.2 LSP 写后验证|3.2 LSP 写后验证 ⭐⭐⭐ 🆕 v0.14]]

> **核心思想**:三层防护——in-process syntax check → LSP delta diagnostics(before-write baseline diff,**只返回新增错**) → per-turn mutation footer。

- 🔍 **深度分析**:[[3.2 LSP 写后验证]]
- 📁 **代码入口**:`agent/lsp/manager.py` + `tools/file_operations.py`

---

### [[3.3 OpenAI 兼容本地代理|3.3 OpenAI 兼容本地代理 🆕 v0.14]]

> **核心思想**:Credential-attaching forwarder,把 Claude Pro / SuperGrok 反向暴露给 Codex / Aider / Cline。

- 🔍 **深度分析**:[[3.3 OpenAI 兼容本地代理]]
- 📁 **代码入口**:`hermes_cli/proxy/server.py`(308 行)
- 🔗 **依赖**:[[2.2 Provider-Transport 双层抽象]] 提供协议转换基础

---

## 推荐学习路径

| 路径 | 目标 | 顺序 |
|------|------|------|
| 路径 A | 学 Agent 工程范式 | 阶段一 → [[2.1 Tool Registry 自注册模式\|2.1]] → [[2.2 Provider-Transport 双层抽象\|2.2]] → [[2.3 Memory 系统\|2.3]] → [[2.4 5 阶段上下文压缩\|2.4]] → [[2.5 主循环 run_conversation\|2.5]] → [[3.1 三层闭环\|3.1]] → [[3.2 LSP 写后验证\|3.2]] |
| 路径 B | 学多平台/插件生态 | 阶段一 → 4.2 Gateway → 4.1 Plugin → 4.3 ACP |
| 路径 C | 学反向 OAuth 代理 | 仅 [[3.3 OpenAI 兼容本地代理\|3.3]](0.5 天)|
| 路径 D | 学自学习闭环 | [[3.1 三层闭环#3.1.1 Background Review\|3.1.1]] → [[3.1 三层闭环#3.1.2 Curator\|3.1.2]] → [[3.1 三层闭环#3.1.3 Multi-agent Kanban\|3.1.3]] → [[2.3 Memory 系统\|2.3]] |
| 路径 E | 学性能工程 | [[2.1 Tool Registry 自注册模式\|Tool Registry 缓存]] → Agent LRU → [[2.3 Memory 系统\|Prompt Caching 跨会话]] |

---

## 配套资源

- 📖 [[hermes-agent-analysis|深度分析(聚合入口)]] — 列出所有原子分析笔记
- 📋 [[hermes-agent|项目简介]] — 模块表 + 快速开始
- 🔗 [[openclaw-vs-hermes-agent|OpenClaw vs Hermes 对比]]
- 🌐 GitHub: https://github.com/NousResearch/hermes-agent

---

## 索引(本目录所有原子分析笔记)

- [[2.1 Tool Registry 自注册模式]]
- [[2.2 Provider-Transport 双层抽象]]
- [[2.3 Memory 系统]]
- [[2.4 5 阶段上下文压缩]]
- [[2.5 主循环 run_conversation]]
- [[3.1 三层闭环]]
- [[3.2 LSP 写后验证]]
- [[3.3 OpenAI 兼容本地代理]]

---

*学习计划制定时间:2026-05-18 | 更新:2026-05-21 | 基于 v0.14.0*
