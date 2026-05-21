---
title: "OpenHarness"
aliases: [OpenHarness, openharness]
tags:
  - opensource
  - testing-benchmark
  - Python
  - mcp
github: https://github.com/nicepkg/openharness
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# OpenHarness

## 项目简介

**OpenHarness** 是一个开源的轻量级代理基础设施框架，提供工具使用、技能、记忆和多代理协调等核心功能。它包含 **ohmo** —— 一个基于 OpenHarness 构建的个人 AI 代理，可以在飞书/Slack/Telegram/Discord 中聊天，并自动执行分支创建、代码编写、测试运行和 PR 提交等任务。

- **GitHub**: https://github.com/HKUDS/OpenHarness
- **PyPI**: `openharness-ai`
- **Stars**: 9,694
- **License**: MIT
- **Python 要求**: >=3.10
- **测试覆盖**: 114 个单元测试 + E2E 测试

---

## 技术栈分析

### 核心依赖
| 依赖 | 版本 | 用途 |
|------|------|------|
| `anthropic` | >=0.40.0 | Claude API 客户端 |
| `openai` | >=1.0.0 | OpenAI API 客户端 |
| `pydantic` | >=2.0.0 | 数据验证 |
| `rich` | >=13.0.0 | 终端美化 |
| `textual` | >=0.80.0 | TUI 框架 |
| `typer` | >=0.12.0 | CLI 框架 |
| `mcp` | >=1.0.0 | Model Context Protocol |
| `websockets` | >=12.0 | WebSocket 支持 |

### 通信集成
| 依赖 | 用途 |
|------|------|
| `slack-sdk` | Slack 集成 |
| `python-telegram-bot` | Telegram 集成 |
| `discord.py` | Discord 集成 |
| `lark-oapi` | 飞书集成 |

### 开发工具链
| 工具 | 用途 |
|------|------|
| **Hatchling** | 构建后端 |
| **Pytest** | 测试框架 |
| **Ruff** | 代码检查 |
| **MyPy** | 类型检查 |
| **React + Ink** | 终端 UI |

---

## 核心功能模块

### 1. Harness 架构 (10 个子系统)

```
openharness/
├── engine/          # Agent Loop - 查询→流→工具调用→循环
├── tools/           # 43+ 工具 - 文件、Shell、搜索、Web、MCP
├── skills/          # 知识 - 按需加载技能 (.md 文件)
├── plugins/         # 扩展 - 命令、钩子、代理、MCP 服务器
├── permissions/     # 安全 - 多级模式、路径规则
├── hooks/           # 生命周期 - PreToolUse/PostToolUse 事件
├── commands/        # 54 个命令 - /help, /commit, /plan, /resume
├── mcp/             # MCP - Model Context Protocol 客户端
├── memory/          # 记忆 - 跨会话持久化知识
├── tasks/           # 任务 - 后台任务管理
├── coordinator/     # 多代理 - 子代理生成、团队协调
├── prompts/         # 上下文 - 系统提示组装
├── config/          # 设置 - 多层配置
└── ui/              # React TUI - 终端界面
```

### 2. Agent Loop (核心引擎)
```python
while True:
    response = await api.stream(messages, tools)
    
    if response.stop_reason != "tool_use":
        break  # 模型完成
    
    for tool_call in response.tool_uses:
        # 权限检查 → 钩子 → 执行 → 钩子 → 结果
        result = await harness.execute_tool(tool_call)
    
    messages.append(tool_results)
    # 循环继续 - 模型看到结果，决定下一步
```

### 3. 工具系统 (43+ 工具)

| 类别 | 工具 | 描述 |
|------|------|------|
| **文件 I/O** | Bash, Read, Write, Edit, Glob, Grep | 核心文件操作 |
| **搜索** | WebFetch, WebSearch, ToolSearch, LSP | 网络和代码搜索 |
| **Notebook** | NotebookEdit | Jupyter 单元格编辑 |
| **代理** | Agent, SendMessage, TeamCreate/Delete | 子代理生成 |
| **任务** | TaskCreate/Get/List/Update/Stop/Output | 后台任务 |
| **MCP** | MCPTool, ListMcpResources | MCP 集成 |
| **模式** | EnterPlanMode, ExitPlanMode | 工作流切换 |
| **计划** | CronCreate/List/Delete | 定时任务 |

### 4. 权限系统

| 模式 | 行为 | 使用场景 |
|------|------|----------|
| **Default** | 写入/执行前询问 | 日常开发 |
| **Auto** | 允许所有操作 | 沙箱环境 |
| **Plan Mode** | 阻止所有写入 | 大规模重构 |

### 5. 多提供商支持

| 工作流 | 格式 | 后端示例 |
|--------|------|----------|
| **Anthropic-Compatible** | Anthropic 格式 | Claude、Kimi、GLM、MiniMax |
| **Claude Subscription** | CLI 订阅桥接 | `~/.claude/.credentials.json` |
| **OpenAI-Compatible** | OpenAI 格式 | OpenAI、DeepSeek、Ollama |
| **Codex Subscription** | Codex CLI 桥接 | `~/.codex/auth.json` |
| **GitHub Copilot** | OAuth 流程 | Copilot 设备流 |

### 6. ohmo 个人代理

```bash
ohmo init             # 初始化 ~/.ohmo 工作区
ohmo config           # 配置频道和提供商
ohmo gateway start    # 启动网关
```

**工作区结构**:
```
~/.ohmo/
├── soul.md           # 长期代理个性
├── identity.md       # 代理身份
├── user.md           # 用户画像
├── BOOTSTRAP.md      # 首次运行仪式
├── memory/           # 个人记忆
└── gateway.json      # 提供商和频道配置
```

---

## 代码结构概览

```
OpenHarness/
├── src/
│   ├── openharness/           # 主包
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── cli.py             # CLI 入口 (50KB)
│   │   ├── api/               # API 客户端
│   │   ├── auth/              # 认证管理
│   │   ├── bridge/            # 桥接层
│   │   ├── channels/          # 通信频道
│   │   ├── commands/          # 54 个命令
│   │   ├── config/            # 配置管理
│   │   ├── coordinator/       # 多代理协调
│   │   ├── engine/            # Agent Loop 引擎
│   │   ├── hooks/             # 生命周期钩子
│   │   ├── keybindings/       # 快捷键
│   │   ├── mcp/               # MCP 客户端
│   │   ├── memory/            # 记忆系统
│   │   ├── output_styles/     # 输出样式
│   │   ├── permissions/       # 权限系统
│   │   ├── personalization/   # 个性化
│   │   ├── platforms.py       # 平台检测
│   │   ├── plugins/           # 插件系统
│   │   ├── prompts/           # 提示词管理
│   │   ├── sandbox/           # 沙箱
│   │   ├── services/          # 服务层
│   │   ├── skills/            # 技能系统
│   │   ├── state/             # 状态管理
│   │   ├── swarm/             # 代理群
│   │   ├── tasks/             # 任务管理
│   │   ├── themes/            # 主题
│   │   ├── tools/             # 44 个工具
│   │   ├── ui/                # React TUI
│   │   ├── utils/             # 工具函数
│   │   └── voice/             # 语音
│   └── ohmo/                  # ohmo 个人代理
│       └── cli.py
├── frontend/                  # React Ink TUI
│   └── terminal/
├── tests/                     # 测试套件
├── scripts/                   # 脚本
└── pyproject.toml
```

---

## 关键实现亮点

### 1. 自定义工具注册
```python
from pydantic import BaseModel, Field
from openharness.tools.base import BaseTool, ToolExecutionContext, ToolResult

class MyToolInput(BaseModel):
    query: str = Field(description="Search query")

class MyTool(BaseTool):
    name = "my_tool"
    description = "Does something useful"
    input_model = MyToolInput

    async def execute(self, arguments: MyToolInput, context: ToolExecutionContext) -> ToolResult:
        return ToolResult(output=f"Result for: {arguments.query}")
```

### 2. 技能系统
```markdown
---
name: my-skill
description: Expert guidance for my domain
---

# My Skill

## When to use
Use when the user asks about [your domain].

## Workflow
1. Step one
2. Step two
```

### 3. 插件兼容
兼容 `claude-code plugins`:
| 插件 | 类型 | 功能 |
|------|------|------|
| `commit-commands` | 命令 | Git 提交、推送、PR |
| `security-guidance` | 钩子 | 文件编辑安全警告 |
| `hookify` | 命令+代理 | 自定义行为钩子 |
| `feature-dev` | 命令 | 功能开发工作流 |

### 4. 流式输出
```python
# JSON 流式输出
oh -p "List functions" --output-format stream-json

# 实时事件流
for event in stream:
    if event.type == "tool_call":
        print(f"Tool: {event.tool_name}")
    elif event.type == "content":
        print(event.text, end="")
```

### 5. 上下文压缩
- **Auto-Compaction**: 自动压缩上下文保留任务状态
- **Channel Logs**: 跨上下文压缩保留频道日志
- **多天长会话**: 无需手动清理即可运行多天

---

## 适用场景建议

### 推荐场景
| 场景 | 说明 |
|------|------|
| **代码助手** | 读取代码、修补文件、运行检查 |
| **自动化脚本** | JSON/stream-json 输出用于自动化 |
| **插件测试** | Claude 风格扩展的实验平台 |
| **多代理原型** | 任务委托和后台执行 |
| **提供商比较** | 跨 Anthropic 兼容后端的沙箱 |
| **个人代理** | ohmo 在聊天应用中工作 |

### CLI 使用示例
```bash
# 交互模式
oh

# 单条命令
oh -p "Explain this codebase"

# JSON 输出
oh -p "List functions" --output-format json

# 流式 JSON
oh -p "Fix bug" --output-format stream-json

# 权限模式
oh --permission-mode auto

# 继续会话
oh -c

# 恢复历史
oh -r
```

### 与竞品对比
| 特性 | OpenHarness | Claude Code | Codex | Aider |
|------|-------------|-------------|-------|-------|
| 开源 | 是 | 否 | 否 | 是 |
| 多提供商 | 是 | 否 | 否 | 部分 |
| 个人代理 | ohmo | 否 | 否 | 否 |
| 插件系统 | 是 | 是 | 有限 | 有限 |
| TUI | React Ink | 自定义 | 自定义 | 有限 |
| 记忆系统 | 是 | 部分 | 否 | 否 |

---

## 总结

OpenHarness 是一个**开源、轻量、可扩展**的代理基础设施框架。其亮点包括：

1. **开源自由**: 完全开源，可审查和扩展
2. **多提供商**: 支持 Claude/OpenAI/Copilot/Codex 等
3. **个人代理**: ohmo 提供聊天集成和长期记忆
4. **插件生态**: 兼容 Claude Code 插件
5. **生产就绪**: 114+ 测试，E2E 覆盖

适合需要**自托管 AI 助手、多提供商灵活性、聊天集成**的开发者。
