---
title: OpenClaw vs Hermes Agent 架构对比
aliases:
  - openclaw-hermes-comparison
  - openclaw vs hermes
tags:
  - 开源分析
  - 架构对比
  - AI-Agent
  - openclaw
  - hermes-agent
github_a: https://github.com/openclaw/openclaw
github_b: https://github.com/NousResearch/hermes-agent
created: 2026-05-19
updated: 2026-05-19
version_compared: openclaw main @ 816fbe0 / hermes-agent v0.14.0
score: 7.7
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# OpenClaw vs Hermes Agent 架构对比

> 配套深度笔记：[[hermes-agent]]、[[hermes-agent-analysis]]、[[hermes-agent-learning-plan]]

## 一句话定论

OpenClaw（TypeScript/Node）和 Hermes Agent（Python）是同源 sibling 项目——血缘相同但**下游战略已分叉**。

- **OpenClaw** → 严格规范的工程团队产品：manifest-first、控制面/运行面分离、严格 plugin 边界、companion apps、ClawHub 治理
- **Hermes** → 快速演化的研究产品：self-improving 闭环、订阅复用、IDE 集成、跨会话 cache、6 入口共享 core

---

## 关键差异速览（5 条）

1. **边界严格度**：OpenClaw `AGENTS.md` 体系把 plugin 边界形式化，禁止深 import core；Hermes plugin API 表面更宽（`ctx.llm` / `tool_override` / Shell hooks）
2. **存储路线**：OpenClaw 文件优先（各 plugin 各自 transcript dir）；Hermes 中央 SQLite + WAL + FTS5 + Trigram CJK
3. **自改进隐喻**：OpenClaw "Dreaming"（light/REM/deep cron 三阶段）；Hermes "Curator + Background Review + Kanban"（状态机 + 每轮 fork + durable 看板）
4. **记忆分工**：OpenClaw 4 个 memory plugin 各司其职（active-memory / memory-core / memory-lancedb / memory-wiki）；Hermes Built-in + 1 External 二元简化
5. **Hermes 显著领先**：(a) LSP delta diagnostics + mutation footer — OpenClaw 真空白；(b) 反向 OpenAI 代理 — OpenClaw 暂无 credential-attaching forwarder

---

## 核心维度对比

### 运行时与分发

| 子项 | OpenClaw | Hermes |
|------|----------|--------|
| 语言 | TypeScript ESM strict / Node 22+ | Python 3.11+ |
| 包管理 | `pnpm` workspace | `pip install hermes-agent` |
| 入口 | gateway 控制面 + web UI + companion apps | 6 入口共享 `AIAgent.run_conversation()` |
| 插件分发 | npm + ClawHub 市场（vetted review） | pip entry-point + huggingface/skills tap |

### Tool 注册机制

| | OpenClaw | Hermes |
|--|----------|--------|
| 注册方式 | manifest-driven：`openclaw.plugin.json` 声明，加载器 manifest-first | AST 扫描 + 模块自注册，`_generation` 计数器驱动 schema cache |
| 边界约束 | `src/plugins/AGENTS.md` 禁止 deep import | 较松，可直接 `from agent import ...` |
| 并行执行 | agent harness 调度 | 8 线程 ThreadPoolExecutor + 路径隔离 |

### 记忆系统

| | OpenClaw | Hermes |
|--|----------|--------|
| Built-in | `MEMORY.md`（兼容 `memory.md`）+ repair 路径 | `MEMORY.md` + `USER.md` 双文件，原子写 + fcntl 锁 |
| 短期 recall | `active-memory` plugin：LRU 15s TTL + circuit breaker | 主流程内置 + Background Review fork |
| 向量库 | `memory-lancedb`：LanceDB + 可配 embedding provider | Built-in + Honcho / Mem0 / RetainDB 等 |
| Wiki 层 | `memory-wiki`：Obsidian-friendly vault，3 种模式 | **无对应** |
| 周期整理 | "Dreaming"：light/REM/deep 三阶段 cron | Curator 7 天周期状态机 + Background Review 每轮 fork |

### LSP / 写后验证

| | OpenClaw | Hermes |
|--|----------|--------|
| LSP delta diagnostics | **真缺口，未实现** | `agent/lsp/` 11 文件，before-write baseline diff，仅返回新增错（v0.14）|
| mutation footer | 未发现 | per-turn "写了 foo.py +15/-3" 注入 user msg |

### 反向 OAuth 代理

| | OpenClaw | Hermes |
|--|----------|--------|
| 反向代理 | **未发现**（同名 extension 均为前向网关） | `hermes proxy`：把 Claude Pro / SuperGrok 反向暴露为 OpenAI 端点（v0.14）|

---

## 选型建议

| 如果你想做... | 优先参考 |
|--------------|---------|
| 多渠道 IM 助手 / 多端产品 / 严格插件治理 | **OpenClaw** |
| 自学习 coding agent / 跨会话演进 / IDE 集成 | **Hermes** |
| Wiki 知识库 bridge（Obsidian 整合） | **OpenClaw** memory-wiki |
| LSP 实时写后验证 | **Hermes** lsp/ |
| 订阅复用反向代理 | **Hermes** proxy |

---

*基于 OpenClaw `main @ 816fbe0` / Hermes Agent v0.14.0 | 2026-05-19*
