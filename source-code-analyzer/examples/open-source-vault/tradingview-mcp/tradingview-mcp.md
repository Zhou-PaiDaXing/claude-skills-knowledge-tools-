---
title: "TradingView MCP"
aliases: [TradingView MCP]
tags:
  - opensource
  - mcp-server
  - trading
  - technical-analysis
github: https://github.com/nicepkg/tradingview-mcp
created: 2026-04-15
updated: 2026-04-15
score: 4.19
lifecycle: ACTIVE
last_audit: 2026-05-21
---

# TradingView MCP

> **Real-time crypto & stock screening, advanced technical indicators — AI Trading Intelligence Framework**

---

## 项目简介

TradingView MCP 是一个功能完整的 AI 驱动交易工具包，作为 MCP (Model Context Protocol) 服务器运行，支持 Claude 和其他 MCP 客户端。它集成了回测引擎、实时情绪分析、Yahoo Finance 数据和 30+ 技术分析工具，是 TradingView 平台最完整的 AI 交易框架。

**核心特点：**
- 回测引擎：6 种策略 + 机构级指标（Sharpe、Calmar、Expectancy）
- 实时情绪：Reddit 社区情绪 + 价格动量
- Yahoo Finance：实时股价、市场快照
- 30+ 技术分析工具：RSI、MACD、布林带、K线形态等
- 多交易所支持：Binance、KuCoin、Bybit、NASDAQ、NYSE、EGX、BIST
- 多智能体分析：技术分析师 + 情绪分析师 + 风险经理
- 零 API Key：基础功能无需任何 API Key

**项目链接：**
- GitHub: https://github.com/atilaahmettaner/tradingview-mcp
- PyPI: https://pypi.org/project/tradingview-mcp-server/
- OpenClaw 集成: 支持 Telegram、WhatsApp、Discord

---

## 技术栈分析

### 核心技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | >= 3.10 | 核心运行时 |
| MCP | >= 1.12.0 | Model Context Protocol |
| tradingview-screener | >= 0.6.4 | TradingView 筛选器 |
| tradingview-ta | >= 3.3.0 | 技术分析数据 |
| feedparser | >= 6.0.12 | RSS 新闻解析 |
| yfinance | 内置 | Yahoo Finance 数据 |
| praw | 内置 | Reddit API |
| pandas/numpy | 内置 | 数据处理和回测 |

### 数据提供商
| 提供商 | 数据类型 |
|--------|----------|
| TradingView | 技术指标、筛选器 |
| Yahoo Finance | 实时股价、市场数据 |
| Reddit | 社区情绪 |
| RSS Feeds | 实时新闻 (Reuters, CoinDesk, CoinTelegraph) |

---

## 核心功能模块

### 1. 回测引擎 (`core/services/backtest_service.py`)
**6 种内置策略：**
| 策略 | 描述 |
|------|------|
| RSI | RSI 超买/超卖均值回归 |
| Bollinger | 布林带均值回归 |
| MACD | MACD 金叉/死叉 |
| EMA Cross | EMA 20/50 金叉/死叉 |
| Supertrend | ATR 趋势跟踪 |
| Donchian | 唐奇安通道突破 (海龟交易) |

**机构级指标：**
- Win Rate (胜率)
- Total Return (总收益)
- Sharpe Ratio (夏普比率)
- Calmar Ratio (卡尔马比率)
- Max Drawdown (最大回撤)
- Profit Factor (盈亏比)
- Expectancy (期望值)
- Walk-Forward 回测 (前向验证)

### 2. 技术分析服务 (`core/services/indicators.py`)
**30+ 技术指标：**
- RSI (相对强弱指数)
- MACD (移动平均收敛发散)
- Bollinger Bands (布林带)
- EMA/SMA (指数/简单移动平均线)
- ATR (平均真实波幅)
- OBV (能量潮)
- Stochastic (随机指标)
- Volume Profile (成交量分布)
- Support/Resistance (支撑/阻力)

**K线形态检测 (15 种)：**
- 锤子线、上吊线
- 吞没形态
- 晨星、暮星
- 十字星
-  etc.

### 3. 筛选器服务 (`core/services/screener_service.py`)
**多交易所支持：**
| 交易所 | 类型 |
|--------|------|
| Binance | 加密货币 |
| KuCoin | 加密货币 |
| Bybit | 加密货币 |
| MEXC | 加密货币 |
| NASDAQ | 美股 |
| NYSE | 美股 |
| EGX | 埃及股票 |
| BIST | 土耳其股票 |
| Bursa Malaysia | 马来西亚 |
| HKEX | 港股 |
| SSE/SZSE | A股 |

**筛选条件 (20+)：**
- 价格变化百分比
- 成交量突破
- RSI 范围
- 布林带位置
- 趋势方向
-  etc.

### 4. 情绪分析服务 (`core/services/sentiment_service.py`)
- **Reddit 情绪**: 多金融社区情绪聚合
- **情绪评分**: 看涨/看跌分数
- **热门帖子**: 提取关键讨论
- **趋势检测**: 情绪变化趋势

### 5. 新闻服务 (`core/services/news_service.py`)
- **RSS 聚合**: Reuters、CoinDesk、CoinTelegraph
- **实时头条**: 最新市场新闻
- **分类**: 按资产类别过滤

### 6. Yahoo Finance 服务 (`core/services/yahoo_finance_service.py`)
- **实时报价**: 价格、涨跌幅、52周高低
- **市场快照**: S&P500、NASDAQ、VIX、BTC、ETH、EUR/USD
- **多资产支持**: 股票、加密货币、ETF、指数、外汇

### 7. 多智能体分析 (`core/services/multi_agent_service.py`)
**三层决策引擎：**
1. **技术分析师**: 布林带、RSI、MACD 分析
2. **情绪与动量分析师**: Reddit 情绪 + 价格动量
3. **风险经理**: 波动率、回撤风险、均值回归信号

**输出信号：**
- STRONG BUY (强烈买入)
- BUY (买入)
- HOLD (持有)
- SELL (卖出)
- STRONG SELL (强烈卖出)

---

## 代码结构概览

```
tradingview-mcp/
├── src/tradingview_mcp/
│   ├── __init__.py
│   ├── server.py                   # MCP 服务器入口 (27KB)
│   └── core/
│       ├── types.py                # 类型定义
│       ├── data/
│       │   ├── egx_indices.py      # EGX 指数数据 (11KB)
│       │   └── egx_sectors.py      # EGX 行业数据 (17KB)
│       ├── services/
│       │   ├── backtest_service.py # 回测引擎 (26KB)
│       │   ├── indicators.py       # 技术指标 (58KB)
│       │   ├── indicators_calc.py  # 指标计算 (9KB)
│       │   ├── screener_service.py # 筛选器服务 (33KB)
│       │   ├── scanner_service.py  # 扫描服务 (11KB)
│       │   ├── sentiment_service.py # 情绪分析 (5KB)
│       │   ├── news_service.py     # 新闻服务 (5KB)
│       │   ├── yahoo_finance_service.py # Yahoo Finance (5KB)
│       │   ├── multi_agent_service.py   # 多智能体 (7KB)
│       │   ├── egx_service.py      # EGX 特定服务 (42KB)
│       │   ├── screener_provider.py # 筛选器提供者 (7KB)
│       │   ├── proxy_manager.py    # 代理管理 (5KB)
│       │   └── coinlist.py         # 币种列表 (1KB)
│       ├── utils/
│       │   └── validators.py       # 参数验证 (3KB)
│       └── portfolio.py            # 投资组合 (7KB)
├── openclaw/
│   └── trading.py                  # OpenClaw 集成脚本
├── tests/
│   └── unit/
│       └── test_validators.py
├── pyproject.toml                  # 项目配置
└── README.md                       # 项目文档
```

---

## 关键实现亮点

### 1. MCP 工具定义
```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="TradingView Multi-Market Screener",
    instructions="Multi-market screener backed by TradingView..."
)

@mcp.tool()
def top_gainers(exchange: str = "KUCOIN", timeframe: str = "15m", limit: int = 25) -> list[dict]:
    """Return top gainers for an exchange and timeframe"""
    ...
```

### 2. 布林带专业评级
```python
# indicators_calc.py
def compute_bb_rating_signal(close, bb_upper, bb_middle, bb_lower):
    """
    专有 ±3 布林带评级系统
    +3: 价格 > 上轨 (极度超买)
    +2: 价格 > 中轨 + 半带宽 (买入信号)
    +1: 价格 > 中轨
    -1: 价格 < 中轨
    -2: 价格 < 中轨 - 半带宽 (卖出信号)
    -3: 价格 < 下轨 (极度超卖)
    """
```

### 3. 回测指标计算
```python
# backtest_service.py
def calculate_metrics(trades, equity_curve):
    returns = np.diff(equity_curve) / equity_curve[:-1]
    
    # Sharpe Ratio
    sharpe = np.sqrt(252) * returns.mean() / returns.std()
    
    # Calmar Ratio
    calmar = annual_return / max_drawdown
    
    # Expectancy
    expectancy = (win_rate * avg_win) - (loss_rate * avg_loss)
    
    return {
        "sharpe_ratio": sharpe,
        "calmar_ratio": calmar,
        "expectancy": expectancy,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate
    }
```

### 4. Walk-Forward 回测
```python
# 前向验证防止过拟合
def walk_forward_backtest(symbol, strategy, train_size=0.7):
    """
    将数据分为训练集和测试集
    在训练集优化参数，在测试集验证
    重复多次确保稳健性
    """
```

### 5. 多时间框架分析
```python
# 周线 -> 日线 -> 4H -> 1H -> 15m 对齐分析
def run_multi_timeframe_analysis(symbol):
    timeframes = ["1W", "1D", "4H", "1H", "15m"]
    signals = {}
    for tf in timeframes:
        signals[tf] = get_technical_analysis(symbol, tf)
    return align_signals(signals)
```

---

## 适用场景建议

### 1. 个人投资者
- **场景**: 股票/加密货币筛选和分析
- **优势**: 免费、实时数据、多维度分析
- **使用**: Claude Desktop + tradingview-mcp

### 2. 量化交易者
- **场景**: 策略回测和优化
- **优势**: 6 种策略、机构级指标、Walk-Forward 验证
- **使用**: `backtest_strategy` + `compare_strategies`

### 3. 交易教育者
- **场景**: 教学技术分析和策略
- **优势**: 可视化信号、多时间框架、情绪结合
- **使用**: `combined_analysis` 展示综合决策

### 4. 风险管理
- **场景**: 投资组合风险评估
- **优势**: 波动率分析、回撤计算、多智能体检视
- **使用**: 风险经理智能体输出

### 5. 市场情绪监控
- **场景**: 跟踪市场情绪变化
- **优势**: Reddit 情绪 + 新闻 + 技术指标
- **使用**: `market_sentiment` + `financial_news`

### 6. 自动化交易研究
- **场景**: 开发自动交易系统
- **优势**: MCP 协议、结构化输出、历史数据
- **使用**: 结合其他 MCP 工具构建工作流

---

## 快速开始

### 安装
```bash
pip install tradingview-mcp-server
```

### Claude Desktop 配置
```json
{
  "mcpServers": {
    "tradingview": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uvx",
      "args": ["--from", "tradingview-mcp-server", "tradingview-mcp"]
    }
  }
}
```

### 示例对话
```
You: "Give me a full market snapshot right now"
AI: [market_snapshot] → S&P500 -3.4%, BTC +0.1%, VIX 31 (+13%)

You: "Backtest RSI strategy on BTC-USD for 2 years"
AI: [backtest_strategy] → +31.5% return | Sharpe 2.1 | WR: 62%

You: "Analyze TSLA with all signals"
AI: [combined_analysis] → BUY (Technical STRONG BUY + Bullish Reddit)
```

---

## OpenClaw 集成

支持通过 OpenClaw 在 Telegram、WhatsApp、Discord 上使用：

```bash
# 安装技能
mkdir -p ~/.agents/skills/tradingview-mcp ~/.openclaw/tools
curl -fsSL https://raw.githubusercontent.com/atilaahmettaner/tradingview-mcp/main/openclaw/SKILL.md \
  -o ~/.agents/skills/tradingview-mcp/SKILL.md
curl -fsSL https://raw.githubusercontent.com/atilaahmettaner/tradingview-mcp/main/openclaw/trading.py \
  -o ~/.openclaw/tools/trading.py
```

---

## 路线图

- [x] TradingView 技术分析 (30+ 指标)
- [x] 多交易所筛选器
- [x] Reddit 情绪分析
- [x] 实时财经新闻
- [x] Yahoo Finance 实时价格
- [x] 回测引擎 (6 策略 + Sharpe/Calmar/Expectancy)
- [ ] Walk-forward 回测 (过拟合检测)
- [ ] Twitter/X 市场情绪
- [ ] 模拟交易 (Paper trading)
- [ ] 托管云服务

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)

---

## 免责声明

本工具仅供教育和研究目的，不构成投资建议。在做出投资决策前，请务必进行自己的研究。

---

## 支持项目

如果这个项目改善了您的工作流，请考虑在 [GitHub Sponsors](https://github.com/sponsors/atilaahmettaner) 上支持开发者。
