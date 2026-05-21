---
title: "Hermes Agent"
aliases: [hermes-agent, NousResearch Hermes]
tags:
  - opensource
  - coding-agent
  - Python
  - multi-platform
  - mcp
  - self-improving
  - lsp
  - openai-proxy
github: https://github.com/NousResearch/hermes-agent
created: 2026-04-15
updated: 2026-05-18
version: v0.14.0 (v2026.5.16)
score: 8.9
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Hermes Agent

> **The agent that grows with you — The self-improving AI agent built by Nous Research**

> 📖 深度分析见：[[hermes-agent-analysis|Hermes Agent 源码洞察]]（v3.0 已更新到 v0.14）
> 📚 源码学习计划见：[[hermes-agent-learning-plan|Hermes Agent 源码学习计划]]（按功能维度 4 阶段路径）

---

## 🆕 v0.14 一句话 (2026-05-18)

> v0.9 → v0.14 五个 release 把 Hermes 从"自学习 Agent 框架"演进成"自学习 + 自整理 + 自验证 + 把订阅复用给所有工具"的工程平台：
>
> **三层闭环**：写代码 → LSP 实时反馈 → 写完打分（background_review）→ 7 天周期归档清理（curator）→ Skills/Memory 跨会话复用 → Cache 跨会话 1h 命中。
>
> **6 个入口**：CLI / TUI(Ink) / Gateway(22 平台) / ACP(IDE) / 🆕 Proxy(OpenAI 兼容代理) / 🆕 Curator(后台管家)。

---

## 项目简介

Hermes Agent 是由 Nous Research 开发的自改进型 AI 智能体，OpenClaw 的精神续作。它的核心创新是**闭环学习系统** — 从经验创建技能、使用中改进、写后自验证、跨会话搜索、构建用户模型。

**核心特点（v0.14 状态）：**
- 🆕 **三层自改进闭环**：background_review（每轮评分）+ curator（7 天周期整理）+ kanban（多 Agent 协作）
- 🆕 **三层写后反馈**：in-process syntax check + LSP semantic diagnostics + per-turn mutation footer
- 🆕 **6 入口共享 AIAgent 核心**：CLI / TUI(Ink React) / Gateway / ACP / Proxy / Curator
- **22 个消息平台**：Telegram / Discord / Slack / Feishu / DingTalk / WeChat / WeCom / iMessage / Signal / WhatsApp / Matrix / Email / SMS / Home Assistant / Webhook / QQBot 🆕 / Yuanbao 🆕 / Google Chat 🆕 / Teams 🆕 / LINE 🆕 / SimpleX 🆕 / Mattermost
- **30+ Model Provider 插件**：OpenAI / Anthropic / Google / Bedrock 🆕 / NVIDIA NIM 🆕 / Vercel AI Gateway 🆕 / GPT-5.5 (Codex OAuth) 🆕 / SuperGrok OAuth 🆕 / Kimi / DeepSeek / MiMo / GLM / Qwen / LM Studio 🆕(升级) / GMI Cloud 🆕 / Azure AI Foundry 🆕 / Novita 🆕 / ...
- **7 种执行环境**：Local / Docker / SSH / Daytona / Singularity / Modal / Vercel Sandbox 🆕
- **MCP 完整支持**：Stdio + HTTP + 🆕 SSE + OAuth + 熔断器 + 动态刷新 + 🆕 Sampling proxy
- **🆕 跨会话 1h Prompt Cache**（Claude/OpenRouter/Nous Portal）
- **🆕 i18n 7 语言**：中/日/德/西/法/乌/土
- **🆕 `pip install hermes-agent`** + lazy install + tiered fallback + 🆕 Native Windows beta

**项目链接：**
- GitHub: https://github.com/NousResearch/hermes-agent
- 文档: https://hermes-agent.nousresearch.com/docs/
- Discord: https://discord.gg/NousResearch
- Skills Hub: https://agentskills.io
- 🆕 Zed Registry: 一键安装（v0.14）

---

## 版本演进时间线

| 版本 | 日期 | 核心主题 |
|------|------|----------|
| **v0.14.0** | 2026-05-16 | **The Foundation Release** — SuperGrok OAuth、OpenAI 本地代理、x_search、Teams E2E、Debloating、PyPI、跨会话 cache、LSP 语义诊断、22 平台 |
| **v0.13.0** | 2026-05-x | **Multi-agent Release** — Kanban、`/goal`、video_analyze、xAI 语音、7 locales、Google Chat (20 平台)、Sessions 跨重启、8 P0 安全、Checkpoints v2、post-write lint、no_agent cron、Provider 插件化、MCP SSE+OAuth、ACP /steer+/queue |
| **v0.12.0** | 2026-05-x | **Curator Release** — Autonomous Curator、background_review 升级、ComfyUI built-in、Teams plugin、Yuanbao、Spotify、Google Meet、`hermes -z`、Models dashboard、Vercel Sandbox、~57% TUI 冷启动 |
| **v0.11.0** | 2026-04-23 | **Interface Release** — Ink TUI 重写、Transport ABC、AWS Bedrock、5 inference paths、GPT-5.5、QQBot、Plugin 表面扩展、`/steer`、Shell hooks、Orchestrator role |
| **v0.10.0** | 2026-04-16 | Nous Tool Gateway（订阅复用 web/image/TTS/browser） |
| **v0.9.0** | 2026-04-13 | **Everywhere Release** — 本地 Dashboard、Fast Mode、iMessage、WeChat、Termux、watch_patterns、Pluggable Context Engine、Backup/Import、/debug |

---

## 技术栈分析

### 核心技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | >= 3.11 | 核心运行时 |
| OpenAI SDK | >= 2.21 | OpenAI API |
| Anthropic SDK | >= 0.39 | Claude API |
| Pydantic | >= 2.12.5 | 数据验证 |
| Rich / Prompt Toolkit | 14.3 / 3.0.52 | 经典 CLI |
| 🆕 **Ink (React)** | — | v0.11 TUI 全栈重写 |
| 🆕 **aiohttp** | — | v0.14 OpenAI 兼容代理 server |
| HTTPX / PyYAML / Jinja2 / Fire / Tenacity | — | HTTP / YAML / 模板 / CLI / 重试 |
| 🆕 **LSP** | — | v0.14 语义诊断（多 language server） |

---

## 快速开始（v0.14）

```bash
pip install hermes-agent && hermes
hermes model
hermes gateway
hermes proxy
hermes curator status
```

---

*更新：2026-05-18（基于 v0.14.0）| 深度分析：[[hermes-agent-analysis]]*
