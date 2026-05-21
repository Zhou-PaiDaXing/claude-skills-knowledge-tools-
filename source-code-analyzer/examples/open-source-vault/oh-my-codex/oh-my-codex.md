---
title: "oh-my-codex (OMX)"
aliases: [oh-my-codex, OMX]
tags:
  - opensource
  - coding-agent
  - multi-agent
  - Python
  - mcp
github: https://github.com/mivanovitch/oh-my-codex
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# oh-my-codex (OMX) 项目分析报告

## 项目概述

**oh-my-codex (OMX)** 是一个为 OpenAI Codex CLI 设计的多智能体编排层（Multi-agent orchestration layer），由 Yeachan Heo 创建并维护。

- **GitHub Stars**: 22,924
- **主要语言**: TypeScript (核心), Rust (探索工具)
- **许可证**: MIT
- **Node.js 要求**: >= 20
- **官方网站**: https://yeachan-heo.github.io/oh-my-codex

### 核心定位

OMX 不替换 Codex，而是为其添加更好的工作层：
- **Codex** 执行实际的 Agent 工作
- **OMX 角色关键词** 使有用的角色可复用
- **OMX 技能** 使常见工作流可复用
- **`.omx/`** 存储计划、日志、记忆和运行时状态

---

## 技术栈分析

### 编程语言

| 语言 | 用途 | 说明 |
|------|------|------|
| **TypeScript** | 核心实现 | 完整类型支持，ESM模块 |
| **Rust** | 探索工具 | omx-explore-harness 高性能组件 |
| **Shell** | 脚本工具 | 辅助脚本 |

### 核心技术依赖

```json
{
  "dependencies": {
    "@iarna/toml": "^2.2.5",           // TOML配置解析
    "@modelcontextprotocol/sdk": "^1.26.0",  // MCP协议支持
    "zod": "^4.3.6"                    // 运行时类型验证
  },
  "devDependencies": {
    "@biomejs/biome": "^2.4.4",       // 代码规范
    "@types/node": "^25.5.0",         // Node类型
    "typescript": "^5.7.0"             // TypeScript编译器
  }
}
```

### 系统要求

- **Node.js**: >= 20
- **Codex CLI**: `npm install -g @openai/codex`
- **tmux**: macOS/Linux 团队模式必需
- **psmux**: Windows 团队模式（次要支持）

---

## 核心功能模块

### 1. 标准工作流

OMX 提供四个核心技能命令：

| 命令 | 用途 | 阶段 |
|------|------|------|
| `$deep-interview` | 澄清意图、边界和非目标 | 需求澄清 |
| `$ralplan` | 批准实施计划和权衡审查 | 计划制定 |
| `$ralph` | 持久完成和验证循环 | 执行完成 |
| `$team` | 协调并行执行 | 团队协作 |

### 2. 项目结构

```
oh-my-codex/
├── src/
│   ├── cli/              # CLI实现
│   │   ├── index.ts     # 主入口
│   │   ├── setup.ts     # 安装配置
│   │   ├── team.ts      # 团队管理
│   │   ├── ralph.ts     # Ralph模式
│   │   └── ...
│   ├── agents/          # Agent定义
│   ├── hooks/           # 生命周期钩子
│   ├── team/            # 团队运行时
│   ├── state/           # 状态管理
│   ├── mcp/             # MCP协议实现
│   ├── hud/             # HUD界面
│   └── wiki/            # Wiki功能
├── agents/              # Agent模板
├── skills/              # 技能定义
├── prompts/             # 提示词模板
├── crates/              # Rust组件
└── templates/           # 项目模板
```

### 3. CLI 命令体系

```bash
# 核心命令
omx setup               # 安装配置
omx --madmax --high     # 启动（推荐方式）
omx doctor              # 诊断检查

# 团队模式
omx team 3:executor "task"    # 创建团队
omx team status <name>        # 查看状态
omx team resume <name>        # 恢复团队
omx team shutdown <name>      # 关闭团队

# 探索工具
omx explore --prompt "..."    # 仓库探索
omx sparkshell <command>      # Shell检查

# Wiki
omx wiki list                 # 列出Wiki
omx wiki query --input '...'  # 查询Wiki
```

### 4. 核心模块详解

#### 4.1 CLI 模块 (`src/cli/`)

| 文件 | 功能 | 大小 |
|------|------|------|
| `index.ts` | 主CLI入口和命令路由 | 104KB |
| `setup.ts` | 安装和配置管理 | 51KB |
| `team.ts` | 团队生命周期管理 | 70KB |
| `explore.ts` | 代码探索功能 | 16KB |
| `doctor.ts` | 诊断和验证 | 26KB |

#### 4.2 团队运行时 (`src/team/`)

- tmux 会话管理
- 工作树协调
- 跨平台支持

#### 4.3 状态管理 (`src/state/`)

- 技能激活状态
- 工作流转换
- 会话历史

#### 4.4 HUD 界面 (`src/hud/`)

- 终端状态显示
- tmux面板管理
- 实时监控

#### 4.5 MCP 协议 (`src/mcp/`)

- Model Context Protocol 实现
- 状态服务器
- 追踪服务器

---

## 代码结构概览

### 核心架构

```
src/
├── index.ts                    # 包入口
├── cli/                        # CLI命令实现
│   ├── index.ts               # 主入口 (104KB)
│   ├── setup.ts               # 安装配置 (51KB)
│   ├── team.ts                # 团队管理 (70KB)
│   ├── ralph.ts               # Ralph模式 (10KB)
│   ├── explore.ts             # 探索工具 (16KB)
│   ├── doctor.ts              # 诊断工具 (26KB)
│   └── __tests__/             # 测试套件
├── agents/                     # Agent定义
│   ├── definitions.ts         # 角色定义
│   └── native-config.ts       # 原生配置
├── hooks/                      # 生命周期钩子
│   ├── agents-overlay.ts      # Agent覆盖层
│   ├── session.ts             # 会话管理
│   └── extensibility/         # 扩展机制
├── team/                       # 团队运行时
│   ├── runtime.ts             # 运行时核心
│   ├── tmux-session.ts        # tmux管理
│   └── __tests__/             # 团队测试
├── state/                      # 状态管理
│   ├── skill-active.ts        # 技能状态
│   └── workflow-transition.ts # 工作流转换
├── mcp/                        # MCP协议
│   ├── state-server.ts        # 状态服务器
│   └── trace-server.ts        # 追踪服务器
├── hud/                        # HUD界面
│   ├── index.ts               # HUD主入口
│   └── tmux.ts                # tmux集成
└── wiki/                       # Wiki功能
```

### 关键文件

| 文件路径 | 用途 | 说明 |
|----------|------|------|
| `src/cli/index.ts` | CLI主入口 | 命令路由和参数解析 |
| `src/cli/setup.ts` | 安装配置 | Codex hooks配置 |
| `src/cli/team.ts` | 团队管理 | tmux协调 |
| `src/hooks/session.ts` | 会话管理 | 生命周期跟踪 |
| `src/state/skill-active.ts` | 技能状态 | 工作流状态机 |

---

## 关键实现亮点

### 1. 原生 Codex Hooks 集成

```typescript
// .codex/hooks.json = 原生Codex钩子注册
// .omx/hooks/*.mjs = OMX插件钩子
```

OMX 通过原生 hooks 实现生命周期管理，而非替代 Codex。

### 2. 团队模式 (Team Mode)

```bash
# 创建3个执行Agent的并行团队
omx team 3:executor "fix the failing tests"
```

特点：
- 基于 tmux 的持久会话
- 工作树隔离
- 协调并行执行

### 3. Ralph 持久模式

```bash
$ralph "carry the approved plan to completion"
```

- 持续完成循环
- 自动验证检查点
- 状态持久化

### 4. 探索工具 (Explore)

Rust 编写的高性能代码探索：
```bash
omx explore --prompt "find where team state is written"
```

### 5. 状态管理架构

```
.omx/
├── plans/              # 计划存储
├── logs/               # 执行日志
├── memory/             # 长期记忆
├── wiki/               # Wiki内容
└── state/              # 运行时状态
```

### 6. 多语言支持

支持 16 种语言：
- 英语、韩语、日语、简体中文、繁体中文
- 越南语、西班牙语、葡萄牙语、俄语、土耳其语
- 德语、法语、意大利语、希腊语、波兰语、乌克兰语

---

## 适用场景建议

### 推荐场景

| 场景 | 适用度 | 说明 |
|------|--------|------|
| **复杂开发任务** | ★★★★★ | 需要多步骤、多文件修改 |
| **代码重构** | ★★★★★ | 大规模代码变更 |
| **团队并行开发** | ★★★★★ | 多人协作同一任务 |
| **探索性编程** | ★★★★☆ | 理解复杂代码库 |
| **日常编码** | ★★★☆☆ | 简单任务可能过于复杂 |

### 推荐工作流

```bash
# 1. 安装
npm install -g @openai/codex oh-my-codex
omx setup

# 2. 启动（推荐方式）
omx --madmax --high

# 3. 使用标准工作流
$deep-interview "clarify the authentication change"
$ralplan "approve the auth plan and review tradeoffs"
$ralph "carry the approved plan to completion"
$team 3:executor "execute the approved plan in parallel"
```

### 平台注意事项

| 平台 | 支持度 | 说明 |
|------|--------|------|
| macOS | ★★★★★ | 主要支持平台 |
| Linux | ★★★★★ | 完全支持 |
| Windows | ★★☆☆☆ | 次要支持，建议使用 WSL2 |

---

## 总结

oh-my-codex 是一个精心设计的 Codex CLI 增强层，通过标准化的工作流和团队协调功能，将个人 AI 编程助手扩展到团队协作场景。

**核心优势**:
- 与 Codex 原生集成，不替代
- 标准化的四阶段工作流
- 强大的团队并行执行能力
- 完善的状态管理和记忆
- 活跃的多语言社区

**最佳实践**:
- 复杂任务使用 `$deep-interview` 先澄清
- 重要变更使用 `$ralplan` 制定计划
- 大规模任务使用 `$team` 并行执行
- 长期任务使用 `$ralph` 持续跟进

**注意事项**:
- 简单任务可能不需要 OMX 的完整工作流
- 团队模式需要 tmux 支持
- Windows 用户建议使用 WSL2
