---
title: "Rowboat"
aliases: [Rowboat, rowboat]
tags:
  - opensource
  - multi-agent
  - Python
  - mcp
github: https://github.com/rowboat-ai/rowboat
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Rowboat

## 项目简介

**Rowboat** 是一个开源的 AI 协作者（AI Coworker），旨在将工作转化为知识图谱并基于该图谱执行操作。它连接用户的电子邮件和会议记录，构建长期存在的知识图谱，并利用这些上下文帮助用户完成工作 - 完全在本地机器上私密运行。

- **GitHub Stars**: 12,405
- **开发语言**: TypeScript
- **许可证**: Apache-2.0
- **官方网址**: https://www.rowboatlabs.com/

### 核心功能

- 连接 Gmail、Google Calendar 和会议记录
- 构建长期知识图谱（Obsidian 兼容的 Markdown 格式）
- 支持会议准备、邮件起草、文档和演示文稿生成
- 实时笔记追踪（Live Notes）
- 语音输入和输出支持
- MCP（Model Context Protocol）工具扩展

---

## 技术栈分析

### 核心语言与运行时
| 技术 | 版本 | 用途 |
|------|------|------|
| TypeScript | 5.9+ | 主要开发语言 |
| Node.js | 18+ | 运行时环境 |
| React | 18.3+ | TUI（终端用户界面） |

### 主要依赖库
| 类别 | 库名 | 用途 |
|------|------|------|
| AI SDK | `@ai-sdk/anthropic`, `@ai-sdk/google`, `@ai-sdk/openai` | 多模型 AI 支持 |
| Web 框架 | `hono` | HTTP 服务器和 API |
| 依赖注入 | `awilix` | IoC 容器 |
| TUI 渲染 | `ink`, `ink-select-input`, `ink-spinner` | 终端交互界面 |
| 验证 | `zod` | 运行时类型验证 |
| Google API | `googleapis`, `google-auth-library` | Gmail/日历集成 |
| MCP | `@modelcontextprotocol/sdk` | 工具扩展协议 |

### 架构特点
- **Monorepo 结构**: 使用 `apps/cli` 和 `apps/docs` 分离应用
- **依赖注入**: 使用 Awilix 实现模块化架构
- **多模型支持**: 通过 AI SDK 支持 Anthropic、Google、OpenAI 等
- **本地优先**: 所有数据以 Markdown 格式本地存储

---

## 核心功能模块

### 1. 知识同步模块 (`src/knowledge/`)
- `sync_gmail.ts` - Gmail 邮件同步
- `sync_calendar.ts` - 日历事件同步
- 将邮件和会议数据转换为知识图谱

### 2. Agent 运行时 (`src/agents/`)
- `runtime.ts` - 核心 Agent 执行引擎（29.6 KB）
- `agents.ts` - Agent 定义和管理
- `repo.ts` - Agent 持久化存储

### 3. 技能系统 (`src/application/assistant/skills/`)
- `builtin-tools/skill.ts` - 内置工具技能
- `mcp-integration/skill.ts` - MCP 服务器集成（12.4 KB）
- `workflow-authoring/skill.ts` - 工作流编排
- `workflow-run-ops/skill.ts` - 工作流运行操作

### 4. TUI 界面 (`src/tui/`)
- `ui.tsx` - 终端用户界面（40.7 KB，使用 Ink）
- `api.ts` - TUI API 接口

### 5. MCP 集成 (`src/mcp/`)
- `mcp.ts` - MCP 客户端实现
- `repo.ts` - MCP 服务器配置存储
- `schema.ts` - MCP 配置类型定义

---

## 代码结构概览

```
rowboat/
├── apps/
│   ├── cli/                    # 主 CLI 应用
│   │   ├── src/
│   │   │   ├── agents/         # Agent 运行时
│   │   │   ├── application/    # 应用逻辑
│   │   │   │   ├── assistant/  # 助手技能和指令
│   │   │   │   └── lib/        # 工具库
│   │   │   ├── config/         # 配置管理
│   │   │   ├── di/             # 依赖注入容器
│   │   │   ├── entities/       # 领域实体
│   │   │   ├── examples/       # 示例数据
│   │   │   ├── knowledge/      # 知识同步
│   │   │   ├── mcp/            # MCP 集成
│   │   │   ├── models/         # AI 模型配置
│   │   │   ├── runs/           # 运行管理
│   │   │   ├── tui/            # 终端界面
│   │   │   ├── app.ts          # 应用入口
│   │   │   └── server.ts       # HTTP 服务器
│   │   ├── bin/app.js          # CLI 入口
│   │   └── package.json
│   └── docs/                   # 文档站点
├── .github/workflows/          # CI/CD 配置
└── README.md
```

---

## 关键实现亮点

### 1. 本地优先架构
- 所有数据存储为纯 Markdown 文件
- 与 Obsidian 兼容的 Vault 结构
- 支持双向链接的知识图谱

### 2. 多模型 AI 支持
```typescript
// 支持多种 AI 提供商
@ai-sdk/anthropic    // Claude
@ai-sdk/google       // Gemini
@ai-sdk/openai       // GPT
ollama-ai-provider   // 本地模型
openrouter/ai-sdk-provider  // OpenRouter
```

### 3. MCP（Model Context Protocol）集成
- 支持外部工具和服务通过 MCP 协议接入
- 内置工具库 + 可扩展的 MCP 服务器
- 支持 Exa、Twitter/X、ElevenLabs、Slack、Linear/Jira、GitHub 等

### 4. 流式渲染引擎
- `stream-renderer.ts` - 实现实时流式输出
- 支持工具调用权限管理
- 人机交互确认机制

### 5. 工作流编排
- 支持复杂的多步骤工作流
- 子流程（subflow）管理
- 工作流运行状态持久化

---

## 适用场景建议

### 适合的场景
1. **个人知识管理** - 需要整合邮件、日历、笔记的知识工作者
2. **会议准备** - 自动汇总与会者背景和历史讨论
3. **内容创作** - 基于知识图谱生成文档、演示文稿
4. **隐私敏感场景** - 数据必须完全本地存储的合规要求
5. **AI 工作流自动化** - 需要自定义 AI 代理执行复杂任务

### 不适合的场景
1. **团队协作** - 当前主要面向个人使用
2. **企业级部署** - 缺少多用户和权限管理
3. **云端同步需求** - 本地优先架构不支持云同步

### 集成建议
- 与 Obsidian 配合使用获得最佳知识管理体验
- 配置 MCP 服务器扩展功能（如需要 Slack、Jira 集成）
- 使用本地模型（Ollama/LM Studio）确保完全离线运行

---

## 相关链接

- **GitHub**: https://github.com/rowboatlabs/rowboat
- **官网**: https://www.rowboatlabs.com/
- **Discord**: https://discord.gg/wajrgmJQ6b
- **Y Combinator**: S24 批次
