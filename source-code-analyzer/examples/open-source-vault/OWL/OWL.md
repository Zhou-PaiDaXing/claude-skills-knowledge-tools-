---
title: "OWL: Optimized Workforce Learning"
aliases: [OWL, CAMEL-AI OWL]
tags:
  - opensource
  - multi-agent
  - Python
  - task-automation
github: https://github.com/camel-ai/owl
created: 2026-04-15
updated: 2026-04-15
score: 5.09
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# OWL: Optimized Workforce Learning for General Multi-Agent Assistance

> **GitHub**: [camel-ai/owl](https://github.com/camel-ai/owl)  
> **Stars**: 19,654  
> **Language**: Python  
> **License**: Apache-2.0  
> **Paper**: [arXiv:2505.23885](https://arxiv.org/abs/2505.23885)

---

## 项目简介

OWL 是一个前沿的多智能体协作框架，旨在推动现实世界任务自动化的边界。它基于 CAMEL-AI 框架构建，通过动态智能体交互实现更自然、高效和稳健的任务自动化。

**核心成就**：
- 在 GAIA 基准测试中获得 **69.09** 平均分，排名开源框架 **#1**
- 被 NeurIPS 2025 接收
- 已开源训练数据集和模型检查点

---

## 技术栈分析

### 核心依赖
| 组件 | 用途 |
|------|------|
| `camel-ai[owl]==0.2.84` | 底层多智能体框架 |
| `gradio>=6.4.0` | Web UI 界面 |
| `mcp-simple-arxiv` / `mcp-server-fetch` | MCP 协议服务 |
| `firecrawl>=2.5.3` / `crawl4ai>=0.3.0` | 网页爬取 |
| `mistralai>=1.7.0` | Mistral AI 模型支持 |
| `docx2markdown>=0.1.1` | 文档转换 |

### 支持模型平台
- OpenAI (GPT-4/5)
- Claude (Anthropic)
- Gemini (Google)
- Qwen (阿里)
- DeepSeek
- Ollama (本地)
- Azure OpenAI
- OpenRouter
- Groq

---

## 核心功能模块

### 1. 多智能体工作流 (Workforce)
```python
# 核心架构：协调器 + 任务代理 + 工作节点
workforce = Workforce(
    "Workforce",
    task_agent=task_agent,
    coordinator_agent=coordinator_agent,
)
```

**预置智能体类型**：
- **Web Agent**: 网页搜索、内容提取、浏览器模拟
- **Document Processing Agent**: PDF/Word/Excel/图片/音频/视频处理
- **Reasoning Coding Agent**: 推理、编程、Excel 处理

### 2. 工具包生态系统 (Toolkits)

| 类别 | 工具包 |
|------|--------|
| **多模态** | BrowserToolkit, VideoAnalysisToolkit, ImageAnalysisToolkit |
| **搜索** | SearchToolkit (Google, DuckDuckGo, Wikipedia, Baidu, Bocha) |
| **文档** | DocumentProcessingToolkit, ExcelToolkit |
| **代码** | CodeExecutionToolkit (Python 沙箱) |
| **MCP** | MCPToolkit (Model Context Protocol) |
| **其他** | ArxivToolkit, GitHubToolkit, WeatherToolkit, RedditToolkit |

### 3. Web 界面
- 基于 Gradio 的交互式 UI
- 支持多语言 (中/英/日)
- 环境变量配置管理
- 实时任务历史记录

---

## 代码结构概览

```
owl/
├── owl/
│   ├── utils/
│   │   ├── enhanced_role_playing.py    # 增强角色扮演核心
│   │   ├── document_toolkit.py         # 文档处理工具
│   │   └── gaia.py                     # GAIA 基准评估
│   ├── webapp.py / webapp_zh.py        # Web 界面 (Gradio)
│   └── .env                            # 环境变量配置
├── examples/
│   ├── run.py                          # 标准示例
│   ├── run_mini.py                     # 最小化示例
│   ├── run_claude.py                   # Claude 模型示例
│   ├── run_qwen.py                     # 通义千问示例
│   ├── run_mcp.py                      # MCP 示例
│   └── ...                             # 其他模型示例
├── community_usecase/                  # 社区用例
│   ├── a_share_investment_agent_camel/ # A股投资智能体
│   ├── stock-analysis/                 # 股票分析
│   ├── cooking-assistant/              # 烹饪助手
│   └── ...
├── pyproject.toml
└── requirements.txt
```

---

## 关键实现亮点

### 1. 增强角色扮演架构
```python
class OwlRolePlaying(RolePlaying):
    """扩展 CAMEL 的 RolePlaying，支持 GAIA 系统消息构造"""
    def _construct_gaia_sys_msgs(self):
        # 构建针对 GAIA 基准优化的系统消息
```

### 2. 浏览器自动化集成
- 基于 Playwright 的浏览器工具包
- 支持多浏览器通道 (chrome, msedge, chromium)
- 支持滚动、点击、输入、下载、导航等操作

### 3. MCP (Model Context Protocol) 支持
```python
# MCP 工具调用示例
from camel.toolkits import MCPToolkit
mcp_toolkit = MCPToolkit(config_path="mcp_config.json")
```

### 4. 文档处理流水线
- 支持 PDF、Word、Excel、PowerPoint 解析
- 集成 OCR 和图像分析
- 自动格式转换为 Markdown

---

## 适用场景建议

### 适合场景
| 场景 | 说明 |
|------|------|
| **复杂研究任务** | 需要多步骤信息收集、分析和总结 |
| **自动化办公** | 文档处理、数据提取、报告生成 |
| **网页数据抓取** | 动态网页交互、表单填写、内容提取 |
| **多模态分析** | 图像、视频、音频内容理解和处理 |
| **代码生成执行** | 自动编写和运行 Python 脚本 |

### 使用建议
1. **模型选择**: 推荐使用 GPT-4/5 或 Claude 以获得最佳工具调用能力
2. **工具配置**: 根据任务需求选择必要的工具包，避免资源浪费
3. **环境配置**: 使用 `.env` 文件管理 API 密钥
4. **GAIA 复现**: 使用 `gaia69` 分支进行基准测试复现

### 快速开始
```bash
# 安装
pip install -e .

# 配置环境变量
cp .env_template .env
# 编辑 .env 添加 OPENAI_API_KEY

# 运行示例
python examples/run.py

# 启动 Web UI
python owl/webapp_zh.py
```

---

## 相关资源

- **文档**: https://docs.camel-ai.org
- **社区**: [Discord](https://discord.camel-ai.org/) | [WeChat](https://ghli.org/camel/wechat.png)
- **依赖框架**: [CAMEL-AI](https://github.com/camel-ai/camel)
- **论文**: [OWL: Optimized Workforce Learning](https://arxiv.org/abs/2505.23885)
