---
title: index
created: 2026-05-21
tags: [open-source]
score: 9.4
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# 开源项目分析索引

> 个人开源研究笔记 · [[personal/INDEX|← 个人知识库]] · [[HOME|← 首页]]
>
> 原始代码仓库在 `opensource/OpenCLI/` 和 `opensource/litellm/`(不在此目录)

> 📁 **目录结构(2026-05-21 起)**:`open-source/<项目名>/` 子目录,每个项目的 概览 / 深度分析 / 学习计划 集中放置。
> 链接保持 Obsidian 短形 `[[文件名]]`,无需关心物理路径,Obsidian 会自动匹配。

---

## AI Agent 框架

| 项目 | 文档 | 说明 |
|------|------|------|
| Hermes Agent | [[hermes-agent\|概览]] · [[hermes-agent-analysis\|深度分析]] · [[hermes-agent-learning-plan\|学习计划]] | Nous Research 自改进 Agent,v0.14 三层闭环 |
| OpenClaw | [[openclaw-analysis\|深度分析]] | TypeScript 多渠道 AI 网关,128 扩展插件 |
| OpenClaw vs Hermes | [[openclaw-vs-hermes-agent\|架构对比]] | 同源项目战略分叉分析 |
| CrewAI | [[crewAI\|分析]] | 角色扮演多 Agent 编排 Python 框架 |
| DeepAgents | [[deepagents\|分析]] | — |
| OWL | [[OWL\|分析]] | — |
| Rowboat | [[rowboat\|概览]] · [[rowboat-analysis\|分析]] | YC S24,本地优先 AI 同事系统 |

---

## AI Coding Agent

| 项目 | 文档 | 说明 |
|------|------|------|
| Claude Code | [[Claude-Code-analysis\|深度分析]] · [[everything-claude-code-analysis\|完整分析]] · [[learn-claude-code-analysis\|学习分析]] | ~1900 文件/512K 行 TypeScript 源码分析 |
| Aider | [[aider-analysis\|分析]] | 终端 AI 结对编程,RepoMap 技术 |
| OpenCode | [[opencode-analysis\|分析]] | TypeScript+Bun+Effect-TS 编程助手 |
| OpenCLI | [[opencli-analysis\|分析]] | — |
| Oh My Codex | [[oh-my-codex\|分析]] | — |

---

## Developer Tools

| 项目 | 文档 |
|------|------|
| n8n-mcp | [[n8n-mcp\|分析]] |
| firecrawl | [[firecrawl\|分析]] |
| markitdown | [[markitdown\|分析]] |
| graphify | [[graphify\|分析]] |
| browser | [[browser\|分析]] |
| obsidian-clipper | [[obsidian-clipper\|分析]] |
| oh-my-mermaid | [[oh-my-mermaid\|分析]] |
| tradingview-mcp | [[tradingview-mcp\|分析]] |
| vibe-kanban | [[vibe-kanban-analysis\|分析]] |

---

## AI 产品与平台

| 项目 | 文档 |
|------|------|
| Superpowers | [[superpowers-analysis\|分析]] |
| PersonaPlex | [[personaplex\|分析]] |
| PM Skills | [[pm-skills-analysis\|分析]] |
| Skills/MiniMax | [[skills-minimax\|分析]] |
| Skills | [[skills\|分析]] |
| MiroFish | [[MiroFish\|分析]] |

---

## 量化交易

| 项目 | 文档 |
|------|------|
| TradingAgents | [[TradingAgents-analysis\|分析]] |
| Vibe Trading | [[Vibe-Trading\|分析]] |

---

## 其他

| 项目 | 文档 |
|------|------|
| awesome | [[awesome\|分析]] |
| awesome-design-md | [[awesome-design-md\|分析]] |
| awesome-persona-distill-skills | [[awesome-persona-distill-skills\|分析]] |
| ai-website-cloner-template | [[ai-website-cloner-template\|分析]] |
| anthropic-sdk-typescript | [[anthropic-sdk-typescript\|分析]] |
| last30days-skill | [[last30days-skill\|分析]] |
| OpenHarness | [[OpenHarness\|分析]] |
| OpenViking | [[OpenViking\|分析]] |
| andrej-karpathy-skills | [[andrej-karpathy-skills\|分析]] |
| claude-usage | [[claude-usage\|分析]] |

---

## 跨项目综合

- 📊 [[SYNTHESIS|开源项目综合对比索引]] — 40+ 笔记的横向评分矩阵 / 模式集群 / 反模式目录

---

## 目录映射

```
open-source/
├── hermes-agent/                    ← 示范:三件套 + 7 个原子分析笔记
│   ├── hermes-agent.md              (概览)
│   ├── hermes-agent-analysis.md     (深度分析聚合入口)
│   ├── hermes-agent-learning-plan.md(学习计划,每章节 wikilink 跳转)
│   ├── 2.1 Tool Registry 自注册模式.md
│   ├── 2.2 Provider-Transport 双层抽象.md
│   ├── 2.3 Memory 系统.md
│   ├── 2.4 5 阶段上下文压缩.md
│   ├── 2.5 主循环 run_conversation.md
│   ├── 3.1 三层闭环.md
│   ├── 3.2 LSP 写后验证.md
│   └── 3.3 OpenAI 兼容本地代理.md
├── openclaw/                        ← 多文件项目:分析 + 架构图 + drawio + vs 对比
├── claude-code/                     ← 3 篇分析变体并列
├── rowboat/                         ← 概览 + 分析
├── aider/  opencode/  opencli/  ... ← 单文件项目,每个一个子目录
└── index.md / SYNTHESIS.md          ← 顶层索引保留
```
