---
title: "CrewAI"
aliases: [CrewAI, crewai]
tags:
  - opensource
  - multi-agent
  - Python
  - role-playing
github: https://github.com/crewAIInc/crewAI
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# CrewAI

## 项目简介

**CrewAI** 是一个用于编排角色扮演、自主 AI 代理的 Python 框架。它完全从零开始构建，**独立于 LangChain 或其他代理框架**，赋予开发者高级简洁性和精确的低级控制能力，适用于创建适用于任何场景的自主 AI 代理。

- **GitHub**: https://github.com/crewAIInc/crewAI
- **Stars**: 48,913
- **License**: MIT
- **Python 要求**: >=3.10, <3.14
- **社区**: 100,000+ 认证开发者

---

## 技术栈分析

### 核心依赖
| 依赖 | 版本 | 用途 |
|------|------|------|
| `pydantic` | ~2.11.9 | 数据验证和序列化 |
| `openai` | >=2.0.0,<3 | OpenAI API 客户端 |
| `instructor` | >=1.3.3 | 结构化输出 |
| `chromadb` | ~1.1.0 | 向量数据库 |
| `textual` | >=7.5.0 | TUI (终端用户界面) |
| `mcp` | ~1.26.0 | Model Context Protocol |
| `lancedb` | >=0.29.2 | 嵌入式向量数据库 |

### 可选依赖组
| 组 | 依赖 | 用途 |
|----|------|------|
| `tools` | crewai-tools | 扩展工具集 |
| `embeddings` | tiktoken | 文本分词 |
| `mem0` | mem0ai | 记忆功能 |
| `docling` | docling | 文档处理 |
| `qdrant` | qdrant-client | 向量数据库 |
| `aws` | boto3 | AWS 集成 |
| `bedrock` | boto3 | AWS Bedrock |
| `google-genai` | google-genai | Google AI |
| `a2a` | a2a-sdk | Agent-to-Agent 协议 |

### 开发工具链
| 工具 | 用途 |
|------|------|
| **UV** | 现代 Python 包管理 |
| **Ruff** | 0.15.1 - 快速 Python 检查 |
| **MyPy** | 1.19.1 - 静态类型检查 |
| **Pytest** | 9.0.3 - 测试框架 |
| **Bandit** | 1.9.2 - 安全检查 |
| **Pre-commit** | Git 钩子 |

---

## 核心功能模块

### 1. 双架构模式

#### Crews (代理团队)
- **角色扮演**: 专业角色定义（研究员、分析师、开发者）
- **目标导向**: 每个代理有明确的目标和背景故事
- **自主协作**: 代理间自然决策和动态任务委托
- **流程类型**: Sequential (顺序) / Hierarchical (层级)

#### Flows (事件驱动工作流)
- **精确控制**: 细粒度执行路径控制
- **状态管理**: 安全的任务间状态传递
- **条件分支**: 基于结果的路由决策
- **原生集成**: 与 Crews 无缝结合

### 2. 核心组件

#### Agent (代理)
```python
from crewai import Agent

researcher = Agent(
    role='Senior Data Researcher',
    goal='Uncover cutting-edge developments in AI',
    backstory='You are a seasoned researcher...',
    verbose=True,
    tools=[SerperDevTool()]
)
```

#### Task (任务)
```python
from crewai import Task

research_task = Task(
    description='Conduct thorough research about {topic}',
    expected_output='A list with 10 bullet points...',
    agent=researcher,
    output_file='report.md'
)
```

#### Crew (团队)
```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, reporting_task],
    process=Process.sequential,
    verbose=True
)
```

#### Flow (流程)
```python
from crewai.flow.flow import Flow, listen, start

class AnalysisFlow(Flow):
    @start()
    def fetch_data(self):
        return {"sector": "tech"}
    
    @listen(fetch_data)
    def analyze(self, data):
        # 执行分析
        pass
```

### 3. 高级功能

#### 记忆系统 (`memory/`)
- **短期记忆**: 会话上下文
- **长期记忆**: 跨会话持久化
- **实体记忆**: 关键信息提取
- **向量存储**: LanceDB/ChromaDB 集成

#### 知识库 (`knowledge/`)
- 文档嵌入和检索
- 支持多种文档格式
- RAG (检索增强生成)

#### 工具系统 (`tools/`)
- 内置工具集
- 自定义工具支持
- 工具调用管理

#### A2A 协议 (`a2a/`)
- Agent-to-Agent 通信
- 跨平台代理协作
- 标准化消息格式

#### MCP 集成 (`mcp/`)
- Model Context Protocol 支持
- 外部工具和服务集成

---

## 代码结构概览

```
crewAI/
├── lib/
│   ├── crewai/                    # 核心库
│   │   ├── src/crewai/
│   │   │   ├── __init__.py        # 主入口
│   │   │   ├── crew.py            # Crew 核心 (85KB)
│   │   │   ├── agent/             # 代理模块
│   │   │   │   ├── core.py        # Agent 核心
│   │   │   │   └── planning_config.py
│   │   │   ├── agents/            # 代理相关
│   │   │   │   ├── agent_builder/
│   │   │   │   ├── crew_agent_executor.py
│   │   │   │   └── tools_handler.py
│   │   │   ├── task.py            # Task 核心 (52KB)
│   │   │   ├── tasks/             # 任务相关
│   │   │   ├── flow/              # Flow 模块
│   │   │   │   └── flow.py        # Flow 核心
│   │   │   ├── llm.py             # LLM 接口 (99KB)
│   │   │   ├── llms/              # LLM 实现
│   │   │   ├── memory/            # 记忆系统
│   │   │   ├── knowledge/         # 知识库
│   │   │   ├── tools/             # 工具系统
│   │   │   ├── skills/            # 技能系统
│   │   │   ├── events/            # 事件系统
│   │   │   ├── state/             # 状态管理
│   │   │   ├── telemetry/         # 遥测
│   │   │   ├── cli/               # 命令行工具
│   │   │   ├── a2a/               # A2A 协议
│   │   │   ├── mcp/               # MCP 集成
│   │   │   ├── rag/               # RAG 系统
│   │   │   ├── hooks/             # 钩子系统
│   │   │   ├── security/          # 安全模块
│   │   │   ├── utilities/         # 工具函数
│   │   │   └── types/             # 类型定义
│   │   └── pyproject.toml
│   ├── crewai-tools/              # 工具库
│   ├── crewai-files/              # 文件处理
│   └── devtools/                  # 开发工具
├── docs/                          # 文档
├── pyproject.toml                 # 工作区配置
└── uv.lock                        # 依赖锁定
```

---

## 关键实现亮点

### 1. 独立架构设计
```python
# 完全独立于 LangChain
# 自定义 Agent 执行器
class CrewAgentExecutor(BaseAgentExecutor):
    """CrewAI 专用代理执行器"""
    pass
```

### 2. 装饰器模式
```python
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MyCrew:
    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'])
    
    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])
    
    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)
```

### 3. 流程控制
```python
from crewai.flow.flow import Flow, listen, start, router, or_

class AdvancedFlow(Flow[MarketState]):
    @start()
    def fetch_data(self):
        return data
    
    @listen(fetch_data)
    def process(self, data):
        return result
    
    @router(process)
    def decide(self):
        if condition:
            return "path_a"
        return "path_b"
    
    @listen("path_a")
    def handle_a(self):
        pass
    
    @listen(or_("path_a", "path_b"))
    def handle_both(self):
        pass
```

### 4. 延迟加载优化
```python
# 重模块延迟导入
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "Memory": ("crewai.memory.unified_memory", "Memory"),
}

def __getattr__(name: str) -> Any:
    if name in _LAZY_IMPORTS:
        module_path, attr = _LAZY_IMPORTS[name]
        mod = importlib.import_module(module_path)
        return getattr(mod, attr)
```

### 5. 类型安全
```python
# Pydantic v2 完整支持
from pydantic import BaseModel, Field

class MarketState(BaseModel):
    sentiment: str = "neutral"
    confidence: float = 0.0
    recommendations: list = []
```

---

## 适用场景建议

### 推荐场景
| 场景 | 说明 | 示例 |
|------|------|------|
| **研究分析** | 多步骤研究任务 | 股票分析、市场调研 |
| **内容创作** | 协作写作 | 博客文章、技术文档 |
| **代码开发** | 多代理编程 | 功能开发、代码审查 |
| **客户服务** | 自动化支持 | 工单处理、FAQ |
| **数据处理** | ETL 管道 | 数据清洗、转换 |
| **企业自动化** | 业务流程 | 报告生成、审批流程 |

### 完整示例
```python
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

# 定义代理
researcher = Agent(
    role='Senior Researcher',
    goal='Research latest AI developments',
    backstory='Expert researcher with 10 years experience',
    tools=[SerperDevTool()],
    verbose=True
)

writer = Agent(
    role='Technical Writer',
    goal='Write comprehensive reports',
    backstory='Professional technical writer',
    verbose=True
)

# 定义任务
research_task = Task(
    description='Research {topic} and find 10 key points',
    expected_output='List of 10 bullet points',
    agent=researcher
)

writing_task = Task(
    description='Write a report based on research',
    expected_output='Full markdown report',
    agent=writer,
    output_file='report.md'
)

# 创建团队
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)

# 执行
result = crew.kickoff(inputs={'topic': 'AI Agents'})
```

### 与竞品对比
| 特性 | CrewAI | LangGraph | AutoGen | ChatDev |
|------|--------|-----------|---------|---------|
| 依赖 | 独立 | LangChain | 多依赖 | 有限 |
| 性能 | 5.76x 更快 | 基准 | 较慢 | 一般 |
| 易用性 | 高 | 中 | 中 | 中 |
| 生产就绪 | 是 | 是 | 部分 | 否 |
| 社区 | 100K+ | 大 | 中 | 小 |
| 企业支持 | AMP 套件 | 有限 | 无 | 无 |

---

## 总结

CrewAI 是一个**独立、高性能、生产级**的多代理编排框架。其亮点包括：

1. **零依赖**: 完全独立于 LangChain，更轻量更快
2. **双模式**: Crews (自主) + Flows (精确) 灵活组合
3. **类型安全**: Pydantic v2 完整类型支持
4. **企业就绪**: AMP 套件提供完整企业功能
5. **活跃社区**: 100,000+ 认证开发者

适合需要**复杂多代理协作、生产级部署、精细控制**的 AI 自动化项目。
