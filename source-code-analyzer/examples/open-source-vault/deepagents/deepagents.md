---
title: "Deep Agents"
aliases: [Deep Agents, deepagents]
tags:
  - opensource
  - multi-agent
  - Python
  - mcp
github: https://github.com/deepagents/deepagents
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Deep Agents 项目分析报告

## 项目概述

**Deep Agents** 是由 LangChain 团队开发的 Agent 框架（Agent Harness），定位为"开箱即用的有主见 Agent"。

- **GitHub Stars**: 20,768
- **主要语言**: Python
- **许可证**: MIT
- **官方网站**: https://docs.langchain.com/oss/python/deepagents/overview
- **Python 要求**: >= 3.11, < 4.0

### 核心定位

Deep Agents 是一个"电池已包含"（batteries-included）的 Agent 框架，开发者无需自己连接提示词、工具和上下文管理，即可获得一个立即可用的 Agent，并按需定制。

---

## 技术栈分析

### 编程语言

| 语言 | 用途 |
|------|------|
| **Python** | 核心实现 (100%) |

### 核心技术依赖

```toml
# 来自 libs/deepagents/pyproject.toml
[project]
dependencies = [
    "langchain-core>=1.2.27,<2.0.0",      # LangChain核心
    "langsmith>=0.3.0",                    # 可观测性
    "langchain>=1.2.15,<2.0.0",           # LangChain框架
    "langchain-anthropic>=1.4.0,<2.0.0",  # Anthropic集成
    "langchain-google-genai>=4.2.1,<5.0.0", # Google集成
    "wcmatch",                             # 通配符匹配
]
```

### 项目结构

```
deepagents/
├── libs/
│   ├── deepagents/       # 核心库
│   ├── cli/             # CLI工具
│   ├── acp/             # Agent Communication Protocol
│   ├── evals/           # 评估工具
│   └── repl/            # REPL环境
├── examples/            # 示例项目
└── .github/            # GitHub配置
```

---

## 核心功能模块

### 1. 开箱即用的功能

| 功能 | 工具/实现 | 说明 |
|------|-----------|------|
| **规划** | `write_todos` | 任务分解和进度跟踪 |
| **文件系统** | `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep` | 读写上下文 |
| **Shell访问** | `execute` | 运行命令（带沙箱） |
| **子Agent** | `task` | 委派工作，隔离上下文窗口 |
| **智能默认** | 内置提示词 | 教导模型有效使用工具 |
| **上下文管理** | 自动摘要 | 对话过长时自动摘要，大输出保存到文件 |

### 2. 核心架构

```
deepagents/
├── __init__.py              # 包入口
├── graph.py                 # 主图组装模块 (29KB)
├── _models.py               # 模型解析
├── backends/                # 后端实现
│   ├── __init__.py
│   ├── protocol.py          # 后端协议
│   └── ...
├── middleware/              # 中间件层
│   ├── async_subagents.py   # 异步子Agent
│   ├── filesystem.py        # 文件系统中间件
│   ├── memory.py            # 记忆中间件
│   ├── permissions.py       # 权限控制
│   ├── skills.py            # 技能中间件
│   ├── subagents.py         # 子Agent中间件
│   └── summarization.py     # 摘要中间件
└── profiles/                # 配置文件
```

### 3. 主要入口函数

```python
from deepagents import create_deep_agent

# 创建默认Agent
agent = create_deep_agent()

# 自定义Agent
agent = create_deep_agent(
    model=init_chat_model("openai:gpt-4o"),
    tools=[my_custom_tool],
    system_prompt="You are a research assistant.",
)
```

### 4. 中间件系统

| 中间件 | 功能 | 文件 |
|--------|------|------|
| **AsyncSubAgentMiddleware** | 异步子Agent支持 | `async_subagents.py` |
| **FilesystemMiddleware** | 文件系统操作 | `filesystem.py` |
| **MemoryMiddleware** | 持久化记忆 | `memory.py` |
| **SubAgentMiddleware** | 子Agent管理 | `subagents.py` |
| **SkillsMiddleware** | 技能系统 | `skills.py` |
| **SummarizationMiddleware** | 自动摘要 | `summarization.py` |

### 5. CLI 工具

```bash
# 安装
curl -LsSf https://raw.githubusercontent.com/langchain-ai/deepagents/main/libs/cli/scripts/install.sh | bash

# 功能特点
- 交互式TUI - 富终端界面，流式响应
- Web搜索 - 基于实时信息的响应
- 无头模式 - 用于脚本和CI的非交互式运行
- 远程沙箱 - 安全执行环境
- 持久记忆 - 跨会话记忆
- 自定义技能 - 可扩展能力
- 人工介入 - 审批流程
```

---

## 代码结构概览

### 核心模块

```python
# deepagents/graph.py - 主图组装模块

def create_deep_agent(
    model: BaseChatModel | None = None,
    tools: Sequence[BaseTool] | None = None,
    system_prompt: str | None = None,
    # ... 更多参数
) -> CompiledStateGraph:
    """
    创建完全配置的Deep Agent
    包含规划、文件系统、子Agent和摘要中间件
    """
```

### 系统提示词设计

```python
BASE_AGENT_PROMPT = """
You are a Deep Agent, an AI assistant that helps users accomplish tasks using tools...

## Core Behavior
- Be concise and direct. Don't over-explain unless asked.
- NEVER add unnecessary preamble ("Sure!", "Great question!"...)
- Don't say "I'll now do X" — just do it.

## Doing Tasks
1. **Understand first** — read relevant files, check existing patterns
2. **Act** — implement the solution
3. **Verify** — check your work against what was asked

## When things go wrong:
- If something fails repeatedly, stop and analyze *why*
- If you're blocked, tell the user what's wrong
"""
```

### LangGraph 原生集成

```python
# create_deep_agent 返回编译后的 LangGraph 图
from langgraph.graph.state import CompiledStateGraph

agent: CompiledStateGraph = create_deep_agent()

# 支持所有 LangGraph 特性
# - 流式输出
# - Studio 可视化
# - 检查点持久化
# - 任意 LangGraph 功能
```

---

## 关键实现亮点

### 1. 灵感来源

项目主要受 **Claude Code** 启发，最初是尝试理解 Claude Code 的通用性原理并使其更加通用。

### 2. 安全模型

采用"信任 LLM"模型：
- Agent 可以执行其工具允许的任何操作
- 在工具/沙箱级别强制执行边界
- 不期望模型自我约束

### 3. MCP 支持

通过 `langchain-mcp-adapters` 支持 Model Context Protocol：
```python
# MCP工具可以无缝集成
```

### 4. 多后端支持

```python
# 支持多种状态后端
from deepagents.backends import StateBackend

# 包括：
# - 内存后端（开发）
# - 数据库后端（生产）
# - 自定义后端
```

### 5. 权限系统

```python
from deepagents.middleware.permissions import FilesystemPermission

# 细粒度文件系统权限控制
permission = FilesystemPermission(
    allow_paths=["/project/src"],
    deny_paths=["/project/secrets"]
)
```

### 6. 异步子Agent

```python
from deepagents import AsyncSubAgent, AsyncSubAgentMiddleware

# 并行执行多个子任务
```

---

## 适用场景建议

### 推荐场景

| 场景 | 适用度 | 说明 |
|------|--------|------|
| **通用Agent开发** | ★★★★★ | 快速构建生产级Agent |
| **代码助手** | ★★★★★ | 类似Claude Code的体验 |
| **自动化工作流** | ★★★★★ | 文件处理、数据分析 |
| **研究助手** | ★★★★☆ | 信息收集和整理 |
| **多步骤任务** | ★★★★★ | 需要规划和执行的任务 |

### 快速开始

```python
# 安装
pip install deepagents
# 或
uv add deepagents

# 基础用法
from deepagents import create_deep_agent

agent = create_deep_agent()
result = agent.invoke({
    "messages": [{"role": "user", "content": "Research LangGraph and write a summary"}]
})

# 自定义
from langchain.chat_models import init_chat_model

agent = create_deep_agent(
    model=init_chat_model("openai:gpt-4o"),
    tools=[my_custom_tool],
    system_prompt="You are a research assistant.",
)
```

### CLI 使用

```bash
# 安装CLI
curl -LsSf https://raw.githubusercontent.com/langchain-ai/deepagents/main/libs/cli/scripts/install.sh | bash

# 启动交互式会话
deepagents

# 无头模式（脚本/CI）
deepagents --headless "run tests and report results"
```

---

## 总结

Deep Agents 是 LangChain 生态系统中一个精心设计的 Agent 框架，提供了生产就绪的默认值和灵活的定制能力。

**核心优势**:
- 100% 开源，MIT 许可
- 提供商无关，支持任何支持工具调用的 LLM
- 基于 LangGraph，生产就绪的运行时
- 电池已包含，开箱即用
- 秒级启动，分钟级定制

**设计哲学**:
- 约定优于配置
- 渐进式定制
- 安全在工具层而非提示词层
- 与 LangChain 生态无缝集成

**最佳实践**:
- 从默认配置开始
- 按需添加自定义工具
- 使用 LangSmith 进行调试和监控
- 生产环境配置持久化后端
