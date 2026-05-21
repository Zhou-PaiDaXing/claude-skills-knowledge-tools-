---
title: "Vibe-Trading"
aliases: [Vibe Trading, Vibe-Trading]
tags:
  - opensource
  - trading
  - Python
  - ai-agent
github: https://github.com/nicepkg/vibe-trading
created: 2026-04-15
updated: 2026-04-15
score: 5.12
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# Vibe-Trading: Your Personal Trading Agent

> **GitHub**: [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading)  
> **Stars**: 1,877  
> **Language**: Python / TypeScript  
> **License**: MIT  
> **PyPI**: `vibe-trading-ai`

---

## 项目简介

Vibe-Trading 是一个 AI 驱动的多智能体金融工作空间，将自然语言请求转化为可执行的交易策略、研究洞察和跨市场的投资组合分析。它整合了 69 个专业金融技能、29 个智能体团队预设和 7 个市场回测引擎。

**核心定位**：自然语言量化金融研究 AI 智能体

---

## 技术栈分析

### 后端技术栈
| 组件 | 版本/说明 | 用途 |
|------|-----------|------|
| Python | >=3.11 | 核心运行时 |
| FastAPI | >=0.104.0 | API 服务框架 |
| LangChain | >=0.1.0 | LLM 应用框架 |
| LangGraph | >=0.2.50 | 智能体工作流编排 |
| Pandas | >=2.0.0 | 数据处理 |
| NumPy / SciPy | >=1.24.0 / >=1.10.0 | 数值计算 |
| DuckDB | >=1.2.0 | 嵌入式分析数据库 |
| scikit-learn | >=1.3.0 | 机器学习 |

### 数据源集成
| 数据源 | 市场覆盖 | 说明 |
|--------|----------|------|
| **AKShare** | A股、期货、外汇 | 免费开源 |
| **yfinance** | 港股、美股 | Yahoo Finance |
| **OKX** | 加密货币 | 免费市场数据 |
| **CCXT** | 100+ 交易所 | 统一接口 |
| **Tushare** | A股 (可选) | Pro 版需要 Token |

### 前端技术栈
- React 19
- Vite
- TypeScript
- Zustand (状态管理)

### 部署方式
- Docker Compose (一键部署)
- PyPI 安装 (`pip install vibe-trading-ai`)
- MCP 插件模式

---

## 核心功能模块

### 1. 技能系统 (69 Skills)

**7 大类别**：

| 类别       | 数量  | 示例技能                                                                            |
| -------- | --- | ------------------------------------------------------------------------------- |
| **数据源**  | 6   | data-routing, tushare, yfinance, okx-market, akshare, ccxt                      |
| **策略**   | 17  | strategy-generate, technical-basic, candlestick, elliott-wave, smc, ml-strategy |
| **分析**   | 15  | factor-research, macro-analysis, valuation-model, earnings-forecast             |
| **资产类别** | 9   | options-strategy, convertible-bond, etf-analysis, asset-allocation              |
| **加密货币** | 7   | perp-funding-basis, liquidation-heatmap, defi-yield, onchain-analysis           |
| **资金流向** | 7   | hk-connect-flow, us-etf-flow, edgar-sec-filings                                 |
| **工具**   | 8   | backtest-diagnose, pine-script, report-generate, web-reader                     |

### 2. 智能体集群 (Swarm)

**29 个预设团队**：

```yaml
# 示例：investment_committee.yaml
name: investment_committee
description: 牛市/熊市辩论 → 风险审查 → PM 最终决策
agents:
  - bull_analyst      # 看涨分析师
  - bear_analyst      # 看跌分析师
  - risk_manager      # 风险经理
  - portfolio_manager # 投资组合经理
```

**典型预设**：
- `investment_committee` - 投资决策委员会
- `global_equities_desk` - 全球股票交易台
- `crypto_trading_desk` - 加密货币交易台
- `quant_strategy_desk` - 量化策略交易台
- `technical_analysis_panel` - 技术分析专家组

### 3. 回测引擎

**7 个市场引擎 + 1 个组合引擎**：

| 引擎 | 市场 |
|------|------|
| ChinaAEngine | A股市场 |
| ChinaFuturesEngine | 中国期货 |
| GlobalEquityEngine | 全球股票 |
| GlobalFuturesEngine | 全球期货 |
| CryptoEngine | 加密货币 |
| ForexEngine | 外汇 |
| OptionsPortfolioEngine | 期权组合 |
| CompositeEngine | 跨市场组合 (新) |

**统计验证方法**：
- Monte Carlo 模拟
- Bootstrap 置信区间
- Walk-Forward 验证

### 4. ReAct 智能体核心

```python
# 三层上下文管理
class AgentLoop:
    # Layer 1: microcompact - 静默裁剪旧工具结果
    # Layer 2: auto_compact - 超出阈值时 LLM 自动压缩
    # Layer 3: compact tool - 模型显式调用压缩工具
```

---

## 代码结构概览

```
Vibe-Trading/
├── agent/                          # 后端 (Python)
│   ├── cli.py                      # CLI 入口 (TUI + 子命令)
│   ├── api_server.py               # FastAPI 服务
│   ├── mcp_server.py               # MCP 服务器 (17 个工具)
│   │
│   ├── src/
│   │   ├── agent/                  # ReAct 智能体核心
│   │   │   ├── loop.py             # 主推理循环
│   │   │   ├── skills.py           # 技能加载器 (69 SKILL.md)
│   │   │   ├── tools.py            # 工具编排
│   │   │   ├── context.py          # 系统提示构建
│   │   │   ├── memory.py           # 运行内存/产物存储
│   │   │   └── trace.py            # 执行追踪写入
│   │   │
│   │   ├── tools/                  # 21 个智能体工具
│   │   │   ├── backtest_tool.py
│   │   │   ├── factor_analysis_tool.py
│   │   │   ├── options_pricing_tool.py
│   │   │   ├── pattern_tool.py
│   │   │   ├── swarm_tool.py
│   │   │   └── ...
│   │   │
│   │   ├── skills/                 # 69 个金融技能 (SKILL.md)
│   │   ├── swarm/                  # Swarm DAG 执行引擎
│   │   ├── session/                # 多轮对话会话管理
│   │   └── providers/              # LLM 提供商抽象
│   │
│   ├── backtest/                   # 回测引擎
│   │   ├── engines/                # 7 个引擎 + 组合引擎
│   │   ├── loaders/                # 5 个数据源 + 自动回退
│   │   └── optimizers/             # MVO, 等波动率, 最大分散, 风险平价
│   │
│   └── config/swarm/               # 29 个 Swarm 预设 YAML
│
├── frontend/                       # Web UI (React 19 + Vite)
│   └── src/
│       ├── pages/                  # Home, Agent, RunDetail, Compare
│       ├── components/             # chat, charts, layout
│       └── stores/                 # Zustand 状态管理
│
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

---

## 关键实现亮点

### 1. 三层上下文压缩机制
```python
def _microcompact(messages: list) -> None:
    """Layer 1: 静默裁剪旧工具结果，保留最近 N 个"""
    tool_msgs = [m for m in messages if m.get("role") == "tool"]
    for msg in tool_msgs[:-KEEP_RECENT]:
        msg["content"] = "[cleared]"
```

### 2. DAG 并行执行引擎
```python
class SwarmRuntime:
    """Swarm DAG 编排引擎
    - 拓扑分层调度
    - 层内并行 (ThreadPoolExecutor)
    - 层间串行
    """
    def start_run(self, preset_name, user_vars):
        # 后台守护线程执行
        # 支持取消和事件回调
```

### 3. 数据源自动回退链
```python
# loaders/registry.py
LOADER_CHAIN = {
    "a_share": ["tushare", "akshare"],
    "hk_us": ["yfinance"],
    "crypto": ["okx", "ccxt"],
}
# 自动尝试多个数据源，零配置覆盖所有市场
```

### 4. MCP 工具暴露 (17 个)
```
list_skills, load_skill, backtest, factor_analysis,
analyze_options, pattern_recognition, get_market_data,
web_search, read_url, read_document, read_file, write_file,
list_swarm_presets, run_swarm, get_swarm_status,
get_run_result, list_runs
```

---

## 适用场景建议

### 适合场景
| 场景 | 示例 |
|------|------|
| **策略回测** | "回测 BTC-USDT MACD 策略，过去 30 天" |
| **多因子研究** | "分析 A 股价值因子的 IC/IR" |
| **期权定价** | "计算苹果期权 Greeks" |
| **宏观分析** | "分析美联储利率决议对黄金的影响" |
| **智能体辩论** | 运行 investment_committee 预设进行多空辩论 |
| **跨市场分析** | A股 + 港股 + 加密货币组合分析 |

### 使用方式

**方式 1: CLI 交互**
```bash
pip install vibe-trading-ai
vibe-trading init    # 交互式配置
vibe-trading         # 启动 TUI
```

**方式 2: Web UI**
```bash
vibe-trading serve --port 8899
cd frontend && npm install && npm run dev
```

**方式 3: MCP 插件**
```json
{
  "mcpServers": {
    "vibe-trading": {
      "command": "vibe-trading-mcp"
    }
  }
}
```

**方式 4: Docker**
```bash
docker compose up --build
```

### 支持的 LLM 提供商
OpenRouter, OpenAI, DeepSeek, Gemini, Groq, DashScope/Qwen, Zhipu, Moonshot/Kimi, MiniMax, Xiaomi MIMO, Ollama (本地)

---

## 生态系统

Vibe-Trading 是 [HKUDS](https://github.com/HKUDS) 智能体生态系统的一部分：

| 项目 | 描述 |
|------|------|
| [ClawTeam](https://github.com/HKUDS/ClawTeam) | 智能体集群智能 |
| [NanoBot](https://github.com/HKUDS/nanobot) | 超轻量级个人 AI 助手 |
| [CLI-Anything](https://github.com/HKUDS/CLI-Anything) | 让所有软件支持智能体 |
| [OpenSpace](https://github.com/HKUDS/OpenSpace) | 自进化 AI 智能体技能 |

---

## 免责声明

Vibe-Trading 仅用于研究、模拟和回测，不构成投资建议，也不执行实盘交易。过往表现不代表未来结果。
